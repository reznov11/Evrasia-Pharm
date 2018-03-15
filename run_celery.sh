#!/bin/bash

source venv/bin/activate
venv/bin/celery worker -A celery_worker.celery --loglevel=info