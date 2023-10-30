from django import forms
from django_filters import FilterSet, CharFilter, ChoiceFilter, DateTimeFilter
from .models import*




class PostFilter(FilterSet):

    author = CharFilter(
                      field_name='author__user__username',
                      widget=forms.TextInput(attrs={'placeholder':'геймер',
                                                    'class':'scro',
                                                 }),
                      label='ПОИСК ПО АВТОРУ',
                      lookup_expr='iregex', # имена без учета регистров символов
                      required = False
                    )


    title = CharFilter(field_name='title', 
                      widget=forms.TextInput(attrs={'placeholder':'текст заголовка',
                                                   'class':'scro',
                                                     }), 
                      label='ПОИСК ПО ЗАГОЛОВКУ', 
                      lookup_expr='iregex',
                      required = False,
                      )
    
    content = CharFilter(
                      field_name='content',
                      widget=forms.TextInput(attrs={'placeholder':'текст новости',
                                                   'class':'scro',
                                                 }),
                      label='ПОИСК ПО ТЕКСТУ',
                      lookup_expr='iregex',
                     required = False
                    )
    category = ChoiceFilter(label='КАТЕГОРИЯ',
                                 widget=forms.Select(attrs={'class':'scro'}),
                                choices = [
                                    ('Tn', 'Танки'),
                                    ('Hl', 'Хилы'),
                                    ('DD', 'ДД'),
                                    ('DR', 'Торговцы'),
                                    ('GM', 'Гилдмастеры'),
                                    ('QG', 'Квестгиверы'),
                                    ('BS', 'Кузнецы'),
                                    ('LW', 'Кожевники'),
                                    ('PM', 'Зельевары'),
                                    ('SM', 'Мастера заклинаний')
                                ]
                                )
                               

    dataCreation = DateTimeFilter(widget=forms.TimeInput(attrs={'placeholder':'позже даты',
                                                               'class':'scro',
                                                        }),
                               label='ПОИСК ПО ДАТЕ',
                               lookup_expr='gt',
                               required = False)
    
    rating = CharFilter(field_name='rating', 
                      widget=forms.TextInput(attrs={'placeholder':'рейтинг',
                                                   'class':'scro'  }), 
                      label='ПОИСК ПО РЕЙТИНГУ', 
                      lookup_expr='iregex',
                      required = False,
                      )