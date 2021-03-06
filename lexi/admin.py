from django.contrib import admin

# Register your models here.
from .models import Configuration, Word

admin.site.register(Configuration)

class WordAdmin(admin.ModelAdmin):
    list_display = ['word', 'is_common', 'is_business_word', 'creation_datetime', 'creation_user']
    ordering = ['word']
    list_per_page = 50
    search_fields = ['word']
    list_filter = ['is_common', 'is_business_word', 'creation_datetime', 'creation_user']
    fields = ['word','is_common', 'is_business_word', 'suggestions']
admin.site.register(Word, WordAdmin)