from django.shortcuts import render
from uploadPhotoTest.models import car

# Create your views here.
def test2(request, pk):
    car_instance = car.objects.get(pk=pk)
    return render(request, "uploadPhotoTest/index.html", {'car_instance': car_instance})
