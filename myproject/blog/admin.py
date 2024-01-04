from django.contrib import admin, messages
from .models import Article, Category, IPAddress
from django.utils.translation import ngettext


# Register your models here.
@admin.action(description="انتشار مقالات انتخاب شده")
def make_published(modeladmin, request, queryset):
    updated = queryset.update(status="p")
    modeladmin.message_user(
        request,
        ngettext(
            "%d مقاله منتشر شد.",
            "%d مقاله منتشر شدند.",
            updated,
        )
        % updated,
        messages.SUCCESS,
    )


@admin.action(description="پیش نویس شدن مقالات انتخاب شده")
def make_draft(modeladmin, request, queryset):
    updated = queryset.update(status="d")
    modeladmin.message_user(
        request,
        ngettext(
            "%d مقاله پیش نویس شد.",
            "%d مقاله پیش نویس شدند.",
            updated,
        )
        % updated,
        messages.SUCCESS,
    )


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('position', 'title', 'slug', 'parent', 'status')
    list_filter = (['status'])
    search_fields = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Category, CategoryAdmin)


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'thumbnail_tag', 'slug', 'author', 'jpublish', 'status', 'is_special', 'category_to_str', 'count_ip_address')
    list_filter = ('publish', 'status')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['-status', '-publish']
    actions = [make_published, make_draft]


admin.site.register(Article, ArticleAdmin)


class IPAddressAdmin(admin.ModelAdmin):
    list_display = ('ip_address',)


admin.site.register(IPAddress, IPAddressAdmin)
