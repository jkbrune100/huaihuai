#!/bin/bash

echo "Starting server"
gunicorn -w 2 -b 0.0.0.0 'app:create_app()'

