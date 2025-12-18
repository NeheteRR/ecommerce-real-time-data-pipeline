from kafka import KafkaConsumer
import json
import os

# If running on host → localhost:29092
# If running inside Docker → ec_kafka:9092
KAFKA_BROKER = os.getenv("KAFKA_BROKER", "localhost:29092")
KAFKA_TOPIC = "products_raw"

def consume_messages():
    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_BROKER,
        api_version=(3, 5, 0),
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        group_id="ecommerce-consumer-group",
        value_deserializer=lambda x: json.loads(x.decode("utf-8"))
    )

    print(f"Listening on {KAFKA_BROKER}, topic={KAFKA_TOPIC}")

    for message in consumer:
        print(json.dumps(message.value, indent=2))

if __name__ == "__main__":
    consume_messages()