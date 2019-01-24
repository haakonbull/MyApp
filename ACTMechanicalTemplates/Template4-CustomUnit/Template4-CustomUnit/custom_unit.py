"""
   This file is the main Python file for the "Template4-CustomUnit" template. 
   
   Remark:
   Python programming expects users to respect certain formats.
   e.g. The leading whitespace (spaces and tabs) at the beginning of a line (i.e. the indentation level of the line) is VERY IMPORTANT in Python.
   DO NOT mix spaces and tabs while indenting a line.
"""

# import external module (units.py) located in the "libraries" folder, which is part of the standard ACT installation
import units

def CreateCustomUnit(analysis):
    """
       The method is called when the toolbar button is clicked.

       Keyword arguments:
       analysis -- the active analysis
    """
    # This will add the "CustomUnit" [defined in XML] load in the selected analysis tree
    analysis.CreateLoadObject("CustomUnit")    


def v2sUnit(load, prop, val):
    """
       Convert the numeric value to a string representation by adding the units 
       Use the function ConvertUnit(value, fromUnit, toUnit) available from the units external module   

       Keyword arguments:
       load -- the current load associated to the callback
       prop -- property of the load that includes unit definition
       val  -- the value to be treated
    """
   
    try:
        fromUnit = prop.Attributes["Unit"] # Accessing the attribute defined in the XML file i.e. "kg m^-2"
        # Convert using the original constituent units (i.e. "kg" to current Mass unit and "m" to the current Length unit)
        massUnit = ExtAPI.DataModel.CurrentUnitFromQuantityName("Mass")
        lenUnit = ExtAPI.DataModel.CurrentUnitFromQuantityName("Length")
        
        toUnit = massUnit + " " + lenUnit + "^-2" # e.g. "lbm in^-2"
        v = units.ConvertUnit(val, fromUnit, toUnit)
        # Convert the numerical value to string
        vs = v.ToString(System.Globalization.CultureInfo.InvariantCulture)
        # The InvariantCulture property is used here for data persistence in a culture-independent format.
        # i.e. To account for comma used as a decimal point in certain culture: 2.5 (English) = 2,5 (French, German) ...in either case, vs = "2.5"
        # Append the [mass length^-2] to the string to be displayed
        retStr  = vs + " [" + massUnit + " " + lenUnit + "^-2" + "]"
        return retStr # e.g. "2.5 [lbm in^-2]"
    except:
        return ""


def s2vUnit(load, prop, str):
    """
       Convert the string to a number
       Use the function: ConvertUnit(value, fromUnit, toUnit) available from the units external module   

       Keyword arguments:
       load -- the current load associated to the callback
       prop -- property of the load that includes unit definition
       str  -- the string to be treated
    """

    try:
        value = System.Double.Parse(str) # e.g. str = "2.5 kg m^-2"  --> val = 2.5

        massUnit = ExtAPI.DataModel.CurrentUnitFromQuantityName("Mass")
        lenUnit = ExtAPI.DataModel.CurrentUnitFromQuantityName("Length")
                
        # We need do the conversion using the original constituent units (i.e. "kg" to current Mass unit and "m" to the current Length unit)
        fromUnit = massUnit + " " + lenUnit + "^-2" # e.g. "lbm in^-2"
        toUnit = prop.Attributes["Unit"] # Accessing the attribute defined in the XML file i.e. "kg m^-2"

        # Note: The toUnit and fromUnit are exactly opposite in the v2sUnit and s2vUnit functions
        return units.ConvertUnit(value, fromUnit, toUnit)
    except:
        return System.Double.MaxValue # Represents the largest possible value of a Double


def getValueUnit(load, prop, value):
    """
       This function is called each time the value of the property is accessed
       Use the function: ConvertUnit(value, fromUnit, toUnit) available from the units external module   

       Keyword arguments:
       load -- the current load associated to the callback
       prop -- property of the load that includes unit definition
       str  -- the string to be treated
    """
    try:
        fromUnit = prop.Attributes["Unit"]

        massUnit = ExtAPI.DataModel.CurrentUnitFromQuantityName("Mass")
        lenUnit = ExtAPI.DataModel.CurrentUnitFromQuantityName("Length")    
        toUnit = massUnit + " " + lenUnit + "^-2"

        return units.ConvertUnit(value, fromUnit, toUnit)
    except:
        return System.Double.MaxValue


def GetSolveCommandsL(load, stream):
    """
       This function adds the required commands to the solver input (ds.dat) file
       
       Keyword arguments:
       load   -- the current load associated to the callback
       stream -- a System.IO.TextWriter object, to which solver commands should be appended (represents the ds.dat file)
    """
       
    propValue = load.Properties["Value"]

    # ConvertToSolverConsistentUnit: Convert from the currently activated unit in the application to the corresponding consistent unit used by the solver
    # It is always recommended to write the values from any ACT loads in SolverConsistentUnit
    convMassfactor = units.ConvertToSolverConsistentUnit(ExtAPI, 1, "Mass", load.Analysis) 
    convLengthfactor = units.ConvertToSolverConsistentUnit(ExtAPI, 1, "Length", load.Analysis)
    
    value = propValue.Value*(convMassfactor/(convLengthfactor**2)) # Converting the number to SolverConsistentUnit
    vs = value.ToString(System.Globalization.CultureInfo.InvariantCulture)
    
    stream.WriteLine("!! Value = " + vs)

