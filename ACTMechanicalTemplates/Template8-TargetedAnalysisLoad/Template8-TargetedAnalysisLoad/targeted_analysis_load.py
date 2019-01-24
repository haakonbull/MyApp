"""
   This file is the main Python file for the "Template8-TargetedAnalysisLoad" template. 
   
   Remark:
   Python programming expects users to respect certain formats.
   e.g. The leading whitespace (spaces and tabs) at the beginning of a line (i.e. the indentation level of the line) is VERY IMPORTANT in Python.
   DO NOT mix spaces and tabs while indenting a line.
"""

def createStaticLoad(analysis):
    """
       This method is called when the toolbar button "Structural Load" is clicked.

       Keyword arguments:
       analysis -- the active analysis
    """

    # We don't need to add any check here as <canadd> callback will do the check
    analysis.CreateLoadObject("Structural Load")


def createModalLoad(analysis):
    """
       This method is called when the toolbar button "Modal Load" is clicked.

       Keyword arguments:
       analysis -- the active analysis
    """

    # We don't need to add any check here as <canadd> callback will do the check
    analysis.CreateLoadObject("Modal Load")


def createUniqueLoad(analysis):
    """
       This method is called when the toolbar button "Unique Load" is clicked.

       Keyword arguments:
       analysis -- the active analysis
    """

    # We don't need to add any check here as <canadd> callback will do the check
    analysis.CreateLoadObject("Unique Load")


def canAddStaticLoad(analysis, loadName):
    """
       Method called to check if the "Structural Load" load object can be created in the current analysis.
       Return True or False.

       Keyword arguments:
       analysis -- the analysis on which the load object is added
       loadName -- the added object name
    """

    # Check the Analysis and Physics type.
    if analysis.AnalysisType.ToString() == "Static" and analysis.PhysicsType.ToString() == "Mechanical":
        return True

    # In case of other analysis/physics type.
    msg = "Selected Analysis is: " + analysis.Name + "\n"
    msg += "Load: " + loadName + " is applicable for Static Structural analysis only"
    ExtAPI.Application.LogWarning(msg)
    return False


def canAddModalLoad(analysis, loadName):
    """
       Method called to check if the "Modal Load" load object can be created in the current analysis.
       Return True or False.

       Keyword arguments:
       analysis -- the analysis on which the load object is added
       loadName -- the added object name
    """

    # Check the analysis type.
    if analysis.AnalysisType.ToString() == "Modal":
        return True

    # In case of other analysis type.
    msg = "Selected Analysis is: " + analysis.Name + "\n"
    msg += "Load: " + loadName + " is applicable for Modal analysis only"
    ExtAPI.Application.LogWarning(msg)
    return False


def canAddUniqueLoad(analysis, loadName):
    """
       Method called to check if the load loadName can be created in the current analysis.
       The criterion used in this function is the name of the load.
       Using this function, it is possible to assess the uniqueness of the load using the "loadName" for the given "analysis".
       Return True or False.

       Keyword arguments:
       analysis -- the analysis on which the load object is added
       loadName -- the added object name
    """

    # Check if the analysis already has a Unique Load.
    for load in analysis.LoadObjects:
        if load.Name == loadName: # loadName == "Unique Load"
            # A unique load is already created.
            msg = "Selected Analysis is: " + analysis.Name + "\n"
            msg += "Only a single Unique Load can be inserted"
            ExtAPI.Application.LogWarning(msg)
            return False

    return True

