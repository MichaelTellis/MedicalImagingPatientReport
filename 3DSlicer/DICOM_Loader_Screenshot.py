import os
import subprocess
import slicer
import DICOMLib
import slicer.util
import ScreenCapture

'''
usage instructions: to use this script in terminal
full Path to 3D slicer + + --python-script + python file name with full path
ex:
/Applications/Slicer.app/Contents/MacOS/Slicer --python-script /Users/michaelmascari/Desktop/DICOM_Loader.py
'''
dirPath = "/Users/michaelmascari/Desktop/DICOMDATA"

#dicomDataDir is the directory with DICOM files. 

dirName = "dataset1_Thorax_Abdomen"
dicomDataDir = os.path.join(dirPath, dirName)
# dicomDatabaseDir is the full path to the directory where your DICOM database is. Find where it is by going into 3D slicer --> Add DICOM data --> DICOM database settings
dicomDatabaseDir = "/Users/michaelmascari/Documents/SlicerDICOMDatabase/ctkDICOM.sql"



#This loads your DICOM data onto your DICOM database in 3D slicer
slicer.dicomDatabase.openDatabase(dicomDatabaseDir, "SLICER")
print(slicer.dicomDatabase.isOpen)
slicer.mrmlScene.Clear(0)  # Resets the Slicer scene to empty without asking the user
DICOMLib.importDicom(dicomDataDir, slicer.dicomDatabase)


# Get the loaded volume node (e.g., first scalar volume in the scene)
outputDir = "/Users/michaelmascari/Desktop/dicomout"
if not os.path.exists(outputDir):
    os.mkdir(outputDir)

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
volumeNodes = slicer.util.getNodesByClass("vtkMRMLScalarVolumeNode")

for node in volumeNodes:

    print(f"{node.GetName()} - {node.GetClassName()}")

    fileName = node.GetName() + ".nii.gz"
    outputFile = os.path.join(outputDir, fileName)

    if slicer.util.saveNode(node, outputFile):
        print("exported to: " + outputFile)
    else: 
        print("export failed")
slicer.mrmlScene.Clear(0)
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
            screenCaptureLogic = ScreenCapture.ScreenCaptureLogic()


            # Define output path
            outputImagePath = "/Users/michaelmascari/Desktop/dicomout"
            imgName = seriesUID + ".png"
            outputImagePath = os.path.join(outputImagePath, imgName)
    
            # Capture and save image of the 3D view
            screenCaptureLogic.showViewControllers(False)
            screenCaptureLogic.captureImageFromView(None, outputImagePath)
            screenCaptureLogic.showViewControllers(True)
            print(f"3D view screenshot saved to: {outputImagePath}")
            slicer.mrmlScene.Clear(0)
print("DICOM loading complete.")
# === Insert segmentation loading here ===
'''
import glob
import time

segmentationDir = "/Users/michaelmascari/Desktop/segmentations"
segmentationExtensions = ['*.seg.nrrd', '*.nrrd', '*.vtk', '*.stl', '*.obj']

for ext in segmentationExtensions:
    segFiles = glob.glob(os.path.join(segmentationDir, ext))
    for segFile in segFiles:
        print(f"Loading segmentation: {segFile}")
        loadedNode = slicer.util.loadNodeFromFile(segFile, 'SegmentationFile')
        if not loadedNode:
            print(f"Failed to load segmentation: {segFile}")
        else:
            print(f"Successfully loaded segmentation: {loadedNode.GetName()}")
'''
# === Now continue with your volume export loop ===



    # Screenshot capture code here
    # Create a ScreenCapture logic instance
    
   








