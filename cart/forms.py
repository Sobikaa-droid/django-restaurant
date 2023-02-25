from django import forms
from .models import Cart, Payment


class AmountForm(forms.ModelForm):
    amount = forms.IntegerField(widget=forms.NumberInput(attrs={
        'required': 'False',
    }), required=False)

    class Meta:
        model = Cart
        fields = ['amount']


class CheckoutForm(forms.ModelForm):
    email = forms.EmailField(required=False)
    payment_type = forms.ModelChoiceField(widget=forms.Select(attrs={
        'required': 'True',
    }), empty_label=None, queryset=Payment.objects.all())

    class Meta:
        model = Payment
        fields = ['email', 'payment_type']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""  # Removes : as label suffix

        self.fields['email'].label = 'Email address'
        self.fields['payment_type'].label = 'Payment type'
        self.fields['email'].help_text = 'Leave blank for default'
