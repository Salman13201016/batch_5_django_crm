from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from .models import*
# Create your views here.

def course_content(req):
    pass
    # return render(req,'course_content.html')

def course_cat_delete(req,cat_id):
    delete_spec_data = get_object_or_404(Category,id=cat_id)
    delete_spec_data.delete()
    return redirect('course_category')
def course_edit(req,cat_id):
    #select * from table_name where id = 1
    if req.method == "POST":
        cat_specific = get_object_or_404(Category,id=cat_id)
        category_name = req.POST.get('category_name')
        description = req.POST.get('description')
        status = req.POST.get('status')
        sort_order = req.POST.get('sort_order')

        cat_specific.category_name = category_name
        cat_specific.description=description
        if status == 'active':
            cat_specific.status = True
        else:
            cat_specific.status = False
        cat_specific.sort_order = sort_order
        cat_specific.save()
        return redirect('course_category')
    else:
        cat_specific_data = get_object_or_404(Category,id=cat_id)
        data = {"cat_data":cat_specific_data}
        return render(req,'category_edit.html',data)


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
