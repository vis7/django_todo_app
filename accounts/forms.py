from django.contrib.auth.forms import UserCreationForm

from accounts.models import User


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')