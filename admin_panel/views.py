from django.shortcuts import render
from django.apps import apps
from django.shortcuts import get_object_or_404
from django.forms import modelform_factory, inlineformset_factory
from django.forms.models import fields_for_model
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
from django.shortcuts import redirect
from account.models import Account
from main_marketplace.models import Product
from django.contrib import messages
from django.http import HttpResponse
from django.db.models import Q

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

class Counter:
    count = 0

    def increment(self):
        self.count += 1
        return ''

    def decrement(self):
        self.count -= 1
        return ''

    def double(self):
        self.count *= 2
        return ''


from django.forms import ModelForm
from django.forms.models import model_to_dict
from django.template.loader import render_to_string
from django.http import JsonResponse


def get_model(num):
    mods = apps.get_models()  # все модели
    model_names = []
    models = []
    for mod in mods:
        if mod._meta.verbose_name[0].isupper():
            model_names.append(mod._meta.verbose_name_plural)
            models.append(mod)
    return models[num]


def get_values_of_objects(objects, object_fields):
    values = []
    for obj in objects:
        temp = []
        for field in object_fields:
            temp.append(getattr(obj, field.name))
        values.append(temp)
    return values


def main_admin_panel(request):
    if not request.user.is_admin:
        return HttpResponse("Нет доступа")
    mods = apps.get_models()  # все модели
    model_names = []
    for mod in mods:
        if mod._meta.verbose_name[0].isupper():
            model_names.append(mod._meta.verbose_name_plural)

    counter = Counter()

    return render(request, 'admin_panel/main_admin_list_page.html', {'table_names': model_names,
                                                                     'counter': counter,
                                                                     'count_products': Product.objects.all().count(),
                                                                     'count_users': Account.objects.all().count()})


@csrf_exempt
def admin_current_table(request, pk):
    context = {}
    selected_model = get_model(pk)  # выбранная пользователем модель(тип данных)

    selected_model_fields = selected_model._meta.fields  # поля принадлежащие модели

    selected_model_objects = selected_model.objects.order_by(
        'id')  # все объекты выбранного типа данных отсортированные по id

    values_of_fields = get_values_of_objects(selected_model_objects, selected_model_fields)  # значения объекта

    field_names = []  # имена полей(столбцов таблицы)

    if request.method == "POST":
        obj_id = request.POST.get('object_id')

        for field in selected_model_fields:  # получаем список имён полей для генерации формы
            if field.editable:
                field_names.append(field.name)

        temp_form = modelform_factory(selected_model,
                                      fields=field_names)  # Форма для выбранного объекта, может используется для создания новой формы, поэтому temp
        obj = get_object_or_404(selected_model, pk=obj_id)  # получаем объект выбранной модели
        form = temp_form(instance=obj)
        modal_context = {
            'form': form,
            'user': request.user,
            'obj': obj,
            'selected_model_name': selected_model._meta.verbose_name,
            'selected_model_objects': selected_model_objects,
            'fields': selected_model_fields,
            'values_of_fields': values_of_fields,
            'tabnum': int(pk),
        }
        result = render_to_string('admin_panel/includes/modal_change_object.html', modal_context)
        return JsonResponse({'result': result})

    context['selected_model_name'] = selected_model._meta.verbose_name_plural
    context['selected_model_objects'] = selected_model_objects
    context['fields'] = selected_model_fields
    context['values_of_fields'] = values_of_fields
    context['tabnum'] = int(pk)

    return render(request, 'admin_panel/admin_table.html', context, )


@csrf_exempt
def accept_change_data(request):
    if request.method == 'POST':
        context = {}
        old_pswd = ''
        selected_model = get_model(int(request.POST.get('tab_id')))  # выбранная пользователем модель(тип данных)
        obj = get_object_or_404(selected_model,
                                pk=int(request.POST.get('object_id')))  # получаем объект выбранной модели

        selected_model_objects = selected_model.objects.order_by(
            'id')  # все объекты выбранного типа данных отсортированные по id

        selected_model_fields = selected_model._meta.fields  # поля принадлежащие модели
        field_names = []  # имена полей(столбцов таблицы)
        for field in selected_model_fields:  # получаем список имён полей для генерации формы
            if field.editable:
                field_names.append(field.name)

        temp_form = modelform_factory(selected_model,
                                      fields=field_names)
        if selected_model == Account:
            old_pswd =  obj.password
        form = temp_form(request.POST, instance=obj)
        if form.is_valid():
            obj = form.save(commit=False)
            if selected_model == Account:
                if old_pswd != form.cleaned_data['password']:
                    obj.set_password(form.cleaned_data['password'])
            obj.save()
        values_of_fields = get_values_of_objects(selected_model_objects, selected_model_fields)  # значения объекта
        context['selected_model_name'] = selected_model._meta.verbose_name
        context['selected_model_objects'] = selected_model_objects
        context['fields'] = selected_model_fields
        context['values_of_fields'] = values_of_fields
        context['tabnum'] = int(request.POST.get('tab_id'))
        context['script_path'] = "/static/js/admin_actions.js"
        result = render_to_string('admin_panel/includes/table_objects.html', context)
        return JsonResponse({'result': result})

        # return render(request, 'admin_panel/admin_table.html', context)


@csrf_exempt
def add_modal_form(request):
    if request.method == "POST":
        context = {}
        selected_model = get_model(int(request.POST.get('tab_id')))  # выбранная пользователем модель(тип данных)
        selected_model_fields = selected_model._meta.fields  # поля принадлежащие модели
        field_names = []  # имена полей(столбцов таблицы)
        for field in selected_model_fields:  # получаем список имён полей для генерации формы
            if field.editable:
                field_names.append(field.name)
        add_form = modelform_factory(selected_model,
                                     fields=field_names)  # Форма для выбранного объекта, может используется для создания новой формы, поэтому temp

        context["add_form"] = add_form
        context['selected_model_name'] = selected_model._meta.verbose_name
        context['tabnum'] = int(request.POST.get('tab_id'))
        result = render_to_string('admin_panel/includes/modal_add_object.html', context)
        return JsonResponse({'result': result})


@csrf_exempt
def accept_add_data(request):
    if request.method == "POST":
        context = {}
        selected_model = get_model(int(request.POST.get('tab_id')))  # выбранная пользователем модель(тип данных)

        selected_model_objects = selected_model.objects.order_by(
            'id')  # все объекты выбранного типа данных отсортированные по id
        selected_model_fields = selected_model._meta.fields  # поля принадлежащие модели
        field_names = []  # имена полей(столбцов таблицы)
        for field in selected_model_fields:  # получаем список имён полей для генерации формы
            if field.editable:
                field_names.append(field.name)

        temp_form = modelform_factory(selected_model, fields=field_names)
        form = temp_form(request.POST)

        if form.is_valid():
            obj = form.save(commit=False)
            print('форма валидная')
            if selected_model == Account:
                obj.set_password(form.cleaned_data['password'])

            obj.save()
        else:
            context_modal_add = {}
            context_modal_add['add_form'] = form
            context_modal_add['tabnum'] = int(request.POST.get('tab_id'))
            print(form.errors)
            result = render_to_string('admin_panel/includes/modal_add_object.html', context_modal_add)
            return JsonResponse({'errors': form.errors, 'result': result})

        values_of_fields = get_values_of_objects(selected_model_objects, selected_model_fields)  # значения объекта

        context['selected_model_name'] = selected_model._meta.verbose
        context['selected_model_objects'] = selected_model_objects
        context['fields'] = selected_model_fields
        context['values_of_fields'] = values_of_fields
        context['tabnum'] = int(request.POST.get('tab_id'))
        context['script_path'] = "/static/js/admin_actions.js"
        result = render_to_string('admin_panel/includes/table_objects.html', context)
        return JsonResponse({'result': result})


@csrf_exempt
def delete_object(request):
    if request.method == "POST":
        context = {}
        selected_model = get_model(int(request.POST.get('tab_id')))  # выбранная пользователем модель(тип данных)
        selected_model_objects = selected_model.objects.order_by(
            'id')  # все объекты выбранного типа данных отсортированные по id
        selected_model_fields = selected_model._meta.fields  # поля принадлежащие модели
        field_names = []  # имена полей(столбцов таблицы)
        for field in selected_model_fields:  # получаем список имён полей для генерации формы
            if field.editable:
                field_names.append(field.name)

        obj = get_object_or_404(selected_model,
                                pk=int(request.POST.get('object_id')))  # получаем объект выбранной модели
        obj.delete()
        values_of_fields = get_values_of_objects(selected_model_objects, selected_model_fields)  # значения объекта

        context['selected_model_name'] = selected_model._meta.verbose_name_plural
        context['selected_model_objects'] = selected_model_objects
        context['fields'] = selected_model_fields
        context['values_of_fields'] = values_of_fields
        context['tabnum'] = int(request.POST.get('tab_id'))
        context['script_path'] = "/static/js/admin_actions.js"
        result = render_to_string('admin_panel/includes/table_objects.html', context)
        return JsonResponse({'result': result})


def set_users_roles(request):
    if not request.user.is_admin:
        return HttpResponse("Нет доступа")
    if request.method == "GET":
        context = {}
        users = Account.objects.all().values()

        context['users'] = users
        return render(request, 'admin_panel/set_users_roles.html', context)
    elif is_ajax(request):
        context = {}
        usr_id = request.POST['user_id']
        usr = Account.objects.get(id = usr_id)
        if request.POST.get('is_staff', False):
            usr.is_staff = True
        else:
            usr.is_staff = False

        if request.POST.get('is_admin', False):
            usr.is_admin = True
        else:
            usr.is_admin = False
        if request.POST.get('is_superuser', False):
            usr.is_superuser = True
        else:
            usr.is_superuser = False
        usr.save()


        users = Account.objects.all().values()
        context['users'] = users
        print(context['users'])
        result = render_to_string('admin_panel/includes/user_tables_roles.html', context)
        return JsonResponse({'result': result})
    elif request.method == "POST":
        print()
        return HttpResponse("Тут логика выдачи")
    else:
        return HttpResponse("Чёто пошло не так")

def search_set_users_roles(request):
    if is_ajax(request):
        context = {}
        search_text = request.POST['search_user_text']
        usrs = Account.objects.all().values()
        if search_text:
            usrs = Account.objects.filter(
                Q(first_name__iregex=search_text)).values()
        context['users'] = usrs
        result = render_to_string('admin_panel/includes/user_tables_roles.html', context)
        return JsonResponse({'result': result})
    else:
        return HttpResponse("Чёто пошло не так")
class ModerateProductList(ListView):
    model = Product
    template_name = 'admin_panel/product_moderate.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        data = {'products': Product.objects.filter(is_moderated=False)}
        return data

def accept_moderate_product(request, pk):
    if is_ajax(request):
        try:
            Product.objects.filter(pk=pk).update(is_moderated=True, is_active = True)
            products = Product.objects.filter(is_moderated = False)
            context = {}
            context ['products'] = products
            result = render_to_string('admin_panel/includes/inc_product_item.html', context)
            return JsonResponse({'result': result})
        except Product.DoesNotExist:
            return HttpResponseNotFound("<h2>Ошибка</h2>")


def cancel_moderate_product(request, pk):
    if is_ajax(request):
        try:
            Product.objects.filter(pk=pk).update(is_moderated=True, is_active = False)
            products = Product.objects.filter(is_moderated=False)
            context = {}
            context['products'] = products
            result = render_to_string('admin_panel/includes/inc_product_item.html', context)
            return JsonResponse({'result': result})
        except Product.DoesNotExist:
            return HttpResponseNotFound("<h2>Ошибка</h2>")

class ModerateUserList(ListView):
    model = Account
    template_name = 'admin_panel/user_moderate.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        data = {'accs': Account.objects.filter(is_moderated=False, is_superuser=False, is_admin=False, is_staff=False)}
        return data

def accept_moderate_user(request, pk):
    if is_ajax(request):
        try:
            Account.objects.filter(pk=pk).update(is_moderated=True)
            accs = Account.objects.filter(is_moderated=False, is_superuser=False, is_admin=False, is_staff=False)
            context = {}
            context['accs'] = accs
            result = render_to_string('admin_panel/includes/inc_user_item.html', context)
            return JsonResponse({'result': result})
        except Product.DoesNotExist:
            return HttpResponseNotFound("<h2>Ошибка</h2>")

def cancel_moderate_user(request, pk):
    if is_ajax(request):
        try:
            Account.objects.filter(pk=pk).update(is_moderated=True, is_active = False)
            accs = Account.objects.filter(is_moderated=False, is_superuser=False, is_admin=False, is_staff=False)
            context = {}
            context['accs'] = accs
            result = render_to_string('admin_panel/includes/inc_user_item.html', context)
            return JsonResponse({'result': result})
        except Product.DoesNotExist:
            return HttpResponseNotFound("<h2>Ошибка</h2>")
