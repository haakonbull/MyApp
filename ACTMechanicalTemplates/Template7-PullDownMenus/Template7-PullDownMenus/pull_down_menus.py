"""
   This file is the main Python file for the "Template7-PullDownMenus" template. 
   
   Remark:
   Python programming expects users to respect certain formats.
   e.g. The leading whitespace (spaces and tabs) at the beginning of a line (i.e. the indentation level of the line) is VERY IMPORTANT in Python.
   DO NOT mix spaces and tabs while indenting a line.
"""


def CreatePullDownMenusLoad(analysis):
    """
       This method is called when the toolbar button is clicked.

       Keyword arguments:
       analysis -- the active analysis
    """

    # Use the analysis to create the PullDownMenusLoad.
    analysis.CreateLoadObject("PullDownMenusLoad")


def OnActivateDynamicPullDown(load, property):
    """
       OnActivate callback that fills dynamically the content of the dynamic pull down menu according to the current selected value from the static pull down menu.
    
       Keyword arguments:
       load -- the current load associated to the callback
       property -- the dynamic pull down property
    """

    # Clear the old values via the Options field.
    property.Options.Clear()

    # Get the value of the static pulldown property via the given load.
    staticValue = load.Properties["StaticPullDown"].Value

    # Fill the dynamic property according to the static pull down menu.
    # It uses the Options field.
    if staticValue == "Option 1":
        property.Options.Add("Option 1.1")
        property.Options.Add("Option 1.2")
        property.Options.Add("Option 1.3")
    elif staticValue == "Option 2":
        property.Options.Add("Option 2.1")
        property.Options.Add("Option 2.2")
        property.Options.Add("Option 2.3")
    elif staticValue == "Option 3":
        property.Options.Add("Option 3.1")
        property.Options.Add("Option 3.2")
        property.Options.Add("Option 3.3")


def IsValidDynamicPullDown(load, property):
    """
       IsValid Callback to check if the current content of the dynamic pull down menu is valid or not.
       This validation can be done based on various criteria to be implemented in this function.
       Return True if the values are synchronized, False otherwise.
    
       Keyword arguments:
       load -- the current load associated to the callback
       property -- the dynamic pull down property
    """

    # Get both static and dynamic values.
    staticValue = load.Properties["StaticPullDown"].Value
    dynamicValue = property.Value

    # For each static value, fill a table with associated dynamic values.
    allowedValues = []
    if staticValue == "Option 1":
        allowedValues = ["Option 1.1", "Option 1.2", "Option 1.3"]
    elif staticValue == "Option 2":
        allowedValues = ["Option 2.1", "Option 2.2", "Option 2.3"]
    elif staticValue == "Option 3":
        allowedValues = ["Option 3.1", "Option 3.2", "Option 3.3"]
    else:
        # If the static pull down property has an unknown value, just invalidate the dynamic one.
        return False

    # Return True if the dynamic value is allowed, False otherwise.
    return dynamicValue in allowedValues
