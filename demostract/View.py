import csv
import cv2
import os
import time
import numpy as np
from datetime import timedelta

from django.http import HttpResponse
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
        uploadFile = request.FILES.get('myfile')
        if uploadFile == None or uploadFile == "":
            return render(request, 'easyPcc/flow_one_step.html', {"msg": "文件必须上传"})
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
        uploadFile = request.FILES.get('myfile')
        if uploadFile == None or uploadFile == "":
            return render(request, 'easyPcc/flow_two_step.html', {"msg": "文件必须上传"})
        if path1 == None or path1 == "":
            return render(request, 'easyPcc/flow_one_step.html', {"msg": "第一步上传文件丢失，返回第一步。"})

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
        RIO = request.POST.get("RIO")
        reduction = request.POST.get("reduction","100")
        path1 = request.POST.get("path1")
        path2 = request.POST.get("path2")

        if path2 == None or path2 == "":
            return render(request, 'easyPcc/flow_two_step.html', {"msg": "第二步上传文件丢失，返回第二步。"})
        if path1 == None or path1 == "":
            return render(request, 'easyPcc/flow_one_step.html', {"msg": "第一步上传文件丢失，返回第一步。"})

        fusion = 'N'
        mask = 'Y'
        reconstructedimage = 'Y'
        info = 'Y'
        NFMask = 'Y'
        BiggestBlob = 'Y'

        trandatafilelist = list()
        trandatafilelist.append(path1)

        tragetfilelist = list()
        tragetfilelist.append(path2)

        learningType = "Classification and Regression Tree (Sklearn)"

        reduction = int(reduction)

        start_time = time.monotonic()

        numberOfClasses = int(2)

        classNameList = ['Class_1', 'Class_2']

        ROI = 'Whole pictures'

        ListAreaNames = list()

        chosenArea = ["Class_1"]


        RefImg = path2


        outfile2 = os.path.join(BASE_DIR, 'demostract', 'media') + '/InformationFile.csv'

        try:
            ListImageWrongSize, ListRunningTimes, ListTestDataTimes, ListApplyModelTimes, ListSaveOutputTimes = Segmentation(
                os.path.join(BASE_DIR, 'demostract', 'media'), trandatafilelist, tragetfilelist, learningType,
                reduction, numberOfClasses, classNameList, ROI, ListAreaNames,
                fusion, mask, reconstructedimage, info, NFMask, BiggestBlob, chosenArea, RefImg)
        except:
            return render(request, 'easyPcc/flow_one_step.html', {"msg": "处理失败，检查上传文件。"})

        end_time = time.monotonic()
        time_all = timedelta(seconds=end_time - start_time)

        # Calculate the mean time of each step
        MeanRunningTime = np.mean(ListRunningTimes)
        MeanRunningTimeTestData = np.mean(ListTestDataTimes)
        MeanRunningTimeModel = np.mean(ListApplyModelTimes)
        MeanRunningTimeOutput = np.mean(ListSaveOutputTimes)

        ReferencePicture = cv2.imread(RefImg)
        sizefirstImage = np.shape(ReferencePicture)

        sizeROI = sizefirstImage

        report = ('Activity report: ' +
                  '\n \n Working directory: ' + str(os.path.join(BASE_DIR, 'demostract', 'media')) +
                  '\n \n Training data: ' + str(trandatafilelist) +
                  '\n \n Number of classes: ' + str(tragetfilelist) +
                  '\n \n Classes name: ' + str(learningType) +
                  '\n \n Fusion of classes: ' + str(fusion) +
                  '\n \n Classe(s) of interest: ' + str(mask) +
                  '\n \n Number of pictures tested: ' + str(len(reconstructedimage)) +
                  '\n \n Size of the pictures: ' + str(sizefirstImage) +
                  '\n \n Model: ' + str() +
                #  '\n \n Number of regions of interest:' + str(len(ListAreaNames)) +
                  '\n \n Regions of interest coordinates: ' + str(ROI) +
                  '\n \n Region names: ' + str(ListAreaNames) +
                  '\n \n Size of the regions of interest: ' + str(sizeROI) +
                  '\n \n Noise reduction: ' + str(reduction) +
                  '\n \n Mask saved: ' + str(mask) +
                  '\n \n Reconstructed image saved: ' + str(reconstructedimage) +
                  '\n \n Information file saved: ' + str(info) +
                  '\n \n Only keep the biggest region: ' + str(BiggestBlob) +
                  '\n \n Reference picture used for choosing the region of interest: ' + str(RefImg) +
                  '\n \n Total Running time: ' + str(time_all) +
                  '\n \n Mean running time for each pictures: ' + str(MeanRunningTime) + 'sec' +
                  '\n \n Mean time to create the test data: ' + str(MeanRunningTimeTestData) + 'sec' +
                  '\n \n Mean time to apply the model: ' + str(MeanRunningTimeModel) + 'sec' +
                  '\n \n Mean time to save the outputs: ' + str(MeanRunningTimeOutput) + 'sec' +
                  '\n \n Pictures which have not been processed because of their size: ' + str(ListImageWrongSize) +
                  '\n \n Pictures List: ' + str(tragetfilelist))

        report = np.array([report])

        outPath = os.path.join(BASE_DIR, 'demostract', 'media') + '/Activity_Report.txt'


        np.savetxt(outPath, report, delimiter="\n", comments='', fmt='%s')

        return render(request, 'easyPcc/result.html',{"outPath":outPath,"outfile2":outfile2})

class Downloadfiel(View):

    def get(self,request):
        outPath = request.GET.get("filenamePath")

        str(outPath).split(".")
        file = open(outPath, 'rb')
        response = HttpResponse(file)
        response['Content-Type'] = 'application/octet-stream'  # 设置头信息，告诉浏览器这是个文件
        response['Content-Disposition'] = 'attachment;filename="{}"'.format(str(outPath).split("/")[len(str(outPath).split("/"))-1])
        return response
