from django.shortcuts import render,redirect
from django.http import HttpResponse

from .models import*

# Create your views here.

def login(req):
    return render(req,'login.html')
def reg(req):
    if req.method == 'GET':
        return render(req,'reg.html')
    else:

        fname = req.POST.get('first_name')
        lname = req.POST.get('last_name')
        email = req.POST.get('email')
        username = req.POST.get('username')
        pw = req.POST.get('password')
        cpw = req.POST.get('confirm_password')

        reg_obj = Registration()

        reg_obj.first_name = fname
        reg_obj.last_name = lname
        reg_obj.email = email
        reg_obj.uname = username
        reg_obj.password = pw

        reg_obj.save()
        return redirect('signin')


    # return HttpResponse(req.POST.get('first_name'))