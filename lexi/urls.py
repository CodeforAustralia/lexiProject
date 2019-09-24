from django.urls import path

from .import views

urlpatterns = [
    #ex: /lexi/
    path('', views.index, name='index'),
    #ex: /lexi/commonwords/
    path('commonwords/', views.commonWords, name='common words'),
    #ex: /lexi/businesswords/
    path('businesswords/', views.businessWords, name='business words'),
    #ex: /lexi/messageanalysis/
    path('messageanalysis/', views.messageAnalysis, name='message analysis'),
    #ex: /lexi/messageanalysis/
    path('messageanalysis/<int:analysis_id>/', views.detail, name='detail'),
]