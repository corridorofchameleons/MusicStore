from django import forms
from django.core.exceptions import ValidationError

from .models import SiteUser, Review, CartItem


class ChangeUserInfoForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='Email')
    phone = forms.IntegerField(required=True, label='Phone number')

    class Meta:
        model = SiteUser
        fields = ('first_name', 'last_name', 'patronym', 'phone', 'address', 'email')


class RegisterUserForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='Email')
    patronym = forms.CharField(required=False, label='Patronym')
    phone = forms.IntegerField(required=True, label='Phone')
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat Password', widget=forms.PasswordInput)

    class Meta:
        model = SiteUser
        fields = ('username', 'first_name', 'last_name', 'patronym',
                  'phone', 'address', 'email', 'password1', 'password2')

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords don\'t match')
        return password2

    def save(self, commit=True):
        user = super().save()
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class ReviewForm(forms.ModelForm):
    rating = forms.ChoiceField(required=True, label='Rate', choices=Review.SCORES, widget=forms.RadioSelect)
    content = forms.CharField(required=True, label='Review', widget=forms.widgets.Textarea())

    class Meta:
        model = Review
        fields = ('rating', 'content')


class CartForm(forms.ModelForm):
    qty = forms.IntegerField()

    class Meta:
        model = CartItem
        fields = ('qty',)


