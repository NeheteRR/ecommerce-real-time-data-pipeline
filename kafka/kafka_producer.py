from kafka import KafkaProducer
import requests
import json

API_URL = "https://fakestoreapi.com/products"
KAFKA_BROKER = "localhost:9092"
KAFKA_TOPIC = "products_raw"

def fetch_and_publish():
    response = requests.get(API_URL)
    data = response.json()
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BROKER,
        value_serializer=lambda v: json.dumps(v).encode("utf-8")
    )
    for product in data:
        producer.send(KAFKA_TOPIC, product)
    producer.flush()
    print(f"Published {len(data)} products to Kafka.")

if __name__ == "__main__":
    fetch_and_publish()
