from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from .models import*
from openpyxl import load_workbook #excel ta k load
from django.contrib import messages
from openpyxl import Workbook #excel banano
from openpyxl.styles import Font
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

def excel_upload(req, excel_file):
    try:
        workbook = load_workbook(excel_file)
        sheet = workbook.active

        # ডেটাবেস থেকে আগে থেকেই থাকা category_name এবং sort_order নিয়ে আসা হচ্ছে
        #select column_name from table_name
        existing_names = set(Category.objects.values_list('category_name', flat=True))
        existing_sort_orders = set(Category.objects.values_list('sort_order', flat=True))

        categories = []
        excel_names = set()
        excel_sort_orders = set()

        # ২ নম্বর রো থেকে ডেটা পড়া শুরু
        for row in sheet.iter_rows(min_row=2, values_only=True):
            category_name = row[0]
            description = row[1]
            status = row[2]
            sort_order = row[3]

            # নাম বা সর্ট অর্ডার ফাঁকা থাকলে স্কিপ করবে
            if not category_name or sort_order is None:
                continue

            # ডেটা ক্লিনিং (আশেপাশের স্পেস মুছে ফেলা)
            category_name = str(category_name).strip()
            description = str(description).strip() if description else ""
            sort_order = str(sort_order).strip()

            # স্ট্যাটাস (True/False) হ্যান্ডেল করা
            if isinstance(status, bool):
                final_status = status
            else:
                # এক্সেল থেকে টেক্সট হিসেবে আসলে চেক করবে
                final_status = str(status).strip().lower() in ['true', 'active', '1', 'yes']

            # ======================================
            # আপনার রিকোয়ারমেন্ট: ডুপ্লিকেট চেকিং
            # ======================================
            # ডেটাবেসে যদি আগে থেকেই এই নাম বা সর্ট অর্ডার থাকে, তাহলে স্কিপ (continue) করবে
            if category_name in existing_names or sort_order in existing_sort_orders:
                continue

            # এক্সেল ফাইলের ভেতরেই যদি ডুপ্লিকেট থাকে (একই ফাইলে দুইবার), তাহলেও স্কিপ করবে
            if category_name in excel_names or sort_order in excel_sort_orders:
                continue

            # ডুপ্লিকেট না হলে নতুন অবজেক্ট লিস্টে যুক্ত করবে
            categories.append(
                Category(
                    category_name=category_name,
                    description=description,
                    status=final_status,
                    sort_order=sort_order
                )
            )

            # এক্সেলের লিস্ট আপডেট করা, যেন ফাইলের ভেতরের ডুপ্লিকেট ধরা যায়
            excel_names.add(category_name)
            excel_sort_orders.add(sort_order)

        # ==========================================
        # Bulk Insert (শুধুমাত্র নতুন ডেটাগুলো সেভ হবে)
        # ==========================================
        if categories:
            Category.objects.bulk_create(categories)
            messages.success(req, f"{len(categories)} new categories uploaded successfully.")
        else:
            messages.warning(req, "No new categories found to insert (All were duplicates).")

    except Exception as e:
        messages.error(req, f"Excel upload failed: {str(e)}")

from django.core.paginator import Paginator

def course_details(req):
    if req.method=="POST":
        cat_id = req.POST.get('category')
        course_title = req.POST.get('course_title')
        course_image = req.FILES.get('course_image')
        course_description = req.POST.get('course_description')
        actual_price = req.POST.get('actual_price')
        discount = req.POST.get('discount')
        prerequisite = req.POST.get('prerequisite')
        duration = req.POST.get('duration')
        status = req.POST.get('status')
        course_details_obj = CourseDetails()
        #select * from category where id = cat_id
        cat_id_fk = Category.objects.get(id=cat_id)
        course_details_obj.category_id_fk = cat_id_fk
        course_details_obj.course_title = course_title
        course_details_obj.course_image = course_image
        course_details_obj.course_description = course_description
        course_details_obj.actual_price = actual_price
        course_details_obj.discount = discount
        course_details_obj.course_prerequisite = prerequisite
        course_details_obj.duration = duration
        course_details_obj.status = status
        course_details_obj.save()
        return redirect('course_details')
    else:
        #select id, category_name from category
        categories = Category.objects.values('id', 'category_name')
        all_data_course = CourseDetails.objects.select_related('category_id_fk').all()

        for i in all_data_course:
            i.disounted_price = i.actual_price - (
            i.actual_price * i.discount / 100)
        all_data = {'cat_data':categories,'course_data':all_data_course}
        return render(req,'course_details.html',all_data)

def category(req):
    if req.method == 'GET':

        #select * from table_name

        cat_data = Category.objects.order_by('-id')
        print("salman")
        limit = 3
        paginator = Paginator(cat_data, limit) #2 = num of rows per page
        page_number = req.GET.get('page')
        page_obj = paginator.get_page(page_number)
        data = {"all_data":page_obj}

        return render(req,'course_category.html',data)
    else:
        if req.POST.get('export_data') == 'excel':
            wb = Workbook()
            ws = wb.active
            ws.title = "Category Data"

            # হেডার
            headers = ["Category Name", "Description", "Status", "Sort Order"]
            ws.append(headers)

            for col_num in range(1, len(headers) + 1):
                cell = ws.cell(row=1, column=col_num)
                cell.font = Font(bold=True)

            # ডেটাবেস থেকে ডেটা এনে বসানো
            categories = Category.objects.order_by('-id')
            for cat in categories:
                #conditional comprehension
                status_text = "Active" if cat.status else "Inactive"
                ws.append([
                    cat.category_name,
                    cat.description,
                    status_text,
                    cat.sort_order
                ])

            response = HttpResponse(
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            response['Content-Disposition'] = 'attachment; filename="Category_Export.xlsx"'
            wb.save(response)
            
            return response # পেজ রিলোড না হয়ে সরাসরি ফাইল ডাউনলোড হবে

        excel_file = req.FILES.get('excel_file')

        if excel_file:
            excel_upload(req, excel_file)

            # excel_upload(req, excel_file)

            return redirect('course_category')
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
