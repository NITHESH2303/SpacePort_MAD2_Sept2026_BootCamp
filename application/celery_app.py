from celery import Celery
from celery.schedules import crontab

celery = Celery("spaceport_tasks")

def init_celery(celery_app, app):
    celery_app.conf.update (
        broker_url = app.config.get('CELERY_BROKER_URL', 'redis://localhost:6379/14'),
        result_backend = app.config.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379/14'),
        timezone='Asia/Kolkata',
        enable_utc=False,
        beat_schedule={
            'pulse-every-10-secs': {
                'task': 'tasks.heartbeat_ping',
                'schedule': 10.0,
            },
            'daily-flight-reminders': {
                'task': 'tasks.daily_flight_reminder',
                'schedule': crontab(hour=16, minute=33),
            },
            'daily-flight-reminders-2': {
                'task': 'tasks.daily_flight_reminder',
                'schedule': crontab(hour=16, minute=35),
            },
        }
    )
    
    TaskBase = celery_app.Task
    
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery_app.Task = ContextTask
    return celery_app