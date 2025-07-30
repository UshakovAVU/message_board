# celery.py
import os
from celery import Celery

# Устанавливаем переменную окружения для Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'board_project.settings')

# Создаем экземпляр Celery
app = Celery('board_project')

# Конфигурация из Django settings
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматическое обнаружение задач
app.autodiscover_tasks()

# Дополнительные настройки для Windows
app.conf.update(
    worker_pool='solo',  # Используем solo вместо prefork для Windows
    worker_max_tasks_per_child=100,
    worker_max_memory_per_child=51200,  # 50MB
    task_track_started=True,
    task_ignore_result=True,
    broker_connection_max_retries=3,
    broker_connection_retry_max_interval=5,

    # Дополнительные настройки производительности
    worker_prefetch_multiplier=1,  # Уменьшаем предварительную выборку
    worker_send_task_events=True,  # Включаем события задач

    # Настройки сериализации
    accept_content=['json'],
    task_serializer='json',
    result_serializer='json',

    # Настройки тайм-аутов
    task_time_limit=300,  # Таймаут задачи в секундах
    task_soft_time_limit=240,  # Мягкий таймаут

    # Настройки логгирования
    worker_hijack_root_logger=False,
    worker_redirect_stdouts=False,

    # Настройки брокера
    broker_transport_options={
        'visibility_timeout': 3600,  # Таймаут видимости задачи
        'max_retries': 3,
        'interval_start': 1,
        'interval_step': 2,
        'interval_max': 30
    }
)


# Функция для автоматического обнаружения задач
@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')