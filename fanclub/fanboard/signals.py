from .tasks.basic import comment_send
from .models import Comment
from django.dispatch import receiver
from django.core.exceptions import PermissionDenied
from django.db.models.signals import post_save, m2m_changed

# необходимо прописать в арр.ру если используем сигналы в отдельном файле,
# обязательно проаисать в setting

# сигнал на добавление комментария к посту
# комментарий добавился письмо ушло 

@receiver(post_save, sender = Comment) # sender = Comment декоратор который помогает функции отработать по сигналу
def notify_comment_send(sender, instance,  **kwargs): # instance(экземпляр Comment)
    
      comment_send(instance)