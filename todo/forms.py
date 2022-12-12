from django import forms

from .models import Change, SharePermission, ToDo


class ToDoForm(forms.ModelForm):
    class Meta:
        model = ToDo
        fields = ['title', 'description', 'category', 'status', 'due_date']

class SharePermissionForm(forms.ModelForm):
    class Meta:
        model = SharePermission
        fields = '__all__'

class ChangeForm(forms.ModelForm):
    class Meta:
        model = Change
        fields = ['title', 'description', 'category', 'due_date', 'status']
