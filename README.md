# 🚀 Power Consumption Prediction - Backend (Django)

This is the Django-based REST API backend for the Power Consumption Prediction system. It uses MongoDB as the primary database and incorporates Machine Learning models for energy usage forecasting.

---

## 🛠 Setup Instructions

### 1. Create Virtual Environment

```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Environment Variables

Create `.env` file in the `backend` directory:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# MongoDB
MONGODB_NAME=power_consumption_db
MONGODB_HOST=localhost
MONGODB_PORT=27017
MONGODB_USER=
MONGODB_PASSWORD=

# JWT
JWT_SECRET_KEY=your-jwt-secret-key
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7

# Email (for alerts)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

SECRET_KEY=django-insecure-pw-prediction-dev
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# MongoDB

MONGODB_URI=mongodb+srv://maskeshubham555_db_user:8eJdX1m0vLH8sZa3@power-consumption-predi.wllmm1i.mongodb.net/power_consumption_db?retryWrites=true&w=majority&appName=power-consumption-prediction
MONGODB_NAME=power_consumption_db
MONGODB_HOST=power-consumption-predi.wllmm1i.mongodb.net
MONGODB_PORT=27017
MONGODB_USER=maskeshubham555_db_user
MONGODB_PASSWORD=8eJdX1m0vLH8sZa3

# JWT

JWT_SECRET_KEY=jwt-secret-key-dev
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7

# Email

EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend

env ===>
SECRET_KEY=django-insecure-pw-prediction-dev
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# MongoDB

MONGODB_URI=mongodb+srv://
MONGODB_NAME=power_consumption_db
MONGODB_HOST=power-consumption-predi.wllmm1i.mongodb.net
MONGODB_PORT=27017
MONGODB_USER=maskeshubham555_db_user
MONGODB_PASSWORD=8eJdX1m0vLH8sZa3

# JWT

JWT_SECRET_KEY=jwt-secret-key-dev
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7

# Email

EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
<>===

### 4. Run Migrations

```bash
python manage.py migrate
```

### 5. Create Superuser

```bash
python manage.py createsuperuser
```

### 6. Run Server

```bash
python manage.py runserver
```

---

## ✅ Required Features

### Functional Requirements

- **User Authentication**: Secure registration and login for Users and Admins.
- **Data Upload & Validation**: Upload Excel datasets with validation and preprocessing.
- **Prediction Generation**: AI-driven power consumption forecasting.
- **Visualization Dashboard**: Real-time charts and usage analytics.
- **Report Generation**: Exportable PDF/Excel reports.
- **Alerts System**: Threshold-based notifications and energy-saving tips.
- **Admin Management**: Full control over users, logs, and ML models.

### Non-Functional Requirements

- **Scalability**: Support for multiple concurrent users and large datasets.
- **Performance**: High-speed prediction response and optimized MongoDB queries.
- **Security**: JWT-based auth, encrypted passwords, and role-based access.
- **Cloud Ready**: Configured for easy deployment to AWS/Heroku/Azure.

---

## 📂 System Modules

### 1️⃣ Authentication Module

- User & Admin Login/Registration
- Role-based Access Control (User/Admin)
- Password Encryption & JWT Token Management

### 2️⃣ User Module

- Consumption Dataset Upload (Excel)
- Household & Device-level Usage Tracking
- Personalized Recommendations & Alerts

### 3️⃣ Admin Module

- Global Analytics & System Logs
- User Activation/Deactivation
- Model Management & Dataset Oversight

### 4️⃣ Data Management Module

- Data Preprocessing (Normalization, Duplicates Removal)
- Raw and Processed Data Storage
- Prediction History Logging

### 5️⃣ Prediction & ML Module

- Models: Linear Regression, Random Forest, LSTM (Planned)
- Short-term & Long-term Forecasts
- Accuracy Metrics (MAE, RMSE)

### 6️⃣ Dashboard & Visualization

- Predicted vs Actual Comparison Graphs
- Peak Hour Detection & Usage Trends
- Appliance-level Pie Charts

### 7️⃣ Reporting & Alerts

- Daily/Weekly/Monthly Automated Reports
- Abnormal Usage & Threshold Alerts
- Estimated Bill & Carbon Footprint Calculation

---

## 🔗 Required APIs (Frontend ↔ Backend)

### 🔐 Authentication

| Method | Endpoint                    | Description           |
| :----- | :-------------------------- | :-------------------- |
| POST   | `/api/auth/register`        | Register new user     |
| POST   | `/api/auth/login`           | User login            |
| POST   | `/api/auth/admin-login`     | Admin portal login    |
| GET    | `/api/auth/profile`         | Get current user info |
| PUT    | `/api/auth/change-password` | Security update       |

### 👤 User & Admin

| Method | Endpoint                         | Description          |
| :----- | :------------------------------- | :------------------- |
| GET    | `/api/users/`                    | List users (Admin)   |
| DELETE | `/api/users/{id}`                | Remove user (Admin)  |
| GET    | `/api/admin/logs`                | System activity logs |
| PUT    | `/api/admin/users/{id}/activate` | Manage status        |

### ⚡ Consumption & Predictions

| Method | Endpoint                         | Description           |
| :----- | :------------------------------- | :-------------------- |
| POST   | `/api/consumption/upload-excel`  | Process dataset       |
| GET    | `/api/consumption/history`       | Historical usage      |
| POST   | `/api/prediction/generate`       | Run ML models         |
| GET    | `/api/prediction/compare-actual` | Accuracy check        |
| POST   | `/api/prediction/retrain`        | Update models (Admin) |

### 📊 Dashboard & Reports

| Method | Endpoint                      | Description   |
| :----- | :---------------------------- | :------------ |
| GET    | `/api/dashboard/user-summary` | Chart data    |
| GET    | `/api/dashboard/peak-hours`   | Energy alerts |
| GET    | `/api/reports/download-pdf`   | Export PDF    |
| GET    | `/api/reports/download-excel` | Export Excel  |

---

## 🗄 Database Collections (MongoDB)

1. **Users**: Credentials, roles, and profiles.
2. **Devices**: Device names, types, and owner details.
3. **ConsumptionData**: Timestamps and power usage (kWh).
4. **Predictions**: Forecasted values vs Actual, MAE/RMSE metrics.
5. **Categories**: Device categories for better analytics.
6. **Alerts**: Notifications, threshold triggers, and tips.
7. **Reports**: History of generated files and paths.

---

## 🚀 Advanced / Future Scope

- **Carbon Footprint Estimation**: Calculate environmental impact.
- **Real-time Monitoring**: WebSocket integration for live data.
- **Mobile App**: Swift/Kotlin expansion.
- **Industrial Support**: Large-scale energy management.

---

## 📁 Project Structure

```
backend/
├── manage.py
├── requirements.txt
├── .env
├── config/              # Core Django Settings & URLs
├── apps/                # Modular Application Folders
│   ├── authentication/
│   ├── users/
│   ├── devices/
│   ├── consumption/
│   ├── predictions/
│   ├── alerts/          (Planned)
│   └── reports/         (Planned)
└── ml_models/           # ML Models & Training Scripts
    ├── train_models.py
    └── *.pkl
```
