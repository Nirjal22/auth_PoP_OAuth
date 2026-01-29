from django.urls import path

from .views import  SecureDataView, UserRegisterView, UserLoginView


urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='user_register'),
    path('login/', UserLoginView.as_view(), name='user_login'), 
    path('secure/', SecureDataView.as_view(), name='secure_data'),
]
