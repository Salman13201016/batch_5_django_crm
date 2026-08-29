
from django.http import HttpResponse
from django.shortcuts import render
def demo(req):
    print("hello wolrd")
    all_header = ""
    for k, v in req.headers.items():
        all_header = all_header + f"{k}: {v}<br>"

    return HttpResponse(f"this is demo function {all_header}")

def demo2(req):

    return HttpResponse("this is demo 2")

def registration(req):
    return render(req,'reg.html')
