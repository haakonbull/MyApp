"""
   This file is the main Python file for the "Template10-Graphics" template. 
"""


def CreateElementSelectorLoad(analysis):
    """
       Callback called when the toolbar button is clicked.

       Keyword arguments:
       analysis -- the active analysis
    """

    # Use the analysis to create the ElementSelectorLoad load.
    analysis.CreateLoadObject("ElementSelectorLoad")


def OnValidateScoping(load, property):
    """
       Function associated to the OnValidate callback.
       Force to redraw the graphic.
    
       Keyword arguments:
       load     -- the load bound containing the Scoping property.
       property -- the Scoping property.
    """

    # Force the controller to redraw elements.
    load.Controller.createElements()


class LoadController():
    """
       The class controller of the ElementSelectorLoad load.
    """

    def __init__(self, extApi, load):
        """
           The constructor of the class.

           Keyword arguments:
           extApi -- the extension API entry point.
           load -- the load controlled by this controller.
        """

        # Store the extension API into a field.
        self.extApi = extApi

        # Store the load into a field.
        self.load = load

        # The scene graphic object.
        self.mesh3d = None

    def createElements(self):
        """
           Method in charge to draw elements related to the scoping property.
           Function to be changed to integrate other graphic representation.
        """

        # Remove old graphic entities.
        self.onremove(self.load)

        # Retrieve the mesh associated to the analysis containing the load.
        mesh = self.load.Analysis.MeshData

        # Check that there is at least one node in mesh.
        if mesh.NodeCount == 0: return

        # Retrieve the Scoping property selection.
        selection = self.load.Properties["Scoping"].Value
        if selection == None: return

        # Retrieve node ids associated to the selection. 
		# For values of SelectionTypeEnum, see Reference Guide page 31.
        nodeIds = []
        if selection.SelectionType == SelectionTypeEnum.GeometryEntities:
            for geoId in selection.Ids:
                nodeIds.extend(mesh.MeshRegionById(geoId).NodeIds)
        if selection.SelectionType == SelectionTypeEnum.MeshNodes: 
            nodeIds.extend(selection.Ids)

        # Retreive element ids associated to node ids.
        elementIds = []
        for nodeId in nodeIds:
            elementIds.extend(mesh.NodeById(nodeId).ConnectedElementIds)

        # Remove duplicated element ids if needed.
        elementIds = list(set(elementIds))

        # Get associated elements.
        elements = [mesh.ElementById(id) for id in elementIds]

        # Use the graphic API to draw the mesh.
        # Use Suspend() to prevent the scene to redraw.
        with self.extApi.Graphics.Suspend():
            self.mesh3d = self.extApi.Graphics.Scene.Factory3D.CreateMesh(elements)
            self.mesh3d.Visible = True


    def onshow(self, load):
        """
           OnShow callback called when the load is selected.

           Keyword arguments:
           load -- the load controlled by this controller.
        """
        
        # Show the graphic object.
        if self.mesh3d:
            self.mesh3d.Visible = True


    def onhide(self, load):
        """
           OnHide callback called when the load unselected, i.e. something 
           else is selected in the tree.

           Keyword arguments:
           load -- the load controlled by this controller.
        """
        
        # Hide the graphic object.
        if self.mesh3d:
            self.mesh3d.Visible = False


    def onremove(self, load):
        """
           OnRemove callback called when the load is removed.

           Keyword arguments:
           load -- the load controlled by this controller.
        """
        
        # Dispose the 3D context.
        if self.mesh3d:
            self.mesh3d.Delete()
            self.mesh3d = None

