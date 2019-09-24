from django.contrib import admin

# Register your models here.
from .models import Business_Word, Message_Analysis

admin.site.register(Business_Word)
admin.site.register(Message_Analysis)