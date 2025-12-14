from kafka import KafkaConsumer
import json

# Kafka Config
KAFKA_BROKER = "localhost:9092"
KAFKA_TOPIC = "products_raw"

def consume_messages():
    # Consumer subscribes to the topic
    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_BROKER,
        auto_offset_reset="earliest",   # read from beginning
        enable_auto_commit=True,
        group_id="ecommerce-consumer-group",
        value_deserializer=lambda x: json.loads(x.decode("utf-8"))
    )

    print(f"Listening for messages on topic: {KAFKA_TOPIC}...")

    # Continuously poll messages
    for message in consumer:
        product = message.value
        print(f"Received product: {json.dumps(product, indent=2)}")

if __name__ == "__main__":
    consume_messages()
