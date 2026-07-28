#!/bin/bash
gunicorn cornhouse.wsgi:application
