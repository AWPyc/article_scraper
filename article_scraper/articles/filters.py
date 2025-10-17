from .models import Article
import django_filters

class ArticleFilter(django_filters.FilterSet):
    url = django_filters.CharFilter(field_name='url', lookup_expr='icontains')

    class Meta:
        model = Article
        fields = ['url']