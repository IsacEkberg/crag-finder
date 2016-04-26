from django import forms
from string import Template

from django.db.models import Q
from django.utils.safestring import mark_safe

from django_api.models import APPROVED, BEING_REVIEWED_DELETE


class RockFaceAdminForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        """This overrides the constructor, and adds the class datetimepicker."""
        super(RockFaceAdminForm, self).__init__(*args, **kwargs)
        self.fields['geo_data'].widget.attrs['class'] = 'hidden'
        self.fields['short_description'].widget = forms.Textarea(attrs={'cols': '40', 'rows': '2'})
        self.fields['long_description'].widget = forms.Textarea(attrs={'cols': '40', 'rows': '5'})


class AreaAdminForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        """This overrides the constructor, and adds the class datetimepicker."""
        super(AreaAdminForm, self).__init__(*args, **kwargs)
        self.fields['short_description'].widget = forms.Textarea(attrs={'cols': '40', 'rows': '2'})
        self.fields['long_description'].widget = forms.Textarea(attrs={'cols': '40', 'rows': '5'})
        self.fields['road_description'].widget = forms.Textarea(attrs={'cols': '40', 'rows': '5'})
        self.fields['clubs'].queryset = self.fields['clubs'].queryset.filter(Q(status=APPROVED) | Q(status=BEING_REVIEWED_DELETE))


class ClubAdminForm(forms.ModelForm):
    change_comment = forms.CharField(label="Kommentar för ändring")

    def __init__(self, *args, **kwargs):
        """This overrides the constructor, and adds the class datetimepicker."""
        super(ClubAdminForm, self).__init__(*args, **kwargs)
        self.fields['change_comment'].widget = forms.Textarea(attrs={'cols': '40', 'rows': '2'})
