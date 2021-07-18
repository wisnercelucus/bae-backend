from django.urls import path

from . import views

urlpatterns = [
    path('', views.getRoutes, name="routes"),
    path('products/', views.getProducts, name="products"),
    path('products/<str:pk>/', views.getProduct, name="product"),
    
    path('users/all/', views.getUsers, name='all-users'),
    path('users/me/', views.getUserProfile, name='my-profile'),

    path('users/register/', views.register, name='register'),   

    path('users/login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
]
