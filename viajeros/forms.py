from django import forms
import re

class PasajeroForm(forms.Form):
    nombre = forms.CharField(max_length=100, required=True)
    cc = forms.IntegerField(required=True)
    destino = forms.ChoiceField(choices=[], required=True)  # Se usará un ChoiceField para la lista desplegable

    def __init__(self, *args, **kwargs):
        ciudades = kwargs.pop('ciudades', [])  # Recibimos las ciudades desde la vista
        super(PasajeroForm, self).__init__(*args, **kwargs)
        
        # Si hay ciudades, las añadimos a la lista de opciones del campo 'destino'
        if ciudades:
            self.fields['destino'].choices = [(ciudad[0], ciudad[0]) for ciudad in ciudades]
        else:
            self.fields['destino'].choices = [('', 'No hay ciudades registradas')]  # Si no hay ciudades, mostramos un mensaje

    def clean_cc(self):
        cc = self.cleaned_data.get('cc')
        cc_str = str(cc)  # Convertimos la cédula a cadena para contar los dígitos

        # Validamos que la cédula tenga entre 6 y 10 dígitos
        if len(cc_str) < 6 or len(cc_str) > 10:
            raise forms.ValidationError("La cédula debe tener entre 6 y 10 dígitos.")
        return cc


class CiudadForm(forms.Form):
    ciudad = forms.CharField(max_length=100, required=True)
    pais = forms.CharField(max_length=100, required=True)

    # Validación para el campo 'ciudad' (solo letras y espacios)
    def clean_ciudad(self):
        ciudad = self.cleaned_data.get('ciudad')

        # Validación para que solo contenga letras y espacios
        if not re.match("^[a-zA-ZáéíóúÁÉÍÓÚÑñ\s]+$", ciudad):
            raise forms.ValidationError("La ciudad debe contener solo letras y espacios.")
        return ciudad

    # Validación para el campo 'pais' (solo letras y espacios)
    def clean_pais(self):
        pais = self.cleaned_data.get('pais')

        # Validación para que solo contenga letras y espacios
        if not re.match("^[a-zA-ZáéíóúÁÉÍÓÚÑñ\s]+$", pais):
            raise forms.ValidationError("El país debe contener solo letras y espacios.")
        return pais
