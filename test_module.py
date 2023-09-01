import numpy as np
from PyQt5 import QtWidgets, QtCore, QtGui
import pyqtgraph.opengl as gl
import time
import trimesh
from MeshViewer.display import MeshViewer

app = QtWidgets.QApplication([])

viewer = MeshViewer()
viewer.set_background_color((0,0,0,1))
viewer.viewer.show()

mesh = trimesh.load('base.stl')
mesh_inst = viewer.add_mesh(mesh, color=(0,0,255,255), pos=[0,0,0])

text = viewer.add_texticon('Hello', pos=[0,0,0.5], color=(255,0,0,255), font=QtGui.QFont('Times New Roman', 20))


index = 0
def update():
    start = time.perf_counter()
    global index
    viewer.update_mesh(mesh_inst,mesh, pos=[index/200,0,0, 0,0,0])
    index += 1
    if index > 50:
        index = 0
    print(time.perf_counter() - start)


t2 = QtCore.QTimer()
t2.timeout.connect(update)
t2.start(50)

if __name__ == '__main__':

    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtWidgets.QApplication.instance().exec_()
