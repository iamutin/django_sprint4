from django.db.models import Count
from django.utils import timezone

from blog.models import Post


def published_posts():
    return (
        Post.objects.filter(
            is_published=True,
            pub_date__lte=timezone.now(),
            category__is_published=True
        )
        .annotate(comment_count=Count('comments'))
        .select_related('author', 'category', 'location')
        .order_by('-pub_date')
    )
