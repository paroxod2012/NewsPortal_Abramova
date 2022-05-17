from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from newsapp.models import User, Category, Post
import datetime
from django.template.loader import render_to_string
from django.shortcuts import redirect
from django.core.mail import send_mail

# @shared_task
# def notify_new_post(sender, instance, *args, **kwargs):
#     for cat_id in instance.postCategory.all():
#         users = Category.objects.filter(pk=cat_id.id).values("subscribers")
#         for user_id in users:
#             send_mail(
#                  subject=f'{instance.title}',
#                  message=f'Greetings {User.objects.get(pk=user_id["subscribers"]).username}! '
#                  f'New interesting post for you! \n'
#                          f'{instance.title} : {instance.text[0:5]}  \n'
#                          f'To access the full version please follow the http://127.0.0.1:8000/news/{instance.id}',
#                  from_email='ksenia.ivanichkina@yandex.ru',
#                  recipient_list=[User.objects.get(pk=user_id["subscribers"]).email]
#              )
#
#             return redirect('/news/')

@shared_task
def weekly_send_for_subscribers():
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

        subscribers = category.subscribers.all()

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

            print(html_content)

            msg.send()