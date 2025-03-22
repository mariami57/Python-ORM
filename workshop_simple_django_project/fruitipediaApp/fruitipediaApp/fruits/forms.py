from django import forms
from .models import Category, Fruit


class CategoryBaseForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

class CategoryForm(CategoryBaseForm):
    pass

class FruitBaseForm(forms.ModelForm):
    class Meta:
        model = Fruit
        fields = '__all__'

class FruitAddForm(FruitBaseForm):
    pass

class FruitEditForm(FruitBaseForm):
    pass

class FruitDeleteForm(FruitBaseForm):
    pass

