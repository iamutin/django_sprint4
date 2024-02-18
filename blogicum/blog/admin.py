from django.contrib import admin

from blog.models import Category, Location, Post


class PostInline(admin.StackedInline):
    model = Post
    extra = 0


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'is_published', 'created_at')
    list_display_links = ('title',)
    list_editable = ('is_published',)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    inlines = (PostInline,)
    list_display = ('name', 'is_published', 'created_at')
    list_display_links = ('name',)
    list_editable = ('is_published',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'pub_date',
        'is_published',
        'author',
        'location',
        'created_at'
    )
    list_editable = ('is_published', 'pub_date')
    list_display_links = ('title',)
    search_fields = ('title',)
    list_filter = ('category', 'location')


admin.site.empty_value_display = 'Не задано'
