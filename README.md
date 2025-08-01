# Locust Lab 
**Locust Lab** is an open-source load testing framework built on top of [Locust](https://locust.io), designed specifically for testing **RESTful APIs**. Currently using [restful-booker](https://restful-booker.herokuapp.com/apidoc/index.html) API's for Testing.  It provides a plug-and-play solution for simulating real-world usage, tracking performance bottlenecks, and preparing for scalability — with plans for future CI/CD and Docker support.


## 🚀 Features

- ✅ Modular structure with authentication and payload utilities
- ✅ Token-based authentication handling
- ✅ Dynamic JSON payloads for request bodies
- ✅ Realistic API testing lifecycle: create, read, update, delete
- ✅ Environment-driven configuration via `.env`
- 🔜 CI/CD integration support (GitHub Actions, Jenkins, etc.)
- 🔜 Docker support for distributed test execution

## 🛠️ Project Structure
``` 
Locuslab/
├── Locustfiles/
│   └── locustfile.py
├── Configurations/
│   ├── auth.py
│   ├── utils.py
│   └── payloads/
│       ├── createBooking.json
│       └── updateBooking.json
├── .env
├── locust.config          
├── requirements.txt
└── README.md

```
## ⚙️ Setup Instructions
### 1. 📥 Clone the Repository
```
git clone https://github.com/jamilsadiq/LocustLab.git
cd LocustLab
```
### 2. 📦 Install Dependencies
```
pip install -r requirements.txt
```
### 3. 🧪 Configure Environment
```
BASE_URL= https://restful-booker.herokuapp.com
USER_NAME= <use_name>
PASSWORD= <password>
```
These values are used by the authentication module to fetch a token.
### 4. 🚀 Run the Test
```
locust --config locust.conf
or
locust -f Locustfiles/locustfile.py
```
## 📊 Simulated Workflow
The booking_lifecycle task simulates a complete REST API cycle for [restful-booker](https://restful-booker.herokuapp.com/apidoc/index.html) APIs:

- ✅ Health Check: /ping

- 📝 Create Booking: /booking

- 🔍 Get Booking by ID: /booking/{id}

- 🔁 Update Booking: /booking/{id}

- ❌ Delete Booking: /booking/{id}

Each step includes response validation, logging, and error reporting.
## 📌 Authentication Handling
Authentication is triggered at the start of the test using credentials from your ```.env``` file. If token acquisition fails, the load test will halt automatically.

## 🐳 Coming Soon
✅ Docker support for containerized execution

✅ GitHub Actions for CI/CD load testing

✅ HTML report generation

✅ Test result thresholding and failure gates

## 🤝 Contributing
Feel free to fork the repository, create pull requests, or open issues if you have suggestions or improvements. You can contribute in areas like:

- Scenario writing

- Environment configuration

- CI/CD integration

- Docker orchestration

- Result reporting

## 📄 License
This project is licensed under the MIT License.

## 👤 Maintainer
- Author: Md. Sadiquzzaman

- GitHub: @jamilsadiq

- Email: jamilsadiq00@gmail.com