from django.urls import path

from base.views import user_views as views

urlpatterns = [
    path('all/', views.getUsers, name='all-users'),
    path('profile/', views.getUserProfile, name='my-profile'),
    path('profile/update/', views.updateUserProfile, name='update-profile'),

    path('register/', views.register, name='register'),   

    path('login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
]
