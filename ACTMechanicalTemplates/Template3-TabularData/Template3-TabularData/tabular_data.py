"""
   This file is the main Python file for the "Template3-TabularData" template. 
   
   Remark:
   Python programming expects users to respect certain formats.
   e.g. The leading whitespace (spaces and tabs) at the beginning of a line (i.e. the indentation level of the line) is VERY IMPORTANT in Python.
   DO NOT mix spaces and tabs while indenting a line.
"""

def createTableLoad(analysis):
    """
       The method is called when the toolbar button is clicked.

       Keyword arguments:
       analysis -- the active analysis
    """

    # Add the "Tabular" ACT load as defined in the XML file in the selected analysis tree.
    analysis.CreateLoadObject("Tabular")


def OnInitFixedRowTable(load, property):
    """
        Called when the property is initialized. Create and
        fill the static rows.

        Keyword arguments:
        load     -- the load linked to the property
        property -- the property linked to the callback
    """

    # Put "False" to the properties "WithAddLine" and "WithDeleteLine"
    # to make the row number of this tabular data fixed.
    # The "Controller" field of the property object gets access to the properties and methods 
    # implemented in the class Worksheet.PropertyGroupEditor.PGEditor (i.e. it is a reference
    # to an instance of this class which is defined into the xml through the "class" attribute).
    # One instance of this class is created per property table.
    property.Controller.WithAddLine = False
    property.Controller.WithDeleteLine = False

    # Override the default initial size of the dialog box.
    property.Controller.size = [225,175]

    numRows = 5

    # Retrieve the fraction property.
    fractionProperty = property.Properties["Fraction"]

    # Create and set the rows content.
    for i in range(numRows):
        property.AddRow()
        fractionProperty.Value = i / float(numRows-1)
        property.SaveActiveRow()


def writeTabularData(load, stream):
    """
       Add commands to the solver input (ds.dat) file
       
       Keyword arguments:
       load   -- the current load linked to the callback
       stream -- a System.IO.TextWriter object, to which solver commands should be appended (represents the ds.dat file)
    """

    # Access the TimeDependent Table
    table1 = load.Properties["TimeDependent Table"]
    dataStep = table1.Properties["Step"]
    dataTime = table1.Properties["Time"]
    dataTest1 = table1.Properties["Test Data1"]

    # Write the data to the solver input (ds.dat) file
    stream.WriteLine("!! Writing data from the TimeDependent Table")
    for i in range(table1.RowCount):
        table1.ActiveRow = i
        stream.WriteLine("!! Step = {0} Time = {1} Value = {2}", dataStep.Value, dataTime.Value, dataTest1.Value)


    # Access the Manual Table
    table2 = load.Properties["Manual Table"]
    dataTest2 = table2.Properties["Test Data2"]

    # Write the data to the solver input (ds.dat) file
    stream.WriteLine("!! Writing data from the Manual Table")
    for i in range(table2.RowCount):
        table2.ActiveRow = i
        stream.WriteLine("!! Value = {0}", dataTest2.Value)

        
    # Access the Fixed Rows Table
    table3 = load.Properties["Fixed Rows Table"]
    dataFraction = table3.Properties["Fraction"]
    dataTest3 = table3.Properties["Test Data3"]

    # Write the data to the solver input (ds.dat) file
    stream.WriteLine("!! Writing data from the Fixed Rows Table")
    for i in range(table3.RowCount):
        table3.ActiveRow = i
        stream.WriteLine("!! Fraction = {0} Value = {1}", dataFraction.Value, dataTest3.Value)
