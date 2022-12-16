

from django import template

from django.utils.safestring import mark_safe
#from mainapp.models import NonStationaryWire, Lampa



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
        'Форма жил проводника': 'form_wire'

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
        'Форма Лампы': 'form_light',
        'Световой поток': 'light_stream',
        'Упаковка производителя':'count_prod',
        'Цветовая температура':'color_temer',
        'Диаметр':'diametr',
        'Наминальное напряжение':'naminal_napr',
        'Цвет':'color',
        'Потребляемая мощность':'potreb_power'
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
    if isinstance(product, Lampa):
        if not product.form_light:
            PRODUCT_SPEC['lampa'].pop('Форма Лампы', None)
        else:
            PRODUCT_SPEC['lampa']['Форма Лампы'] = 'form_light'
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