from django import forms

from .models import InventoryItem, Patient, Vaccination, Visit


class BootstrapFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.setdefault('class', 'form-check-input')
            else:
                field.widget.attrs.setdefault('class', 'form-control')


class PatientForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Patient
        fields = [
            'name',
            'species',
            'breed',
            'sex',
            'birth_date',
            'age_text',
            'features',
            'comment',
            'owner_full_name',
            'owner_phone',
            'owner_comment',
        ]
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'features': forms.Textarea(attrs={'rows': 3}),
            'comment': forms.Textarea(attrs={'rows': 3}),
            'owner_comment': forms.Textarea(attrs={'rows': 3}),
        }


class VisitForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Visit
        fields = ['date', 'short_description', 'treatment']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'treatment': forms.Textarea(attrs={'rows': 4}),
        }


class VaccinationForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Vaccination
        fields = ['vaccine_name', 'vaccination_date', 'next_vaccination_date']
        widgets = {
            'vaccination_date': forms.DateInput(attrs={'type': 'date'}),
            'next_vaccination_date': forms.DateInput(attrs={'type': 'date'}),
        }


class InventoryItemForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = InventoryItem
        fields = ['name', 'stock']


class InventoryAdjustmentForm(BootstrapFormMixin, forms.Form):
    quantity = forms.IntegerField(label='Кількість', min_value=1)
