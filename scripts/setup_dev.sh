#!/usr/bin/env bash
python3 -m venv venv
source venv/bin/activate
pip install -r backend/requirements.txt
cd frontend && npm install
echo "Dev env set up. Copy .env.example -> .env and add your HF_API_TOKEN"
