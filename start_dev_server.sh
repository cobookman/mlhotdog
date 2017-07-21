#!/bin/bash
gunicorn -b :8080 server:app -w 8
