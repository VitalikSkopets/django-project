from django import forms


VEHICLES_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 11)]


class CartAddVehicleForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=VEHICLES_QUANTITY_CHOICES, coerce=int)
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
