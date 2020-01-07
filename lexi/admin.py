from django.contrib import admin

# Register your models here.
from .models import Business_Word, Message_Analysis, Configuration

admin.site.register(Business_Word)
admin.site.register(Message_Analysis)
admin.site.register(Configuration)