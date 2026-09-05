# 🚀 SkillInfy Tech Software Development Internship Portfolio

Welcome to my official internship repository for **SkillInfy Tech**! This repository contains a collection of robust, modular, and professional Python applications built during my software development internship. Each project highlights core programming concepts, file persistence, API integrations, and modern user interface design.

---

## 📁 Repository Structure

```text
Skillinfytech_internship/
│
├── weather_forecast_app/
│   └── weather_forecast.py          # Real-time weather dashboard via OpenWeather API
│
├── expense_tracker_app/
│   ├── expense_tracker.py      # CLI tool for logging expenses and generating CSV reports
│   └── expenses.csv            # Local persistent data storage
│
└── inventory_system/
    ├── inventory_management.py # Streamlit web app with sidebar menu and custom metrics
    └── inventory.csv           # Persistent local stock records

Here is the complete `README.md` text formatted in a clean code block so you can easily copy and paste it directly into your file:

```markdown
```

---

## 🛠️ Projects Overview

### 1. Weather Forecast App (`weather_forecast_app/`)

* **Description:** A weather tool that fetches live atmospheric data using the OpenWeatherMap API.
* **Key Features:**
* Secure API key integration and URL parameter encoding using the `requests` library.
* Real-time extraction and parsing of dynamic JSON payloads.
* Robust network error handling and timeout protections.


* **How to Run:**
```bash
cd weather_forecast_app
streamlit run weather_forecast.py

```



### 2. Personal Expense Tracker (`expense_tracker_app/`)

* **Description:** A modular expense logger that tracks daily spending habits and categorizes financial records locally.
* **Key Features:**
* Automated timestamps via Python's `datetime` module.
* Local data persistence using dynamic cross-platform CSV file handling (`os.path`).
* Custom filtering options and automated category reporting engines.


* **How to Run:**
```bash
cd expense_tracker_app
python expense_tracker.py

```



### 3. Inventory Management System (`inventory_system/`)

* **Description:** A fully menu-driven web dashboard built with **Streamlit** to manage stock quantities, pricing, and valuation.
* **Key Features:**
* **Sidebar Menu Navigation:** Clean, button-driven workflow separating views, additions, updates, and alerts.
* **Smart Upsert Logic:** Automatically detects existing Product IDs to modify records or create new entries safely.
* **Low-Stock Warnings:** Instantly flags items with fewer than 5 units remaining.
* **Custom Financial Metrics:** Large, styled cards displaying total unique products and overall stock valuation.


* **How to Run:**
```bash
cd inventory_system
streamlit run inventory_management.py

```



---

## ⚙️ Tech Stack & Requirements

* **Language:** Python 3.x
* **Core Libraries:** `requests`, `pandas`, `streamlit`, `csv`, `os`, `datetime`

To install all required dependencies at once, run:

```bash
pip install requests pandas streamlit

```

---

## 👤 Author

* **Intern:** Vivan Kansara
* **Organization:** SkillInfy Tech

```

```
