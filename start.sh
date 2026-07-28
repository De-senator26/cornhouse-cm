#!/bin/bash
python manage.py migrate
echo "from apps.users.models import User; User.objects.filter(username='Admin').exists() or User.objects.create_superuser('Admin', 'swengkaanslem@gmail.com', 'Anslem26')" | python manage.py shell
gunicorn cornhouse.wsgi:application