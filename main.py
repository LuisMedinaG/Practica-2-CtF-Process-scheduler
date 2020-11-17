import matplotlib.pyplot as plt
import random


class Process():
    def __init__(self, processId, startTime, duration):
        self.processId = processId
        self.startTime = startTime
        self.duration = duration

    def __repr__(self):
        return f"ID: {self.processId}  STRT: {self.startTime}  DUR: {self.duration}"


def makeRandomProcesses(numProcesses, maxDuration=100):
    processes = []
    for processId in range(numProcesses):
        duration = random.randint(1, maxDuration)
        startTime = random.randint(0, maxDuration)
        processes.append(Process(processId, startTime, duration))

    return processes


def get_cmap(n, name='hsv'):
    return plt.cm.get_cmap(name, n)


def plotProcesses(processes):
    # Hide menu toolbar
    plt.rcParams['toolbar'] = 'None'

    # Style configuration
    fig, ax = plt.subplots()
    ax.axes.yaxis.set_visible(False)

    # Initialize range of posible colors
    cmap = get_cmap(len(processes), 'viridis_r')

    barWidth = 10
    y_position = 0
    for p in processes:
        ax.broken_barh([(p.startTime, p.duration)], (y_position, barWidth - 1),
                       facecolors=cmap(p.processId))
        y_position += barWidth

    plt.show()


def main():
    processes = makeRandomProcesses(4)
    plotProcesses(processes)


if __name__ == '__main__':
    main()
