import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation


class Process():
    """Process class"""
    def __init__(self, processId, startTime, duration):
        self.processId = processId
        self.startTime = startTime
        self.duration = duration

    def __repr__(self):
        return f"ID: {self.processId}  STRT: {self.startTime}  DUR: {self.duration}"


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


def plotProcesses(processes):
    # Hide menu toolbar
    plt.rcParams['toolbar'] = 'None'

    # Style configuration
    fig, ax = plt.subplots()
    ax.axes.yaxis.set_visible(False)

    # Initialize range of posible colors
    maxFinishTime = getMaxFinishTime(processes)
    barWidth = 10

    barCollection = []

    def createBars():
        yPosition = 0
        for p in processes:
            rect, = ax.barh(
                y=yPosition,
                width=p.duration,
                left=p.startTime,
                height=barWidth - 1)
            barCollection.append(rect)
            yPosition += barWidth

    """ TODO: Falta hacer la parte de la animacion. """
    # def drawProcess(globalTime):
    #     for p, b in zip(processes, barCollection):
    #         if globalTime >= p.startTime:
    #             if globalTime >= p.startTime + p.duration:
    #                 currDuration = p.duration
    #             else:
    #                 currDuration = globalTime - p.startTime
    #         else:
    #             currDuration = 0
    #     b.set_height(globalTime)
    # animation.FuncAnimation(fig, drawProcess, frames=50)

    createBars()
    plt.show()


def main():
    processes = makeRandomProcesses(numProcesses=5)
    plotProcesses(processes)


if __name__ == '__main__':
    main()
