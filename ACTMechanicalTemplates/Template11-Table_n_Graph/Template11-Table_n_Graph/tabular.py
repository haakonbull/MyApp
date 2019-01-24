# \file tabular.py
#
# This file contains the Tabular class used for the display of result tabular data information in the DataView.
#
#
#------------------------------------------------------------------------
#
# Copyright (c) ANSYS INC 2013, all rights reserved.
#
#------------------------------------------------------------------------
#
# \author: David Roche
#
#

# -----------------------------------
#   Tabular Class
# -----------------------------------

import clr

clr.AddReference("Ans.UI.Toolkit")
clr.AddReference("Ans.UI.Toolkit.Base")

import Ansys.UI.Toolkit

class Tabular(Ansys.UI.Toolkit.GridView):

    def __init__(self):
        Ansys.UI.Toolkit.GridView.__init__(self)
        self.view = self

        self._window = None
        self._needUpdate = False

        self.view.CopyRequested += self._onCopy

    # ------------------------
    #   public
    # ------------------------

    def setdata(self, labels, columns, lineNumber=True, update=True):
        if len(labels) != len(columns):
            raise Exception("Labels an columns must have the same size")
        self.labels = labels
        self.columns = columns
        self.linenumber = lineNumber
        self._needUpdate = True
        if update: self.update()

    def update(self):

        if not self._needUpdate: return
        self._needUpdate = False

        view = self.view
        columns = self.columns
        labels = self.labels

        view.Clear()
        view.SuspendLayout()

        view.ColumnHeadersVisible = True
        view.RowHeadersVisible = self.linenumber

        view.ColumnCount = len(labels)
        view.RowCount = len(max(columns, key=lambda column:len(column)))

        for j, column in enumerate(columns):
            for i, value in enumerate(column):
                cell = Ansys.UI.Toolkit.GridViewTextCell(str(value))
                cell.ReadOnly = True
                view.Cells.SetCell(i, j, cell)

        for label, column in zip(labels, view.Columns):
            column.Text = label
            column.ResizeToContents()

        self.view.ResumeLayout()     

    def clear(self):
        if self.view != None:
            self.view.Clear()

    def dispose(self):
        if self.view != None:
            self.view.Hide()
            self.view.Dispose()
            self.view = None

    # ------------------------
    #   Events
    # ------------------------

    def _onCopy(self, sender, args):
        pass
        #args.Handled = False
        #clip = "" 
        #for cell in args.SelectedCells:
        #    clip += cell.Text + "\n"
        #data = Ansys.UI.Toolkit.DataObject()
        #data.SetText(clip)
        #Ansys.UI.Toolkit.Clipboard.SetDataObject(data)
