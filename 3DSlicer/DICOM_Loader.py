import os
import subprocess
import slicer
import DICOMLib
import slicer.util

'''
usage instructions: to use this script in terminal
full Path to 3D slicer + + --python-script + python file name with full path
ex:
/Applications/Slicer.app/Contents/MacOS/Slicer --python-script /Users/michaeltellis/SlicerData/3DVisualizationDataset/DICOM_Loader.py
'''
dirPath = "/Users/michaeltellis/SlicerData/3DVisualizationDataset"

#dicomDataDir is the directory with DICOM files. 

dirName = "dataset1_Thorax_Abdomen"
dicomDataDir = os.path.join(dirPath, dirName)
# dicomDatabaseDir is the full path to the directory where your DICOM database is. Find where it is by going into 3D slicer --> Add DICOM data --> DICOM database settings
dicomDatabaseDir = "/Users/michaeltellis/Documents/SlicerDICOMDatabase/ctkDICOM.sql"



#This loads your DICOM data onto your DICOM database in 3D slicer
slicer.dicomDatabase.openDatabase(dicomDatabaseDir, "SLICER")
print(slicer.dicomDatabase.isOpen)
DICOMLib.importDicom(dicomDataDir, slicer.dicomDatabase)

#This loads every series UID into the database
patientUIDs = slicer.dicomDatabase.patients()
for patientUID in patientUIDs:
    studyUIDs = slicer.dicomDatabase.studiesForPatient(patientUID)
    for studyUID in studyUIDs:
        seriesUIDs = slicer.dicomDatabase.seriesForStudy(studyUID)
        for seriesUID in seriesUIDs:
            print(f"Loading series: {seriesUID}")
            success = DICOMLib.loadSeriesByUID([seriesUID])
            if not success:
                print(f"Failed to load series: {seriesUID}")
print("DICOM loading complete.")

# Get the loaded volume node (e.g., first scalar volume in the scene). Need to hange to more specific name, works for 1 volume for now
volumeNodes = slicer.util.getNodesByClass("vtkMRMLScalarVolumeNode")
outputDir = "/Users/michaeltellis/SlicerData/AutomaticNiiDataOutput"
if not os.path.exists(outputDir):
    os.mkdir(outputDir)
for node in volumeNodes:
    print(f"{node.GetName()} - {node.GetClassName()}")

    fileName = node.GetName() + ".nii.gz"
    outputFile = os.path.join(outputDir, fileName)

    if slicer.util.saveNode(node, outputFile):
        print("exported to: " + outputFile)
    else: 
        print("export failed")
    #Below is total segmentator
    segmentationInputFile = outputFile
    segmentationOutputDir = "/Users/michaeltellis/SlicerData/AutomaticNiiDataOutput/Segmentations"
    if not os.path.exists(segmentationOutputDir):
        os.mkdir(segmentationOutputDir)
    #subprocess.run(["totalsegmentator", "-i", segmentationInputFile, "-o", segmentationOutputDir,"--task", "total", "--fast"])
    #totalsegScript = "/Users/michaeltellis/3DSlicerScripts/run_totalseg.sh"
    #subprocess.run([totalsegScript,segmentationInputFile,segmentationOutputDir], check=True)




