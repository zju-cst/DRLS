#!/usr/bin/env bash
export FLASK_APP=autoapp.py
export FLASK_DEBUG=0
npm run build
flask run --host=0.0.0.0 --port=5000