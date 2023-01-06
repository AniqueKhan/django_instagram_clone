from django import forms
from .models import Story

class NewStoryForm(forms.ModelForm):
    content = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple':True}),required=True)
    caption = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}),required=True)

    class Meta:
        model = Story
        fields = ('content','caption',)