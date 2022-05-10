from django import forms
from .models import Post, User, Category

class NewsForm(forms.ModelForm):
   class Meta:
       model = Post
       fields = [
           'author',
           'postCategory',
           'title',
           'text',
       ]

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'

# class CategoryForm(forms.ModelForm):
#     category = forms.ModelChoiceField(queryset=Category.objects.all())
#
#     class Meta:
#          model = Category
#          fields = ['category']