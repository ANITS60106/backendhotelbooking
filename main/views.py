from django.http import HttpResponse

def home(request):
    return HttpResponse("<h1>Добро пожаловать на сайт бронирования отелей!</h1>")