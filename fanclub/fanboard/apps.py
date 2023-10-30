from django.apps import AppConfig


class FanboardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'fanboard'

    def ready(self):
        import fanboard.signals
      
        
        # нам надо переопределить метод ready, 
 # чтобы при готовности нашего приложения импортировался модуль со всеми функциями обработчиками