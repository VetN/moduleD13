import datetime
from datetime import datetime
from datetime import timedelta

from fanboard.models import *

from django.template.loader import render_to_string
from django.core.mail.message import EmailMultiAlternatives
from fanclub.settings import DEFAULT_FROM_EMAIL


def week_news(): 
    template = 'mail/mail_newsweek.html'
    email_subject = f'Новые посты за неделю.'
    all_user = Profile.objects.all()
   
    time = datetime.today() - timedelta(weeks=1) #((second=50))
    post_week= Post.objects.filter(dataCreation__gte= time)    
    
    for user in all_user:
        
         
        user_email=User.email
        user=user
       
        html = render_to_string(
                    template_name = template,
                    context = {
                        'post_foruser': post_week,
                        'user': user,
                        },
                    )
        msg = EmailMultiAlternatives(
                    subject= email_subject,
                    body='',
                    from_email= DEFAULT_FROM_EMAIL,
                    to = [user_email,]
                    

                    )
        msg.attach_alternative(html, 'text/html')
        msg.send()






