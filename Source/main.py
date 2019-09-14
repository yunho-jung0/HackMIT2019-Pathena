import osmnx as ox
import matplotlib.pyplot as plt

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from Source.MapWindow import MapWindow


def main():

    place_name = "Richardson, Texas, USA"
    graph = ox.graph_from_place(place_name)
    print(type(graph))

    fig, ax = ox.plot_graph(graph)
    plt.tight_layout()

    """
    app = QApplication(sys.argv)
    window = MapWindow()
    window.setFixedWidth(1366)
    window.setFixedHeight(768)
    window.show()
    app.exec_()
    
    """


if __name__ == '__main__':
    main()

