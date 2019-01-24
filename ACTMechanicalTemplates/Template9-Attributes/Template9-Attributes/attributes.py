"""
   This file is the main Python file for the "Template9-Attributes" template. 
   
   Remark:
   Python programming expects users to respect certain formats.
   e.g. The leading whitespace (spaces and tabs) at the beginning of a line (i.e. the indentation level of the line) is VERY IMPORTANT in Python.
   DO NOT mix spaces and tabs while indenting a line.
"""

def CreateGenerateLoad(analysis):
    """
       Method called when the toolbar button is clicked.

       Keyword arguments:
       analysis -- the active analysis
    """

    # Use the analysis to create the GenerateLoad.
    analysis.CreateLoadObject("GenerateLoad")


def OnInit(load):
    """
       Method called when the load is initialized (creation
       or resume).
    
       Keyword arguments:
       load -- the initialized load
    """

    # Retreive stored data.
    isGenerated = load.Attributes['isGenerated']

    # Check that isGenerated is defined and True.
    if(isGenerated != None and isGenerated == True):
        # Then, retreive and log persistent data
        # When you close and reopen Mechanical, you will see the Persistent data in the ACT log file
        values = load.Attributes['values']
        ExtAPI.Log.WriteMessage('Persistent data: ' + str(values))
    else:
        ExtAPI.Log.WriteMessage('No persistent data saved.')


def OnGenerate(load, progress):
    """
       Method called when the load is generated. This method must 
       return True if the generation succeed, False otherwise.

       OnGenerate for the load can only be executed only after the mesh is already generated
    
       Keyword arguments:
       load -- the generated load
       progress -- A function used to set the progress of the generate process
    """

    # Reteive the integer value.
    endRange = load.Properties['Range'].Value

    # Create a range from 0 to endRange.
    values = range(endRange)

    # Store values and generation-state into attributes.
    load.Attributes['values'] = values
    load.Attributes['isGenerated'] = True

    # Display the result range.
    load.Properties['Result'].Value = str(values)

    # Return True to indicates that the generation has successfully ended.
    return True


def OnClearData(load):
    """
       Method called when the data associated to the load
       are cleared.
    
       Keyword arguments:
       load -- the cleared load
    """

    # Reset stored attribute values.
    load.Attributes['values'] = None
    load.Attributes['isGenerated'] =  False

    # Reset Result property
    load.Properties['Result'].Value = 'Not Generated'

