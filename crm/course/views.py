from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import*
# Create your views here.

def course_content(req):
    pass
    # return render(req,'course_content.html')
def category(req):
    if req.method == 'GET':

        #select * from table_name

        cat_data = Category.objects.order_by('-id')
        print("salman")
        data = {"all_data":cat_data}

        return render(req,'course_category.html',data)
    else:
        category_name = req.POST.get('category_name')
        description = req.POST.get('description')
        status = req.POST.get('status')
        sort_order = req.POST.get('sort_order')

        cat = Category()
        cat.category_name =category_name
        cat.description = description
        if status == 'active':
            cat.status = True
        else:
            cat.status = False
        cat.sort_order = sort_order

        if(Category.objects.filter(category_name=category_name).exists()):
            return redirect('course_category')
        elif(Category.objects.filter(sort_order=sort_order).exists()):
            return redirect('course_category')
        else:

            cat.save()

        return redirect('course_category')
