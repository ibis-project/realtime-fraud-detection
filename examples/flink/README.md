# Ibis Flink backend example

This directory contains an example using the Apache Flink backend for Ibis.

## Installation prerequisites

* **Docker Compose:** This tutorial uses Docker Compose to manage an Apache Kafka environment (including sample data generation) and a Flink cluster (for [remote execution](#remote-execution)). You can [download and install Docker Compose from the official website](https://docs.docker.com/compose/install/).
* **JDK 11:** Flink requires Java 11. If you don't already have JDK 11 installed, you can [get the appropriate Eclipse Temurin release](https://adoptium.net/temurin/releases/?package=jdk&version=11).
* **Python:** To follow along, you need Python 3.10 or 3.11.

## Installing the Flink backend for Ibis

We strongly recommend creating a virtual environment for your project. In your virtual environment, install the dependencies from the requirements file:

```bash
python -m pip install -r examples/flink/requirements.txt
```

## Running the example

The [included window aggregation example](./window_aggregation.py) uses the Flink backend for Ibis to process the aforementioned payment messages, computing the total pay amount per province in the past 10 seconds (as of each message, for the province in the incoming message).

### Local execution

You can run the example using the Flink mini cluster from your project directory:

```bash
python window_aggregation.py local
```

Within a few seconds, you should see messages from the `sink` topic (containing the results of your computation) flooding the screen.

> [!NOTE]
> The mini cluster shuts down as soon as the Python session ends, so we print the Kafka messages until the process is cancelled (e.g. with <kbd>Ctrl</kbd>+<kbd>C</kbd>).

### Remote execution

You can also submit the example to a remote cluster. First, you will need to spin up a remote Flink cluster:
```bash
docker compose up
```
We will [use the method described in the official Flink documentation](https://nightlies.apache.org/flink/flink-docs-release-1.18/docs/deployment/cli/#submitting-pyflink-jobs) to submit the example to this remote cluster.

> [!TIP]
> You can find the `./bin/flink` executable with the following command:
> 
> ```bash
> python -c'from pathlib import Path; import pyflink; print(Path(pyflink.__spec__.origin).parent / "bin" / "flink")'
> ```

My full command looks like this:

```bash
/opt/miniconda3/envs/ibis-dev/lib/python3.10/site-packages/pyflink/bin/flink run --jobmanager localhost:8081 --python window_aggregation.py
```

The command will exit after displaying a submission message:

```bash
Job has been submitted with JobID b816faaf5ef9126ea5b9b6a37012cf56
```

Similar to how we viewed messages in the `payment_msg` topic, we can print results from the `sink` topic:

```pycon
>>> from kafka import KafkaConsumer
>>> 
>>> consumer = KafkaConsumer("sink")
>>> for _, msg in zip(range(10), consumer):
...     print(msg)
... 
ConsumerRecord(topic='sink', partition=0, offset=8264, timestamp=1702076548075, timestamp_type=0, key=None, value=b'{"province_id":1,"pay_amount":102381.88254099473}', headers=[], checksum=None, serialized_key_size=-1, serialized_value_size=49, serialized_header_size=-1)
ConsumerRecord(topic='sink', partition=0, offset=8265, timestamp=1702076548480, timestamp_type=0, key=None, value=b'{"province_id":1,"pay_amount":114103.59313794877}', headers=[], checksum=None, serialized_key_size=-1, serialized_value_size=49, serialized_header_size=-1)
ConsumerRecord(topic='sink', partition=0, offset=8266, timestamp=1702076549085, timestamp_type=0, key=None, value=b'{"province_id":5,"pay_amount":65711.48588438489}', headers=[], checksum=None, serialized_key_size=-1, serialized_value_size=48, serialized_header_size=-1)
ConsumerRecord(topic='sink', partition=0, offset=8267, timestamp=1702076549488, timestamp_type=0, key=None, value=b'{"province_id":3,"pay_amount":388965.01567530684}', headers=[], checksum=None, serialized_key_size=-1, serialized_value_size=49, serialized_header_size=-1)
ConsumerRecord(topic='sink', partition=0, offset=8268, timestamp=1702076550098, timestamp_type=0, key=None, value=b'{"province_id":4,"pay_amount":151524.24311058817}', headers=[], checksum=None, serialized_key_size=-1, serialized_value_size=49, serialized_header_size=-1)
ConsumerRecord(topic='sink', partition=0, offset=8269, timestamp=1702076550502, timestamp_type=0, key=None, value=b'{"province_id":2,"pay_amount":290018.422116076}', headers=[], checksum=None, serialized_key_size=-1, serialized_value_size=47, serialized_header_size=-1)
ConsumerRecord(topic='sink', partition=0, offset=8270, timestamp=1702076550910, timestamp_type=0, key=None, value=b'{"province_id":5,"pay_amount":47098.24626524143}', headers=[], checksum=None, serialized_key_size=-1, serialized_value_size=48, serialized_header_size=-1)
ConsumerRecord(topic='sink', partition=0, offset=8271, timestamp=1702076551516, timestamp_type=0, key=None, value=b'{"province_id":4,"pay_amount":155309.68873659955}', headers=[], checksum=None, serialized_key_size=-1, serialized_value_size=49, serialized_header_size=-1)
ConsumerRecord(topic='sink', partition=0, offset=8272, timestamp=1702076551926, timestamp_type=0, key=None, value=b'{"province_id":2,"pay_amount":367397.8759861871}', headers=[], checksum=None, serialized_key_size=-1, serialized_value_size=48, serialized_header_size=-1)
ConsumerRecord(topic='sink', partition=0, offset=8273, timestamp=1702076552530, timestamp_type=0, key=None, value=b'{"province_id":3,"pay_amount":182191.45302431137}', headers=[], checksum=None, serialized_key_size=-1, serialized_value_size=49, serialized_header_size=-1)
```

## Shutting down the Compose environment

Press <kbd>Ctrl</kbd>+<kbd>C</kbd> to stop the Docker Compose containers. Once stopped, run `docker compose down` to remove the services created for this tutorial.
