from django.apps import AppConfig


class NewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'newsapp'

    def ready(self):
         import newsapp.signals
    #
    #     from .tasks import send_mails
    #     from .scheduler import news_scheduler
    #
    #     print('START')
    #
    #     news_scheduler.add_job(
    #         id='mail send',
    #         func=send_mails,
    #         trigger='interval',
    #         seconds=10,
    #     )
    #
    #     news_scheduler.start()





