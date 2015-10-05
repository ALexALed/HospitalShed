import datetime
from django import forms
from .models import Schedule, Doctor

ATTRS = {'class': 'form-control'}
HOUR_CHOICES = [('{0}:00'.format(hour), '{0}:00'.format(hour))
                for hour in range(0, 24)]


class ReceptionForm(forms.ModelForm):
    doctor = forms.ModelChoiceField(queryset=Doctor.objects.all(),
                                    empty_label=None,
                                    widget=forms.Select(attrs=ATTRS))
    patient = forms.CharField(widget=forms.TextInput(attrs=ATTRS))
    reception_date = forms.DateField(initial=datetime.date.today(),
                                     widget=forms.DateInput(attrs=ATTRS))
    reception_time = forms.ChoiceField(choices=HOUR_CHOICES,
                                       widget=forms.Select(attrs=ATTRS))

    def clean(self):
        cleaned_data = super(ReceptionForm, self).clean()
        self.cleaned_data['reception_time'] = datetime.datetime.strptime(
            cleaned_data['reception_time'], '%H:%M').time()

    class Meta:
        model = Schedule
        fields = ('doctor', 'patient', 'reception_date', 'reception_time')
