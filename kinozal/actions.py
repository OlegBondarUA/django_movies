import logging
from threading import Thread, Lock

from django.db.models import Model

from deep_translator import GoogleTranslator


translator = GoogleTranslator('uk', 'en')

logger = logging.getLogger('logit')

lock = Lock()


def translate_film(modeladmin, request, queryset):
    for obj in queryset:
        Thread(target=translate_object, args=(obj,)).start()


translate_film.short_description = 'Translate Movie'


def translate_object(obj: Model):
    try:
        with lock:
            translate_list = [obj.title, obj.description, obj.duration]
            translated = translator.translate_batch(translate_list)

            obj.title_en = translated[0]
            obj.description_en = translated[1]
            obj.duration_en = translated[2]
            obj.save()
    except Exception as error:
            logger.error(f'translate - {obj.title} -> {error}')


def translate_name(modeladmin, request, queryset):
    objects_list = []
    for obj in queryset:
        if not obj.name_en:
            objects_list.append(obj)

    Thread(
        target=translate_name_data,
        args=(objects_list, modeladmin.model)
    ).start()


def translate_name_data(objects_list: list[Model], model: Model):
    objects_names_list = []
    try:
        translated = translator.translate_batch(
            [obj.name for obj in objects_list]
        )
        for obj, translated_name in zip(objects_list, translated):
            obj.name_en = translated_name
            objects_names_list.append(obj)

        model.objects.bulk_update(objects_names_list, ['name_en'])
    except Exception as error:
        logger.error(f'Translating name error -> {error}')
