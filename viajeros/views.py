from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.contrib import messages
from .forms import PasajeroForm
from .forms import CiudadForm
from django.shortcuts import render, redirect


def index(request):
    return render(request, 'viajeros/index.html')

# Lista de pasajeros
pasajeros = [
    # ("David Velez", 70555952, "Boston"),
    # ("Juan Porras", 8152612, "Barcelona"),
    # ("Clara López", 42722915, "Bogotá"),
    # Agrega más pasajeros aquí hasta alcanzar el mínimo solicitado
]

# Lista de ciudades y países
ciudades = [
    # ("Boston", "USA"),
    # ("Barcelona", "España"),
    # ("Bogotá", "Colombia"),
    # Agrega más ciudades aquí
]

# Función para agregar pasajero
def agregar_pasajero(request):
    if request.method == 'POST':
        form = PasajeroForm(request.POST)
        if form.is_valid():
            cc = form.cleaned_data['cc']
            # Verifica si la cédula ya está en la lista de pasajeros
            pasajeros = request.session.get('pasajeros', [])
            if any(p[1] == cc for p in pasajeros):
                messages.error(request, "Ya existe un pasajero con esta cédula.")
            else:
                # Si es válido, agrega el pasajero
                nombre = form.cleaned_data['nombre']
                destino = form.cleaned_data['destino']
                pasajeros.append((nombre, cc, destino))
                request.session['pasajeros'] = pasajeros  # Guardar en la sesión
                messages.success(request, "Pasajero agregado correctamente.")
                form = PasajeroForm()  # Limpiar el formulario
        else:
            messages.error(request, "Por favor, corrige los errores en el formulario.")
    else:
        form = PasajeroForm()

    return render(request, 'viajeros/agregar_pasajero.html', {'form': form})

# Función para agregar ciudad
def agregar_ciudad(request):
    if request.method == 'POST':
        form = CiudadForm(request.POST)
        if form.is_valid():
            ciudad = form.cleaned_data['ciudad']
            pais = form.cleaned_data['pais']
            # Verifica si la ciudad ya existe
            ciudades = request.session.get('ciudades', [])
            if any(c[0] == ciudad for c in ciudades):
                messages.error(request, "La ciudad ya está registrada.")
            else:
                ciudades.append((ciudad, pais))
                request.session['ciudades'] = ciudades  # Guardar en la sesión
                messages.success(request, "Ciudad agregada exitosamente.")
                return render(request, 'viajeros/agregar_ciudad.html', {'form': form})
        else:
            messages.error(request, "La ciudad y el país deben ser válidos.")
    else:
        form = CiudadForm()  # Al cargar el formulario vacío

    return render(request, 'viajeros/agregar_ciudad.html', {'form': form})

# Función para ver el destino de un pasajero
def ver_destino(request):
    # Obtén los pasajeros y ciudades de la sesión
    pasajeros = request.session.get('pasajeros', [])
    ciudades = request.session.get('ciudades', [])
    
    # Verificar si hay pasajeros y ciudades registradas
    if not pasajeros or not ciudades:
        messages.error(request, "Debes agregar al menos un pasajero y una ciudad.")
        return redirect('agregar_pasajero')  # Redirige a la página para agregar pasajeros
    
    ciudad = request.GET.get('ciudad')
    cc = request.GET.get('cc')

    if ciudad:
        # Contamos cuántos pasajeros viajan a esta ciudad
        count = sum(1 for p in pasajeros if p[2].lower() == ciudad.lower())
        if count > 0:
            messages.success(request, f"Hay {count} pasajero(s) viajando a {ciudad}.")
        else:
            messages.error(request, f"No hay pasajeros viajando a {ciudad}.")
        return render(request, 'viajeros/ver_destino.html', {'ciudad': ciudad})

    elif cc:
        if not cc:
            messages.error(request, "Debes ingresar el número de cédula.")
            return render(request, 'viajeros/ver_destino.html')

        try:
            cc = int(cc)  # Intentamos convertir la cédula a número
        except ValueError:
            messages.error(request, "La cédula debe ser un número válido.")
            return render(request, 'viajeros/ver_destino.html')

        # Buscar la ciudad correspondiente a la cédula
        destino = next((p[2] for p in pasajeros if p[1] == cc), None)
        if not destino:
            messages.error(request, "Pasajero no encontrado.")
            return render(request, 'viajeros/ver_destino.html')

        return render(request, 'viajeros/ver_destino.html', {'destino': destino})

    return render(request, 'viajeros/ver_destino.html')


def ver_pais(request):
    # Obtén los pasajeros y ciudades de la sesión
    pasajeros = request.session.get('pasajeros', [])
    ciudades = request.session.get('ciudades', [])
    
    # Verificar si hay pasajeros y ciudades registradas
    if not pasajeros or not ciudades:
        messages.error(request, "Debes agregar al menos un pasajero y una ciudad.")
        return redirect('agregar_pasajero')  # Redirige a la página para agregar pasajeros
    
    pais = request.GET.get('pais')
    cc = request.GET.get('cc')

    if pais:
        # Contamos cuántos pasajeros viajan a este país
        count = sum(1 for p in pasajeros if next((c[1] for c in ciudades if c[0] == p[2]), None) == pais)
        if count > 0:
            messages.success(request, f"Hay {count} pasajero(s) viajando a {pais}.")
        else:
            messages.error(request, f"No hay pasajeros viajando a {pais}.")
        return render(request, 'viajeros/ver_pais.html', {'pais': pais})

    elif cc:
        if not cc:
            messages.error(request, "Debes ingresar el número de cédula.")
            return render(request, 'viajeros/ver_pais.html')

        try:
            cc = int(cc)  # Intentamos convertir la cédula a número
        except ValueError:
            messages.error(request, "La cédula debe ser un número válido.")
            return render(request, 'viajeros/ver_pais.html')

        # Buscar la ciudad correspondiente a la cédula
        destino = next((p[2] for p in pasajeros if p[1] == cc), None)
        if not destino:
            messages.error(request, "Pasajero no encontrado.")
            return render(request, 'viajeros/ver_pais.html')

        # Buscar el país correspondiente a la ciudad
        pais = next((c[1] for c in ciudades if c[0] == destino), None)

        return render(request, 'viajeros/ver_pais.html', {'pais': pais})

    return render(request, 'viajeros/ver_pais.html')
