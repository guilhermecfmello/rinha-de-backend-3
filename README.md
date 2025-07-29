# 💸 Full Application Setup Guide

This guide explains how to run the full stack of this project, including the main app, background worker, and the payment processor.

## 🐘 1. Run Main Database

Start the main PostgreSQL database using Docker:

```bash
docker-compose -f docker-compose.yaml up -d
```

---

## 💳 2. Run Payment Processor and Its Database

Start the payment processor service along with its database:

```bash
docker-compose -f docker-compose-payment-processor.yaml up
```

---

## 🚀 3. Run API

Navigate to the API folder:

```bash
cd api
```

Activate the virtual environment:

```bash
source venv/bin/activate
```

Run the FastAPI app:

```bash
pip install -r requirements.txt
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

---

## ⚙️ 4. Run Background Worker

Navigate to the worker folder:

```bash
cd worker
```

Activate the virtual environment:

```bash
source venv/bin/activate  # or use `.env\Scriptsctivate` on Windows
```

Run the worker process:

```bash
pip install -r requirements.txt
python main.py
```

---

## ✅ Done!

Your full application stack should now be running locally.
