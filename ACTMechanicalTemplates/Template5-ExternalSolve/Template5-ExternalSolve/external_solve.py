"""
   This file is the main Python file for the "Template5-APDLBasedResultEvaluation" template. 
   
   Remark:
   Python programming expects users to respect certain formats.
   e.g. The leading whitespace (spaces and tabs) at the beginning of a line (i.e. the indentation level of the line) is VERY IMPORTANT in Python.
   DO NOT mix spaces and tabs while indenting a line.
"""

# The os module is useful for path concatenation
import os

# The ansys module contains the RunANSYS command
import ansys
# This is defined in the file "ansys.py" located in the "libraries" folder, which is part of the standard ACT installation

def CreateAPDLBasedResultEvaluation(analysis):
    """
       This callback is called when the toolbar button is clicked.

       Keyword argument:
       analysis -- the active analysis
    """

    # The MAPL command that we will use works only with Modal analysis.
    # Note: an other approch to restrict the load creation is the "canadd" callback.
    if str(analysis.AnalysisType) == "Modal":
        # Use the analysis to create the APDL Based Result Evaluation result.
        analysis.CreateResultObject("APDLBasedResultEvaluation")
    else:
        # Display an error message in the Mechanical message log.
        ExtAPI.Application.LogError("This result works only with Modal analysis.")


class APDLBasedResultEvaluationController:
    """
       Controller for the APDL Based Result Evaluation result.

       This controller implements two callbacks: onstarteval and getvalue.
       "onstarteval" is called before result evaluation. 
       "getvalue" is called to get nodal values one by one so that Mechanical can use them as any other standard result.
    """

    def __init__(self, extAPI, result):
        """
           The constructor of the controller class
        
           Keyword arguments:
           extAPI -- the extension API
           result -- the result object associated with this controller
        """
        
        # Save the Extension API object for further use.
        self.extAPI = extAPI

        # Create a dictionary to save the values of the result.
        # The keys of the dictionary will be the node identifiers,
        # and the values a list of 3 associated results (X, Y, Z)
        self.values = {}
    
    def evaluate (self,result, stepInfo, collector):
        """
           The evaluate callback function of this controller.

           This method creates an APDL macro file, runs an ANSYS solve
           with this file and reads the result file to fill the "values" member
           and returns a list of result associated with the given node identifier.
           

           Keyword arguments:
           result       --  the result object associated with this controller
           stepInfo     --  object with properties that provides information 
                            on the current result set number or the current time step
           collector    --  used by the application for displaying the result
        """

        step = stepInfo.Set          # access the step's set number.  
        nodeIds = collector.Ids      # access the ids on which the collector needs results. 

        # Get the working directory of the analysis.
        workingDir = result.Analysis.WorkingDir

        # Get the file name of the ansys solver files.
        ansysResultFilename = os.path.join(workingDir, "file")

        # Create a filename for our results.
        resultFilename = os.path.join(workingDir, "results.txt")

        # Open the macro file that we will write into.
        macroFilename = "macro.inp"
        try:
            macroFile = open(os.path.join (workingDir, macroFilename),'w')
        except IOError:
            # If and error appened during file opening, print a message and exit.
            self.extAPI.Log.WriteError("Cannot open the file: "+ macroFilename)
            return

        # Write the first part of the APDL macro.
        macroFile.write("/batch\n")
        macroFile.write("/post1\n")
        macroFile.write("FILE," +  '\'' + ansysResultFilename + '\'' +'\n')
        macroFile.write("SET,,,velo,,,," + str(step) + '\n')

        # To write the node ids, we use the function "createNodalComponent" defined below.
        scoping = result.Properties["Geometry"].Value
        mesh = result.Analysis.MeshData
        self.createNodalComponent(scoping.Ids, "velapdl" + str(result.Id), mesh, macroFile)

        # Write the last part of the APDL macro
        macroFile.write("CMSEL, S, velapdl" + str(result.Id) + "\n")
        macroFile.write("*GET, ncount, NODE, 0, count\n")
        macroFile.write("*dim,varray,array,ncount,4\n")
        macroFile.write("nnum = ndnext(0)\n")
        macroFile.write("*do,_nn,1,ncount\n")
        macroFile.write("varray(_nn,1) = nnum\n")
        macroFile.write("varray(_nn,2) = ux(nnum)\n")
        macroFile.write("varray(_nn,3) = uy(nnum)\n")
        macroFile.write("varray(_nn,4) = uz(nnum)\n")
        macroFile.write("nnum = ndnext(nnum)\n")
        macroFile.write("*enddo\n")
        macroFile.write("alls\n")
        macroFile.write("*cfopen,results,txt\n")
        macroFile.write("*vwrite,varray(1,1),varray(1,2),varray(1,3),varray(1,4)\n")
        macroFile.write("(F10.0,'  ',E10.4,'  ',E10.4,'  ',E10.4)\n")
        macroFile.write("*cfclose\n")
        macroFile.write("fini\n")
        macroFile.write("/exit")

        # Close the file.
        macroFile.close()

        # Run ANSYS in batch mode with this macro file.
        commandlinestring = " -b nolist -i " + macroFilename + " -o out.lis /minimise"
        ansys.RunANSYS(ExtAPI, commandlinestring, runDir=workingDir, exelocation=None, minimized=True)

        # Read the result file generated by the command.
        with open(resultFilename) as fp:
            # Parse each line of the file.
            for line in fp:
                # Split the line with the whitespace separator.
                v = line.split()
                # Check the validity of the split
                if len(v) == 4:
                    # The first column is the node identifier.
                    nodeId = int(float(v[0]))
                    # Fill the class "values" dictionnary with the 3 others columns.
                    self.values[nodeId] = [float(v[1]), float(v[2]), float(v[3])]


        # Check that we have values for this node id.
        for nodeId in nodeIds:
            collector.SetValues(nodeId,self.values[nodeId])




    def createNodalComponent(self, geometryIds, groupName, mesh, macroFile):
        """
           Helper method to create element component from a given geometryId IDs.

           It writes APDL "CMBLOCK" command in the given file stream "macrofile" according
           to the given geometry identifiers.

           Keyword arguments:
           geometryIds -- a list of geometry IDs
           groupName   -- the name of the element component to be created
           mesh        -- the mesh object
           stream      -- the stream used to write the APDL commands
        """

        # First get the total number of nodes.
        nodeCount = 0;
        for geometryId in geometryIds:
            meshRegion = mesh.MeshRegionById(geometryId)
            nodeCount += meshRegion.NodeCount

        # Write the CMBLOCK command with the given group name and the node count.
        macroFile.write("CMBLOCK,"+ groupName + ",NODE,"  +  str(nodeCount) +"\n")
        macroFile.write("(8i10)\n")

        # Write the list of node identifiers
        blockCounter = 0
        for geometryId in geometryIds:
            # Get the node ids via the mesh region.
            meshRegion = mesh.MeshRegionById(geometryId)
            nodeIds = meshRegion.NodeIds
            # For each node id, write the formatted id.
            for nodeId in nodeIds:
                blockCounter += 1
                macroFile.write('% 10d' % nodeId)

                # Every 8 blocks, start a new line.
                if blockCounter % 8 == 0:
                     macroFile.write("\n")

        #Write a new line at the end of the file.
        macroFile.write("\n")
