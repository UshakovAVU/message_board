from django.apps import AppConfig


class BoardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'board'

    def ready(self):
        try:
            # Отложенный импорт моделей и сигналов
            from . import signals
            from . import tasks

            # Подключаем сигналы к задачам
            from .signals import response_created, response_accepted
            from .tasks import send_response_notification, send_accept_notification

            response_created.connect(send_response_notification.delay)
            response_accepted.connect(send_accept_notification.delay)

        except Exception as e:
            # Обработка ошибок при импорте
            print(f"Ошибка при подключении сигналов: {e}")


