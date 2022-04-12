import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cars_API.settings')

app = Celery("cars_API")
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@app.task(bind=True)
def celery_test(self):
    print("PING PING CELERY, request{}".format(self.request))
