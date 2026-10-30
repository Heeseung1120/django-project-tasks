import json

from django.db import IntegrityError
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from .models import Project


def a_diccionario(proyecto):

    datos = model_to_dict(proyecto)
    datos["id"] = proyecto.pk
    return datos


def leer_json(request):

    try:
        return json.loads(request.body)
    except json.JSONDecodeError:
        return None

@method_decorator(csrf_exempt, name="dispatch")
class ProjectView(View):

    def get(self, request, pk=None):
        # Sin pk: lista todos los proyectos
        if pk is None:
            proyectos = [a_diccionario(p) for p in Project.objects.all()]
            return JsonResponse(proyectos, safe=False)

        try:
            proyecto = Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            return JsonResponse({"error": "Proyecto no encontrado"}, status=404)
        return JsonResponse(a_diccionario(proyecto))

    def post(self, request):
        datos = leer_json(request)
        if datos is None:
            return JsonResponse({"error": "JSON no valido"}, status=400)

        try:
            proyecto = Project.objects.create(**datos)
        except (TypeError, ValueError, IntegrityError) as error:
            return JsonResponse({"error": str(error)}, status=400)
        return JsonResponse(a_diccionario(proyecto), status=201)

    def put(self, request, pk):
        try:
            proyecto = Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            return JsonResponse({"error": "Proyecto no encontrado"}, status=404)

        datos = leer_json(request)
        if datos is None:
            return JsonResponse({"error": "JSON no valido"}, status=400)

        campos = [campo.name for campo in Project._meta.fields if campo.name != "id"]
        for campo, valor in datos.items():
            if campo not in campos:
                return JsonResponse({"error": f"Campo no valido: {campo}"}, status=400)
            setattr(proyecto, campo, valor)

        try:
            proyecto.save()
        except (TypeError, ValueError, IntegrityError) as error:
            return JsonResponse({"error": str(error)}, status=400)
        return JsonResponse(a_diccionario(proyecto))


    def delete(self, request, pk):
        try:
            proyecto = Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            return JsonResponse({"error": "Proyecto no encontrado"}, status=404)

        proyecto.delete()
        return JsonResponse({"mensaje": "Proyecto eliminado correctamente"})