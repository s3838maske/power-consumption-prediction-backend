# ⚡ Power Consumption Prediction - Setup Guide

This document provides a step-by-step guide to set up the Power Consumption Prediction project on a new PC. The project consists of a **React (Vite) Frontend** and a **Django REST Backend**.

---

## 📋 Prerequisites

Ensure you have the following installed:

- **Node.js** (v18.0 or higher)
- **Python** (v3.10 or higher)
- **MongoDB** (Local instance or [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) account)
- **Git**

---

## 🛠️ Step 1: Clone the Repository

```bash
git clone https://github.com/s3838maske/power-consumption-prediction.git
cd power-consumption-prediction
```

---

## 🐍 Step 2: Backend Setup (Django)

### 1. Create and Activate Virtual Environment

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Environment Configuration

Create a `.env` file in the `backend/` directory:

```env
SECRET_KEY=your-django-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# MongoDB Configuration
MONGODB_NAME=power_consumption_db
MONGODB_HOST=localhost
MONGODB_PORT=27017

# JWT Settings
JWT_SECRET_KEY=your-jwt-secret-key
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=60
```

### 4. Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Admin (Superuser)

```bash
python manage.py createsuperuser
```

### 6. Train initial ML Models

```bash
python ml_models/train_models.py
```

### 7. Run Backend Server

```bash
python manage.py runserver
```

The backend will be available at: **http://localhost:8000**

---

## ⚛️ Step 3: Frontend Setup (React)

### 1. Install Dependencies

Open a new terminal in the project root:

```bash
cd frontend
npm install
```

### 2. Environment Configuration

Create a `.env` file in the `frontend/` directory:

```env
VITE_API_URL=http://localhost:8000/api
```

### 3. Run Development Server

```bash
npm run dev
```

The frontend will be available at: **http://localhost:5173**

---

## 🔗 API Reference & Flow

### 🔐 1. Authentication Flow

| Method   | Endpoint              | Description                     |
| :------- | :-------------------- | :------------------------------ |
| **POST** | `/api/auth/register/` | Create a new user account       |
| **POST** | `/api/auth/login/`    | Get JWT access & refresh tokens |
| **GET**  | `/api/auth/me/`       | Fetch profile of logged-in user |

### 👤 2. User Data & Predictions

| Method   | Endpoint                            | Description                           |
| :------- | :---------------------------------- | :------------------------------------ |
| **POST** | `/api/consumption/upload-data/`     | Upload Excel file with usage data     |
| **GET**  | `/api/consumption/dashboard-stats/` | Fetch aggregated usage stats & charts |
| **GET**  | `/api/consumption/predictions/`     | Get usage forecasts from ML models    |

### 🛠️ 3. Admin Operations

| Method     | Endpoint           | Description                            |
| :--------- | :----------------- | :------------------------------------- |
| **GET**    | `/api/users/`      | List all registered users (Admin only) |
| **DELETE** | `/api/users/{id}/` | Delete a specific user (Admin only)    |

---

## 📂 Project Structure Notice

- **Shared Files**: `README.md` in the root folder contains general project info.
- **Frontend**: All React code is located in the `frontend/` directory.
- **Backend**: All Python/Django code is located in the `backend/` directory.

---

## ✅ Verification Checklist

1. **Frontend**: Login page appears at `http://localhost:5173`.
2. **Backend**: Admin panel accessible at `http://localhost:8000/admin`.
3. **Integration**: Successful login redirects you to the User or Admin dashboard.
4. **Data**: Uploading `sample_data.xlsx` updates the graphs in real-time.
