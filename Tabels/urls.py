from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
#    path('<name>/', views.Server.as_view(), name='Servers'),
    path('<name>/', views.HomeView.as_view(), name='Testing'),
]