import os

from django.shortcuts import render
from django.views import View


class Index(View):
    def get(self,request):
        return render(request, 'easyPcc/flow_one_step')
    def post(self,request):
        pass

class UpdaLoad(View):
    def get(self, request):
        pass
    def post(self,request):
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        uploadFile = request.FILES.get('myfile', '1')
        print(uploadFile.name)
        f = open(os.path.join(BASE_DIR, 'media', 'image', uploadFile.name), 'wb')
        for chunk in uploadFile.chunks():
            f.write(chunk)
        f.close()
        return render(request, 'easyPcc/flow_two_step')

