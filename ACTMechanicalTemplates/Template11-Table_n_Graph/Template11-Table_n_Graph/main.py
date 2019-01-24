"""
   This file is the main Python file for the "Template11" template. 
   
   Remark:
   Python programming expects users to respect certain formats.
   e.g. The leading whitespace (spaces and tabs) at the beginning of a line (i.e. the indentation level of the line) is VERY IMPORTANT in Python.
   DO NOT mix spaces and tabs while indenting a line.
"""

# Import the tabularand  helper modules for creating tables and graph. 
# This Python files tabular.py should be at same folder as this (main.py) file
# Note: Since these are external modules (not part of standard ACT bundle), the capabilities provided by these modules may be made available differently in future versions of ACT . 
#       Consequently, the use of these modules should require some refactoring when the extension will be used with future versions of Mechanical.

import clr
clr.AddReference("Ans.UI.Toolkit")
clr.AddReference("Ans.UI.Toolkit.Base")
import Ansys.UI.Toolkit

import tabular
import chart

# Define some global variables to use across functions
tabularPanel, figurePanel = None, None
figures = None
figure = None
tab = None
        
def showTable(analysis):
    """
       Method called when the show button is clicked.

       Keyword arguments:
       analysis -- the active analysis
    """
    
    global tabularPanel, figurePanel, figure, tab, figures
    if tabularPanel == None:
        if Ansys.UI.Toolkit.Window.MainWindow == None:
            Ansys.UI.Toolkit.Window.MainWindow = Ansys.UI.Toolkit.Window()
        # --- Create TabularData ---
        tab = tabular.Tabular()
        tab.labels = ['X', 'Y1', 'Y2']
        tabularPanel = ExtAPI.UserInterface.AttachControlToPanel(tab.view, MechanicalPanelEnum.TabularData)

        # --- Create Figure ---
        figure = chart.Figure()
        figures = chart.Figures(0,0) 
        figure.title('X Vs. Y Plot')
        figure.xlabel('X Values')
        figure.ylabel('Y Values')
        figurePanel = ExtAPI.UserInterface.AttachControlToPanel(figures.view, MechanicalPanelEnum.Graph)

        # Populate the table
        XArray = [0.0,1.0,2.0,3.0]
        Y1Array = [100.0,300.0,200.0,400.0]
        Y2Array = [400.0,200.0,300.0,100.0]    
        # Now display the table 
        columns = [XArray, Y1Array, Y2Array]
        tab.setdata(tab.labels, columns)
        tabularPanel.Show()

        # Clear the old figures and replot
        figures.clear()
        figure.plot(XArray, Y1Array, '-r+', variablelabel="Y1") 
        figure.plot(XArray, Y2Array, '-bo', variablelabel="Y2")
        figure.legend()
        figures.setfigures(1,1,figure)
        figurePanel.Show()
    
def hideTable(analysis):
    """
       Method called when the hide button is clicked.

       Keyword arguments:
       analysis -- the active analysis
    """
    global tabularPanel, figurePanel, figure, tab, figures
    if tabularPanel != None: # hide if the panels were created
        tabularPanel.Hide()
        figurePanel.Hide()
        figure.Dispose()
        figures.Dispose()
        tab.Dispose()
        tabularPanel.Close()
        figurePanel.Close()
        tabularPanel, figurePanel = None, None
        Ansys.UI.Toolkit.Window.MainWindow = None