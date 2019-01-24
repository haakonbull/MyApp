

import os
import myUtils

a = 1
# ---------- Disse maa vaere med for aa bruke MessageBox.Show ---------- 
clr.AddReference("Ans.UI.Toolkit.Base")
clr.AddReference("Ans.UI.Toolkit")
from Ansys.UI.Toolkit import *
# __________ Disse maa vaere med for aa bruke MessageBox.Show __________ 


def init(context):
    if hasEvaluationEnded(None): return
    ExtAPI.Log.WriteMessage("---------- init ----------") 
    ExtAPI.Log.WriteMessage("- The extension MyApp has just loaded --- ")
    input_is_string = isinstance(context, basestring)
    ExtAPI.Log.WriteMessage("Print true if the input is a string:")
    ExtAPI.Log.WriteMessage(str(input_is_string))
    ExtAPI.Log.WriteMessage("Print the input string \"context\":")
    ExtAPI.Log.WriteMessage("The input string is: ")
    ExtAPI.Log.WriteMessage(context)
    ExtAPI.Log.WriteMessage("__________ init __________ ")
	
def OnClickPythonFunction(currentAnalysis):
	# ---------- Haakon ---------- 
	#MessageBox.Show("Haakon is the man!!!")
	ExtAPI.Log.WriteMessage("I am just about to add a load called Haakons_load.")
	load = currentAnalysis.CreateLoadObject("Haakons_load", ExtAPI.ExtensionManager.CurrentExtension)
	ExtAPI.Log.WriteMessage("I just added a load called Haakons_load.")
	a = 2
	a = 3
	a = 4
	a = 5
	a = 2
	print("finished")
    # __________ Haakon __________ 

	
def Say_Hello(someinput):
    if hasEvaluationEnded(None): return
    a = 1 
    #MessageBox.Show("Hello moron. Compile script = false!")
    a = 1
    input_is_string = isinstance(someinput, basestring)
    ExtAPI.Log.WriteMessage("Print true if the input is a string:")
    ExtAPI.Log.WriteMessage(str(input_is_string))
    a = 2
    a = 3
    a = 4
    a = 5
    Random_function_not_connected(None)
    MessageBox.Show("Extension finished")
	


def Random_function_not_connected():
    a =1
    a = 2
    MessageBox.Show("Extension finished")
    print("hei du")
    a = 3
    for i in range(0,100):
        a = a + 1

    
def createBladeLoad(currentAnalysis):
    if hasEvaluationEnded(None): return
    ExtAPI.Log.WriteMessage("The input string is: ")
    ExtAPI.Log.WriteMessage(context)
    ExtAPI.Log.WriteMessage("Clicked on Convection on Blade button...")
    load = currentAnalysis.CreateLoadObject("bladeLoad", ExtAPI.ExtensionManager.CurrentExtension)

def writeConvLoad(load,stream):
    if hasEvaluationEnded(None): return
    ExtAPI.Log.WriteMessage("Write bladeLoad...")
    stream.Write("/com,\n")
    stream.Write("/com,*********** Conv. Blade Load "+load.Caption+" ***********\n")
    stream.Write("/com,\n")

    # Collect the user inputs
    propGeo = load.Properties["Geometry"]
    geoType = propGeo.Properties['DefineBy'].Value
    if geoType == 'Named Selection':
        refName = propGeo.Value.Name
    else:
        refIds = propGeo.Value.Ids
        
    thickness = load.Properties["Thickness"].Value
    filmCoeff = load.Properties["FilmCoeff"].Value
    temperature = load.Properties["Temperature"].Value

    # Convert the user inputs to APDL commands
                                  
    stream.Write("thickness="+thickness.ToString()+"\n")
    stream.Write("film_coefficient="+filmCoeff.ToString()+"\n")
    stream.Write("temperature="+temperature.ToString()+"\n")

    stream.Write("\n/prep7\n")
    
    mesh = load.Analysis.MeshData
    geo = load.Analysis.GeoData

    if geoType != 'Named Selection':
        # Create the element component if user has selected Geometry
        myUtils.createElementComponent(refIds, "boltConv" + load.Id.ToString(), mesh, stream)
        stream.Write("CMSEL, S, boltConv"+ load.Id.ToString() + "\n")
    else:
        stream.Write("CMSEL,S,"+refName+"\n")

    # Reuse the APDL commands for applying the load
    SourceDir = ExtAPI.ExtensionManager.CurrentExtension.InstallDir
    macFile = "APDL_script_for_convection.inp"

    # Read the macro and copy the commands to ds.dat
    fs = open(os.path.join(SourceDir, macFile), "r")
    allLines = fs.readlines()
    fs.close()
    stream.Write("".join(allLines))
    
# Alternatively, you can call the input file directly .... by /input command
# inpComm = """/inp,'%s' \n"""%os.path.join(SourceDir, macFile)
# stream.Write(inpComm)
 

 
 
#------------------------- EVALUATION ------------------------- 
isEvaluation = False    # Compile with this option if license locked version
#isEvaluation = True    # Compile with this option if not license locked, i.e. no <appstoreid> in XML
expY = '2019'
expM = '08'
expD = '30'
expV = 19.2

import os, time
import math
import System
import Ansys
clr.AddReference("Ans.UI.Toolkit")
clr.AddReference("Ans.UI.Toolkit.Base")
from Ansys.UI.Toolkit import *
if ExtAPI.Context == 'Mechanical':
    import ansys
    import units

# Evaluation check
def hasEvaluationEnded(dummy):
    global MajorVersion
    global MinorVersion
    MajorVersion = Ansys.Utilities.ApplicationConfiguration.DefaultConfiguration.VersionInfo.MajorVersion
    MinorVersion = Ansys.Utilities.ApplicationConfiguration.DefaultConfiguration.VersionInfo.MinorVersion
    if isEvaluation:
        today = time.strftime('%Y%m%d')
        expDate = expY+expM+expD
        appName = ExtAPI.ExtensionManager.CurrentExtension.Name
        currentV = float(str(MajorVersion) + '.' + str(MinorVersion))
        if currentV > expV:
            ExtAPI.Application.LogError(appName + ' is limited to version ' + str(expV) +'!')
            return True
        elif int(today) > int(expDate):
            ExtAPI.Application.LogError('Evaluation period for ' + appName + ' has expired!')
            return True
        else:
            ExtAPI.Application.LogInfo('Evaluation period for ' + appName + ' ends '+expY+'.'+expM+'.'+expD)
            return False
    else: return False
 
#_________________________ EVALUATION _________________________  
