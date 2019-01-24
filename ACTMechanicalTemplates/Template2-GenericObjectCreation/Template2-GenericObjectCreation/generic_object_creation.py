"""
   This file is the main Python file for the "Template2-GenericObjectCreation" template. 
   
   Remark:
   Python programming expects users to respect certain formats.
   e.g. The leading whitespace (spaces and tabs) at the beginning of a line (i.e. the indentation level of the line) is VERY IMPORTANT in Python.
   DO NOT mix spaces and tabs while indenting a line.
"""

def createGroup(analysis):
    """
        Add the "parent" ACT object as defined in the XML file in model tree above analyses
        
        Keyword arguments:
        analysis -- the active analysis
    """
    ExtAPI.Log.WriteMessage("createParent")
    ExtAPI.DataModel.CreateObject("parent")


def createChild(parent):
    """
       Create a child ACT object as defined in the XML file under the parent object
       This function refers to the "createChild" action defined in the parent object
       
       Keyword arguments:
       parent -- the parent ACT object
    """
    ExtAPI.Log.WriteMessage("createChild")
    parent.CreateChild("child")


def writeParentData(load, stream):
    """
       Add the required commands to the solver input (ds.dat) file
       
       Keyword arguments:
       load -- the load associated to the callback
       stream -- a System.IO.TextWriter object, to which solver commands should be appended (represents the ds.dat file)
    """

    # Access the childrens for this parent object
    stream.WriteLine("!! Inside Parent: " + load.Caption)
    inpData = load.Properties["Test Data"].Value
    stream.WriteLine("!! Input data for the parent = " + str(inpData))

    
    # Go over each child and write required commands for that child
    childrenCount = 0
    for index, child in enumerate(load.Children):
        if not child.Suppressed:
            # Access the child if it is not suppressed
            writeChildData(child, stream, childrenCount)
        else:

            stream.WriteLine("!! Child(" + str(index) + "): " + child.Caption + " is Suppressed.")
        childrenCount += 1
            
    stream.WriteLine("!! Number of children objects = " + str(childrenCount))


def writeChildData(child, stream, childIndex):
    """
       Add commands for a child. Is called from the parent  
       This function is called as many times as the number of child objects
       The inputs for the function are flexible (i.e. user can define the number of arguments and their order)
       
       Keyword arguments:
       child      -- a child ACT object
       stream     -- a System.IO.TextWriter object, to which solver commands should be appended (represents the ds.dat file)
       childIndex -- the index of the child in the parent children collection
    """
    
    # Add all the required commands to the solver input (ds.dat) file
    stream.WriteLine("!! Inside Child(" + str(childIndex) + "): " + child.Caption)
    childPropertyData = child.Properties["Test Data2"].Value
    stream.WriteLine("!! Input data for the child = " + str(childPropertyData))

    # Access the parent details from the child
    parentPropertyData = child.Parent.Properties["Test Data"].Value
    stream.WriteLine("!! Input data for the parent (" + child.Parent.Caption +  ") = " + str(parentPropertyData))

