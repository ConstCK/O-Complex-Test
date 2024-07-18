from django import forms


class ForecastOrderForm(forms.Form):
    city = forms.CharField(label="Город",
                           min_length=2,
                           max_length=128,
                           error_messages={'required': ''}
                           )
