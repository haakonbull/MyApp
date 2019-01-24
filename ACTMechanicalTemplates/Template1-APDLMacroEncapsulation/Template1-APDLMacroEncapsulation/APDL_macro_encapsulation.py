"""
   This file is the main Python file for the "Template1-APDLMacroEncapsulation" template. 
   
   Remark:
   Python programming expects users to respect certain formats.
   e.g. The leading whitespace (spaces and tabs) at the beginning of a line (i.e. the indentation level of the line) is VERY IMPORTANT in Python.
   DO NOT mix spaces and tabs while indenting a line.
"""

# Import the "os" python module for file management purpose.
import os

def createBladeLoad(analysis):
    """
       The method is called when the toolbar button is clicked.

       Keyword arguments:
       analysis -- the active analysis
    """
    
    analysis.CreateLoadObject("bladeLoad")


def writeConvectionLoad(load, stream):
    """
       The GetSolveCommands callback should add all the required commands to the solver 
       input (ds.dat) file. The file APDL_script_for_convection.inp acts as a template 
       for the commands that will be written into the solver input. Values provided by the 
       user in the UI replace the key fields ($thickness$, $film_coefficient$, $temperature$ and $blade_comp$).

       This method is called when the solver input is being written.

   	   Keyword arguments:
   	   load -- the load associated with this callback
   	   stream -- a System.IO.TextWriter object, to which solver commands should be appended (represents the 
                 ds.dat file) 
    """

    ##################################
    # Step-1 : Collect the user inputs.
    ##################################
    # Get the NamedSelection name.
    namedSelection = load.Properties["Geometry"].Value
    refName = namedSelection.Name 

    # Get the other inputs required for the APDL macro.
    thickness = load.Properties["Thickness"].Value
    filmCoeff = load.Properties["FilmCoeff"].Value
    temperature = load.Properties["Temperature"].Value

    ##################################
    # Step-2: Read the APDL commands (from an external file) for applying the load.
    ##################################
    extensionDir = ExtAPI.ExtensionManager.CurrentExtension.InstallDir
    macroFile = "APDL_script_for_convection.inp"

    # Read the macro and copy the commands to a string
    fs = open(os.path.join(extensionDir, macroFile), "r")
    allLines = fs.read()
    fs.close()

    ##################################
    # Step-3: Replace the vaiables in those commands with the user inputs.
    ##################################
    allLines = allLines.replace("$thickness$", str(thickness))
    allLines = allLines.replace("$film_coefficient$", str(filmCoeff))
    allLines = allLines.replace("$temperature$", str(temperature))
    allLines = allLines.replace("$blade_comp$", refName)
    
    # Add the command lines to solver input (ds.dat) file.
    stream.WriteLine(allLines)

