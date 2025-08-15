from django import forms
from .models import Chamado

class ChamadoForm(forms.ModelForm):
    class Meta:
        model = Chamado
        fields = ['assunto', 'descricao', 'setor', 'urgencia']
        widgets = {
            'descricao': forms.Textarea(attrs={
                'rows': 5,
                'class': 'form-control',
                'placeholder': 'Descreva detalhadamente seu chamado...'
            }),
            'setor': forms.Select(attrs={
                'class': 'form-select'
            }),
            'urgencia': forms.Select(attrs={
                'class': 'form-select'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['assunto'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Assunto do chamado'
        })
        
    def clean_assunto(self):
        assunto = self.cleaned_data.get('assunto')
        if len(assunto) < 10:
            raise forms.ValidationError("O assunto deve ter pelo menos 10 caracteres.")
        return assunto
        
    def clean_descricao(self):
        descricao = self.cleaned_data.get('descricao')
        if len(descricao) < 20:
            raise forms.ValidationError("A descrição deve ter pelo menos 20 caracteres.")
        return descricao
    
