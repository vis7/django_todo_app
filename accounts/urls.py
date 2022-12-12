from django.urls import path

from .views import activate, signup

app_name = 'accounts'

urlpatterns = [
    path('accounts/signup', signup, name='signup'),
    path('activate/<uidb64>/<token>', activate, name='activate'),
]
