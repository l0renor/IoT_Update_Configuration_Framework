from django import forms

from rest.models import IPRule


class ConfigForm(forms.ModelForm):
    class Meta:
        model = IPRule
        fields = ('chain', 'destination_port', 'packet_type', 'action')

    def __init__(self, *args, **kwargs):
        super(ConfigForm, self).__init__(*args, **kwargs)
        self.fields['destination_port'].widget.attrs.update({'style': 'background-color: #5e42a6;'})


class DeleteConfigForm(forms.Form):
    id = forms.IntegerField(label='ID')

    def __init__(self, *args, **kwargs):
        super(DeleteConfigForm, self).__init__(*args, **kwargs)
        self.fields['id'].widget.attrs.update({'style': 'background-color: #493382;'})
