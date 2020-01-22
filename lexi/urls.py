from django.urls import path

from .import views

app_name = 'lexi'
urlpatterns = [
    #ToDo: Define Generic Views (https://docs.djangoproject.com/en/2.2/intro/tutorial04/)
    path('', views.index, name='index'),
    path('analysis/', views.analysis, name='analysis'),
    path('word_test/', views.word_test, name='word test'),
    #path('import', views.import_words, name='import words'),   #For admin purposes only! ToDo: Move to Admin module.
]