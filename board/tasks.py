from celery import shared_task
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from .models import Advertisement, Comment
import logging

# Настройка логирования
logger = logging.getLogger(__name__)


@shared_task(bind=True, default_retry_delay=300, max_retries=3)
def send_response_notification(self, comment_id):
    try:
        try:
            comment = Comment.objects.get(id=comment_id)
            ad = comment.advertisement

            subject = _('Новый отклик на ваше объявление')
            message = _(
                'Пользователь {username} оставил отклик на ваше объявление "{title}".\n'
                'Текст отклика: {comment_text}'
            ).format(
                username=comment.author.get_full_name() or comment.author.username,
                title=ad.title,
                comment_text=comment.text[:100]
            )

            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [ad.author.email],
                fail_silently=False,
            )

            logger.info(f'Email sent to {ad.author.email} about new response')

        except ObjectDoesNotExist as e:
            logger.warning(f'Object not found: {str(e)}')
            raise self.retry(exc=e)
        except Exception as e:
            logger.error(f'Error sending email: {str(e)}')
            raise self.retry(exc=e)

    except self.max_retries:
        logger.error(f'Max retries reached for task {self.request.id}')


@shared_task(bind=True, default_retry_delay=300, max_retries=3)
def send_accept_notification(self, comment_id):
    try:
        try:
            comment = Comment.objects.get(id=comment_id)

            subject = _('Ваш отклик принят')
            message = _(
                'Ваш отклик на объявление "{title}" был принят автором.\n'
                'Автор объявления: {author_name}'
            ).format(
                title=comment.advertisement.title,
                author_name=comment.advertisement.author.get_full_name() or comment.advertisement.author.username
            )

            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [comment.author.email],
                fail_silently=False,
            )

            logger.info(f'Email sent to {comment.author.email} about response acceptance')

        except ObjectDoesNotExist as e:
            logger.warning(f'Object not found: {str(e)}')
            raise self.retry(exc=e)
        except Exception as e:
            logger.error(f'Error sending email: {str(e)}')
            raise self.retry(exc=e)

    except self.max_retries:
        logger.error(f'Max retries reached for task {self.request.id}')
