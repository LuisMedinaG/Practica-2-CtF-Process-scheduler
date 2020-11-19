import tkinter as tk
import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Process():
    def __init__(self, processId, startTime, duration):
        self.processId = processId
        self.startTime = startTime
        self.duration = duration

    def __repr__(self):
        return f" {self.processId}  |  {self.startTime}  |  {self.duration}"


class App:
    def __init__(self, windowTitle, windowSize):
        self.windowTitle = windowTitle
        self.windowSize = windowSize
        self.leftFrame  = None
        self.rightFrame = None
        self.mainWindow = None
        
        self.startTimeEntry = None
        self.durationEntry = None

        self.fig = None
        self.ax = None

        self.barCollection = []
        self.processes = []
        self.totalProc = 0
        self.globalTime = 0

        self.listaBoxL = None
        self.listaOrd = None

        self.createWindow()

    def run(self):
        self.mainWindow.mainloop()

    def createWindow(self, ):
        self.mainWindow = tk.Tk()
        self.mainWindow.title(self.windowTitle)
        self.mainWindow.geometry(self.windowSize)

        self.mainWindow.grid_columnconfigure(0, weight=1)
        self.mainWindow.grid_columnconfigure(1, weight=3)
        self.mainWindow.grid_rowconfigure(0, weight=1)
        
        self.leftFrame = tk.Frame(self.mainWindow)
        self.rightFrame = tk.Frame(self.mainWindow, bg='grey')
        self.leftFrame.grid(row=0, column=0, ipadx=2, padx=5, pady=5, sticky="nsew")
        self.rightFrame.grid(row=0, column=1, ipadx=5, padx=5, pady=5, sticky="nsew") 

        self.leftFrame.columnconfigure(0, weight=1)
        self.leftFrame.columnconfigure(1, weight=1)
        self.leftFrame.rowconfigure(6, weight=1)

        etiquetaTitulo = tk.Label(self.leftFrame, text="Control de Procesos")
        etiquetaTitulo.grid(row=0, column=0, columnspan=2, pady=5, sticky="ew")

        etiquetaInicio = tk.Label(self.leftFrame, text="Inicio")
        etiquetaInicio.grid(row=1, column=0, sticky="ew")

        etiquetaDuracion = tk.Label(self.leftFrame, text="Duracion")
        etiquetaDuracion.grid(row=1, column=1, sticky="ew")

        self.startTimeEntry = tk.Entry(self.leftFrame)
        self.startTimeEntry.grid(row=2, column=0, padx=10, pady=10,sticky="ew")
        self.durationEntry = tk.Entry(self.leftFrame)
        self.durationEntry.grid(row=2, column=1, padx=10, pady=10,sticky="ew")

        botonAgregar = tk.Button(self.leftFrame, text="Agregar proceso", command=self.addProcess)
        botonAgregar.grid(row=3, column=0, columnspan=2, ipady=5, padx=10, pady=(5, 20),sticky="ew")

        etiquetaProcesos = tk.Label(self.leftFrame, text="Lista de procesos")
        etiquetaProcesos.grid(row=4, column=0, columnspan=2, pady=(20, 5), sticky="ew")

        etiquetaProcesos = tk.Label(self.leftFrame, text=" ID  |  TIEMPO LLEGADA  |  DURACION ")
        etiquetaProcesos.grid(row=5, column=0, sticky="ew")
        etiquetaProcesos = tk.Label(self.leftFrame, text=" ID  |  EJECUCION")
        etiquetaProcesos.grid(row=5, column=1, sticky="ew")

        self.listaBoxL = tk.Listbox(self.leftFrame)
        self.listaBoxL.grid(row=6, column=0, pady=5, padx=5, sticky="nsew")
        self.listaBoxR = tk.Listbox(self.leftFrame)
        self.listaBoxR.grid(row=6, column=1, pady=5, padx=5, sticky="nsew")

        botonIniciar = tk.Button(self.leftFrame, text="Comenzar", command=self.beginAnimation)
        botonIniciar.grid(row=7, column=0, columnspan=2, pady=5, padx=5, ipady=15, ipadx=10, sticky="ew")

    def addProcess(self):
        # Get text from input
        try:
            startTime = int(self.startTimeEntry.get())
            duration = int(self.durationEntry.get())
        except ValueError:
            entryErrorLbl = tk.Label(self.leftFrame, text="ERROR: Valores invalidos", justify=tk.CENTER, bg='red')
            entryErrorLbl.grid(row=3, column=0, columnspan=2)
            entryErrorLbl.after(1500, entryErrorLbl.destroy)
            return

        self.startTimeEntry.delete(0, "end")
        self.durationEntry.delete(0, "end")

        process = Process(self.totalProc, startTime, duration)

        self.listaBoxL.insert("end", process)
        self.processes.append(process)
        self.totalProc += 1

    def createProcessesTable(self):
        pass

    def createProcessesBarhs(self):
        self.fig = plt.Figure(figsize=(5,5))
        self.ax = self.fig.add_subplot(1,1,1)
        self.ax.axes.yaxis.set_visible(False)

        barWidth = 10
        yPosition = 0
        for p in self.processes:
            rect, = self.ax.barh(
                y=yPosition,
                width=p.duration,
                left=p.startTime,
                height=barWidth - 1)
            yPosition += barWidth
            self.barCollection.append(rect)

        
        self.fig.tight_layout()
        mpl_canvas = FigureCanvasTkAgg(self.fig, self.rightFrame)
        mpl_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def animateProcesses(self, animationSpeed=0.1):
        maxFinishTime = getMaxFinishTime(self.processes)
        for globalTime in range(maxFinishTime):
            for pro, bar in zip(self.processes, self.barCollection):
                if globalTime >= pro.startTime:
                    if globalTime >= pro.startTime + pro.duration:
                        currDuration = pro.duration
                    else:
                        currDuration = globalTime - pro.startTime
                else:
                    currDuration = 0
                bar.set_width(currDuration)

            self.fig.canvas.draw()
            plt.pause(animationSpeed)

    def beginAnimation(self):
        # --- FOR TESTING ---
        self.processes = makeRandomProcesses(5, 10)

        if not self.processes:
            return

        self.createProcessesTable()
        self.createProcessesBarhs()
        self.animateProcesses()


# --- FOR TESTING ---
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
    app = App("Practica 2", "800x600")
    app.run()


if __name__ == '__main__':
    main()
