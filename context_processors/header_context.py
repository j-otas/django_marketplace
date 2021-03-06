from django.template.context_processors import request
from django.shortcuts import get_object_or_404
from main_marketplace.models import SubCategory, MainCategory,City

def main_categories(request):
    return {'main_categories': MainCategory.objects.all()}

def categories(request):
    return {'categories': SubCategory.objects.all()}

def full_categories(request):
    full_categories = { }

    for main in MainCategory.objects.all():
        full_categories[main] = SubCategory.objects.filter(main_category = main)

    return {'full_categories':  full_categories}

def selected_city(request):
    try:
        if City.objects.get(id = request.session['selected_city_id']):
            selected_city, created = City.objects.get_or_create(id = request.session['selected_city_id'])
        else:
            select_city_id, created = City.objects.get_or_create(name="Иркутск")
            select_city_id = select_city_id.id
            request.session["selected_city_id"] = select_city_id
            selected_city = City.objects.get( id=select_city_id)
        return {'selected_city': selected_city}
    except:
        print("ВЫБРАННОГО ГОРОДА НЕТ -- БУДЕТ ОТОБРАЖЕН ИРКУТСК")
        select_city_id, created = City.objects.get_or_create( name="Иркутск")
        select_city_id = select_city_id.id
        request.session["selected_city_id"] = select_city_id
        selected_city = City.objects.get( id=request.session['selected_city_id'])
        return {'selected_city': selected_city}

def all_cities(request):
    return {'all_cities': City.objects.all()}