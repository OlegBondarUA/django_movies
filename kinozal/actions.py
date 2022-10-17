import logging
from threading import Thread

from django.db.models import Model

from deep_translator import GoogleTranslator


translator = GoogleTranslator('uk', 'en')

logger = logging.getLogger('logit')


def translate_film(modeladmin, request, queryset):
    for obj in queryset:
        Thread(target=translate_object, args=(obj,)).start()


def translate_object(obj: Model):
    translate_list = (obj.title, obj.description)
    translated = translator.translate_batch(translate_list)

    obj.title_en = translated[0]
    obj.description_en = translated[1]
    obj.save()
    logger.info(f'Hello - {obj.title_en}')


translate_film.short_description = 'Translate Movie'
