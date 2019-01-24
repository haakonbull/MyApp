"""
   This file is the main Python file for the "Template6-GenericObject" template. 
   
   Remark:
   Python programming expects users to respect certain formats.
   e.g. The leading whitespace (spaces and tabs) at the beginning of a line (i.e. the indentation level of the line) is VERY IMPORTANT in Python.
   DO NOT mix spaces and tabs while indenting a line.
"""


def createGroup(analysis):
    """
       The method is called when the toolbar button is clicked.

       Keyword arguments:
       analysis -- the active analysis
    """

    # Add a "parent" object [defined in XML] in solution tree of the analyis.
    analysis.CreatePostObject("parent")


def createChild(obj):
    """
       The method is called when the "CreateChild" action button is clicked

       Keyword arguments:
       obj -- the object containing the action
    """

    # Add a "child" load [defined in XML] under the "parent" object.
    obj.CreateChild("child")


def evaluateResult(obj):
    """
       The method is called when the "Evaluate" action button is clicked or
       from the generateChildren method.

       Keyword arguments:
       obj -- the object to avaluate
    """

    # Set the State property to Evaluated.
    obj.Properties["State"].Value = "Evaluated"

    # Force to update the object state.
    obj.Suppressed = True
    obj.Suppressed = False


def generateChildren(obj):
    """
       Helper method to generate the children of a "parent" object.

       Keyword arguments:
       obj -- the "parent" object containing the children
    """

    for child in obj.Children:
        evaluateResult(child)


def clearChildren(obj):
    """
       Helper method to clear children of a "parent" object.

       Keyword arguments:
       obj -- the "parent" object containing children
    """

    for child in obj.Children:
        child.Properties["State"].Value = "Need Evaluation"

        # Force Mechanical to re-validate properties and update the object state.
        child.Suppressed = True
        child.Suppressed = False


def isStateValid(obj, property):
    """
       Checks the validity of the State property.

       Keyword arguments:
       obj -- the object containing the property
       property -- the property to check
    """

    return property.Value == "Evaluated"


