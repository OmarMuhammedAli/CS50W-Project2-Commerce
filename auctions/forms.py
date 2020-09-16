from django import forms


class CreateNewListting(forms.Form):
    title = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter title',
            'class':'col-sm-11 form-control'
        })
    )
    starting_bid = forms.DecimalField(
        label='Starting Bid',
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter starting bid amount',
            'class':'col-sm-11 form-control'
        })
    )
    image_url = forms.URLField(
        label='Image URL (Optional)',
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Image URL',
            'class':'col-sm-11 form-control'
        })
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'Enter item description',
            'style': 'height: 10em',
            'class':'col-sm-11 form-control'
        })
    )