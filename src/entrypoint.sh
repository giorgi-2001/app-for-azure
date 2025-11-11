#!/bin/bash

alembic upgrade head 

gunicorn --bind=0.0.0.0:80 main:app
