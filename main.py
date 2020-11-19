import tkinter as tk
import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Process():
    """Process class"""

    def __init__(self, processId, startTime, duration):
        self.processId = processId
        self.startTime = startTime
        self.duration = duration

    def __repr__(self):
        return f"Id: {self.processId}  Tiempo inicio: {self.startTime}  Duracion: {self.duration}"


class App:
    def __init__(self, windowTitle, windowSize):
        self.windowTitle = windowTitle
        self.windowSize = windowSize
        self.parteDer = None
        self.mainWindow = None
        self.startTimeEntry = None
        self.durationEntry = None

        self.fig = None
        self.ax = None

        self.processes = []
        self.totalProc = 0

        self.createWindow()

    def run(self):
        self.mainWindow.mainloop()

    def createWindow(self, ):
        self.mainWindow = tk.Tk()
        self.mainWindow.title(self.windowTitle)
        self.mainWindow.geometry(self.windowSize)
        self.mainWindow.configure(bg='white')

        parteIzq = tk.Frame(self.mainWindow, bg='white')
        parteIzq.place(relx=0.03, rely=0.05, relwidth=0.2, relheight=1)
        self.parteDer = tk.Frame(self.mainWindow)
        self.parteDer.place(relx=0.3, rely=0.05, relwidth=0.8, relheight=1)

        etiquetaTitulo = tk.Label(
            parteIzq,
            text="Control de Procesos",
            justify=tk.CENTER,
            bg='white')
        etiquetaTitulo.place(relheight=0.05, relwidth=1)

        etiquetaInicio = tk.Label(
            parteIzq, text="Inicio", justify=tk.CENTER, bg='white')
        etiquetaInicio.place(rely=0.05, relheight=0.05, relwidth=0.4)

        etiquetaDuracion = tk.Label(
            parteIzq, text="Duracion", justify=tk.LEFT, bg='white')
        etiquetaDuracion.place(
            rely=0.05, relx=0.5, relheight=0.05, relwidth=0.4)

        self.startTimeEntry = tk.Entry(parteIzq)
        self.startTimeEntry.place(rely=0.1, relheight=0.03, relwidth=0.35)
        self.durationEntry = tk.Entry(parteIzq)
        self.durationEntry.place(
            rely=0.1, relx=0.51, relheight=0.03, relwidth=0.35)

        botonAgregar = tk.Button(parteIzq, text="+", command=self.addProcess)
        botonAgregar.pack(side=tk.LEFT)
        botonAgregar.place(rely=0.1, relx=0.9, relheight=0.03, relwidth=0.12)

        etiquetaProcesos = tk.Label(text="Lista de procesos")
        etiquetaProcesos.place(
            rely=.25, relx=.02, relheight=0.04, relwidth=0.22)

        self.listaBox = tk.Listbox(parteIzq)
        self.listaBox.pack(side=tk.LEFT)
        self.listaBox.place(rely=.25, relx=0.01, relheight=.35, relwidth=.99)

        botonIniciar = tk.Button(
            parteIzq, text="Iniciar", command=self.beginAnimation)
        botonIniciar.pack(expand=True)
        # botonIniciar.place(rely=.8, relx=.1, relheight=.1, relwidth=.9)

    def addProcess(self):
        # Get text from input
        startTime = self.startTimeEntry.get()
        duration = self.durationEntry.get()

        # Clean the tk.Entry
        self.startTimeEntry.delete(0, "end")
        self.durationEntry.delete(0, "end")

        process = Process(self.totalProc, startTime, duration)
        self.processes.append(process)
        self.totalProc += 1

        etiquetaExito = tk.Label(text="Proceso añadido", bg='white')
        etiquetaExito.place(rely=.2, relheight=0.05, relwidth=0.25)
        etiquetaExito.after(1000, etiquetaExito.destroy)

        etiquetaExito = tk.Label(text="Proceso añadido", bg='white')
        etiquetaExito.place(rely=.2, relheight=0.05, relwidth=0.25)
        etiquetaExito.after(1000, etiquetaExito.destroy)

        self.listaBox.insert("end", process)

        # DEBUGGING
        print(process)

    def plotProcesses(self):
        self.fig = plt.Figure(figsize=(4.5, 6.4))
        self.ax = self.fig.add_subplot(1, 1, 1)
        self.ax.axes.yaxis.set_visible(False)

        # maxFinishTime = getMaxFinishTime(self.processes)
        # barCollection = []
        barWidth = 10
        yPosition = 0
        for p in self.processes:
            rect, = self.ax.barh(
                y=yPosition,
                width=p.duration,
                left=p.startTime,
                height=barWidth - 1)
            yPosition += barWidth
            # barCollection.append(rect)

    def beginAnimation(self):
        # DEBUG
        self.processes = makeRandomProcesses(4)
        self.plotProcesses()

        self.fig.subplots_adjust(
            left=0.05, right=0.4, bottom=0.3, top=1, wspace=0, hspace=0)
        linea = FigureCanvasTkAgg(self.fig, self.parteDer)
        linea.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        """ TODO: Falta hacer la parte de la animacion. """
        def animateProcess(globalTime):
            for p, b in zip(self.processes, self.barCollection):
                if globalTime >= p.startTime:
                    if globalTime >= p.startTime + p.duration:
                        currDuration = p.duration
                    else:
                        currDuration = globalTime - p.startTime
                else:
                    currDuration = 0
            b.set_height(globalTime)
        #
        # animation.FuncAnimation(fig, animateProcess, frames=50)


def makeRandomProcesses(numProcesses, maxDuration=100):
    """Create N processes, with random start and duration"""
    processes = []
    for processId in range(numProcesses):
        duration = random.randint(1, maxDuration)
        startTime = random.randint(0, maxDuration)
        processes.append(Process(processId, startTime, duration))

    return processes


def getMaxFinishTime(processes):
    maxFinishTime = 1
    for p in processes:
        pFinishTime = p.startTime + p.duration
        maxFinishTime = max(maxFinishTime, pFinishTime)
    return maxFinishTime


def main():
    app = App("Practica 2", "1200x720")
    app.beginAnimation()
    app.run()


if __name__ == '__main__':
    main()
