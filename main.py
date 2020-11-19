import tkinter as tk
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Process():
    def __init__(self, processId, startTime, duration):
        self.processId = processId
        self.startTime = startTime
        self.duration = duration
        self.rectangle = None

    def __repr__(self):
        return f" Id: {self.processId}  |  Tiempo inicio: {self.startTime}  |  Duracion: {self.duration} "


class App:
    def __init__(self, windowTitle, windowSize):
        self.windowTitle = windowTitle
        self.windowSize = windowSize
        self.leftFrame = None
        self.rightFrame = None
        self.mainWindow = None

        self.processes = []
        self.totalProc = 0
        self.globalTime = 0

        self.fig = None

        self.createWindow()

    def createWindow(self, ):
        self.mainWindow = tk.Tk()
        self.mainWindow.title(self.windowTitle)
        self.mainWindow.geometry(self.windowSize)

        self.mainWindow.grid_columnconfigure(0, weight=1)
        self.mainWindow.grid_columnconfigure(1, weight=3)
        self.mainWindow.grid_rowconfigure(0, weight=1)

        self.leftFrame = tk.Frame(self.mainWindow)
        self.rightFrame = tk.Frame(self.mainWindow, bg='grey')
        self.leftFrame.grid(
            row=0, column=0, ipadx=2, padx=5, pady=5, sticky="nsew")
        self.rightFrame.grid(
            row=0, column=1, ipadx=5, padx=5, pady=5, sticky="nsew")

        self.leftFrame.columnconfigure(0, weight=1)
        self.leftFrame.columnconfigure(1, weight=1)
        self.leftFrame.rowconfigure(6, weight=1)

        self.rightFrame.columnconfigure(0, weight=1)
        self.rightFrame.rowconfigure(0, weight=1)

        etiquetaTitulo = tk.Label(self.leftFrame, text="Control de Procesos")
        etiquetaTitulo.grid(row=0, column=0, columnspan=2, pady=5, sticky="ew")

        etiquetaInicio = tk.Label(self.leftFrame, text="Inicio")
        etiquetaInicio.grid(row=1, column=0, sticky="ew")

        etiquetaDuracion = tk.Label(self.leftFrame, text="Duracion")
        etiquetaDuracion.grid(row=1, column=1, sticky="ew")

        self.startTimeEntry = tk.Entry(self.leftFrame)
        self.startTimeEntry.grid(
            row=2, column=0, padx=10, pady=10, sticky="ew")
        self.durationEntry = tk.Entry(self.leftFrame)
        self.durationEntry.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

        self.botonAgregar = tk.Button(
            self.leftFrame, text="Agregar proceso", command=self.addProcess)
        self.botonAgregar.grid(
            row=3,
            column=0,
            columnspan=2,
            ipady=5,
            padx=10,
            pady=(5, 20),
            sticky="ew")

        etiquetaProcesos = tk.Label(self.leftFrame, text="Lista de procesos")
        etiquetaProcesos.grid(
            row=4, column=0, columnspan=2, pady=(20, 5), sticky="ew")

        etiquetaProcesos = tk.Label(
            self.leftFrame, text=" ID  |  TIEMPO LLEGADA  |  DURACION ")
        etiquetaProcesos.grid(row=5, column=0, sticky="ew")
        etiquetaProcesos = tk.Label(self.leftFrame, text=" ID  |  EJECUCION")
        etiquetaProcesos.grid(row=5, column=1, sticky="ew")

        self.listaBoxL = tk.Listbox(self.leftFrame)
        self.listaBoxL.grid(row=6, column=0, pady=5, padx=5, sticky="nsew")
        self.listaBoxR = tk.Listbox(self.leftFrame)
        self.listaBoxR.grid(row=6, column=1, pady=5, padx=5, sticky="nsew")

        globalTimeLbl = tk.Label(self.leftFrame, text="Tiempo global: ")
        globalTimeLbl.grid(row=7, column=0, ipady=20, sticky="ew")
        self.globalTimeCnt = tk.Label(self.leftFrame, text="0")
        self.globalTimeCnt.grid(row=7, column=1, ipady=20, sticky="ew")

        self.botonIniciar = tk.Button(
            self.leftFrame, text="Comenzar", command=self.startSimulation)
        self.botonIniciar.grid(
            row=8,
            column=0,
            columnspan=2,
            pady=5,
            padx=5,
            ipady=15,
            ipadx=10,
            sticky="ew")

    def run(self):
        self.mainWindow.mainloop()

    def addProcess(self):
        # Get text from input
        try:
            startTime = int(self.startTimeEntry.get())
            duration = int(self.durationEntry.get())
        except ValueError:
            entryErrorLbl = tk.Label(
                self.leftFrame,
                text="ERROR: Valores invalidos",
                justify=tk.CENTER,
                bg='red')
            entryErrorLbl.grid(row=3, column=0, columnspan=2)
            entryErrorLbl.after(1500, entryErrorLbl.destroy)
            return

        self.startTimeEntry.delete(0, "end")
        self.durationEntry.delete(0, "end")

        process = Process(self.totalProc, startTime, duration)

        self.listaBoxL.insert("end", process)
        self.processes.append(process)
        self.totalProc += 1

    def getMaxFinishTime(self):
        maxFinishTime = 1
        for p in self.processes:
            pFinishTime = p.startTime + p.duration
            maxFinishTime = max(maxFinishTime, pFinishTime)
        return maxFinishTime

    def createProcessesBarhs(self):
        try: 
            self.canvas.get_tk_widget().destroy()
        except:
            pass

        plt.rcParams.update({'figure.autolayout': True})

        self.fig = plt.Figure(figsize=(1, 1))
        self.ax = self.fig.add_subplot(1, 1, 1)
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
            p.rectangle = rect

        mpl_canvas = FigureCanvasTkAgg(self.fig, self.rightFrame)
        mpl_canvas.get_tk_widget().grid(row=0, column=0, sticky="snew")

    def startAnimation(self, animationSpeed=0.1):
        self.listaBoxR.delete(0, 'end')
        maxFinishTime = self.getMaxFinishTime()
        self.processes.sort(key=lambda proc: proc.startTime)

        for globalTime in range(maxFinishTime + 1):
            self.globalTimeCnt.configure(text=str(globalTime))
            self.listaBoxR.delete(0, 'end')

            for p in self.processes:
                if globalTime >= p.startTime:
                    if globalTime >= p.startTime + p.duration:
                        currDuration = p.duration
                    else:
                        currDuration = globalTime - p.startTime
                else:
                    currDuration = 0

                p.rectangle.set_width(currDuration)
                self.listaBoxR.insert(
                    'end', f' Id: {p.processId}  |  Ejecucion: {currDuration}')

            self.fig.canvas.draw()
            plt.pause(animationSpeed)

    def startSimulation(self):
        # # --- FOR TESTING ---
        # self.processes = makeRandomProcesses(5, 10)

        if not self.processes:
            return

        self.createProcessesBarhs()
        self.startAnimation(0.5)

        # Clear all
        self.processes = []
        self.listaBoxL.delete(0, 'end')
        
        # TODO: clear canvas


# --- FOR TESTING ---
def makeRandomProcesses(numProcesses, maxDuration=100):
    """Create N processes, with random start and duration"""
    processes = []
    for processId in range(numProcesses):
        duration = random.randint(1, maxDuration)
        startTime = random.randint(0, maxDuration)
        processes.append(Process(processId, startTime, duration))
    return processes


def main():
    app = App("Practica 2", "1200x800")
    app.run()


if __name__ == '__main__':
    main()
