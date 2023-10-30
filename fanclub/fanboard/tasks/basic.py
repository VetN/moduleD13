
from django.template.loader import render_to_string
from django.core.mail.message import EmailMultiAlternatives
#from news.models import User
from django.conf import settings
from fanclub.settings import DEFAULT_FROM_EMAIL


# функция рассылки уведомления на почту при добавлении новой комментария под постом
# так делаю, если хочу, чтобы рассылка шла  персональная
# это дает возможность обратиться к подписчику по имени
# и получить другие данные юзера
# функция передана в signals.py и  включается там

def comment_send(instance):
    template = 'mail/mail_addcomment.html'
    email_subject = f'Новый комментарий  к посту {instance.commentPost.title} от автора {instance.commentUser.username}'
    email_user = instance.commentPost.author.user.email
    user = instance.commentPost.author.user
    html = render_to_string(
                template_name = template,
                context = {
                   
                    'com': instance, # сам комментарий
                    'user': user,

                    },
                )
    msg = EmailMultiAlternatives(
                    subject= email_subject,
                    body='',
                    from_email= DEFAULT_FROM_EMAIL,
                    to = [email_user,]
                    

            )
    msg.attach_alternative(html, 'text/html')
    msg.send()