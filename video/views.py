from django.http import HttpResponse
from django.shortcuts import render ,redirect
from .models import *
from django.core.mail import EmailMessage
from django.views.decorators import gzip
from django.http import StreamingHttpResponse
import cv2
import threading
import datetime
from django.utils import timezone
from .forms import TimeForm
from .models import CountModel
from django.core.exceptions import ObjectDoesNotExist
Time=0
@gzip.gzip_page
def Home(request):

    try:
        cam = VideoCamera()
        return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
    except:
        pass
    return render(request, 'home.html')


def home_view(request):
    global Time
    context ={}
    form = TimeForm()
    context['form']= form
    if request.POST:
        Time = request.POST['time']
       
        try:
            CountControl=CountModel.objects.get(id=1)
        except ObjectDoesNotExist:
            new_count=CountModel(id=1)
            new_count.save()
        return redirect("Home")
    return render(request, "home.html", context)

#to capture video class
class VideoCamera(object):

    def __init__(self):
        self.video = cv2.VideoCapture(0)
        (self.grabbed, self.frame) = self.video.read()
        self.T1=threading.Thread(target=self.update, args=())
        self.T1.start()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        image = self.frame
        _, jpeg = cv2.imencode('.jpg', image)    
        return jpeg.tobytes()

    def update(self):
        global counter
        fshape = self.frame.shape
        fheight = fshape[0]
        fwidth = fshape[1]
           
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        counter=CountModel.objects.get(id=1)
        video_name='output'+str(counter.count)+'.mp4'
        out = cv2.VideoWriter(video_name,fourcc, 20.0, (fwidth,fheight))
        counter.count=counter.count+1
        counter.save()
        time_count=0
        while True:
            now =  datetime.datetime.now()
            if time_count==0:
                first_time=(now.minute*60 )+now.second
                time_count=time_count+1
            
            now_time=(now.minute*60 )+now.second

            if (now_time-first_time) == int(Time)-1:
                self.__del__()
                break
            
            (self.grabbed, self.frame) = self.video.read()

            out.write(self.frame)

           

def gen(camera):
    time_count=0
    while True:
        now =  datetime.datetime.now()
        if time_count==0:
                temp_time=(now.minute*60 )+now.second
                time_count=time_count+1
        now_time=(now.minute*60 )+now.second

        if (now_time-temp_time) ==int(Time)-1:            
            break

        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

        

