from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.contrib import messages
from .forms import PasajeroForm
from .forms import CiudadForm
from django.shortcuts import render, redirect


def index(request):
    # Obtén los pasajeros y ciudades de la sesión
    pasajeros = request.session.get('pasajeros', [])
    ciudades = request.session.get('ciudades', [])
    
    # Determina si el botón debe estar desactivado
    botones_desactivados = not (pasajeros and ciudades)

    return render(request, 'index.html', {'botones_desactivados': botones_desactivados})

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
    pasajeros = request.session.get('pasajeros', [])
    ciudades = request.session.get('ciudades', [])
    botones_desactivados = not (pasajeros and ciudades)
    hay_ciudades = len(ciudades) > 0  # Nueva variable para indicar si hay ciudades
    
    if request.method == 'POST':
        form = PasajeroForm(request.POST, ciudades=ciudades)
        if form.is_valid():
            cc = form.cleaned_data['cc']
            if any(p[1] == cc for p in pasajeros):
                messages.error(request, "Ya existe un pasajero con esta cédula.")
            else:
                nombre = form.cleaned_data['nombre']
                destino = form.cleaned_data['destino']
                pasajeros.append((nombre, cc, destino))
                request.session['pasajeros'] = pasajeros
                messages.success(request, "Pasajero agregado correctamente.")
                form = PasajeroForm()
            botones_desactivados = not (pasajeros and ciudades)
        else:
            messages.error(request, "Por favor, corrige los errores en el formulario.")
    else:
        form = PasajeroForm(ciudades=ciudades)
    
    return render(request, 'agregar_pasajero.html', {
        'form': form,
        'botones_desactivados': botones_desactivados,
        'hay_ciudades': hay_ciudades  # Pasar variable al template
    })


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
                
                # Actualiza el estado de los botones después de agregar la ciudad
                pasajeros = request.session.get('pasajeros', [])
                botones_desactivados = not (pasajeros and ciudades)
                return render(request, 'agregar_ciudad.html', {'form': form, 'botones_desactivados': botones_desactivados})

        else:
            messages.error(request, "La ciudad y el país deben ser válidos.")
    else:
        form = CiudadForm()  # Al cargar el formulario vacío

    # Obtén los pasajeros y ciudades de la sesión
    pasajeros = request.session.get('pasajeros', [])
    ciudades = request.session.get('ciudades', [])

    # Los botones sólo se habilitan cuando ambos, pasajeros y ciudades, están presentes
    botones_desactivados = not (pasajeros and ciudades)

    return render(request, 'agregar_ciudad.html', {'form': form, 'botones_desactivados': botones_desactivados})


# Función para ver el destino de un pasajero
def ver_destino(request):
    # Obtén los pasajeros y ciudades de la sesión
    pasajeros = request.session.get('pasajeros', [])
    ciudades = request.session.get('ciudades', [])
    
    # Define una variable para el estado del botón
    botones_desactivados  = not (pasajeros and ciudades)

    ciudad = request.GET.get('ciudad')
    cc = request.GET.get('cc')

    if ciudad:
        count = sum(1 for p in pasajeros if p[2].lower() == ciudad.lower())
        messages.success(request, f"Hay {count} pasajero(s) viajando a {ciudad}.") if count > 0 else messages.error(request, f"No hay pasajeros viajando a {ciudad}.")
        return render(request, 'ver_destino.html', {'ciudad': ciudad, 'botones_desactivados': botones_desactivados})

    elif cc:
        try:
            cc = int(cc)
            destino = next((p[2] for p in pasajeros if p[1] == cc), None)
            if not destino:
                messages.error(request, "Pasajero no encontrado.")
            return render(request, 'ver_destino.html', {'destino': destino, 'botones_desactivados': botones_desactivados })
        except ValueError:
            messages.error(request, "La cédula debe ser un número válido.")

    return render(request, 'ver_destino.html', {'botones_desactivados': botones_desactivados})

   

def ver_pais(request):
    # Obtén los pasajeros y ciudades de la sesión
    pasajeros = request.session.get('pasajeros', [])
    ciudades = request.session.get('ciudades', [])
    
    # Define el estado del botón según si hay pasajeros y ciudades
    botones_desactivados = not (pasajeros and ciudades)

    pais = request.GET.get('pais')
    cc = request.GET.get('cc')

    if pais and not botones_desactivados:
        # Contamos cuántos pasajeros viajan a este país
        count = sum(1 for p in pasajeros if next((c[1] for c in ciudades if c[0] == p[2]), None) == pais)
        if count > 0:
            messages.success(request, f"Hay {count} pasajero(s) viajando a {pais}.")
        else:
            messages.error(request, f"No hay pasajeros viajando a {pais}.")
        return render(request, 'ver_pais.html', {'pais': pais, 'botones_desactivados': botones_desactivados})

    elif cc and not botones_desactivados:
        try:
            cc = int(cc)  # Intentamos convertir la cédula a número
            # Buscar la ciudad correspondiente a la cédula
            destino = next((p[2] for p in pasajeros if p[1] == cc), None)
            if not destino:
                messages.error(request, "Pasajero no encontrado.")
                return render(request, 'ver_pais.html', {'botones_desactivados': botones_desactivados})

            # Buscar el país correspondiente a la ciudad
            pais = next((c[1] for c in ciudades if c[0] == destino), None)
            return render(request, 'ver_pais.html', {'pais': pais, 'botones_desactivados': botones_desactivados})
        
        except ValueError:
            messages.error(request, "La cédula debe ser un número válido.")
    
    return render(request, 'ver_pais.html', {'botones_desactivados': botones_desactivados})
