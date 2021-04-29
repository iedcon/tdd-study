from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Item, List

# Create your views here.
def home_page(request):
    return render(request, 'home.html')


def view_list(request, list_id):
    target_list = List.objects.get(id=list_id)
    return render(request, 'list.html', {'list': target_list})


def new_list(request):
    new_list = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], list=new_list)
    return redirect(f'/lists/{new_list.id}/')


def add_item(request, list_id):
    Item.objects.create(text=request.POST['item_text'], list_id=list_id)
    return redirect(f'/lists/{list_id}/')