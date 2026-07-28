#!/bin/bash
gunicorn cornhouse.wsgi:application --threads 4
