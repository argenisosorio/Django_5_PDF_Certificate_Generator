from django.shortcuts import render
import os
import csv
import time
import sys
import traceback
from subprocess import Popen

def home(request):
    if request.method == 'POST':
        name_event = request.POST.get('id_name_event')
        id_event_acronyms = request.POST.get('id_event_acronyms')
        print(f'Nombre del evento: {name_event}')
        print(f'Siglas del evento: {id_event_acronyms}')

    return render(request, 'pdf_generator/home.html')

def generar(reemplazos, nombre, cedula, rol, contador, siglas_evento):
    """
    Genera el certificado en formato pdf.
    """
    tiempo = str(int(time.time()))  # Para el nombre temporal
    nombretmp = '/tmp/' + tiempo + str(contador) + '.certificado.svg'  # Nombre único temporal del svg modificado
    with open('../utils/certificado.svg', 'r') as entrada, open(nombretmp, 'w') as salida:
        for line in entrada:  # Reemplazo de variables en el archivo svg
            for src, target in reemplazos.items():
                line = line.replace(src, target)
            salida.write(line)
    certsalida = cedula + '-' + siglas_evento + "-" + rol + '.pdf'  # Nombre del certificado pdf final
    print("-" + str(contador) + " Generando certificado" " para " + nombre)
    # Generación del certificado temporal tomando en cuenta ambas láminas del svg.
    x = Popen(['/usr/bin/inkscape', nombretmp, '-D', '--export-filename=' + certsalida, '--export-type=pdf'])
    x.wait()  # Esperar a que Inkscape termine antes de continuar
    print("\n-Removiendo archivos temporales...\n")
    time.sleep(5)
    if os.path.exists(nombretmp):
        x = Popen(['rm', nombretmp])  # Eliminación de archivos temporales
    os.chdir("..")  # Retrocediento un directorio para conseguir a la carpeta utils