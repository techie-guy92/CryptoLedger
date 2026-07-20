import logging
import time

from celery import shared_task
from django.core.cache import cache
from django.db import models
from django.utils.timezone import localtime, now

from .models import *

# Start the Celery worker
# celery -A config.celery_config worker --loglevel=info
# celery -A config.celery_config worker --pool=solo --loglevel=info
# celery -A config.celery_config worker --pool=solo --loglevel=info -B

# Start Celery beat
# celery -A config.celery_config beat --loglevel=info
