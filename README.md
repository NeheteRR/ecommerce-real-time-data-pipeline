# 🛒 E-Commerce Product Management System

## Flask + MongoDB CRUD Application

## 📌 Project Overview

This project is a full-stack CRUD application built using Flask and MongoDB.
It provides both:

🔹 RESTful APIs for Create, Read, Update, Delete (CRUD) operations
🔹 A simple and user-friendly web interface to manage products visually

The application demonstrates backend development, database integration, REST API design, and a basic frontend interface using Flask templates.

🎯 Features
🔧 Backend (REST API)
- Create a product
- Fetch all products
- Fetch a product by ID
- Update a product
- Delete a product
- Uses MongoDB ObjectId as the primary identifier

🖥️ Frontend (Web Interface)
- Display all products in a dashboard
- Add new products via a form
- Edit existing products
- Delete products with confirmation popup

🧰 Tech Stack
| Layer     | Technology                         |
|-----------|------------------------------------|
| Backend   | Python, Flask                      |
| Database  | MongoDB                            |
| Frontend  | HTML, CSS, Jinja2                  |
| Server    | Flask Development Server           |

📁 Project Structure
```bash
crud_app/
│── app.py
│
├── templates/
│   ├── index.html      # Product dashboard
│   ├── add.html        # Add product form
│   └── edit.html       # Edit product form
│
└── README.md
```

## ⚙️ Installation & Setup
1️⃣ Clone the Repository
```bash
git clone https://github.com/your-username/ecommerce-crud-flask.git
cd ecommerce-crud-flask
```

2️⃣ Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate
```

3️⃣ Install Dependencies
```bash
pip install flask pymongo
```

4️⃣ Start MongoDB
Make sure MongoDB is running locally on:
```bash
mongodb://localhost:27018
```

- Database name: ecommerce_db
- Collection name: products

▶️ Run the Application
```bash
python app.py
```
Server will start at:
```bash
http://localhost:5000
```

## 🌐 Web Interface Routes
| Route        | Description                          |
|--------------|--------------------------------------|
| `/`          | Product dashboard                    |
| `/add`       | Add new product                      |
| `/edit/<id>` | Edit product                         |
| `/delete/<id>` | Delete product (with confirmation) |
