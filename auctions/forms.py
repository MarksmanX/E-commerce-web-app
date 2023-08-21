from django import forms
from .models import Bid, Item

class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['amount']
        labels = {'amount': 'Bid Amount'}
        widgets = {'amount': forms.NumberInput(attrs={'step': '0.01'})}

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['title', 'description', 'starting_price', 'image']
        widgets = {
            'seller': forms.HiddenInput(),
        }

    image = forms.ImageField(required=False)    