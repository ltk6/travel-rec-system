@echo off

echo =========================
echo 0. Installing Requirements
echo =========================
start cmd /k python -m pip install -r requirements.txt

echo =========================
echo 1. Seeding database
echo =========================
start cmd /k python -m backend.n3_database.seed_with_vectors

echo =========================
echo 2. Starting backend API
echo =========================
start cmd /k python -m backend.n8_api.app

echo =========================
echo 3. Starting Streamlit UI
echo =========================
start cmd /k streamlit run frontend\n7_ui\app.py