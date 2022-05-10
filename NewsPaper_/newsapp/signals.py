from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.core.mail import send_mail

from .models import Post, Category, User

from django.shortcuts import redirect


@receiver(m2m_changed, sender=Post.postCategory.through)
def notify_new_post(sender, instance, *args, **kwargs):
    for cat_id in instance.postCategory.all():
        users = Category.objects.filter(pk=cat_id.id).values("subscribers")
        for user_id in users:
            send_mail(
                 subject=f'{instance.title}',
                 message=f'Greetings {User.objects.get(pk=user_id["subscribers"]).username}! '
                 f'New interesting post for you! \n'
                         f'{instance.title} : {instance.text[0:5]}  \n'
                         f'To access the full version please follow the http://127.0.0.1:8000/news/{instance.id}',
                 from_email='ksenia.ivanichkina@yandex.ru',
                 recipient_list=[User.objects.get(pk=user_id["subscribers"]).email]
             )

            return redirect('/news/')