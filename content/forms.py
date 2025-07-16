from django import forms
from .models import EducationalContent


class EducationalContentForm(forms.ModelForm):
    class Meta:
        model = EducationalContent
        fields = ['title', 'content', 'category', 'difficulty_level', 'is_published', 'featured']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter a descriptive title'}),
            'content': forms.Textarea(attrs={'rows': 12, 'placeholder': 'Write your educational content here...'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'difficulty_level': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add CSS classes for styling
        for field_name, field in self.fields.items():
            if field_name not in ['is_published', 'featured']:
                field.widget.attrs['class'] = 'form-control'
        
        # Add help text
        self.fields['title'].help_text = 'Choose a clear, descriptive title (max 200 characters)'
        self.fields['content'].help_text = 'Provide comprehensive educational content'
        self.fields['category'].help_text = 'Select the most appropriate category'
        self.fields['difficulty_level'].help_text = 'Choose the appropriate difficulty level'
        self.fields['is_published'].help_text = 'Check to make this content visible to users'
        self.fields['featured'].help_text = 'Check to feature this content prominently'


class ContentFilterForm(forms.Form):
    CATEGORY_CHOICES = [('', 'All Categories')] + EducationalContent.CATEGORY_CHOICES
    DIFFICULTY_CHOICES = [('', 'All Levels')] + EducationalContent.DIFFICULTY_CHOICES
    
    category = forms.ChoiceField(
        choices=CATEGORY_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    difficulty_level = forms.ChoiceField(
        choices=DIFFICULTY_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by title, content, or author'
        })
    )
