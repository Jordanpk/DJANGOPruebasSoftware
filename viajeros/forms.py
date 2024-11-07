from django import forms
import re


class PasajeroForm(forms.Form):
    nombre = forms.CharField(max_length=100, required=True)
    cc = forms.IntegerField(required=True)
    destino = forms.CharField(max_length=100, required=True)

    def clean_cc(self):
        cc = self.cleaned_data.get('cc')
        cc_str = str(cc)  # Convertimos la cédula a cadena para contar los dígitos

        # Validamos que la cédula tenga entre 6 y 10 dígitos
        if len(cc_str) < 6 or len(cc_str) > 10:
            raise forms.ValidationError("La cédula debe tener entre 6 y 10 dígitos.")
        return cc

class CiudadForm(forms.Form):
    # Formulario para ciudades
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