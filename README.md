# 🛒 E-Commerce Product Management System  
### Real-Time Streaming Pipeline + CRUD Web Application

---

## 📌 Project Overview

This project is a **full end-to-end E-Commerce Product Management System** that demonstrates **real-time data streaming, big data processing, backend APIs, database integration, and a web interface**.

The system ingests product data from an external API, streams it through Kafka, processes it using Spark Structured Streaming, stores it in MongoDB, and exposes the data through both **REST APIs and a user-friendly web interface** built with Flask.

---

---

## 🎯 Features

### 🔹 Real-Time Data Pipeline
- Fetches product data from FakeStore API
- Streams data using Apache Kafka
- Real-time transformation using Spark Structured Streaming
- Writes processed data into MongoDB
- Fault-tolerant processing with Spark checkpoints

---

### 🔹 Backend (Flask REST APIs)
- Create a product
- Fetch all products
- Update product by ID
- Delete product by ID
- Uses MongoDB `ObjectId` as the primary identifier

---

### 🔹 Frontend (Web Interface)
- View all products in a dashboard
- Add new products using a form
- Edit existing products
- Delete products with confirmation popup
- Clean and simple UI using Flask + Jinja2 templates

---

### 🔹 Orchestration & Deployment
- Apache Airflow for workflow orchestration
- Docker & Docker Compose for containerized services
- Services communicate via Docker network

---

## 🧰 Tech Stack

| Layer          | Technology |
|----------------|-----------|
| Language       | Python |
| Streaming      | Apache Kafka |
| Processing     | Apache Spark (Structured Streaming) |
| Database       | MongoDB |
| Backend API    | Flask |
| Frontend       | HTML, CSS, Jinja2 |
| Orchestration  | Apache Airflow |
| Containerization | Docker, Docker Compose |

---

## 📁 Project Structure

```bash
BD_Ecommerce/
│
├── kafka/
│   ├── kafka_producer.py
│   └── kafka_consumer.py
│
├── spark_jobs/
│   └── transform_products.py
│
├── mongodb/
│   └── setup_collections.py
│
├── airflow/
│   └── dags/
│       └── ecommerce_etl_dag.py
│
├── templates/
│   ├── index.html      # Product dashboard
│   ├── add.html        # Add product form
│   └── edit.html       # Edit product form
│
├── app.py              # Flask API + Web Interface
├── docker-compose.yml
├── requirements.txt
└── README.md
```
## ⚙️ Installation & Setup
1️⃣ Clone the Repository
```bash
git clone https://github.com/your-username/BD_Ecommerce.git
cd BD_Ecommerce
```

2️⃣ Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate
```

3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

4️⃣ Start Services Using Docker
```bash
docker compose up -d
```

Flask Application

▶️ Running the Pipeline
1. Kafka Producer
```bash
python kafka/kafka_producer.py
```

2. Spark Streaming Job
```bash
docker exec -it ec_spark \
/opt/spark/bin/spark-submit \
--conf spark.jars.ivy=/tmp/ivy \
--packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1,org.mongodb.spark:mongo-spark-connector_2.12:10.3.0 \
/app/spark_jobs/transform_products.py
```

🌐 Flask Application
Start Flask App
```bash
python app.py
```


Server runs on:
```bash
http://localhost:5000

```
🔗 REST API Endpoints

| Method | Endpoint          | Description          |
|--------|-------------------|----------------------|
| POST   | `/products`       | Add product          |
| GET    | `/products`       | Fetch all products   |
| PUT    | `/products/<id>`  | Update product       |
| DELETE | `/products/<id>`  | Delete product       |

🖥️ Web Interface Routes

| Route        | Description                          |
|--------------|--------------------------------------|
| `/`          | Product dashboard                    |
| `/add`       | Add new product                      |
| `/edit/<id>` | Edit product                         |
| `/delete/<id>` | Delete product (with confirmation) |


📊 MongoDB Details
- Host: mongodb://localhost:27018
- Database: ecommerce_db
- Collection: products
- ⚠️ Note: MongoDB creates databases and collections only after data insertion