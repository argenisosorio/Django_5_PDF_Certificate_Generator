# forms.py
from django import forms
from django.core.validators import FileExtensionValidator

class CertificateForm(forms.Form):
    name_event = forms.CharField(
        max_length=200,
        label="Nombre del Evento",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    event_acronyms = forms.CharField(
        max_length=50,
        label="Siglas del Evento",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    csv_file = forms.FileField(
        label="Archivo CSV",
        validators=[FileExtensionValidator(allowed_extensions=['csv'])],
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.csv'
        })
    )

    svg_file = forms.FileField(
        label="Archivo SVG",
        validators=[FileExtensionValidator(allowed_extensions=['svg'])],
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.svg'
        })
    )
