import django.forms
from django_filters import FilterSet, DateFilter
from .models import Post

class NewsFilter(FilterSet):

    date = DateFilter(field_name='dateCreation', lookup_expr='gt', label='Date from', widget=django.forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Post
        fields = {'title': ['exact'], 'postCategory': ['exact']}


