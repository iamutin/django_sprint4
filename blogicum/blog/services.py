from django.db.models import Count
from django.utils import timezone

from blog.models import Post


def get_published_posts():
    return Post.objects.filter(
        is_published=True,
        pub_date__lte=timezone.now(),
        category__is_published=True
    )


def annotate_comment_count(queryset=Post.objects):
    return queryset.annotate(
        comment_count=Count('comments')
    ).order_by('-pub_date')
