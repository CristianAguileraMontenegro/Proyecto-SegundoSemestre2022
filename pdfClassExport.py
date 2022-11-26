import tkinter
from tkinter import filedialog
from fpdf.enums import XPos, YPos
from fpdf import FPDF


class PdfRecetaMedica:
        def __init__(self, nombreDoctor, rutDoctor, nombreClinica, direccion, fecha, rutTutor, nombrePaciente, edad, direccionPaciente, prescripcion) -> None:
                
                pdf = FPDF(orientation = 'P', unit = 'mm', format='A4') 
                pdf.add_page()

                # TEXTO

                #MAXIMO W=190

                pdf.set_font('Arial', '', 10)

                pdf.cell(w = 40, h = 30, txt = '', border = 1, 
                        align = 'C', fill = 0)

                pdf.image('PDFs/logo-2.png',
                        x= 12, y= 12,
                        w = 36, h = 28)

                pdf.cell(w = 70, h = 30, txt = f'{nombreClinica}', border = 1, 
                        align = 'C', fill = 0)

                #LOS new_x y new_y indican la posicion de la siguiente celda

                pdf.cell(w = 0, h = 10, txt = 'Dr/a '+str(nombreDoctor), border = 1, new_x=XPos.LEFT, new_y=YPos.NEXT,##w = 0 autoajusta hasta el ultimo borde y ln = 2 para que la siguiente se posiscione abajo de la celda actual
                        align = 'L', fill = 0)

                pdf.cell(w = 0, h = 10, txt = f'Rut {rutDoctor}', border = 1, new_x=XPos.LEFT, new_y=YPos.NEXT, ##w = 0 autoajusta hasta el ultimo borde y ln = 1 para que la siguiente se posiscione al siguiente lado
                        align = 'L', fill = 0)

                pdf.cell(w = 0, h = 10, txt = f'{direccion}', border = 1, new_x=XPos.LMARGIN, new_y=YPos.NEXT, ##w = 0 autoajusta hasta el ultimo borde y ln = 1 para que la siguiente se posiscione al siguiente lado
                        align = 'L', fill = 0)

                pdf.multi_cell(w = 95, h = 10, txt = f'Fecha:\n{fecha}', border = 1, new_x=XPos.RIGHT, new_y=YPos.TOP, ##w = 0 autoajusta hasta el ultimo borde y ln = 1 para que la siguiente se posiscione al siguiente lado
                        align = 'L', fill = 0)

                pdf.multi_cell(w = 95, h = 10, txt = f'Rut:\n{rutTutor}', border = 1, new_x=XPos.LMARGIN, new_y=YPos.NEXT, ##w = 0 autoajusta hasta el ultimo borde y ln = 1 para que la siguiente se posiscione al siguiente lado
                        align = 'L', fill = 0)

                pdf.multi_cell(w = 70, h = 10, txt = f'Nombre paciente:\n{nombrePaciente}', border = 1, new_x=XPos.RIGHT, new_y=YPos.TOP, ##w = 0 autoajusta hasta el ultimo borde y ln = 1 para que la siguiente se posiscione al siguiente lado
                        align = 'L', fill = 0)

                pdf.multi_cell(w = 50, h = 10, txt = f'Edad:\n{edad}', border = 1, new_x=XPos.RIGHT, new_y=YPos.TOP, ##w = 0 autoajusta hasta el ultimo borde y ln = 1 para que la siguiente se posiscione al siguiente lado
                        align = 'L', fill = 0)

                pdf.multi_cell(w = 70, h = 10, txt = f'Dirección:\n{direccionPaciente}', border = 1, new_x=XPos.LMARGIN, new_y=YPos.NEXT, ##w = 0 autoajusta hasta el ultimo borde y ln = 1 para que la siguiente se posiscione al siguiente lado
                        align = 'L', fill = 0)

                pdf.multi_cell(w = 0, h = 10, txt = f'Prescripcion:\n{prescripcion}', border = 1, new_x=XPos.LMARGIN, new_y=YPos.NEXT, ##w = 0 autoajusta hasta el ultimo borde y ln = 1 para que la siguiente se posiscione al siguiente lado
                        align = 'J', fill = 0)

                pdf.multi_cell(w = 95, h = 15, txt = '________________\n Firma Veterinario', border = 'LBT', new_x=XPos.RIGHT, new_y=YPos.TOP, ##w = 0 autoajusta hasta el ultimo borde y ln = 1 para que la siguiente se posiscione al siguiente lado
                        align = 'C', fill = 0)

                pdf.multi_cell(w = 95, h = 15, txt = '________________\n Firma Tutor', border = 'RBT', new_x=XPos.RIGHT, new_y=YPos.TOP, ##w = 0 autoajusta hasta el ultimo borde y ln = 1 para que la siguiente se posiscione al siguiente lado
                        align = 'C', fill = 0)


                tkinter.Tk().withdraw() # prevents an empty tkinter window from appearing

                folder_path = filedialog.askdirectory()
                print(folder_path)

                folder_path = folder_path+"/pdf_Receta.pdf"
                pdf.output(str(folder_path), 'F')


class PdfFichaHospt:
        def __init__(self, nombreDoctor, rutDoctor, nombreClinica, direccion, especie, nombrePaciente, edad, peso, raza, color, motivoHospt) -> None:
                
                pdf = FPDF(orientation = 'P', unit = 'mm', format='A4') 
                pdf.add_page()

                # TEXTO

                #MAXIMO W=190

                pdf.set_font('Arial', '', 10)

                pdf.cell(w = 40, h = 30, txt = '', border = 1, 
                        align = 'C', fill = 0)

                pdf.image('PDFs/logo-2.png',
                        x= 12, y= 12,
                        w = 36, h = 28)

                pdf.cell(w = 70, h = 30, txt = f'{nombreClinica}', border = 1, 
                        align = 'C', fill = 0)

                #LOS new_x y new_y indican la posicion de la siguiente celda

                pdf.cell(w = 0, h = 10, txt = 'Dr/a '+str(nombreDoctor), border = 1, new_x=XPos.LEFT, new_y=YPos.NEXT,##w = 0 autoajusta hasta el ultimo borde y ln = 2 para que la siguiente se posiscione abajo de la celda actual
                        align = 'L', fill = 0)

                pdf.cell(w = 0, h = 10, txt = f'Rut {rutDoctor}', border = 1, new_x=XPos.LEFT, new_y=YPos.NEXT, ##w = 0 autoajusta hasta el ultimo borde y ln = 1 para que la siguiente se posiscione al siguiente lado
                        align = 'L', fill = 0)

                pdf.cell(w = 0, h = 10, txt = f'{direccion}', border = 1, new_x=XPos.LMARGIN, new_y=YPos.NEXT, ##w = 0 autoajusta hasta el ultimo borde y ln = 1 para que la siguiente se posiscione al siguiente lado
                        align = 'L', fill = 0)

                pdf.multi_cell(w = 65, h = 10, txt = f'Nombre Paciente:\n{nombrePaciente}', border = 1, new_x=XPos.RIGHT, new_y=YPos.TOP, ##w = 0 autoajusta hasta el ultimo borde y ln = 1 para que la siguiente se posiscione al siguiente lado
                        align = 'L', fill = 0)

                pdf.multi_cell(w = 65, h = 10, txt = f'Especie:\n{especie}', border = 1, new_x=XPos.RIGHT, new_y=YPos.TOP, ##w = 0 autoajusta hasta el ultimo borde y ln = 1 para que la siguiente se posiscione al siguiente lado
                        align = 'L', fill = 0)

                pdf.multi_cell(w = 0, h = 10, txt = f'Peso:\n{peso}', border = 1, new_x=XPos.LMARGIN, new_y=YPos.NEXT, ##w = 0 autoajusta hasta el ultimo borde y ln = 1 para que la siguiente se posiscione al siguiente lado
                        align = 'L', fill = 0)

                pdf.multi_cell(w = 65, h = 10, txt = f'Edad:\n{edad}', border = 1, new_x=XPos.RIGHT, new_y=YPos.TOP, ##w = 0 autoajusta hasta el ultimo borde y ln = 1 para que la siguiente se posiscione al siguiente lado
                        align = 'L', fill = 0)

                pdf.multi_cell(w = 65, h = 10, txt = f'Raza:\n{raza}', border = 1, new_x=XPos.RIGHT, new_y=YPos.TOP, ##w = 0 autoajusta hasta el ultimo borde y ln = 1 para que la siguiente se posiscione al siguiente lado
                        align = 'L', fill = 0)

                pdf.multi_cell(w = 0, h = 10, txt = f'Color:\n{color}', border = 1, new_x=XPos.LMARGIN, new_y=YPos.NEXT, ##w = 0 autoajusta hasta el ultimo borde y ln = 1 para que la siguiente se posiscione al siguiente lado
                        align = 'L', fill = 0)
                
                pdf.multi_cell(w = 0, h = 10, txt = f'Motivo de hospitalización:\n{motivoHospt}', border = 1, new_x=XPos.LMARGIN, new_y=YPos.NEXT, ##w = 0 autoajusta hasta el ultimo borde y ln = 1 para que la siguiente se posiscione al siguiente lado
                        align = 'L', fill = 0)

                pdf.multi_cell(w = 95, h = 15, txt = '________________\n Firma Veterinario', border = 'LBT', new_x=XPos.RIGHT, new_y=YPos.TOP, ##w = 0 autoajusta hasta el ultimo borde y ln = 1 para que la siguiente se posiscione al siguiente lado
                        align = 'C', fill = 0)

                pdf.multi_cell(w = 95, h = 15, txt = '________________\n Firma Tutor', border = 'RBT', new_x=XPos.RIGHT, new_y=YPos.TOP, ##w = 0 autoajusta hasta el ultimo borde y ln = 1 para que la siguiente se posiscione al siguiente lado
                        align = 'C', fill = 0)


                tkinter.Tk().withdraw() # prevents an empty tkinter window from appearing

                folder_path = filedialog.askdirectory()
                print(folder_path)

                folder_path = folder_path+"/pdf_Hospt.pdf"
                pdf.output(str(folder_path), 'F')

class PdfFichaOperacion:
        def __init__(self, nombreDoctor, rutDoctor, nombreClinica, direccion, especie, rutTutor, nombrePaciente, edad, direccionPaciente, peso, raza, color, nombreTutor, numtelefono, diagnostico, operacion) -> None:
                
                pdfReceta = FPDF()

                pdf = FPDF(orientation = 'P', unit = 'mm', format='A4') 
                pdf.add_page()

                # TEXTO

                #MAXIMO W=190

                pdf.set_font('Arial', '', 10)

                pdf.cell(w = 40, h = 30, txt = '', border = 1, 
                        align = 'C', fill = 0)

                pdf.image('logo-2.png',
                        x= 12, y= 12,
                        w = 36, h = 28)

                pdf.cell(w = 70, h = 30, txt = f'{nombreClinica}', border = 1, 
                        align = 'C', fill = 0)

                #LOS new_x y new_y indican la posicion de la siguiente celda

                pdf.cell(w = 0, h = 10, txt = 'Dr/a '+str(nombreDoctor), border = 1, new_x=XPos.LEFT, new_y=YPos.NEXT,##w = 0 autoajusta hasta el ultimo borde y ln = 2 para que la siguiente se posiscione abajo de la celda actual
                        align = 'L', fill = 0)

                pdf.cell(w = 0, h = 10, txt = f'Rut {rutDoctor}', border = 1, new_x=XPos.LEFT, new_y=YPos.NEXT, ##w = 0 autoajusta hasta el ultimo borde y ln = 1 para que la siguiente se posiscione al siguiente lado
                        align = 'L', fill = 0)

                pdf.cell(w = 0, h = 10, txt = f'{direccion}', border = 1, new_x=XPos.LMARGIN, new_y=YPos.NEXT, ##w = 0 autoajusta hasta el ultimo borde y ln = 1 para que la siguiente se posiscione al siguiente lado
                        align = 'L', fill = 0)

                pdf.multi_cell(w = 65, h = 10, txt = f'Nombre Paciente:\n{nombrePaciente}', border = 1, new_x=XPos.RIGHT, new_y=YPos.TOP, ##w = 0 autoajusta hasta el ultimo borde y ln = 1 para que la siguiente se posiscione al siguiente lado
                        align = 'L', fill = 0)

                pdf.multi_cell(w = 65, h = 10, txt = f'Especie:\n{especie}', border = 1, new_x=XPos.RIGHT, new_y=YPos.TOP, ##w = 0 autoajusta hasta el ultimo borde y ln = 1 para que la siguiente se posiscione al siguiente lado
                        align = 'L', fill = 0)

                pdf.multi_cell(w = 0, h = 10, txt = f'Peso:\n{peso}', border = 1, new_x=XPos.LMARGIN, new_y=YPos.NEXT, ##w = 0 autoajusta hasta el ultimo borde y ln = 1 para que la siguiente se posiscione al siguiente lado
                        align = 'L', fill = 0)

                pdf.multi_cell(w = 65, h = 10, txt = f'Edad:\n{edad}', border = 1, new_x=XPos.RIGHT, new_y=YPos.TOP, ##w = 0 autoajusta hasta el ultimo borde y ln = 1 para que la siguiente se posiscione al siguiente lado
                        align = 'L', fill = 0)

                pdf.multi_cell(w = 65, h = 10, txt = f'Raza:\n{raza}', border = 1, new_x=XPos.RIGHT, new_y=YPos.TOP, ##w = 0 autoajusta hasta el ultimo borde y ln = 1 para que la siguiente se posiscione al siguiente lado
                        align = 'L', fill = 0)

                pdf.multi_cell(w = 0, h = 10, txt = f'Color:\n{color}', border = 1, new_x=XPos.LMARGIN, new_y=YPos.NEXT, ##w = 0 autoajusta hasta el ultimo borde y ln = 1 para que la siguiente se posiscione al siguiente lado
                        align = 'L', fill = 0)

                pdf.multi_cell(w = 45, h = 10, txt = f'Nombre tutor:\n{nombreTutor}', border = 1, new_x=XPos.RIGHT, new_y=YPos.TOP, ##w = 0 autoajusta hasta el ultimo borde y ln = 1 para que la siguiente se posiscione al siguiente lado
                        align = 'L', fill = 0)

                pdf.multi_cell(w = 45, h = 10, txt = f'Rut tutor:\n{rutTutor}', border = 1, new_x=XPos.RIGHT, new_y=YPos.TOP, ##w = 0 autoajusta hasta el ultimo borde y ln = 1 para que la siguiente se posiscione al siguiente lado
                        align = 'L', fill = 0)

                pdf.multi_cell(w = 45, h = 10, txt = f'Numero Telefono:\n{numtelefono}', border = 1, new_x=XPos.RIGHT, new_y=YPos.TOP, ##w = 0 autoajusta hasta el ultimo borde y ln = 1 para que la siguiente se posiscione al siguiente lado
                        align = 'L', fill = 0)

                pdf.multi_cell(w = 0, h = 10, txt = f'Dirección:\n{direccionPaciente}', border = 1, new_x=XPos.LMARGIN, new_y=YPos.NEXT, ##w = 0 autoajusta hasta el ultimo borde y ln = 1 para que la siguiente se posiscione al siguiente lado
                        align = 'L', fill = 0)

                pdf.multi_cell(w = 0, h = 5, txt = f'Diagnóstico:\n{diagnostico}', border = 1, new_x=XPos.LMARGIN, new_y=YPos.NEXT, ##w = 0 autoajusta hasta el ultimo borde y ln = 1 para que la siguiente se posiscione al siguiente lado
                        align = 'L', fill = 0)
                
                pdf.multi_cell(w = 0, h = 5, txt = f'Cirugía a realizar:\n{operacion}', border = 1, new_x=XPos.LMARGIN, new_y=YPos.NEXT, ##w = 0 autoajusta hasta el ultimo borde y ln = 1 para que la siguiente se posiscione al siguiente lado
                        align = 'L', fill = 0)

                pdf.multi_cell(w = 95, h = 15, txt = '________________\n Firma Veterinario', border = 'LBT', new_x=XPos.RIGHT, new_y=YPos.TOP, ##w = 0 autoajusta hasta el ultimo borde y ln = 1 para que la siguiente se posiscione al siguiente lado
                        align = 'C', fill = 0)

                pdf.multi_cell(w = 95, h = 15, txt = '________________\n Firma Tutor', border = 'RBT', new_x=XPos.RIGHT, new_y=YPos.TOP, ##w = 0 autoajusta hasta el ultimo borde y ln = 1 para que la siguiente se posiscione al siguiente lado
                        align = 'C', fill = 0)


                tkinter.Tk().withdraw() # prevents an empty tkinter window from appearing

                folder_path = filedialog.askdirectory()
                print(folder_path)

                folder_path = folder_path+"/pdf_Operacion.pdf"
                pdf.output(str(folder_path), 'F')

class PdfFichaGeneral:
        def __init__(self, nombreDoctor, rutDoctor, nombreClinica, direccion, fecha, nombrePaciente, especie, peso, edad, frecResp, frecCard, temp, tratamientos, vacSum, causaVisita) -> None:
                
                pdf = FPDF(orientation = 'P', unit = 'mm', format='A4') 
                pdf.add_page()

                # TEXTO

                #MAXIMO W=190

                pdf.set_font('Arial', '', 10)

                pdf.cell(w = 40, h = 30, txt = '', border = 1, 
                        align = 'C', fill = 0)

                pdf.image('PDFs/logo-2.png',
                        x= 12, y= 12,
                        w = 36, h = 28)

                pdf.cell(w = 70, h = 30, txt = f'{nombreClinica}', border = 1, 
                        align = 'C', fill = 0)

                #LOS new_x y new_y indican la posicion de la siguiente celda

                pdf.cell(w = 0, h = 10, txt = 'Dr/a '+str(nombreDoctor), border = 1, new_x=XPos.LEFT, new_y=YPos.NEXT,##w = 0 autoajusta hasta el ultimo borde y ln = 2 para que la siguiente se posiscione abajo de la celda actual
                        align = 'L', fill = 0)

                pdf.cell(w = 0, h = 10, txt = f'Rut {rutDoctor}', border = 1, new_x=XPos.LEFT, new_y=YPos.NEXT, ##w = 0 autoajusta hasta el ultimo borde y ln = 1 para que la siguiente se posiscione al siguiente lado
                        align = 'L', fill = 0)

                pdf.cell(w = 0, h = 10, txt = f'{direccion}', border = 1, new_x=XPos.LMARGIN, new_y=YPos.NEXT, ##w = 0 autoajusta hasta el ultimo borde y ln = 1 para que la siguiente se posiscione al siguiente lado
                        align = 'L', fill = 0)

                pdf.multi_cell(w = 45, h = 10, txt = f'Fecha:\n{fecha}', border = 1, new_x=XPos.RIGHT, new_y=YPos.TOP, ##w = 0 autoajusta hasta el ultimo borde y ln = 1 para que la siguiente se posiscione al siguiente lado
                        align = 'L', fill = 0)

                pdf.multi_cell(w = 45, h = 10, txt = f'Nombre paciente:\n{nombrePaciente}', border = 1, new_x=XPos.RIGHT, new_y=YPos.TOP, ##w = 0 autoajusta hasta el ultimo borde y ln = 1 para que la siguiente se posiscione al siguiente lado
                        align = 'L', fill = 0)

                pdf.multi_cell(w = 45, h = 10, txt = f'Especie:\n{especie}', border = 1, new_x=XPos.RIGHT, new_y=YPos.TOP, ##w = 0 autoajusta hasta el ultimo borde y ln = 1 para que la siguiente se posiscione al siguiente lado
                        align = 'L', fill = 0)

                pdf.multi_cell(w = 0, h = 10, txt = f'Edad:\n{edad}', border = 1, new_x=XPos.LMARGIN, new_y=YPos.NEXT, ##w = 0 autoajusta hasta el ultimo borde y ln = 1 para que la siguiente se posiscione al siguiente lado
                        align = 'L', fill = 0)

                pdf.multi_cell(w = 45, h = 10, txt = f'Frec. Respiratoria:\n{frecResp}', border = 1, new_x=XPos.RIGHT, new_y=YPos.TOP, ##w = 0 autoajusta hasta el ultimo borde y ln = 1 para que la siguiente se posiscione al siguiente lado
                        align = 'L', fill = 0)

                pdf.multi_cell(w = 45, h = 10, txt = f'Frec. Cardiaca:\n{frecCard}', border = 1, new_x=XPos.RIGHT, new_y=YPos.TOP, ##w = 0 autoajusta hasta el ultimo borde y ln = 1 para que la siguiente se posiscione al siguiente lado
                        align = 'L', fill = 0)

                pdf.multi_cell(w = 45, h = 10, txt = f'Temperatura:\n{temp}', border = 1, new_x=XPos.RIGHT, new_y=YPos.TOP, ##w = 0 autoajusta hasta el ultimo borde y ln = 1 para que la siguiente se posiscione al siguiente lado
                        align = 'L', fill = 0)

                pdf.multi_cell(w = 0, h = 10, txt = f'Peso:\n{peso}', border = 1, new_x=XPos.LMARGIN, new_y=YPos.NEXT, ##w = 0 autoajusta hasta el ultimo borde y ln = 1 para que la siguiente se posiscione al siguiente lado
                        align = 'L', fill = 0)

                pdf.multi_cell(w = 95, h = 10, txt = f'Tratamientos:\n{tratamientos}', border = 1, new_x=XPos.RIGHT, new_y=YPos.TOP, ##w = 0 autoajusta hasta el ultimo borde y ln = 1 para que la siguiente se posiscione al siguiente lado
                        align = 'L', fill = 0)
                
                pdf.multi_cell(w = 0, h = 10, txt = f'Vacunas Suministradas:\n{vacSum}', border = 1, new_x=XPos.LMARGIN, new_y=YPos.NEXT, ##w = 0 autoajusta hasta el ultimo borde y ln = 1 para que la siguiente se posiscione al siguiente lado
                        align = 'L', fill = 0)

                pdf.multi_cell(w = 0, h = 10, txt = f'Causa de la Visita:\n{causaVisita}', border = 1, new_x=XPos.LMARGIN, new_y=YPos.NEXT, ##w = 0 autoajusta hasta el ultimo borde y ln = 1 para que la siguiente se posiscione al siguiente lado
                        align = 'L', fill = 0)

                pdf.multi_cell(w = 95, h = 15, txt = '________________\n Firma Veterinario', border = 'LBT', new_x=XPos.RIGHT, new_y=YPos.TOP, ##w = 0 autoajusta hasta el ultimo borde y ln = 1 para que la siguiente se posiscione al siguiente lado
                        align = 'C', fill = 0)

                pdf.multi_cell(w = 95, h = 15, txt = '________________\n Firma Tutor', border = 'RBT', new_x=XPos.RIGHT, new_y=YPos.TOP, ##w = 0 autoajusta hasta el ultimo borde y ln = 1 para que la siguiente se posiscione al siguiente lado
                        align = 'C', fill = 0)


                tkinter.Tk().withdraw() # prevents an empty tkinter window from appearing

                folder_path = filedialog.askdirectory()
                print(folder_path)

                folder_path = folder_path+"/pdf_General.pdf"
                pdf.output(str(folder_path), 'F')

# pdf1 = PdfFichaGeneral('doctor epico', 'rutEpico', 'direccionEpica', '10-09','kira', 'perro', '10 kg', 1, '60bmp', '80bmp', '10°C', 'Tratamientos:O', 'vacunaLol', 'Por weon')

# pdf2 = PdfRecetaMedica('doctor epico', 'rutEpico', 'direccionEpica', '10-09', 'rutTutorEpico', 'kira', 1, 'direccionPacienteEpica', 'prescripcionEpica')

# pdf3 = PdfFichaHospt('doctor epico', 'rutEpico', 'direccionEpica', 'perro', 'kira', 1, '10 kg','kiltro', 'rubia', 'Por weon')

# pdf4 = PdfFichaOperacion('doctor epico', 'rutEpico', 'direccionEpica', 'perro', 'rutTutorEpico', 'kira', 1, 'DireccionPAcienteEpica', '10 kg', 'kiltro', 'rubia', 'NombreTutorEpico', 65312541, 'PerroGuaton', 'apendicitis')

