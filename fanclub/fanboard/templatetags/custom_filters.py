from django import template
import os

list = os.path.join('static/assets/bad_words.txt') # путь
with open(list, 'r', encoding='utf-8') as file:
    list_badwords = [word.rstrip('\n') for word in file.readlines()]
   



register = template.Library()

@register.filter(name='censor')

def censor(textUser):
    for w in list_badwords:
        textUser = textUser.replace(w, "(слово удалено-проверка фильтром censor)")
    return textUser

