import calendar
import random
import time
from datetime import datetime
from json import dumps
from random import randint
from time import sleep

from kafka import KafkaProducer, errors


def write_data(producer):
    data_cnt = 20000
    order_id = calendar.timegm(time.gmtime())
    max_price = 100000
    payment_topic = "payment"
    order_topic = "order"

    print(
        f"Producing {data_cnt} records to payment topic {payment_topic} and order topic {order_topic}"
    )
    for _ in range(data_cnt):
        # produce payment info to payment topic
        ts = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        rd = random.random()
        order_id += 1
        pay_amount = max_price * rd
        pay_platform = 0 if random.random() < 0.9 else 1
        province_id = randint(0, 6)
        payment_data = {
            "createTime": ts,
            "orderId": order_id,
            "payAmount": pay_amount,
            "payPlatform": pay_platform,
            "provinceId": province_id,
        }
        # produce order info to order topic
        order_data = {
            "createTime": ts,
            "orderId": order_id,
            "category": random.choice(
                [
                    "gas_transport",
                    "grocery_pos",
                    "home",
                    "shopping_pos",
                    "kids_pets",
                    "personal_care",
                    "health_fitness",
                    "travel",
                    "misc_pos",
                    "food_dining",
                    "entertainment",
                ]
            ),
            "merchantId": randint(0, 1000),
        }
        producer.send(payment_topic, value=payment_data)
        producer.send(order_topic, value=order_data)
        sleep(0.5)


def create_producer():
    print("Connecting to Kafka brokers")
    for _i in range(6):
        try:
            producer = KafkaProducer(
                bootstrap_servers=["kafka:29092"],
                value_serializer=lambda x: dumps(x).encode("utf-8"),
            )
            print("Connected to Kafka")
            return producer
        except errors.NoBrokersAvailable:
            print("Waiting for brokers to become available")
            sleep(10)

    raise RuntimeError("Failed to connect to brokers within 60 seconds")


if __name__ == "__main__":
    producer = create_producer()
    write_data(producer)
