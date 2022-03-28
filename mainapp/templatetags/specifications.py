

from django import template

from django.utils.safestring import mark_safe
from mainapp.models import Smartphone, Notebook, Lighting, NonStationaryWire, Lampa



register = template.Library()



TABLE_HEAD = """
                <table class="table">
                  <tbody>
             """

TABLE_TAIL = """
                  </tbody>
                </table>
             """

TABLE_CONTENT = """
                    <tr>
                      <td>{name}</td>
                      <td>{value}</td>
                    </tr>
                """


PRODUCT_SPEC = {
    'notebook': {
        'Диагональ': 'diagonal',
        'Тип дисплея': 'display',
        'Частота процессора': 'processor_freq',
        'Оперативная память': 'ram',
        'Видеокарта': 'video',
        'Время работы аккумулятора': 'time_without_charge',
        'Количество': 'count_view'

    },
    'smartphone': {
        'Диагональ': 'diagonal',
        'Тип дисплея': 'display',
        'Разрешение экрана': 'resolutions',
        'Заряд аккумулятора': 'accum_volume',
        'Оперативная память': 'ram',
        'Наличие слота для SD карты': 'sd',
        'Максимальный объем SD карты': 'sd_volume',
        'Камера (МП)': 'main_cam_mp',
        'Фронтальная камера (МП)': 'frontal_cam_mp',
        'Количество': 'count_view'
    },
    'lighting': {

        'Наименование товара': 'name',
        'Серия': 'seria',
        'Брэнд': 'brand',
        'Артикул производителя': 'articals',
        'Срок гарантии': 'garant_time',
        'Страна производитель': 'created_cantry',
        'Мощность': 'power',
        'Цоколь': 'plinth',
        'Форма Лампы': 'form_light',
        'Количество': 'count_view'
    },

    'nonstationarywire': {

        'Наименование товара': 'name',
        'Серия': 'seria',
        'Брэнд': 'brand',
        'Артикул производителя': 'articals',
        'Срок гарантии': 'garant_time',
        'Страна производитель': 'created_cantry',
        'Наминальное сечение проводника': 'nominal_section',
        'Материал жил проводника': 'material',
        'Класс токопроводящей жилы': 'conductor_class',
        'Форма жил проводника': 'form_wire',
        'Количество': 'count_view'

    },

    'lampa': {

        'Наименование товара': 'name',
        'Серия': 'seria',
        'Брэнд': 'brand',
        'Артикул производителя': 'articals',
        'Срок гарантии': 'garant_time',
        'Страна производитель': 'created_cantry',
        'Мощность': 'power',
        'Цоколь': 'plinth',
        'Форма Лампы': 'form_light'
    },
}


def get_product_spec(product, model_name):
    table_content = ""
    for name, value in PRODUCT_SPEC[model_name].items():
        table_content += TABLE_CONTENT.format(name=name, value=getattr(product, value))
    return table_content 


@register.filter
def product_spec(product):
    model_name = product.__class__._meta.model_name
    if isinstance(product, Smartphone):
        if not product.sd:
            PRODUCT_SPEC['smartphone'].pop('Максимальный объем SD карты', None)
        else:
            PRODUCT_SPEC['smartphone']['Максимальный объем SD карты'] = 'sd_volume'
    return mark_safe(TABLE_HEAD + get_product_spec(product, model_name) + TABLE_TAIL)
	
'''  
    def get_product_spec(product, model_name):
    table_content = ''
    for name, value in PRODUCT_SPEC[model_name].items():
        table_content += TABLE_CONTENT.format(name=name, value=getattr(product, value))
    return table_content


@register.filter
def product_spec(product):
    model_name = product.__class__._meta.model_name
    if isinstance(product, Smartphone):
        if not product.sd:
            PRODUCT_SPEC['smartphone'].pop('Максимальный объем SD карты', None)
        else:
            PRODUCT_SPEC['smartphone']['Максимальный объем SD карты'] = 'sd_volume_max'
    return mark_safe(TABLE_HEAD + get_product_spec(product, model_name) + TABLE_TAIL)

'''