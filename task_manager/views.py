from django.http import HttpResponse

def index(request):
    return HttpResponse("Привет, мир! Добро пожаловать в task_manager!")