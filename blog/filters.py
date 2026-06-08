import django_filters
from blog.models import Post, Category, Comment


class PostFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    is_published = django_filters.BooleanFilter()
    created_at = django_filters.DateFromToRangeFilter()

    class Meta:
        model = Post
        fields = ['title', 'is_published', 'created_at']