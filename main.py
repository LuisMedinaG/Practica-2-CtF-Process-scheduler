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
        return f"ID: {self.processId}  STRT: {self.startTime}  DUR: {self.duration}"

class App:
    def __init__(self, windowTitle, windowSize):
        self.windowTitle = windowTitle
        self.windowSize = windowSize

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
        parteDer = tk.Frame(self.mainWindow)
        parteDer.place(relx=0.3, rely=0.05, relwidth=0.8, relheight=1)

        etiquetaTitulo = tk.Label(
            parteIzq, text="Control de Procesos", justify=tk.CENTER, bg='white')
        etiquetaTitulo.place(relheight=0.05, relwidth=1)

        etiquetaInicio = tk.Label(
            parteIzq, text="Inicio", justify=tk.CENTER, bg='white')
        etiquetaInicio.place(rely=0.05, relheight=0.05, relwidth=0.4)

        etiquetaDuracion = tk.Label(
            parteIzq, text="Duracion", justify=tk.LEFT, bg='white')
        etiquetaDuracion.place(rely=0.05, relx=0.5, relheight=0.03, relwidth=0.4)

        self.startTimeEntry = tk.Entry(parteIzq)
        self.startTimeEntry.place(rely=0.1, relheight=0.03, relwidth=0.35)
        self.durationEntry = tk.Entry(parteIzq)
        self.durationEntry.place(rely=0.1, relx=0.51, relheight=0.03, relwidth=0.35)

        botonAgregar = tk.Button(parteIzq, text="+", command=self.addProcess)
        botonAgregar.pack(side=tk.LEFT)
        botonAgregar.place(rely=0.1, relx=0.9, relheight=0.03, relwidth=0.12)

        botonIniciar = tk.Button(parteIzq, text="Iniciar", command=self.beginAnimation)
        botonIniciar.pack(side=tk.LEFT)

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
        print("DEBUG: START ANIMATION")

        """ TODO: Falta hacer la parte de la animacion. """
        # def animateProcess(globalTime):
        #     for p, b in zip(processes, barCollection):
        #         if globalTime >= p.startTime:
        #             if globalTime >= p.startTime + p.duration:
        #                 currDuration = p.duration
        #             else:
        #                 currDuration = globalTime - p.startTime
        #         else:
        #             currDuration = 0
        #     b.set_height(globalTime)
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
    app.run()

if __name__ == '__main__':
    main()
