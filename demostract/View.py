import csv
import cv2
import os
import time
import numpy as np
from datetime import timedelta

from django.shortcuts import render
from django.views import View

from demostract.Util.FunctionForSegmentation import Segmentation


class Index(View):
    def get(self,request):
        return render(request, 'easyPcc/flow_one_step.html')
    def post(self,request):
        pass

class UpdaLoad(View):
    def get(self, request):
        pass
    def post(self,request):
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        uploadFile = request.FILES.get('myfile', '1')
        print(uploadFile.name)
        path1 = os.path.join(BASE_DIR, 'demostract', 'media', uploadFile.name)
        f = open(path1, 'wb')
        for chunk in uploadFile.chunks():
            f.write(chunk)
        f.close()
        return render(request, 'easyPcc/flow_two_step.html', {"path1": path1})

class UpdaLoad2(View):
    def get(self, request):
        pass
    def post(self,request):
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        path1 = request.POST.get("path1")
        uploadFile = request.FILES.get('myfile', '1')
        print(uploadFile.name)
        path2 = os.path.join(BASE_DIR, 'demostract', 'media', uploadFile.name)
        f = open(path2, 'wb')
        for chunk in uploadFile.chunks():
            f.write(chunk)
        f.close()
        return render(request, 'easyPcc/flow_three_step.html', {"path1": path1,"path2": path2})

class LearningType(View):

    def get(self, request):
        pass
    def post(self,request):
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        learningType  = request.POST.get("learningType")
        path1 = request.POST.get("path1")
        path2 = request.POST.get("path2")

        f = open(path1, "r", newline='')
        TrainData = list(csv.reader(f))
        f.close()
        # TrainData.remove(['Class', 'Image', 'x', 'y', 'B', 'G', 'R', 'H', 'S', 'V', 'L', 'a', 'b'])
        # TrainData = np.asarray(TrainData)
        # classes = TrainData[:, 0]

        f2 = open(path2, "r", newline='')
        f2.close()

        # Initialize the list
        ListImageWrongSize = []

        fusion = 'N'
        mask = 'N'
        reconstructedimage = 'N'
        info = 'N'
        NFMask = 'N'
        BiggestBlob = 'N'
        # Call the function
        start_time = time.monotonic()

        ListImageWrongSize, ListRunningTimes, ListTestDataTimes, ListApplyModelTimes, ListSaveOutputTimes = Segmentation(
            os.path.join(BASE_DIR, 'demostract', 'media'), self.ListtrainingData, self.listPictureNames, self.comboBox_model.currentText(),
            self.spinbox_noiseReduction.value(), self.classes, self.classesNamesList, self.ROI, self.ListAreaNames,
            fusion, mask, reconstructedimage, info, NFMask, BiggestBlob, self.ListClassesForSurface, self.RefImg)

        end_time = time.monotonic()
        time_all = timedelta(seconds=end_time - start_time)

        # Calculate the mean time of each step
        MeanRunningTime = np.mean(ListRunningTimes)
        MeanRunningTimeTestData = np.mean(ListTestDataTimes)
        MeanRunningTimeModel = np.mean(ListApplyModelTimes)
        MeanRunningTimeOutput = np.mean(ListSaveOutputTimes)

        ReferencePicture = cv2.imread(self.RefImg)
        sizefirstImage = np.shape(ReferencePicture)

        sizeROI = sizefirstImage

        report = ('Activity report: ' +
                  '\n \n Working directory: ' + str(self.WorkingDirectory) +
                  '\n \n Training data: ' + str(self.ListtrainingData) +
                  '\n \n Number of classes: ' + str(self.classes) +
                  '\n \n Classes name: ' + str(self.classesNamesList) +
                  '\n \n Fusion of classes: ' + str(fusion) +
                  '\n \n Classe(s) of interest: ' + str(self.ListClassesForSurface) +
                  '\n \n Number of pictures tested: ' + str(len(self.listPictureNames)) +
                  '\n \n Size of the pictures: ' + str(sizefirstImage) +
                  '\n \n Model: ' + str(self.comboBox_model.currentText()) +
                  '\n \n Number of regions of interest:' + str(len(self.ListAreaNames)) +
                  '\n \n Regions of interest coordinates: ' + str(self.ROI) +
                  '\n \n Region names: ' + str(self.ListAreaNames) +
                  '\n \n Size of the regions of interest: ' + str(sizeROI) +
                  '\n \n Noise reduction: ' + str(self.spinbox_noiseReduction.value()) +
                  '\n \n Mask saved: ' + str(mask) +
                  '\n \n Reconstructed image saved: ' + str(reconstructedimage) +
                  '\n \n Information file saved: ' + str(info) +
                  '\n \n Only keep the biggest region: ' + str(BiggestBlob) +
                  '\n \n Reference picture used for choosing the region of interest: ' + str(self.RefImg) +
                  '\n \n Total Running time: ' + str(time_all) +
                  '\n \n Mean running time for each pictures: ' + str(MeanRunningTime) + 'sec' +
                  '\n \n Mean time to create the test data: ' + str(MeanRunningTimeTestData) + 'sec' +
                  '\n \n Mean time to apply the model: ' + str(MeanRunningTimeModel) + 'sec' +
                  '\n \n Mean time to save the outputs: ' + str(MeanRunningTimeOutput) + 'sec' +
                  '\n \n Pictures which have not been processed because of their size: ' + str(ListImageWrongSize) +
                  '\n \n Pictures List: ' + str(self.listPictureNames))

        report = np.array([report])
        np.savetxt(self.WorkingDirectory + '/Activity_Report.txt', report, delimiter="\n", comments='', fmt='%s')

        return render(request, 'easyPcc/flow_three_step.html')

