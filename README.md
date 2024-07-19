# Realtime Fraud Detection

This repository contains a demo for real-time fraud detection.

## Installation prerequisites

* **Docker Compose:** This tutorial uses Docker Compose to manage an Apache Kafka environment (including sample data generation) and a Flink cluster (for [remote execution](#remote-execution)). You can [download and install Docker Compose from the official website](https://docs.docker.com/compose/install/).

## Spinning up the services using Docker Compose

From your project directory, run `docker compose up kafka init-kafka data-generator` to create Kafka topics and generate sample data.

After a few seconds, you should see messages indicating your Kafka environment is ready:

```bash
realtime-fraud-detection-init-kafka-1      | Successfully created the following topics:
realtime-fraud-detection-init-kafka-1      | payment
realtime-fraud-detection-init-kafka-1      | order
realtime-fraud-detection-init-kafka-1      | sink
realtime-fraud-detection-init-kafka-1 exited with code 0
realtime-fraud-detection-data-generator-1  | Connected to Kafka
realtime-fraud-detection-data-generator-1  | Producing 20000 records to payment topic payment and order topic order
```

The `payment` Kafka topic contains messages in the following format:

```json
{
    "createTime": "2023-09-20 22:19:02.224",
    "orderId": 1695248388,
    "payAmount": 88694.71922270155,
    "payPlatform": 0,
    "provinceId": 6,
}
```

The `order` Kafka topic contains messages in the following format:
```json
{
    "createTime": "2024-07-19 20:47:25.707", 
    "orderId": 1721422046, 
    "category": "kids_pets", 
    "merchantId": 869,
}
```

In a separate terminal, we can explore what these messages look like:

```pycon
>>> from kafka import KafkaConsumer
>>>
>>> consumer = KafkaConsumer("payment")
>>> for _, msg in zip(range(3), consumer):
...     print(msg)
... 
ConsumerRecord(topic='payment', partition=0, offset=628, timestamp=1702073942808, timestamp_type=0, key=None, value=b'{"createTime": "2023-12-08 22:19:02.808", "orderId": 1702074256, "payAmount": 79901.88673289565, "payPlatform": 1, "provinceId": 1}', headers=[], checksum=None, serialized_key_size=-1, serialized_value_size=131, serialized_header_size=-1)
ConsumerRecord(topic='payment', partition=0, offset=629, timestamp=1702073943310, timestamp_type=0, key=None, value=b'{"createTime": "2023-12-08 22:19:03.309", "orderId": 1702074257, "payAmount": 34777.62234573957, "payPlatform": 0, "provinceId": 3}', headers=[], checksum=None, serialized_key_size=-1, serialized_value_size=131, serialized_header_size=-1)
ConsumerRecord(topic='payment', partition=0, offset=630, timestamp=1702073943811, timestamp_type=0, key=None, value=b'{"createTime": "2023-12-08 22:19:03.810", "orderId": 1702074258, "payAmount": 17101.347666982423, "payPlatform": 0, "provinceId": 2}', headers=[], checksum=None, serialized_key_size=-1, serialized_value_size=132, serialized_header_size=-1)
```