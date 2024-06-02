#!/bin/bash

ls -la

cd /usr/local/app

alembic upgrade head

uvicorn main:app --host 0.0.0.0 --port ${PORT}