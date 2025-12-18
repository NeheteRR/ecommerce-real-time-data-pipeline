from airflow import DAG
from airflow.decorators import task
from airflow.utils.dates import days_ago
import requests
from kafka import KafkaProducer
import json

# Config
API_URL = "https://fakestoreapi.com/products"
KAFKA_BROKER = "localhost:9092"
KAFKA_TOPIC = "products_raw"

default_args = {
    "owner": "airflow",
    "start_date": days_ago(1),
}

with DAG(
    dag_id="ecommerce_etl_pipeline",
    default_args=default_args,
    schedule_interval="@daily",
    catchup=False,
) as dag:

    @task()
    def extract_products():
        """Fetch product data from FakeStore API."""
        response = requests.get(API_URL)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"API fetch failed: {response.status_code}")

    @task()
    def publish_to_kafka(products):
        """Publish product data to Kafka."""
        producer = KafkaProducer(
            bootstrap_servers="ec_kafka:9092",
            value_serializer=lambda v: json.dumps(v).encode("utf-8")
        )
        for product in products:
            producer.send(KAFKA_TOPIC, product)
        producer.flush()
        producer.close()
        return f"Published {len(products)} messages to {KAFKA_TOPIC}"

    # Workflow
    product_data = extract_products()
    publish_to_kafka(product_data)
