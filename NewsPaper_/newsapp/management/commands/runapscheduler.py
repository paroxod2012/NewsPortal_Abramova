import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from django.core.mail import EmailMultiAlternatives
from newsapp.models import User, Category, Post
import datetime
from django.template.loader import render_to_string

logger = logging.getLogger(__name__)


# наша задача по выводу текста на экра
def my_job():
    for category in Category.objects.all():
        news_from_each_category = []
        week_number_last = datetime.datetime.now().isocalendar()[1] - 1

        for news in Post.objects.filter(postCategory=category.id,
                                        dateCreation__week=week_number_last).values('pk',
                                                                                    'title',
                                                                                    'dateCreation',
                                                                                    'postCategory__name'):
            date_format = news.get("dateCreation").strftime("%m/%d/%Y")

            new = (f' http://127.0.0.1:8000/news/{news.get("pk")}, {news.get("title")}, '
                   f'Category: {news.get("postCategory__name")}, Date creation: {date_format}')

            news_from_each_category.append(new)
        print()
        print('+++++++++++++++++++++++++++++', category.name, '++++++++++++++++++++++++++++++++++++++++++++')
        print()
        print("Письма будут отправлены подписчикам категории:", category.name, '( id:', category.id, ')')

        # переменная subscribers содержит информацию по подписчиках, в дальшейшем понадобится их мыло
        subscribers = category.subscribers.all()

        # этот цикл лишь для вывода инфы в консоль об адресах подписчиков, ни на что не влияет, для удобства и тестов
        print('по следующим адресам email: ')
        for qaz in subscribers:
            print(qaz.email)

        print()
        print()

        for subscriber in subscribers:
            print('____________________________', subscriber.email, '___________________________________')
            print()
            print('Письмо, отправленное по адресу: ', subscriber.email)
            html_content = render_to_string(
                'sender.html', {'user': subscriber,
                                'text': news_from_each_category,
                                'category_name': category.name,
                                'week_number_last': week_number_last})

            msg = EmailMultiAlternatives(
                subject=f'Greetings, {subscriber.username}, new papers in your favorite category!',
                from_email='ksenia.ivanichkina@yandex.ru',
                to=[subscriber.email]
            )

            msg.attach_alternative(html_content, 'text/html')
            print()

            # для удобства в консоль выводим содержимое нашего письма, в тестовом режиме проверим, что и
            # кому отправляем
            print(html_content)

            # Чтобы запустить реальную рассылку нужно раскоментить нижнюю строчку
            msg.send()

# функция, которая будет удалять неактуальные задачи
def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу нашему задачнику
        scheduler.add_job(
            my_job,
            trigger=CronTrigger(second="*/10"),
            # То же, что и интервал, но задача тригера таким образом более понятна django
            id="my_job",  # уникальный айди
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")

# time_threshold = datetime.datetime.now() - datetime.timedelta(weeks=1)
#     new_posts = Post.objects.filter(dateCreation__gt=time_threshold)
#     cat = new_posts.values_list('postCategory')
#     subscribers = User.objects.filter(category__in=cat)
#     # emails = subscribers.values_list('email').distinct()
#     # email_cat_dict = {}
#     # for e in emails:
#     #     email_cat_dict.update({e[0]: list(User.objects.get(email=e[0]).category_set.all())})
#     # emails_list = list(email_cat_dict.keys())
#     variables = {'new_posts': new_posts, }
#
#     for sub in subscribers:
#         send_mail(
#             subject=f'New articles for you!',
#             message=f'Greetings {User.objects.get(pk=sub["subscribers"]).username}! '
#                     f'New interesting post for you! \n'
#                     f'{new_posts.title} : {new_posts.text[0:5]}',
#             from_email='ksenia.ivanichkina@yandex.ru',
#             recipient_list=[User.objects.get(pk=sub["subscribers"]).email]
#         )