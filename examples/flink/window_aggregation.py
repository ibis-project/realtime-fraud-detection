from __future__ import annotations

import sys
import urllib.request
from itertools import islice

from kafka import KafkaConsumer
from pyflink.table import EnvironmentSettings, TableEnvironment

import ibis

local = len(sys.argv) > 1 and sys.argv[1] == "local"

# 1. create a TableEnvironment
env_settings = EnvironmentSettings.in_streaming_mode()
table_env = TableEnvironment.create(env_settings)
# write all the data to one file
table_env.get_config().set("parallelism.default", "1")

# The `flink` backend does not create `TableEnvironment` objects; pass
# the `TableEnvironment` object created above to `ibis.flink.connect`.
con = ibis.flink.connect(table_env)

# Flink’s streaming connectors aren't part of the binary distribution.
# Link the Kafka connector for cluster execution by adding a JAR file.
urllib.request.urlretrieve(
    "https://repo.maven.apache.org/maven2/org/apache/flink/flink-sql-connector-kafka/3.0.2-1.18/flink-sql-connector-kafka-3.0.2-1.18.jar",
    filename="flink-sql-connector-kafka-3.0.2-1.18.jar",
)
con.raw_sql("ADD JAR 'flink-sql-connector-kafka-3.0.2-1.18.jar'")

# 2. create source Table
source_schema = ibis.schema(
    {
        "createTime": "timestamp(3)",
        "orderId": "int64",
        "payAmount": "float64",
        "payPlatform": "int32",
        "provinceId": "int32",
    }
)

source_configs = {
    "connector": "kafka",
    "topic": "payment",
    "properties.bootstrap.servers": "localhost:9092" if local else "kafka:29092",
    "properties.group.id": "test_3",
    "scan.startup.mode": "earliest-offset",
    "format": "json",
}

t = con.create_table(
    "payment",
    schema=source_schema,
    tbl_properties=source_configs,
    watermark=ibis.watermark(
        time_col="createTime", allowed_delay=ibis.interval(seconds=15)
    ),
)

# 3. create sink Table
sink_schema = ibis.schema(
    {
        "province_id": "int32",
        "pay_amount": "float64",
    }
)

sink_configs = {
    "connector": "kafka",
    "topic": "sink",
    "properties.bootstrap.servers": "localhost:9092" if local else "kafka:29092",
    "format": "json",
}

con.create_table(
    "total_amount_by_province_id", schema=sink_schema, tbl_properties=sink_configs
)

# 4. query from source table and perform calculations
agged = t.select(
    province_id=t.provinceId,
    pay_amount=t.payAmount.sum().over(
        range=(-ibis.interval(seconds=10), 0),
        group_by=t.provinceId,
        order_by=t.createTime,
    ),
)

# 5. emit query result to sink table
con.insert("total_amount_by_province_id", agged)

if local:
    # Use the Kafka Python client to stream records from the sink topic.
    # Otherwise, the mini cluster will shut down upon script completion.
    consumer = KafkaConsumer("sink")
    for msg in islice(consumer, 10):
        print(msg)
