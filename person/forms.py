from django import forms
from .models import Person

class PersonForm(forms.ModelForm):
    """
    A ModelForm for creating and updating Person instances.
    
    This form handles the validation and presentation of Person data,
    providing a secure interface for person-related operations in views.
    Automatically generated from the Person model with configurable fields.
    """

    class Meta:
        """
        Metadata class defining the form's relationship to the model.
        
        Attributes:
            model (Model): The Django model class this form is based on
            fields (list): The model fields to include in the form
            labels (dict): Custom display labels for form fields
            help_texts (dict): Descriptive help text for each field
            error_messages (dict): Custom error messages
            widgets (dict): Custom widgets for field rendering
        """
        model = Person

        fields = [
            'name',
            'email',
            'age'
        ]