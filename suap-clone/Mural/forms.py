# Mural/forms.py
from django import forms
from .models import Card

class CardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ['titulo', 'descricao']
        widgets = {
            'descricao': forms.Textarea(attrs={
                'rows': 4,
                'class': 'form-control',
                'placeholder': 'Digite a descrição do card...'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['titulo'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Título do card'
        })
        
    def clean_titulo(self):
        titulo = self.cleaned_data.get('titulo')
        if len(titulo) < 5:
            raise forms.ValidationError("O título deve ter pelo menos 5 caracteres.")
        return titulo