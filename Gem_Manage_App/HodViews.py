import random
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage #To upload Profile Picture
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json
import xlwt

from Gem_Manage_App.models import CustomUser,  Sample, Sender, User, SingleSample, Task, SystemSetting,\
    Subjects, SessionYearModel,Attendance, AttendanceReport, UserGroup, MemberType, PrintSetting,UserGroupStatus, Preinstall, Members
from .forms import AddStudentForm, EditStudentForm


def admin_home(request):

    count1=SingleSample.objects.filter(SingleSample_status=("收样")).count()
    count2=SingleSample.objects.filter(SingleSample_status=("检测中")).count()
    count3=SingleSample.objects.filter(SingleSample_status=("检测完成")).count()
    count4=SingleSample.objects.filter(SingleSample_status=("审核通过")).count()
    count5=SingleSample.objects.filter(SingleSample_status=("退回")).count()
    count6=SingleSample.objects.filter(SingleSample_status=("完成")).count()
    context={
        "count1":count1,
        "count2":count2,
        "count3":count3,
        "count4":count4,
        "count5":count5,
        "count6":count6,
    }
    return render(request, "hod_template/home_content.html", context)


def add_staff(request):
    return render(request, "hod_template/add_staff_template.html")


def add_staff_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method ")
        return redirect('add_staff')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        address = request.POST.get('address')

        try:
            user = CustomUser.objects.creates_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name, user_type=2)
            user.staffs.address = address
            user.save()
            messages.success(request, "Staff Added Successfully!")
            return redirect('add_staff')
        except:
            messages.error(request, "Failed to Add Staff!")
            return redirect('add_staff')




def add_receipt(request):
    samples = Sample.objects.all()
    context = {
        "samples": samples
    }
    return render(request, "hod_template/add_receipt_template.html",context)


def add_receipt_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('add_receipt')
    else:
        identification_id = request.POST.get('identification_id')
        receipt_tel = request.POST.get('receipt_tel')
        sample_status = request.POST.get('sample_status')
        sender_company = request.POST.get('sender_company')
        sample_sender = request.POST.get('sample_sender')
        sender_tel = request.POST.get('sender_tel')
        postal_code = request.POST.get('postal_code')
        basket_id = request.POST.get('basket_id')
        finish_date = request.POST.get('finish_date')
        identification_cost = request.POST.get('identification_cost')
        sample_collectr_name=request.POST.get('sample_collectr')
        sample_collectr = User.objects.get(user_name=sample_collectr_name)
        # try:
        sender1=Sender(sender_company=sender_company,sample_sender=sample_sender,postal_code=postal_code,sender_tel=sender_tel)
        sender1.save()
        receipt_model =Sample(identification_id=identification_id,receipt_tel=receipt_tel,sample_status=sample_status,basket_id=basket_id,sender=sender1,finish_date=finish_date,sample_collectr=sample_collectr,identification_cost=identification_cost)
        receipt_model.save()
        messages.success(request, "Receipt Added Successfully!")
        return redirect('add_receipt')
        # except:
        #     messages.error(request, "Failed to Add Receipt!")
        #     return redirect('add_receipt')


def manage_receipt(request):
    samples = Sample.objects.all()
    context = {
        "samples": samples
    }
    return render(request, 'hod_template/manage_receipt_template.html', context)


def edit_receipt(request, receipt_id):
    sample = Sample.objects.get(identification_id=receipt_id)
    context = {
        "sample": sample,
        "receipt_id": receipt_id
    }
    return render(request, 'hod_template/edit_receipt_template.html', context)


def edit_receipt_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
    else:
        identification_id = request.POST.get('identification_id')
        id = request.POST.get('id')
        receipt_tel = request.POST.get('receipt_tel')
        sample_status = request.POST.get('sample_status')
        sender_company = request.POST.get('sender_company')
        sample_sender = request.POST.get('sample_sender')
        sender_tel = request.POST.get('sender_tel')
        postal_code = request.POST.get('postal_code')
        basket_id = request.POST.get('basket_id')
        finish_date = request.POST.get('finish_date')
        identification_cost = request.POST.get('identification_cost')
        sample_collectr_name = request.POST.get('sample_collectr')
        sample_collectr = User.objects.get(user_name=sample_collectr_name)
        try:
            sender1=Sender.objects.get(id=id)
            sender1.sender_company=sender_company
            sender1.sample_sender=sample_sender
            sender1.postal_code=postal_code
            sender1.sender_tel=sender_tel
            sender1.save()
            receipt_model = Sample.objects.get(identification_id=identification_id)
            receipt_model.receipt_tel=receipt_tel
            receipt_model.sample_status=sample_status
            receipt_model.basket_id=basket_id
            receipt_model.finish_date=finish_date
            receipt_model.identification_cost=identification_cost
            receipt_model.sample_collectr=sample_collectr
            receipt_model.save()
            messages.success(request, "Receipt Added Successfully!")
            return redirect('/edit_receipt/' + identification_id)
        except:
            messages.error(request, "Failed to Add Receipt!")
            return redirect('/edit_receipt/'+identification_id)


def delete_receipt(request, receipt_id):
    sample = Sample.objects.get(identification_id=receipt_id)
    try:
        sample.delete()
        messages.success(request, "Receipt Deleted Successfully.")
        return redirect('manage_receipt')
    except:
        messages.error(request, "Failed to Delete Receipt.")
        return redirect('manage_receipt')


def add_task(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('add_task')
    else:
        identification_id = request.POST.get('identification_id_input')
        sample = Sample.objects.get(identification_id=identification_id)
        single_sample_name = request.POST.get('single_sample_name_input')
        single_sample_num = int(request.POST.get('single_sample_num_input'))
        sample_type = request.POST.get('sample_type_input')
        require = request.POST.get('require_input')
        status = request.POST.get('identification_id_input')
        checkcode = ''
        for i in range(4):  # 循环4次输出四个字符
            index = random.randrange(0, 4)
            if index != i and index + 1 != i:
                checkcode += chr(random.randint(97, 122))  # 小写字母ASCII值为：97~122
            elif index + 1 == i:
                checkcode += chr(random.randint(65, 90))  # 大写字母ASCII值为：65~90
            else:
                checkcode += str(random.randint(0, 9))  # 随机输出数字0~9中的1个
        try:
            thepost = SingleSample.objects.filter(identification_id=sample).count()
        except SingleSample.DoesNotExist:
            thepost = 0
        for i in range(single_sample_num):
            singlesample = SingleSample(gemstone_id=(sample.identification_id + '000' + str(i+thepost)),
                                        identification_id=sample, single_sample_name=single_sample_name,verification_code=checkcode,sample_type=sample_type,require=require)
            singlesample.save()
            task_model = Task(gemstone_id=singlesample, identification_id=sample)
            task_model.save()
        return redirect('add_task')


def manage_sample(request):
    tasks = Task.objects.all()

    context = {
        "tasks": tasks
    }
    return render(request, 'hod_template/manage_sample_template.html', context)

def add_remarks(request,remarks_id):
    SingleSample_temp=SingleSample.objects.get(gemstone_id=remarks_id)
    task = Task.objects.get(gemstone_id=SingleSample_temp)
    context = {
        "task": task,
        "remarks_id": remarks_id,
    }
    return render(request, 'hod_template/add_remarks_template.html', context)


def add_remarks_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
    else:
        id=request.POST.get('gemstone_id')
        print(id)
        image_input = request.POST.get('image_input')
        remarks_input = request.POST.get('remarks_input')
        singlesample_model=SingleSample.objects.get(gemstone_id=id)
        singlesample_model.image=image_input
        singlesample_model.remarks=remarks_input
        singlesample_model.save()
        messages.success(request, "Receipt Added Successfully!")
        return redirect('/add_remarks/'+id)

def edit_sample(request,sample_id):
    singlesample = SingleSample.objects.get(gemstone_id=sample_id)
    context = {
        "singlesample": singlesample,
        "receipt_id": sample_id
    }
    return render(request, 'hod_template/edit_sample_template.html', context)


def edit_sample_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
    else:
        gemstone_id = request.POST.get('gemstone_id')
        gemstone_appearance = request.POST.get('gemstone_appearance')
        gemstone_mass = request.POST.get('gemstone_mass')
        gemstone_density = request.POST.get('gemstone_density')
        refraction_index = request.POST.get('refraction_index')
        light_characteristc = request.POST.get('light_characteristc')
        observation_result = request.POST.get('observation_result')
        heavy_metal = request.POST.get('heavy_metal')
        infrared = request.POST.get('infrared')
        cut = request.POST.get('cut')
        color_level = request.POST.get('color_level')
        Cleanliness_level = request.POST.get('Cleanliness_level')
        diamond_cut = request.POST.get('diamond_cut')
        others = request.POST.get('others')
        try:
            singlesample_model=SingleSample.objects.get(gemstone_id=gemstone_id)
            singlesample_model.gemstone_appearance=gemstone_appearance
            singlesample_model.gemstone_mass=gemstone_mass
            singlesample_model.gemstone_density=gemstone_density
            singlesample_model.refraction_index=refraction_index
            singlesample_model.light_characteristc=light_characteristc
            singlesample_model.observation_result=observation_result
            singlesample_model.heavy_metal=heavy_metal
            singlesample_model.infrared=infrared
            singlesample_model.cut=cut
            singlesample_model.color_level=color_level
            singlesample_model.Cleanliness_level=Cleanliness_level
            singlesample_model.diamond_cut=diamond_cut
            singlesample_model.others=others
            singlesample_model.save()
            messages.success(request, "Receipt Added Successfully!")
            return redirect('/edit_sample/' + gemstone_id)
        except:
            messages.error(request, "Failed to Add Receipt!")
            return redirect('/edit_sample/'+gemstone_id)

def sample_approve(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
    else:
        if '通过审核' in request.POST:
            tasks = Task.objects.all()
            context = {
                "tasks": tasks
            }
            check_box_list = request.POST.getlist('check_box_list')
            for i in range(len(check_box_list)):
                id=check_box_list[i]
                singlesample_model=SingleSample.objects.get(gemstone_id=id)
                singlesample_model.SingleSample_status="审核通过"
                singlesample_model.save()
            return render(request, "hod_template/manage_sample_template.html",context)
        if '未通过审核' in request.POST:
            tasks = Task.objects.all()
            context = {
                "tasks": tasks
            }
            check_box_list = request.POST.getlist('check_box_list')
            for i in range(len(check_box_list)):
                id = check_box_list[i]
                singlesample_model = SingleSample.objects.get(gemstone_id=id)
                singlesample_model.SingleSample_status = "未通过"
                singlesample_model.save()
            return render(request, "hod_template/manage_sample_template.html", context)

def manage_task(request):
    tasks = Task.objects.all()
    identification_staff = User.objects.filter(group=(UserGroup.objects.get(group_name="检测员")))
    context = {
        "identification_staff": identification_staff,
        "tasks": tasks
    }
    return render(request, 'hod_template/manage_task_template.html', context)

def add_identification_staff(request):
    if '任务完成' in request.POST:
        tasks = Task.objects.all()
        context = {
            "tasks": tasks
        }
        check_box_list = request.POST.getlist('check_box_list1')
        for i in range(len(check_box_list)):
            id = check_box_list[i]
            singlesample_model = SingleSample.objects.get(gemstone_id=id)
            singlesample_model.SingleSample_status = "完成"
            singlesample_model.save()
        return render(request, "hod_template/manage_task_template.html", context)
    if '批量分派' in request.POST:
        tasks = Task.objects.all()
        context = {
            "tasks": tasks
        }
        check_box_list = request.POST.getlist('check_box_list1')
        print(check_box_list)
        for i in range(len(check_box_list)):
            id = check_box_list[i]
            singlesample_model = SingleSample.objects.get(gemstone_id=id)
            task_model = Task.objects.get(gemstone_id=singlesample_model)
            identification_staff = request.POST.get('identification_staff')
            user_model = User.objects.get(user_name=identification_staff)
            task_model.identification_staff = user_model
            task_model.save()
        return render(request, "hod_template/manage_task_template.html", context)


def add_certification(request):
    return render(request, "hod_template/add_certification_template.html")


def manage_certification(request):
    certifications = Task.objects.all()
    context = {
        "certifications": certifications
    }
    return render(request, "hod_template/manage_certification_template.html", context)


def fail_certification(request):
    certifications = Task.objects.all()
    context = {
        "certifications": certifications
    }
    check_box_list = request.POST.getlist('check_box_list1')
    print(check_box_list[0])
    for i in range(len(check_box_list)):
        id = check_box_list[i]
        singlesample_model = SingleSample.objects.get(gemstone_id=id)
        singlesample_model.SingleSample_status = "证书作废"
        singlesample_model.save()
    return render(request, "hod_template/manage_certification_template.html", context)


def print_certification(request, cid):
    certifications = Task.objects.get(id=cid)
    context = {
        "certifications": certifications,
        "cid": cid
    }
    return render(request, "hod_template/print_certification_template.html", context)




def show_certification(request, cid):
    certifications = Task.objects.get(id=cid)
    context = {
        "certifications": certifications,
        "cid" : cid
    }
    return render(request, "hod_template/show_certification_template.html", context)



def manage_excel(request):
    tasks = Task.objects.all()
    context = {
        "tasks": tasks
    }
    return render(request, "hod_template/manage_excel_template.html",context)


def add_member(request):
    membertypes=MemberType.objects.all()
    context = {
        "membertypes": membertypes
    }
    return render(request, "hod_template/add_member_template.html",context)


def add_member_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method ")
        return redirect('add_member')
    else:
        id = request.POST.get('id')
        member_name = request.POST.get('member_name')
        telephone = request.POST.get('telephone')
        company_address = request.POST.get('company_address')
        member_type_name=request.POST.get('member_type')# 会员类型
        member_type=MemberType.objects.get(member_type=member_type_name)
        legal_representative=request.POST.get('legal_representative') # 法人代表
        license_number=request.POST.get('license_number') # 执照号
        postal_code=request.POST.get('postal_code') # 邮政编码
        company_name=request.POST.get('company_name') # 公司名
        # try:
        member_model = Members(id=id, member_name = member_name,
        company_address=company_address,
        member_type = member_type,
        telephone = telephone,
        legal_representative = legal_representative,
        license_number=license_number, postal_code = postal_code,
        company_name = company_name)
        member_model.save()
        messages.success(request, "Member Added Successfully!")
        return redirect('add_member')




def manage_member(request, **kwargs):
    members = Members.objects.all()
    context = {
        "members": members,
    }
    return render(request, "hod_template/manage_member_template.html", context)


def edit_member(request, member_id):
    members = Members.objects.get(id=member_id)
    membertypes = MemberType.objects.all()
    context = {
        "members": members,
        "member_id": member_id,
        "membertypes": membertypes,
    }
    return render(request, "hod_template/edit_member_template.html", context)


def edit_member_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('add_member')
    else:
        # members=request.POST.get('members')
        id = request.POST.get('member_id')
        member_name = request.POST.get('member_name')
        telephone = request.POST.get('telephone')
        company_address = request.POST.get('company_address')
        member_type_name = request.POST.get('member_type')  # 会员类型
        print(member_type_name)
        member_type = MemberType.objects.get(member_type=member_type_name)
        legal_representative=request.POST.get('legal_representative') # 法人代表
        license_number=request.POST.get('license_number') # 执照号
        postal_code=request.POST.get('postal_code') # 邮政编码
        company_name=request.POST.get('company_name') # 公司名
        try:
            member_model = Members( id=id, member_name = member_name,
            company_address=company_address,
            member_type = member_type,
            telephone = telephone,
            legal_representative = legal_representative,
            license_number=license_number, postal_code = postal_code,
            company_name = company_name)
            member_model.save()
            messages.success(request, "Member Updated Successfully.")

            return redirect('/edit_member/'+id)

        except:
            messages.error(request, "Failed to Update Member.")
            return redirect('/edit_member/'+id)



def delete_member(request, member_id):
    members = Members.objects.get(id=member_id)
    try:
        members.delete()
        messages.success(request, "Member Deleted Successfully.")
        return redirect('manage_member')
    except:
        messages.error(request, "Failed to Delete Member.")
        return redirect('manage_member')

def search_tel(request):#没写好!!!查询手机号
    telephone = request.POST.get('telephone')
    print(telephone)
    members=Members.objects.all().filter(telephone=telephone)
    context = {
        "members": members
    }
    return render(request, 'manage_member.html',context)
#【系统管理】
def manage_system(request):
    return render(request, 'hod_template/manage_system_template.html')

#【a1】
def a1(request):
    usergroups=UserGroup.objects.all()
    users=User.objects.all()
    context = {
        "usergroups": usergroups,
        "users": users
    }
    return render(request,"hod_template/a1.html",context)
def delete_usergroup(request, usergroup_id):
    usergroup = UserGroup.objects.get(id=usergroup_id)
    try:
        usergroup.delete()
        messages.success(request, "usergroup Deleted Successfully.")
        return redirect('a1')
    except:
        messages.error(request, "Failed to Delete usergroup.")
        return redirect('a1')
def add_usergroup(request):
    return render(request, "hod_template/add_usergroup_template.html")
def add_usergroup_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('add_usergroup')
    else:
        group_name = request.POST.get('group_name')
        group_describe= request.POST.get('group_describe')

        try:
            usergroup = UserGroup(group_name=group_name,group_describe=group_describe)
            usergroup.save()
            messages.success(request, "添加成功！")
            return redirect('a1')
        except:
            messages.error(request, "添加失败")
            return redirect('add_usergroup')
def edit_usergroup(request, usergroup_id):
    usergroup = UserGroup.objects.get(id=usergroup_id)#这里可能会报错
    context = {
        "usergroup": usergroup,
        "id": usergroup_id
    }
    return render(request, 'hod_template/edit_usergroup_template.html', context)
def edit_usergroup_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method")
    else:
        usergroup_id=request.POST.get('usergroup_id')
        group_name=request.POST.get('group_name')
        group_describe=request.POST.get('group_describe')

        try:
            usergroup=UserGroup.objects.get(id=usergroup_id)
            usergroup.group_name=group_name
            usergroup.group_describe=group_describe
            usergroup.save()
            messages.success(request, "Course Updated Successfully.")
            return redirect('/edit_usergroup/'+usergroup_id)

        except:
            messages.error(request, "Failed to Update Usergroup.")
            return redirect('/edit_usergroup/'+usergroup_id)


def add_user_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
    else:
        user_name = request.POST.get('user_name')
        group = request.POST.get('group')
        password = request.POST.get('group_name')
        email = request.POST.get('email')
        tel = request.POST.get('tel')
        user_group=UserGroup.objects.get(group_name=group)

        try:
            user = User(user_name=user_name,group=user_group,password=password,email=email,tel=tel)
            user.save()
            messages.success(request, "添加成功！")
            return redirect('a1')
        except:
            messages.error(request, "添加失败")
            return redirect('add_usergroup')


def edit_user(request, user_id):
    user = User.objects.get(id=user_id)#这里可能会报错
    context = {
        "user": user,
        "id": user_id
    }
    return render(request, 'hod_template/edit_user_template.html', context)


def edit_user_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method")
    else:
        id=request.POST.get('id')
        user_name = request.POST.get('user_name')
        group = request.POST.get('group')
        password = request.POST.get('group_name')
        email = request.POST.get('email')
        tel = request.POST.get('tel')
        user_group=UserGroup.objects.get(group_name=group)
        # try:
        user=User.objects.get(id=id)
        user.user_name=user_name
        user.group=user_group
        user.password=password
        user.email=email
        user.tel=tel
        user.save()
        messages.success(request, "Course Updated Successfully.")
        #     return redirect('/edit_usergroup/'+id)
        # except:
        #     messages.error(request, "Failed to Update User.")
        #     return redirect('/edit_usergroup/'+id)

def delete_user(request, user_id):
    user = User.objects.get(id=user_id)
    try:
        user.delete()
        messages.success(request, "usergroup Deleted Successfully.")
        return redirect('a1')
    except:
        messages.error(request, "Failed to Delete usergroup.")
        return redirect('a1')
#【a2】
def a2(request):
    return render(request,"hod_template/a2.html")
def a2(request):
    if request.method != "POST":
        systemsetting = SystemSetting.objects.get(id=1)
        context = {
            "systemsetting": systemsetting,
            "id": 1
        }
        return render(request, 'hod_template/a2.html', context)

#该函数用于写回数据库
def edit_systemsetting_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method")
    else:
        systemsetting_id=1

        #获取当前页面的数据
        station_letter=request.POST.get('station_letter')
        station_num=request.POST.get('station_num')
        now_position=request.POST.get('now_position')
        now_number=request.POST.get('now_number')
        feature_type=request.POST.get('feature_type')
        feature_digit=request.POST.get('feature_digit')
        #
        image_add=request.POST.get('image_add')
        pic_size=request.POST.get('pic_size')
        QR_add=request.POST.get('QR_add')
        #
        page_size=request.POST.get('page_size')
        read_type=request.POST.get('method')
        gorge=request.POST.get('gorge')
        baud_rate=request.POST.get('baud_rate')
        parity_check=request.POST.get('parity_check')
        data_bit=request.POST.get('data_bit')
        overtime=request.POST.get('overtime')
        stop_bit=request.POST.get('stop_bit')
        hand_control=request.POST.get('hand_control')

        try:
            #获取对象
            systemsetting=SystemSetting.objects.get(id=1)
            #然后开始设置值
            systemsetting.station_letter=station_letter
            systemsetting.station_num=station_num
            systemsetting.now_position=now_position
            systemsetting.now_number=now_number
            systemsetting.feature_type=feature_type
            systemsetting.feature_digit=feature_digit
            systemsetting.image_add=image_add
            systemsetting.pic_size=pic_size
            systemsetting.QR_add=QR_add
            #
            systemsetting.page_size=page_size
            systemsetting.read_type=read_type
            systemsetting.gorge=gorge
            systemsetting.baud_rate=baud_rate
            systemsetting.parity_check=parity_check
            systemsetting.data_bit=data_bit
            systemsetting.overtime=overtime
            systemsetting.stop_bit=stop_bit
            systemsetting.hand_control=hand_control
            #保存
            systemsetting.save()
            messages.success(request, "Updated Successfully.")
            return redirect('/a2/')
        except:
            messages.error(request, "Failed to Update.")
            return redirect('/a2')

#【a3】
def a3(request):
    return render(request,"hod_template/a3.html")

#pip install django-import-export
def backup(request):
	# 指定数据类型
    response = HttpResponse(content_type='application/ms-excel')
    # 设置文件名称
    response['Content-Disposition'] = 'attachment; filename="result.xls"'
    # 创建工作簿
    wb = xlwt.Workbook(encoding='utf-8')
    # 创建表
    ws = wb.add_sheet('Menu')
    row_num = 0
    font_style = xlwt.XFStyle()
    # 二进制
    font_style.font.bold = True
#这里定义一下表头的名字就可以
    # 表头内容
    columns = ['序号', '会员类型', '状态', '描述']
    # 写进表头内容
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    # 获取数据库数据
#这里把表的类名的属性名都放进去
    rows = models.MemberType.objects.values_list('id', 'member_type', 'status', 'describe')
    # 遍历提取出来的内容
    for row in rows:
        row_num += 1
        # 逐行写入Excel

        for col_num in range(len(row)):
            #return HttpResponse(col_num)
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response
#【a4】
def a4(request):
    usergroupstatuss = UserGroupStatus.objects.all()
    usergroups=UserGroup.objects.all()
    context = {
        "usergroupstatuss": usergroupstatuss,
        "usergroups": usergroups,
    }
    return render(request,"hod_template/a4.html",context)
def delete_usergroupstatus(request, usergroupstatus_id):
    usergroupstatus = UserGroupStatus.objects.get(id=usergroupstatus_id)
    try:
        usergroupstatus.delete()
        messages.success(request, "usergroup Deleted Successfully.")
        return redirect('a4')
    except:
        messages.error(request, "Failed to Delete usergroup.")
        return redirect('a4')
def add_usergroupstatus(request):
    usergroups=UserGroup.objects.all()
    context = {
        "usergroups": usergroups,
    }
    return render(request, "hod_template/add_usergroupstatus_template.html",context)
def add_usergroupstatus_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('add_usergroupstatus')
    else:

        user_group=UserGroup.objects.get(group_name=request.POST.get('user_group'))
        usergroup_status_values= request.POST.get('usergroup_status_values')

        try:
            usergroupstatus = UserGroupStatus(user_group=user_group,usergroup_status_values=usergroup_status_values)
            usergroupstatus.save()
            messages.success(request, "添加成功！该提示写在HodViews.add_usergroupstatus_save里面")
            return redirect("add_usergroupstatus")
        except:
            messages.error(request, "添加失败！该提示写在HodViews.add_usergroupstatus_save里面")
            return redirect('add_usergroupstatus')
def edit_usergroupstatus(request, usergroupstatus_id):
    usergroupstatus = UserGroupStatus.objects.get(id=usergroupstatus_id)#这里可能会报错
    usergroups = UserGroup.objects.all()
    context = {
        "usergroups": usergroups,
        "usergroupstatus": usergroupstatus,
        "usergroupstatus_id": usergroupstatus_id
    }
    return render(request, 'hod_template/edit_usergroupstatus_template.html', context)
def edit_usergroupstatus_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method")
    else:
        usergroupstatus_id=request.POST.get('usergroupstatus_id')
        user_group = UserGroup.objects.get(group_name=request.POST.get('user_group'))
        usergroup_status_values = request.POST.get('usergroup_status_values')
        # try:
        usergroupstatus=UserGroupStatus.objects.get(id=usergroupstatus_id)
        usergroupstatus.user_group=user_group
        usergroupstatus.usergroup_status_values=usergroup_status_values
        usergroupstatus.save()

        messages.success(request, "Course Updated Successfully.")
        return redirect('/edit_usergroupstatus/'+usergroupstatus_id)
        #
        # except:
        #     messages.error(request, "Failed to Update Usergroupstatus.")
        #     return redirect('/edit_usergroupstatus/'+usergroupstatus_id)
#【a5】
def a5(request):
    preinstalls = Preinstall.objects.all()
    context = {
        "preinstalls": preinstalls
    }
    return render(request,"hod_template/a5.html",context)
def delete_preinstall(request, preinstall_id):
    preinstall = Preinstall.objects.get(id=preinstall_id)
    try:
        preinstall.delete()
        messages.success(request, "usergroup Deleted Successfully.")
        return redirect('a5')
    except:
        messages.error(request, "Failed to Delete usergroup.")
        return redirect('a5')
def add_preinstall(request):
    return render(request, "hod_template/add_preinstall_template.html")
def add_preinstall_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('add_preinstall')
    else:
        sample_type=request.POST.get('sample_type')
        type=request.POST.get('type')
        preinstall_value= request.POST.get('preinstall_value')
        try:
            # sample_type=SampleType.objects.get(sample_type_id=sample_type_id)
            preinstall = Preinstall(preinstall_value=preinstall_value,sample_type=sample_type,type=type)#这里很容易出错
            preinstall.save()
            messages.success(request, "添加成功！")
            return redirect("add_preinstall")
        except:
            messages.error(request, "添加失败！")
            return redirect('add_preinstall')
def edit_preinstall(request, preinstall_id):
    preinstall = Preinstall.objects.get(id=preinstall_id)#这里可能会报错
    context = {
        "preinstall": preinstall,
        "id": preinstall_id
    }
    return render(request, 'hod_template/edit_preinstall_template.html', context)


def edit_preinstall_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method")
    else:
        preinstall_id = request.POST.get('preinstall_id')
        type = request.POST.get('type')
        preinstall_value = request.POST.get('preinstall_value')
        sample_type = request.POST.get('sample_type')

        try:
            # preinstall.type.key=[1,]
            preinstall = Preinstall.objects.get(id=preinstall_id)
            preinstall.preinstall_value = preinstall_value
            preinstall.type = type
            preinstall.sample_type = sample_type

            preinstall.save()

            messages.success(request, "Course Updated Successfully.")
            return redirect('/edit_preinstall/' + preinstall_id)

        except:
            messages.error(request, "Failed to Update Course.")
            return redirect('/edit_preinstall/' + preinstall_id)
#【a6】
def a6(request):
    membertypes = MemberType.objects.all()
    context = {
        "membertypes": membertypes
    }
    return render(request,"hod_template/a6.html",context)
def delete_membertype(request, membertype_id):
    membertype = MemberType.objects.get(id=membertype_id)
    try:
        membertype.delete()
        messages.success(request, "usergroup Deleted Successfully.")
        return redirect('a6')
    except:
        messages.error(request, "Failed to Delete usergroup.")
        return redirect('a6')
def add_membertype(request):
    return render(request, "hod_template/add_membertype_template.html")
def add_membertype_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('add_membertype')
    else:
        member_type = request.POST.get('member_type')
        status= request.POST.get('status')
        describe=request.POST.get('describe')
        try:
            membertype = MemberType(member_type=member_type,status=status,describe=describe)
            membertype.save()
            messages.success(request, "添加成功！")
            return redirect("add_membertype")
        except:
            messages.error(request, "添加失败！")
            return redirect('add_membertype')
def edit_membertype(request, membertype_id):
    membertype = MemberType.objects.get(id=membertype_id)#这里可能会报错
    context = {
        "membertype": membertype,
        "id": membertype_id
    }
    return render(request, 'hod_template/edit_membertype_template.html', context)
def edit_membertype_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method")
    else:
        membertype_id=request.POST.get('membertype_id')
        member_type = request.POST.get('member_type')
        status= request.POST.get('status')
        describe=request.POST.get('describe')

        try:
            membertype=MemberType.objects.get(id=membertype_id)
            membertype.member_type=member_type
            membertype.status=status
            membertype.describe=describe
            membertype.save()

            messages.success(request, "Course Updated Successfully.")
            return redirect('/edit_membertype/'+membertype_id)

        except:
            messages.error(request, "Failed to Update Course.")
            return redirect('/edit_membertype/'+membertype_id)
#【a7】
def a7(request):
    # pt=PrintSetting.objects.get(id=1)
    if request.method != "POST":
        pt = PrintSetting.objects.get(id=1)
        return render(request, "hod_template/a7.html", {"pt":pt,'id':json.dumps(1)})
    else:
        # 获取到数据库中已经存在的对象
        num = request.POST.get("typet")
        print(num)
        pt = PrintSetting.objects.get(id=num)
        start_x=request.POST.get("start_x")
        #然后使用 try和except 来写入数据库
        if request.POST.get("sub"):
            # messages.error(request, "Failed to Update")
            try:
                pt.start_x=request.POST.get("start_x")
                pt.start_y=request.POST.get("start_y")
                pt.row_spacing=request.POST.get("row_spacing")
                pt.col_spacing=request.POST.get("col_spacing")
                pt.page_spacing=request.POST.get("page_spacing")
                pt.row_words=request.POST.get("row_words")
                pt.row_max=request.POST.get("row_max")
                pt.picture_x=request.POST.get("picture_x")
                pt.picture_y=request.POST.get("picture_y")
                pt.pic_sizex=request.POST.get("pic_sizex")
                pt.pic_sizey=request.POST.get("pic_sizey")
                pt.QR_X=request.POST.get("QR_X")
                pt.QR_Y = request.POST.get("QR_Y")
                pt.QR_size=request.POST.get("QR_size")
                pt.page_sizex=request.POST.get("page_sizex")
                pt.page_sizey=request.POST.get("page_sizey")
                pt.font=request.POST.get("font")
                pt.horizontal=request.POST.get("horizontal")
                pt.save()
                return render(request, "hod_template/a7.html",{"pt":pt})
            #特殊情况处理，一般不用管
            except:
                messages.error(request, "Failed to Update")
                return redirect('admin_profile')
        return render(request, "hod_template/a7.html", {"pt": pt})




def admin_view_attendance(request):
    subjects = Subjects.objects.all()
    session_years = SessionYearModel.objects.all()
    context = {
        "subjects": subjects,
        "session_years": session_years
    }
    return render(request, "hod_template/admin_view_attendance.html", context)


@csrf_exempt
def check_email_exist(request):
    email = request.POST.get("email")
    user_obj = CustomUser.objects.filter(email=email).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)

@csrf_exempt
def check_username_exist(request):
    username = request.POST.get("username")
    user_obj = CustomUser.objects.filter(username=username).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)

def admin_profile(request):
    user = CustomUser.objects.get(id=request.user.id)

    context={
        "user": user
    }
    return render(request, 'hod_template/admin_profile.html', context)


def admin_profile_update(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('admin_profile')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')

        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            if password != None and password != "":
                customuser.set_password(password)
            customuser.save()
            messages.success(request, "Profile Updated Successfully")
            return redirect('admin_profile')
        except:
            messages.error(request, "Failed to Update Profile")
            return redirect('admin_profile')
    


def staff_profile(request):
    pass


def student_profile(requtest):
    pass



