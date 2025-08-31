from django.shortcuts import render

def home(request):
    context = {
        'message': '¡Hola, Django 5!',
    }
    return render(request, 'pdf_generator/home.html', context)