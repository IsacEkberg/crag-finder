from django import forms


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
        #self.fields['long_description'].widget = forms.Textarea(attrs={'cols': '40', 'rows': '5'})
        #self.fields['road_description'].widget = forms.Textarea(attrs={'cols': '40', 'rows': '5'})
