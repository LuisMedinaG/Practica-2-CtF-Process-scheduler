import tkinter as tk
import matplotlib as plt
import matplotlib.animation as animacion
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

TAM_VENTANA = "1200x720"
NOMBRE_VENTANA = "Simulador v1.0"
COLOR_VENTANA = "white"

cajasTextoInicio = []
cajasTextoDuracion = []
procesos = []
contadorGlobal = -1
ventanaSimulador = tk.Tk()
tiempoMaximo = 0


class Proceso:
    def __init__(self, id, inicio, duracion):
        self.id = id
        self.inicio = inicio
        self.duracion = duracion

    def dameID(self):
        return self.id

    def dameTiempoInicio(self):
        return self.inicio

    def dameTiempoDuracion(self):
        return self.duracion


def agregarNuevoProceso():
    return 0


def iniciarSimulacion():
    return 0


def animarProcesos(self, i, ejes):
    global  contadorGlobal
    contadorGlobal += 1
    if contadorGlobal <= 10:
        ejes.barh(y=2, width=contadorGlobal, left=0, height=1)
    ejes.set_xticks([0, 10])
    return 0


# Configuracion de la ventana y elementos graficos

ventanaSimulador.geometry(TAM_VENTANA)
ventanaSimulador.title(NOMBRE_VENTANA)
ventanaSimulador.configure(bg=COLOR_VENTANA)

parteIzq = tk.Frame(ventanaSimulador, bg=COLOR_VENTANA)
parteIzq.place(relx=0.03, rely=0.05, relwidth=0.25, relheight=1)
parteDer = tk.Frame(ventanaSimulador)
parteDer.place(relx=0.3, rely=0.05, relwidth=0.75, relheight=1)

etiquetaTitulo = tk.Label(parteIzq, text="Control de Procesos", justify=tk.CENTER,
                          bg=COLOR_VENTANA)
etiquetaTitulo.place(relheight=0.05, relwidth=1)

etiquetaInicio = tk.Label(parteIzq, text="Inicio", justify=tk.CENTER, bg=COLOR_VENTANA)
etiquetaInicio.place(rely=0.05, relheight=0.05, relwidth=0.5)

etiquetaDuracion = tk.Label(parteIzq, text="Duracion", justify=tk.LEFT, bg=COLOR_VENTANA)
etiquetaDuracion.place(rely=0.05, relx=0.5, relheight=0.03, relwidth=0.5)

cajaTextoInicio = tk.Entry(parteIzq)
cajaTextoInicio.place(rely=0.1, relheight=0.03, relwidth=0.45)
cajaTextoDuracion = tk.Entry(parteIzq)
cajaTextoDuracion.place(rely=0.1, relx=0.51, relheight=0.03, relwidth=0.45)

botonAgregar = tk.Button(parteIzq, text="Agregar nuevo", command=agregarNuevoProceso())
botonAgregar.place(rely=0.9, relx=0.25, relheight=0.03, relwidth=0.5)

# Configuracion de la Grafica

figura = plt.figure.Figure(figsize=(4.5, 6.4))
ejes = figura.add_subplot(1, 1, 1)

figura.subplots_adjust(left=0.01, right=0.92, bottom=0.2, top=1, wspace=0, hspace=0)

ejes.grid(False)
ejes.set_xticks([0, 10])
ejes.get_yaxis().set_visible(False)

ejes.barh(y=0, width=2, left=2, height=1)
ejes.barh(y=1, width=2, left=1, height=1)

linea = FigureCanvasTkAgg(figura, parteDer)
linea.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

animacionGrafica = animacion.FuncAnimation(figura, animarProcesos, fargs=(0, ejes),
                                           interval=500, repeat=False)

ventanaSimulador.mainloop()
