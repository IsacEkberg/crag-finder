from captcha.fields import CaptchaField
from django import forms
from django.db.models import Q
from django_api.models import APPROVED, BEING_REVIEWED_DELETE
from django.contrib.auth.models import User
from pagedown.widgets import AdminPagedownWidget


class RockFaceAdminForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        """This overrides the constructor, and adds the class datetimepicker."""
        super(RockFaceAdminForm, self).__init__(*args, **kwargs)
        self.fields['geo_data'].widget.attrs['class'] = 'hidden'
        self.fields['short_description'].widget = forms.Textarea(attrs={'cols': '40', 'rows': '2'})
        self.fields['long_description'].widget = AdminPagedownWidget()


class AreaAdminForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        """This overrides the constructor, and adds the class datetimepicker."""
        super(AreaAdminForm, self).__init__(*args, **kwargs)
        self.fields['short_description'].widget = forms.Textarea(attrs={'cols': '40', 'rows': '2'})
        self.fields['clubs'].queryset = self.fields['clubs'].queryset.filter(Q(status=APPROVED) | Q(status=BEING_REVIEWED_DELETE))
        self.fields['long_description'].widget = AdminPagedownWidget()


class NewUserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(NewUserForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True

    captcha = CaptchaField()

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class ClubAdminForm(forms.ModelForm):
    change_comment = forms.CharField(label="Kommentar för ändring")

    def __init__(self, *args, **kwargs):
        """This overrides the constructor, and adds the class datetimepicker."""
        super(ClubAdminForm, self).__init__(*args, **kwargs)
        self.fields['change_comment'].widget = forms.Textarea(attrs={'cols': '40', 'rows': '2'})
