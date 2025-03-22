from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import  Fruit, Category
from .forms import CategoryForm, FruitAddForm, FruitEditForm, FruitDeleteForm


# Create your views here.
def index(request):
    return render(request, 'common/index.html')

def dashboard(request):
    fruits = Fruit.objects.all()
    context = {'fruits': fruits}
    return render(request, 'common/dashboard.html', context)

def create_fruit_view(request):
    if request.method == "GET":
        form = FruitAddForm()
    else:
        form = FruitAddForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')

    context = {'form': form}
    return render(request, 'fruits/create-fruit.html', context)

def fruit_details_view(request, pk):
    fruit = Fruit.objects.get(pk=pk)
    context = {'fruit': fruit}
    return render(request, 'fruits/details-fruit.html', context)

def edit_fruit_view(request, pk):
    fruit = Fruit.objects.get(pk=pk)
    if request.method == "GET":
        form = FruitEditForm(instance=fruit)
    else:
        form = FruitEditForm(request.POST, instance=fruit)
        if form.is_valid():
            fruit.save()
            return redirect('dashboard')
    context = {'form': form, 'fruit': fruit}

    return render(request, 'fruits/edit-fruit.html', context)

def delete_fruit_view(request, pk):
    fruit = Fruit.objects.get(pk=pk)
    if request.method == "GET":
        form = FruitDeleteForm(instance=fruit)
    else:
        form = FruitDeleteForm(request.POST, instance=fruit)
        if form.is_valid():
            fruit.delete()
            return redirect('dashboard')
    context = {'form': form, 'fruit': fruit}
    return render(request, 'fruits/delete-fruit.html', context)


def create_category_view(request):
    if request.method == 'GET':
        form = CategoryForm()
    else:
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    context = {'form': form}
    return render(request, 'categories/create-category.html', context)