from django import forms
from .models import Catch


class CatchForm(forms.ModelForm):
    class Meta:
        model = Catch
        fields = ['fish_type', 'weight', 'location', 'catch_date', 'status', 'price', 'notes']
        widgets = {
            'catch_date': forms.DateInput(attrs={'type': 'date'}),
            'weight': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
            'price': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
            'notes': forms.Textarea(attrs={'rows': 4}),
            'fish_type': forms.TextInput(attrs={'placeholder': 'e.g., Tilapia, Salmon, Tuna'}),
            'location': forms.TextInput(attrs={'placeholder': 'e.g., Lake Victoria, Off Coast of Mombasa'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add CSS classes for styling
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        
        # Make price field optional
        self.fields['price'].required = False
        self.fields['notes'].required = False


class CatchFilterForm(forms.Form):
    STATUS_CHOICES = [('', 'All Statuses')] + Catch.STATUS_CHOICES
    
    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    fish_type = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by fish type'
        })
    )
    
    location = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by location'
        })
    )
