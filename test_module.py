import sys
import numpy as np
from PyQt5 import QtWidgets, QtCore, QtGui
import pyqtgraph.opengl as gl
import time
import trimesh
from MeshViewer.display import MeshViewer

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # Central Widget
        self.central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout = QtWidgets.QVBoxLayout(self.central_widget)

        # MeshViewer setup
        self.viewer = MeshViewer(self.central_widget)
        self.viewer.set_background_color((0,0,0,1))
        self.layout.addWidget(self.viewer.viewer)

        # Load mesh and display
        mesh = trimesh.load('base.stl')
        print(mesh.vertices.shape)
        
        self.mesh_inst = self.viewer.add_mesh(self.mesh, color=(0,0,255,255), pos=[0,0,0])
        text = self.viewer.add_texticon('Hello', pos=[0,0,0], color=(255,0,0,255), font=QtGui.QFont('Times New Roman', 20))

        # Timer for animation
        self.index = 0
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(50)

    def update_animation(self):
        start = time.perf_counter()
        self.viewer.update_mesh(self.mesh_inst, self.mesh, pos=[self.index/20,0,0, 0,0,0])
        self.index += 1
        if self.index > 50:
            self.index = 0
        print(time.perf_counter() - start)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
