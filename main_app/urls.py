from django.urls import path
from main_app import views


urlpatterns = [
    path('publishers/', views.publisher_list),
    path('publisher/<int:pk>/', views.publisher_detail),
    path('shop/<int:pk>/', views.shop_details),
]
