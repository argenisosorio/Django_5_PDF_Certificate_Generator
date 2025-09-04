from django.shortcuts import render, redirect
import os
import csv
import time
import tempfile
from django.http import HttpResponse
from django.contrib import messages
from django.conf import settings
from .forms import CertificateForm 
from subprocess import Popen

def home(request):
    if request.method == 'POST':
        form = CertificateForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                # Obtener datos del formulario
                name_event = form.cleaned_data['name_event']
                event_acronyms = form.cleaned_data['event_acronyms']
                csv_file = form.cleaned_data['csv_file']
                svg_file = form.cleaned_data['svg_file']

                # Crear directorio para el evento
                event_dir = os.path.join(settings.MEDIA_ROOT, 'certificados', event_acronyms)
                os.makedirs(event_dir, exist_ok=True)

                # Guardar el archivo SVG subido
                svg_path = os.path.join(event_dir, 'plantilla.svg')
                with open(svg_path, 'wb+') as destination:
                    for chunk in svg_file.chunks():
                        destination.write(chunk)

                contador = 0

                # Leer el archivo CSV correctamente
                decoded_file = csv_file.read().decode('utf-8').splitlines()
                csv_reader = csv.reader(decoded_file)

                # Archivo para registro final
                csv_final_path = os.path.join(event_dir, 'data_final.csv')

                with open(csv_final_path, 'w', newline='', encoding='utf-8') as myfile:
                    wr = csv.writer(myfile)
                    wr.writerow(['Nombre', 'Cédula', 'Evento', 'Rol', 'Archivo'])
                    
                    for row in csv_reader:
                        if not row or row[0].startswith('#'):
                            continue
                            
                        if len(row) < 3:
                            continue

                        nombre = row[0].strip()
                        cedula = row[1].strip()
                        tipo_rol = row[2].strip()

                        # Mapear roles
                        roles_map = {
                            '0': 'Profesor',
                            '1': 'Estudiante', 
                            '2': 'Facilitador',
                            '3': 'Asistente',
                            '4': 'Ponente',
                            '5': 'Organizador',
                            '6': 'Colaborador'
                        }

                        rol = roles_map.get(tipo_rol, 'Participante')

                        reemplazos = {
                            '{{nombre_del_participante}}': nombre,
                            '{{cedula}}': cedula,
                            '{{Rol}}': rol,
                            '{{evento}}': name_event
                        }

                        # Generar certificado
                        pdf_filename = f"{cedula}-{event_acronyms}-{rol}.pdf"
                        pdf_path = os.path.join(event_dir, pdf_filename)

                        success = generar_certificado(
                            reemplazos, 
                            svg_path,  # Pasar la ruta del SVG subido
                            pdf_path
                        )

                        if success:
                            # Registrar en CSV final
                            wr.writerow([
                                nombre, 
                                cedula, 
                                name_event, 
                                rol, 
                                pdf_filename
                            ])
                            contador += 1
                
                messages.success(
                    request, 
                    f"¡Proceso completado! Se generaron {contador} certificados."
                )
                
                # Ofrecer descarga del archivo CSV final
                response = HttpResponse(content_type='text/csv')
                response['Content-Disposition'] = f'attachment; filename="participantes_{event_acronyms}.csv"'

                with open(csv_final_path, 'r', encoding='utf-8') as f:
                    response.write(f.read())

                return response

            except Exception as e:
                messages.error(request, f"Error durante el proceso: {str(e)}")
                # Log del error para debugging
                print(f"Error: {str(e)}")
    
    else:
        form = CertificateForm()

    return render(request, 'pdf_generator/home.html', {'form': form})

def generar_certificado(reemplazos, svg_path, pdf_path):
    """
    Genera el certificado en formato PDF usando la plantilla SVG proporcionada
    """
    try:
        # Crear archivo SVG temporal
        with tempfile.NamedTemporaryFile(mode='w', suffix='.svg', delete=False, encoding='utf-8') as temp_svg:

            # Leer plantilla SVG desde el archivo subido
            with open(svg_path, 'r', encoding='utf-8') as plantilla:
                for line in plantilla:
                    # Reemplazar los placeholders
                    for src, target in reemplazos.items():
                        line = line.replace(src, target)
                    temp_svg.write(line)

            temp_svg_path = temp_svg.name

        # Generar PDF con inkscape
        comando = [
            '/usr/bin/inkscape',
            temp_svg_path,
            '--export-filename=' + pdf_path,
            '--export-type=pdf'
        ]

        proceso = Popen(comando)
        proceso.wait()

        # Limpiar archivo temporal
        if os.path.exists(temp_svg_path):
            os.unlink(temp_svg_path)

        print(f"Certificado generado: {pdf_path}")
        return True

    except Exception as e:
        print(f"Error generando certificado: {str(e)}")
        return False
