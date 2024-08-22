import json
from django.http import JsonResponse
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


from Users.models import UserStyle
from App.models import LearningStyles
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
        try:
            if request.user.is_authenticated:
                data = json.loads(request.body)
                visual_ia = data.get('visualIA', 0)
                auditory_ia = data.get('auditoryIA', 0)
                kinesthetic_ia = data.get('kinestheticIA', 0)

                MaxtypeLearning = max(visual_ia, auditory_ia, kinesthetic_ia)
                
                if MaxtypeLearning == visual_ia:
                    typeLearning = 'Visual'
                elif MaxtypeLearning == auditory_ia:
                    typeLearning = 'Auditivo'
                else:
                    typeLearning = 'Kinestésico'

                learning_style, created = LearningStyles.objects.get_or_create(name=typeLearning)
                values_dict = {
                    'visual': int(round(float(visual_ia))),
                    'auditivo': int(round(float(auditory_ia))),
                    'kinestesico': int(round(float(kinesthetic_ia)))
                }

                # Verifica si el usuario ya tiene un UserStyle
                user_style, created = UserStyle.objects.update_or_create(
                    user=request.user,
                    defaults={'values': values_dict, 'learningStyle': learning_style}
                )

                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'error': 'User is not authenticated'}, status=401)

        except json.JSONDecodeError:
            print('Invalid JSON')
            return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            print(e)
            return JsonResponse({'success': False, 'error': str(e)}, status=500)    



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
    visual = int(round(float(request.GET.get('visual', 0))))
    auditivo = int(round(float(request.GET.get('auditivo', 0))))
    kinestesico = int(round(float(request.GET.get('kinestesico', 0))))

    print(visual, auditivo, kinestesico)
    datos = {
        'Visual': visual,
        'Auditivo': auditivo,
        'Kinestésico': kinestesico,
    }

    etiquetas = list(datos.keys())
    valores = list(datos.values())

    # Añade el primer valor al final para cerrar el círculo
    valores += valores[:1]

    angulos = np.linspace(0, 2 * np.pi, len(etiquetas), endpoint=False).tolist()
    angulos += angulos[:1]

    # Determina el rango del eje radial basado en el valor máximo de los datos
    max_valor = max(valores)
    rango = max(30, max_valor)  

    fig, ax = plt.subplots(figsize=(5, 5), subplot_kw=dict(polar=True))
    ax.set_ylim(0, rango)  
    ax.fill(angulos, valores, color='blue', alpha=0.1)
    ax.plot(angulos, valores, color='blue', linewidth=0.2)

    # Configura los ticks del eje radial
    ticks = np.linspace(0, rango, num=5)
    ax.set_yticks(ticks)
    ax.set_yticklabels([str(int(tick)) for tick in ticks], fontsize=8)
    ax.set_xticks(angulos[:-1])
    ax.set_xticklabels(etiquetas, fontsize=11)
    ax.spines['polar'].set_visible(False)
    ax.set_theta_offset(np.pi / 4)

    buf = io.BytesIO()
    canvas = FigureCanvas(fig)
    canvas.print_png(buf)
    plt.close(fig)

    response = HttpResponse(buf.getvalue(), content_type='image/png')
    return response
