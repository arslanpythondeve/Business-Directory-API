from celery import Celery

celery = Celery(
    "business_app",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
)

celery.autodiscover_tasks(["src.business_app"])