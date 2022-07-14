from django import forms
from .models import Account

class AccountForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'username', 'email', 'password']

    def __init__(self, *args, **kwargs):
        super(AccountForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
            # placeholder
            field_name = field.replace("_", " ").title()
            self.fields[field].widget.attrs.update({'placeholder': f"Enter {field_name}"})

    def clean(self):
        cleaned_data = super(AccountForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("Password Doesn't Match!")

        if len(password) < 6:
            raise forms.ValidationError("Password should be at least 6 character!")

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'username', 'email', 'phone_number', 'profile_picture']

    def __init__(self, *args, **kwargs):
        super(ProfileEditForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
            # placeholder
            field_name = field.replace("_", " ").title()
            self.fields[field].widget.attrs.update({'placeholder': f"Enter {field_name}"})
        self.fields['profile_picture'].widget.attrs.update({'class': 'd-block'})
        self.fields['profile_picture'].widget.attrs.update({'required': 'required'})