import tkinter
from tkinter import filedialog
from fpdf.enums import XPos, YPos
from fpdf import FPDF


class PdfRecetaMedica:
        def __init__(self, nombreDoctor, rutDoctor, nombreClinica, direccion, fecha, rutTutor, nombrePaciente, edad, direccionPaciente, prescripcion) -> None:
                self.nombreDoctor = nombreDoctor
                self.rutDoctor = rutDoctor
                self.nombreClinica = nombreClinica
                self.direccion = direccion
                self.fecha = fecha
                self.rutTutor = rutTutor
                self.nombrePaciente = nombrePaciente
                self.edad = edad
                self.direccionPaciente = direccionPaciente
                self.prescripcion = prescripcion
                self.pdf = FPDF(orientation = 'P', unit = 'mm', format='A4') 
                self.pdf.add_page()

                # TEXTO

                #MAXIMO W=190

                self.pdf.set_font('Arial', '', 10)

                self.pdf.cell(w = 40, h = 30, txt = '', border = 1, 
                        align = 'C', fill = 0)

                self.pdf.image('PDFs/logo-2.png',
                        x= 12, y= 12,
                        w = 36, h = 28)

                self.pdf.cell(w = 70, h = 30, txt = f'{self.nombreClinica}', border = 1, 
                        align = 'C', fill = 0)

                #LOS new_x y new_y indican la posicion de la siguiente celda

                self.pdf.cell(w = 0, h = 10, txt = 'Dr/a '+str(self.nombreDoctor), border = 1, new_x=XPos.LEFT, new_y=YPos.NEXT,##w = 0 autoajusta hasta el ultimo borde y ln = 2 para que la siguiente se posiscione abajo de la celda actual
                        align = 'L', fill = 0)

                self.pdf.cell(w = 0, h = 10, txt = f'Rut {self.rutDoctor}', border = 1, new_x=XPos.LEFT, new_y=YPos.NEXT, ##w = 0 autoajusta hasta el ultimo borde y ln = 1 para que la siguiente se posiscione al siguiente lado
                        align = 'L', fill = 0)

                self.pdf.cell(w = 0, h = 10, txt = f'{self.direccion}', border = 1, new_x=XPos.LMARGIN, new_y=YPos.NEXT, ##w = 0 autoajusta hasta el ultimo borde y ln = 1 para que la siguiente se posiscione al siguiente lado
                        align = 'L', fill = 0)

                self.pdf.multi_cell(w = 95, h = 10, txt = f'Fecha:\n{self.fecha}', border = 1, new_x=XPos.RIGHT, new_y=YPos.TOP, ##w = 0 autoajusta hasta el ultimo borde y ln = 1 para que la siguiente se posiscione al siguiente lado
                        align = 'L', fill = 0)

                self.pdf.multi_cell(w = 95, h = 10, txt = f'Rut:\n{self.rutTutor}', border = 1, new_x=XPos.LMARGIN, new_y=YPos.NEXT, ##w = 0 autoajusta hasta el ultimo borde y ln = 1 para que la siguiente se posiscione al siguiente lado
                        align = 'L', fill = 0)

                self.pdf.multi_cell(w = 70, h = 10, txt = f'Nombre paciente:\n{self.nombrePaciente}', border = 1, new_x=XPos.RIGHT, new_y=YPos.TOP, ##w = 0 autoajusta hasta el ultimo borde y ln = 1 para que la siguiente se posiscione al siguiente lado
                        align = 'L', fill = 0)

                self.pdf.multi_cell(w = 50, h = 10, txt = f'Edad:\n{self.edad}', border = 1, new_x=XPos.RIGHT, new_y=YPos.TOP, ##w = 0 autoajusta hasta el ultimo borde y ln = 1 para que la siguiente se posiscione al siguiente lado
                        align = 'L', fill = 0)

                self.pdf.multi_cell(w = 70, h = 10, txt = f'Dirección:\n{self.direccionPaciente}', border = 1, new_x=XPos.LMARGIN, new_y=YPos.NEXT, ##w = 0 autoajusta hasta el ultimo borde y ln = 1 para que la siguiente se posiscione al siguiente lado
                        align = 'L', fill = 0)

                self.pdf.multi_cell(w = 0, h = 10, txt = f'Prescripcion:\n{self.prescripcion}', border = 1, new_x=XPos.LMARGIN, new_y=YPos.NEXT, ##w = 0 autoajusta hasta el ultimo borde y ln = 1 para que la siguiente se posiscione al siguiente lado
                        align = 'J', fill = 0)

                self.pdf.multi_cell(w = 95, h = 15, txt = '________________\n Firma Veterinario', border = 'LBT', new_x=XPos.RIGHT, new_y=YPos.TOP, ##w = 0 autoajusta hasta el ultimo borde y ln = 1 para que la siguiente se posiscione al siguiente lado
                        align = 'C', fill = 0)

                self.pdf.multi_cell(w = 95, h = 15, txt = '________________\n Firma Tutor', border = 'RBT', new_x=XPos.RIGHT, new_y=YPos.TOP, ##w = 0 autoajusta hasta el ultimo borde y ln = 1 para que la siguiente se posiscione al siguiente lado
                        align = 'C', fill = 0)



        def exportar(self):
                folder_path = filedialog.askdirectory()
                if(folder_path != ''):
                        folder_path = folder_path+f"/pdf_Receta_{self.nombrePaciente}.pdf"
                        self.pdf.output(str(folder_path), 'F')
                        return 0
                else:
                        return 1


class PdfFichaHospt:
        def __init__(self, nombreDoctor, rutDoctor, nombreClinica, direccion, especie, nombrePaciente, edad, peso, raza, color, motivoHospt) -> None:
                self.nombreDoctor = nombreDoctor
                self.rutDoctor = rutDoctor
                self.nombreClinica = nombreClinica
                self.direccion = direccion
                self.especie = especie
                self.nombrePaciente = nombrePaciente
                self.edad = edad
                self.peso = peso
                self.raza = raza
                self.color = color
                self.motivoHospt = motivoHospt
                
                self.pdf = FPDF(orientation = 'P', unit = 'mm', format='A4') 
                self.pdf.add_page()

                # TEXTO

                #MAXIMO W=190

                self.pdf.set_font('Arial', '', 10)

                self.pdf.cell(w = 40, h = 30, txt = '', border = 1, 
                        align = 'C', fill = 0)

                self.pdf.image('PDFs/logo-2.png',
                        x= 12, y= 12,
                        w = 36, h = 28)

                self.pdf.cell(w = 70, h = 30, txt = f'{self.nombreClinica}', border = 1, 
                        align = 'C', fill = 0)

                #LOS new_x y new_y indican la posicion de la siguiente celda

                self.pdf.cell(w = 0, h = 15, txt = 'Dr/a '+str(self.nombreDoctor), border = 1, new_x=XPos.LEFT, new_y=YPos.NEXT,##w = 0 autoajusta hasta el ultimo borde y ln = 2 para que la siguiente se posiscione abajo de la celda actual
                        align = 'L', fill = 0)

                self.pdf.cell(w = 0, h = 15, txt = f'{self.direccion}', border = 1, new_x=XPos.LMARGIN, new_y=YPos.NEXT, ##w = 0 autoajusta hasta el ultimo borde y ln = 1 para que la siguiente se posiscione al siguiente lado
                        align = 'L', fill = 0)

                self.pdf.multi_cell(w = 65, h = 10, txt = f'Nombre Paciente:\n{self.nombrePaciente}', border = 1, new_x=XPos.RIGHT, new_y=YPos.TOP, ##w = 0 autoajusta hasta el ultimo borde y ln = 1 para que la siguiente se posiscione al siguiente lado
                        align = 'L', fill = 0)

                self.pdf.multi_cell(w = 65, h = 10, txt = f'Especie:\n{self.especie}', border = 1, new_x=XPos.RIGHT, new_y=YPos.TOP, ##w = 0 autoajusta hasta el ultimo borde y ln = 1 para que la siguiente se posiscione al siguiente lado
                        align = 'L', fill = 0)

                self.pdf.multi_cell(w = 0, h = 10, txt = f'Peso:\n{self.peso}', border = 1, new_x=XPos.LMARGIN, new_y=YPos.NEXT, ##w = 0 autoajusta hasta el ultimo borde y ln = 1 para que la siguiente se posiscione al siguiente lado
                        align = 'L', fill = 0)

                self.pdf.multi_cell(w = 65, h = 10, txt = f'Edad:\n{self.edad}', border = 1, new_x=XPos.RIGHT, new_y=YPos.TOP, ##w = 0 autoajusta hasta el ultimo borde y ln = 1 para que la siguiente se posiscione al siguiente lado
                        align = 'L', fill = 0)

                self.pdf.multi_cell(w = 65, h = 10, txt = f'Raza:\n{self.raza}', border = 1, new_x=XPos.RIGHT, new_y=YPos.TOP, ##w = 0 autoajusta hasta el ultimo borde y ln = 1 para que la siguiente se posiscione al siguiente lado
                        align = 'L', fill = 0)

                self.pdf.multi_cell(w = 0, h = 10, txt = f'Color:\n{self.color}', border = 1, new_x=XPos.LMARGIN, new_y=YPos.NEXT, ##w = 0 autoajusta hasta el ultimo borde y ln = 1 para que la siguiente se posiscione al siguiente lado
                        align = 'L', fill = 0)
                
                self.pdf.multi_cell(w = 0, h = 10, txt = f'Motivo de hospitalización:\n{self.motivoHospt}', border = 1, new_x=XPos.LMARGIN, new_y=YPos.NEXT, ##w = 0 autoajusta hasta el ultimo borde y ln = 1 para que la siguiente se posiscione al siguiente lado
                        align = 'L', fill = 0)

                self.pdf.multi_cell(w = 95, h = 15, txt = '________________\n Firma Veterinario', border = 'LBT', new_x=XPos.RIGHT, new_y=YPos.TOP, ##w = 0 autoajusta hasta el ultimo borde y ln = 1 para que la siguiente se posiscione al siguiente lado
                        align = 'C', fill = 0)

                self.pdf.multi_cell(w = 95, h = 15, txt = '________________\n Firma Tutor', border = 'RBT', new_x=XPos.RIGHT, new_y=YPos.TOP, ##w = 0 autoajusta hasta el ultimo borde y ln = 1 para que la siguiente se posiscione al siguiente lado
                        align = 'C', fill = 0)



        def exportar(self):
                folder_path = filedialog.askdirectory()
                if(folder_path != ''):
                        folder_path = folder_path+f"/pdf_Hospitalizacion_{self.nombrePaciente}.pdf"
                        self.pdf.output(str(folder_path), 'F')
                        return 0
                else:
                        return 1

class PdfFichaOperacion:
        def __init__(self, nombreDoctor, rutDoctor, nombreClinica, direccion, especie, rutTutor, nombrePaciente, edad, direccionPaciente, peso, raza, color, nombreTutor, numtelefono, diagnostico, operacion) -> None:
                self.nombreDoctor = nombreDoctor
                self.rutDoctor = rutDoctor
                self.nombreClinica = nombreClinica
                self.direccion = direccion
                self.especie = especie
                self.rutTutor = rutTutor
                self.nombrePaciente = nombrePaciente
                self.edad = edad
                self.direccionPaciente = direccionPaciente
                self.peso = peso
                self.raza = raza
                self.color = color
                self.nombreTutor = nombreTutor
                self.numtelefono = numtelefono
                self.diagnostico = diagnostico
                self.operacion = operacion
                pdfReceta = FPDF()

                self.pdf = FPDF(orientation = 'P', unit = 'mm', format='A4') 
                self.pdf.add_page()

                # TEXTO

                #MAXIMO W=190

                self.pdf.set_font('Arial', '', 10)

                self.pdf.cell(w = 40, h = 30, txt = '', border = 1, 
                        align = 'C', fill = 0)

                self.pdf.image('PDFs/logo-2.png',
                        x= 12, y= 12,
                        w = 36, h = 28)

                self.pdf.cell(w = 70, h = 30, txt = f'{self.nombreClinica}', border = 1, 
                        align = 'C', fill = 0)

                #LOS new_x y new_y indican la posicion de la siguiente celda

                self.pdf.cell(w = 0, h = 15, txt = 'Dr/a '+str(self.nombreDoctor), border = 1, new_x=XPos.LEFT, new_y=YPos.NEXT,##w = 0 autoajusta hasta el ultimo borde y ln = 2 para que la siguiente se posiscione abajo de la celda actual
                        align = 'L', fill = 0)

                self.pdf.cell(w = 0, h = 15, txt = f'{self.direccion}', border = 1, new_x=XPos.LMARGIN, new_y=YPos.NEXT, ##w = 0 autoajusta hasta el ultimo borde y ln = 1 para que la siguiente se posiscione al siguiente lado
                        align = 'L', fill = 0)

                self.pdf.multi_cell(w = 65, h = 10, txt = f'Nombre Paciente:\n{self.nombrePaciente}', border = 1, new_x=XPos.RIGHT, new_y=YPos.TOP, ##w = 0 autoajusta hasta el ultimo borde y ln = 1 para que la siguiente se posiscione al siguiente lado
                        align = 'L', fill = 0)

                self.pdf.multi_cell(w = 65, h = 10, txt = f'Especie:\n{self.especie}', border = 1, new_x=XPos.RIGHT, new_y=YPos.TOP, ##w = 0 autoajusta hasta el ultimo borde y ln = 1 para que la siguiente se posiscione al siguiente lado
                        align = 'L', fill = 0)

                self.pdf.multi_cell(w = 0, h = 10, txt = f'Peso:\n{self.peso}', border = 1, new_x=XPos.LMARGIN, new_y=YPos.NEXT, ##w = 0 autoajusta hasta el ultimo borde y ln = 1 para que la siguiente se posiscione al siguiente lado
                        align = 'L', fill = 0)

                self.pdf.multi_cell(w = 65, h = 10, txt = f'Edad:\n{self.edad}', border = 1, new_x=XPos.RIGHT, new_y=YPos.TOP, ##w = 0 autoajusta hasta el ultimo borde y ln = 1 para que la siguiente se posiscione al siguiente lado
                        align = 'L', fill = 0)

                self.pdf.multi_cell(w = 65, h = 10, txt = f'Raza:\n{self.raza}', border = 1, new_x=XPos.RIGHT, new_y=YPos.TOP, ##w = 0 autoajusta hasta el ultimo borde y ln = 1 para que la siguiente se posiscione al siguiente lado
                        align = 'L', fill = 0)

                self.pdf.multi_cell(w = 0, h = 10, txt = f'Color:\n{self.color}', border = 1, new_x=XPos.LMARGIN, new_y=YPos.NEXT, ##w = 0 autoajusta hasta el ultimo borde y ln = 1 para que la siguiente se posiscione al siguiente lado
                        align = 'L', fill = 0)

                self.pdf.multi_cell(w = 45, h = 10, txt = f'Nombre tutor:\n{self.nombreTutor}', border = 1, new_x=XPos.RIGHT, new_y=YPos.TOP, ##w = 0 autoajusta hasta el ultimo borde y ln = 1 para que la siguiente se posiscione al siguiente lado
                        align = 'L', fill = 0)

                self.pdf.multi_cell(w = 45, h = 10, txt = f'Rut tutor:\n{self.rutTutor}', border = 1, new_x=XPos.RIGHT, new_y=YPos.TOP, ##w = 0 autoajusta hasta el ultimo borde y ln = 1 para que la siguiente se posiscione al siguiente lado
                        align = 'L', fill = 0)

                self.pdf.multi_cell(w = 45, h = 10, txt = f'Numero Telefono:\n{self.numtelefono}', border = 1, new_x=XPos.RIGHT, new_y=YPos.TOP, ##w = 0 autoajusta hasta el ultimo borde y ln = 1 para que la siguiente se posiscione al siguiente lado
                        align = 'L', fill = 0)

                self.pdf.multi_cell(w = 0, h = 10, txt = f'Dirección:\n{self.direccionPaciente}', border = 1, new_x=XPos.LMARGIN, new_y=YPos.NEXT, ##w = 0 autoajusta hasta el ultimo borde y ln = 1 para que la siguiente se posiscione al siguiente lado
                        align = 'L', fill = 0)

                self.pdf.multi_cell(w = 0, h = 5, txt = f'Diagnóstico:\n{self.diagnostico}', border = 1, new_x=XPos.LMARGIN, new_y=YPos.NEXT, ##w = 0 autoajusta hasta el ultimo borde y ln = 1 para que la siguiente se posiscione al siguiente lado
                        align = 'L', fill = 0)
                
                self.pdf.multi_cell(w = 0, h = 5, txt = f'Cirugía a realizar:\n{self.operacion}', border = 1, new_x=XPos.LMARGIN, new_y=YPos.NEXT, ##w = 0 autoajusta hasta el ultimo borde y ln = 1 para que la siguiente se posiscione al siguiente lado
                        align = 'L', fill = 0)

                self.pdf.multi_cell(w = 95, h = 15, txt = '________________\n Firma Veterinario', border = 'LBT', new_x=XPos.RIGHT, new_y=YPos.TOP, ##w = 0 autoajusta hasta el ultimo borde y ln = 1 para que la siguiente se posiscione al siguiente lado
                        align = 'C', fill = 0)

                self.pdf.multi_cell(w = 95, h = 15, txt = '________________\n Firma Tutor', border = 'RBT', new_x=XPos.RIGHT, new_y=YPos.TOP, ##w = 0 autoajusta hasta el ultimo borde y ln = 1 para que la siguiente se posiscione al siguiente lado
                        align = 'C', fill = 0)



        def exportar(self):
                folder_path = filedialog.askdirectory()
                if(folder_path != ''):
                        folder_path = folder_path+f"/pdf_Operacion_{self.nombrePaciente}.pdf"
                        self.pdf.output(str(folder_path), 'F')
                        return 0
                else:
                        return 1

class PdfFichaGeneral:
        def __init__(self, nombreDoctor, rutDoctor, nombreClinica, direccion, fecha, nombrePaciente, especie, peso, edad, frecResp, frecCard, temp, tratamientos, vacSum, causaVisita) -> None:
                self.nombreDoctor = nombreDoctor
                self.rutDoctor = rutDoctor
                self.nombreClinica = nombreClinica
                self.direccion = direccion
                self.fecha = fecha
                self.nombrePaciente = nombrePaciente
                self.especie = especie
                self.peso = peso
                self.edad = edad
                self.frecResp = frecResp
                self.frecCard = frecCard
                self.temp = temp
                self.tratamientos = tratamientos
                self.vacSum = vacSum
                self.causaVisita = causaVisita
                self.pdf = FPDF(orientation = 'P', unit = 'mm', format='A4') 
                self.pdf.add_page()

                # TEXTO

                #MAXIMO W=190

                self.pdf.set_font('Arial', '', 10)

                self.pdf.cell(w = 40, h = 30, txt = '', border = 1, 
                        align = 'C', fill = 0)

                self.pdf.image('PDFs/logo-2.png',
                        x= 12, y= 12,
                        w = 36, h = 28)

                self.pdf.cell(w = 70, h = 30, txt = f'{self.nombreClinica}', border = 1, 
                        align = 'C', fill = 0)

                #LOS new_x y new_y indican la posicion de la siguiente celda

                self.pdf.cell(w = 0, h = 15, txt = 'Dr/a '+str(self.nombreDoctor), border = 1, new_x=XPos.LEFT, new_y=YPos.NEXT,##w = 0 autoajusta hasta el ultimo borde y ln = 2 para que la siguiente se posiscione abajo de la celda actual
                        align = 'L', fill = 0)

                self.pdf.cell(w = 0, h = 15, txt = f'{self.direccion}', border = 1, new_x=XPos.LMARGIN, new_y=YPos.NEXT, ##w = 0 autoajusta hasta el ultimo borde y ln = 1 para que la siguiente se posiscione al siguiente lado
                        align = 'L', fill = 0)

                self.pdf.multi_cell(w = 45, h = 10, txt = f'Fecha:\n{self.fecha}', border = 1, new_x=XPos.RIGHT, new_y=YPos.TOP, ##w = 0 autoajusta hasta el ultimo borde y ln = 1 para que la siguiente se posiscione al siguiente lado
                        align = 'L', fill = 0)

                self.pdf.multi_cell(w = 45, h = 10, txt = f'Nombre paciente:\n{self.nombrePaciente}', border = 1, new_x=XPos.RIGHT, new_y=YPos.TOP, ##w = 0 autoajusta hasta el ultimo borde y ln = 1 para que la siguiente se posiscione al siguiente lado
                        align = 'L', fill = 0)

                self.pdf.multi_cell(w = 45, h = 10, txt = f'Especie:\n{self.especie}', border = 1, new_x=XPos.RIGHT, new_y=YPos.TOP, ##w = 0 autoajusta hasta el ultimo borde y ln = 1 para que la siguiente se posiscione al siguiente lado
                        align = 'L', fill = 0)

                self.pdf.multi_cell(w = 0, h = 10, txt = f'Edad:\n{self.edad}', border = 1, new_x=XPos.LMARGIN, new_y=YPos.NEXT, ##w = 0 autoajusta hasta el ultimo borde y ln = 1 para que la siguiente se posiscione al siguiente lado
                        align = 'L', fill = 0)

                self.pdf.multi_cell(w = 45, h = 10, txt = f'Frec. Respiratoria:\n{self.frecResp}', border = 1, new_x=XPos.RIGHT, new_y=YPos.TOP, ##w = 0 autoajusta hasta el ultimo borde y ln = 1 para que la siguiente se posiscione al siguiente lado
                        align = 'L', fill = 0)

                self.pdf.multi_cell(w = 45, h = 10, txt = f'Frec. Cardiaca:\n{self.frecCard}', border = 1, new_x=XPos.RIGHT, new_y=YPos.TOP, ##w = 0 autoajusta hasta el ultimo borde y ln = 1 para que la siguiente se posiscione al siguiente lado
                        align = 'L', fill = 0)

                self.pdf.multi_cell(w = 45, h = 10, txt = f'Temperatura:\n{self.temp}', border = 1, new_x=XPos.RIGHT, new_y=YPos.TOP, ##w = 0 autoajusta hasta el ultimo borde y ln = 1 para que la siguiente se posiscione al siguiente lado
                        align = 'L', fill = 0)

                self.pdf.multi_cell(w = 0, h = 10, txt = f'Peso:\n{self.peso}', border = 1, new_x=XPos.LMARGIN, new_y=YPos.NEXT, ##w = 0 autoajusta hasta el ultimo borde y ln = 1 para que la siguiente se posiscione al siguiente lado
                        align = 'L', fill = 0)

                self.pdf.multi_cell(w = 95, h = 10, txt = f'Tratamientos:\n{self.tratamientos}', border = 1, new_x=XPos.RIGHT, new_y=YPos.TOP, ##w = 0 autoajusta hasta el ultimo borde y ln = 1 para que la siguiente se posiscione al siguiente lado
                        align = 'L', fill = 0)
                
                self.pdf.multi_cell(w = 0, h = 10, txt = f'Vacunas Suministradas:\n{self.vacSum}', border = 1, new_x=XPos.LMARGIN, new_y=YPos.NEXT, ##w = 0 autoajusta hasta el ultimo borde y ln = 1 para que la siguiente se posiscione al siguiente lado
                        align = 'L', fill = 0)

                self.pdf.multi_cell(w = 0, h = 10, txt = f'Causa de la Visita:\n{self.causaVisita}', border = 1, new_x=XPos.LMARGIN, new_y=YPos.NEXT, ##w = 0 autoajusta hasta el ultimo borde y ln = 1 para que la siguiente se posiscione al siguiente lado
                        align = 'L', fill = 0)

                self.pdf.multi_cell(w = 95, h = 15, txt = '________________\n Firma Veterinario', border = 'LBT', new_x=XPos.RIGHT, new_y=YPos.TOP, ##w = 0 autoajusta hasta el ultimo borde y ln = 1 para que la siguiente se posiscione al siguiente lado
                        align = 'C', fill = 0)

                self.pdf.multi_cell(w = 95, h = 15, txt = '________________\n Firma Tutor', border = 'RBT', new_x=XPos.RIGHT, new_y=YPos.TOP, ##w = 0 autoajusta hasta el ultimo borde y ln = 1 para que la siguiente se posiscione al siguiente lado
                        align = 'C', fill = 0)


        def exportar(self):
                folder_path = filedialog.askdirectory()
                if(folder_path != ''):
                        folder_path = folder_path+f"/pdf_General_{self.nombrePaciente}.pdf"
                        self.pdf.output(str(folder_path), 'F')
                        return 0
                else:
                        return 1
