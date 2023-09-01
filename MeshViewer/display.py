import numpy as np
from PyQt5 import QtWidgets, QtCore, QtGui
import pyqtgraph.opengl as gl
import xml.etree.ElementTree as ET
import trimesh


class MeshViewer(QtWidgets.QWidget):

    def __init__(self, parent=None):
        """ Create a GLViewWidget and use it to display a robot model, meshes, trajectories and text icons.

        Args:
            robot (rtb., optional): _description_. Defaults to None.
            parent (_type_, optional): parent class of GLViewWidget. Defaults to None.
        """
        super().__init__(parent)
        self.viewer = gl.GLViewWidget(self)
        
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.viewer)
        self.setLayout(layout)
        
        

        
    def set_background_color(self, color:tuple=(0,0,0,1)):
        self.viewer.setBackgroundColor(QtGui.QColor(int(color[0]*255),
                                                    int(color[1]*255),
                                                    int(color[2]*255),
                                                    int(color[3]*255)))
        
    def add_texticon(self, text:str=None, pos:list= None, color:tuple=(255,255,255,255), font: QtGui.QFont = QtGui.QFont('Helvetica', 14)):
        """ Add text icon to viewer

        Args:
            text (str): string to be displayed
            pos (list, optional): position of text icon in x, y, z axis (unit is meters). Defaults to None.
            color (tuple, optional): color in terms of RGB or RGBA. Defaults to (255,255,255,255).
            font (QtGui.QFont, optional): font style and size. Defaults to QtGui.QFont('Helvetica', 14).

        Returns:
            gl.GLTextItem: GLTextItem Instance
        """
        
        text = gl.GLTextItem(text=text, color=color, font=font)
        self.viewer.addItem(text)
        if pos is not None:
            text.setData(pos=pos)
        return text
    
    
    def clear_texticon(self, text:gl.GLTextItem):
        self.viewer.removeItem(text)
        
    def add_mesh(self, mesh:trimesh.base.Trimesh, color:tuple=(255,255,255,255), pos:list=None):
        """_summary_

        Args:
            mesh (trimesh.base.Trimesh): trimesh object
            color (tuple, optional): color in terms of RGB or RGBA. Defaults to (255,255,255,255).
            pos (list, optional): position of mesh in x, y, z axis (unit is meters). Defaults to None.

        Returns:
            gl.GLMeshItem: GLMeshItem Instance
        """
        mesh_item = gl.GLMeshItem(vertexes=mesh.vertices, faces=mesh.faces, smooth=False, drawEdges=False, edgeColor=(0,0,0,1), color=color, pos=pos)
        mesh_item.setShader("edgeHilight")
        self.viewer.addItem(mesh_item)
        
        return mesh_item
    
    def clear_mesh(self, mesh:gl.GLMeshItem):
        """ Remove mesh from viewer

        Args:
            mesh (gl.GLMeshItem): mesh to be removed
        """
        self.viewer.removeItem(mesh)
        
    def update_mesh(self,mesh_item:gl.GLMeshItem, mesh:trimesh.base.Trimesh, pos:list=None):
        """ Update mesh location

        Args:
            mesh_item (gl.GLMeshItem): mesh to be updated
            mesh (trimesh.base.Trimesh): new mesh/or the mesh to apply transformation
            pos (list, optional): new location of mesh in x, y, z, r, p, y axis (unit is meters). Defaults to None.
            
        """
        def compute_transformation_matrix(vertices, location:list):
            T = np.eye(4)
            T[:3, 3] = location[:3]
            T[:3, :3] = trimesh.transformations.euler_matrix(location[3], location[4], location[5])[:3, :3]
            transformed_vertices = np.dot(
                    T,
                    np.hstack((vertices, np.ones(
                        (vertices.shape[0], 1)))).T).T[:, :3]   
            return transformed_vertices
        mesh_item.setMeshData(vertexes=compute_transformation_matrix(mesh.vertices, pos), faces=mesh.faces)        
        
    def add_image(self, image:np.ndarray, pos:list=None):
        """ Add image to viewer

        Args:
            image (np.ndarray): image array
            pos (list, optional): position of image in x, y, z axis (unit is meters). Defaults to None.

        Returns:
            gl.GLImageItem: GLImageItem Instance
        """
        image_item = gl.GLImageItem(image=image)
        self.viewer.addItem(image_item)
        if pos is not None:
            image_item.setData(pos=pos)
        return image_item
    
    def clear_image(self, image:gl.GLImageItem):
        """ Remove image from viewer

        Args:
            image (gl.GLImageItem): image to be removed
        """
        self.viewer.removeItem(image)
