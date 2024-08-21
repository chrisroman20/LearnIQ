from django.views.generic import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Create your views here.
import matplotlib.pyplot as plt
import numpy as np
import io
from django.http import HttpResponse
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas



@method_decorator(login_required(login_url='/login/'), name='dispatch')
class Home(View):
    template_name = 'App/appHome.html'
    context = {}
    def get(self, request):
        self.context = {
        }
        return render(request,self.template_name, self.context)
    
    def post(self, request):
        self.context = {
        }
        return render(request,self.template_name, self.context)
    
    

class AppTest(View):
    template_name = 'App/appTest.html'
    context = {}
    def get(self, request):
        self.context = {
        }
        return render(request,self.template_name, self.context)
    
    def post(self, request):
        self.context = {
        }
        return render(request,self.template_name, self.context)
    
class Informacion(View):
    template_name = 'App/informacion.html'
    context = {}
    def get(self, request):
        self.context = {
        }
        return render(request,self.template_name, self.context)
    
    def post(self, request):
        self.context = {
        }
        return render(request,self.template_name, self.context)
    

def graficar_radar_estilos_aprendizaje(request):
    # Datos de ejemplo de los estilos de aprendizaje
    datos = {
        'Visual': 29,
        'Auditivo': 36,
        'Kinestésico': 40,
    }

    # Nombres de las categorías
    etiquetas = list(datos.keys())
    valores = list(datos.values())

    # Añadir el primer valor al final para cerrar el círculo
    valores += valores[:1]

    # Ángulos para cada categoría
    angulos = np.linspace(0, 2 * np.pi, len(etiquetas), endpoint=False).tolist()
    angulos += angulos[:1]

    # Crear la figura y el gráfico de radar
    fig, ax = plt.subplots(figsize=(5, 5), subplot_kw=dict(polar=True))

    # Ajustar los límites del eje radial
    ax.set_ylim(0, 50)  # Ajusta el rango según sea necesario

    # Dibujar el gráfico de radar
    ax.fill(angulos, valores, color='blue', alpha=0.1)
    ax.plot(angulos, valores, color='blue', linewidth=0.2)

    # Personalización de las etiquetas y el estilo
    ax.set_yticks([10, 20, 30, 40, 50])  # Configura el número de ejes radiales visibles
    ax.set_yticklabels(['10', '20', '30', '40', '50'], fontsize=8)  # Mostrar los valores en los anillos

    ax.set_xticks(angulos[:-1])
    ax.set_xticklabels(etiquetas, fontsize=11)

    # Ajustar los límites del gráfico para que no se vea circular
    ax.spines['polar'].set_visible(False)  # Oculta la línea circular externa
    ax.set_theta_offset(np.pi / 4)  # Rota el gráfico para alinearlo mejor

    buf = io.BytesIO()
    canvas = FigureCanvas(fig)
    canvas.print_png(buf)
    plt.close(fig)

    response = HttpResponse(buf.getvalue(), content_type='image/png')
    return response