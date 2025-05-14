#!/bin/bash
cp .env.deployment .env
source env/bin/activate
gunicorn main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:7080