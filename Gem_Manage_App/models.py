import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.hashers import make_password, check_password


class SessionYearModel(models.Model):
    id = models.AutoField(primary_key=True)
    session_start_year = models.DateField()
    session_end_year = models.DateField()
    objects = models.Manager()


# Overriding the Default Django Auth User and adding One More Field (user_type)
class CustomUser(AbstractUser):
    user_type_data = ((1, "HOD"), (2, "Staff"), (3, "Student"))
    user_type = models.CharField(default=1, choices=user_type_data, max_length=10)


class AdminHOD(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class Staffs(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class Courses(models.Model):
    id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    # def __str__(self):


#     return self.course_name


class Subjects(models.Model):
    id = models.AutoField(primary_key=True)
    subject_name = models.CharField(max_length=255)
    course_id = models.ForeignKey(Courses, on_delete=models.CASCADE, default=1)  # need to give defauult course
    staff_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class Students(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    gender = models.CharField(max_length=50)
    profile_pic = models.FileField()
    address = models.TextField()
    course_id = models.ForeignKey(Courses, on_delete=models.DO_NOTHING, default=1)
    session_year_id = models.ForeignKey(SessionYearModel, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class Attendance(models.Model):
    # Subject Attendanceme'm
    id = models.AutoField(primary_key=True)
    subject_id = models.ForeignKey(Subjects, on_delete=models.DO_NOTHING)
    attendance_date = models.DateField()
    session_year_id = models.ForeignKey(SessionYearModel, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class AttendanceReport(models.Model):
    # Individual Student Attendance
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Students, on_delete=models.DO_NOTHING)
    attendance_id = models.ForeignKey(Attendance, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class LeaveReportStudent(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    leave_date = models.CharField(max_length=255)
    leave_message = models.TextField()
    leave_status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class LeaveReportStaff(models.Model):
    id = models.AutoField(primary_key=True)
    staff_id = models.ForeignKey(Staffs, on_delete=models.CASCADE)
    leave_date = models.CharField(max_length=255)
    leave_message = models.TextField()
    leave_status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class FeedBackStudent(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class FeedBackStaffs(models.Model):
    id = models.AutoField(primary_key=True)
    staff_id = models.ForeignKey(Staffs, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class NotificationStudent(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class NotificationStaffs(models.Model):
    id = models.AutoField(primary_key=True)
    stafff_id = models.ForeignKey(Staffs, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class StudentResult(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    subject_id = models.ForeignKey(Subjects, on_delete=models.CASCADE)
    subject_exam_marks = models.FloatField(default=0)
    subject_assignment_marks = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

class Receipts(models.Model):
    identification_id = models.TextField(primary_key=True)
    receipt_tel = models.TextField()
    sample_status = models.TextField()
    sender_company = models.TextField()
    sample_sender = models.TextField()
    sender_tel = models.TextField()
    postal_code = models.TextField()
    gemstone_sum = models.TextField()
    basket_id = models.TextField()
    finish_date = models.DateTimeField()
    identification_cost = models.FloatField()
    payment_state = models.BooleanField()
    sample_date = models.DateTimeField(auto_now_add=True)


class MemberType(models.Model):
    id = models.AutoField(primary_key=True)
    member_type = models.CharField(max_length=20)
    status = models.TextField('会员类型状态')
    describe=models.TextField('会员类型介绍',blank=True)
    objects = models.Manager()


class Members(models.Model): #会员
    id = models.AutoField(primary_key=True)# ID
    member_name = models.CharField(max_length=50)
    telephone = models.CharField(max_length=50)
    member_type = models.ForeignKey(MemberType, on_delete=models.CASCADE,null=True) # 会员类型
    legal_representative = models.CharField(max_length=50) # 法人代表
    license_number = models.CharField(max_length=50) # 执照号
    postal_code = models.CharField(max_length=50) # 邮政编码
    company_name = models.CharField(max_length=100) # 公司名
    company_address = models.TextField() # 公司地址
    objects = models.Manager()

class UserGroup(models.Model):
    id=id = models.AutoField(primary_key=True)
    group_name=models.CharField(max_length=20)
    group_describe=models.TextField(blank=True)
    objects = models.Manager()

class User(models.Model):
    def __str__(self):
        return self.user_name

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = '用户信息'
    id=models.AutoField(primary_key=True)
    user_name=models.CharField(max_length=20)
    group=models.ForeignKey(UserGroup,on_delete=models.CASCADE)
    password=models.CharField('密码',max_length=20)
    email=models.CharField('邮箱',max_length=50)
    tel=models.CharField('电话号码',max_length=30)
    objects = models.Manager()

    def save(self, *args, **kwargs):
        self.password = make_password(self.password, None, 'pbkdf2_sha256')
        super(User, self).save(*args, **kwargs)

#模块表
class Module(models.Model):
    id = models.AutoField(primary_key=True)
    module_name=models.CharField('模块名',max_length=20)
    objects = models.Manager()

#送货人
class Sender(models.Model):
    id = models.AutoField(primary_key=True)
    sender_company=models.CharField('送样人单位',max_length=50)
    sample_sender=models.CharField('送样人姓名', max_length=20)
    sender_tel = models.CharField('送样人电话',max_length=20)
    postal_code=models.CharField('邮政编码',max_length=6)
    objects = models.Manager()

#样品单
class Sample(models.Model):
    identification_id=models.CharField('检测批号',max_length=20,primary_key=True)
    receipt_tel = models.CharField('检测室电话', max_length=20)
    sample_status=models.CharField('收样状态',max_length=20)
    basket_id=models.CharField('框号',max_length=10)

    #送样人
    sender=models.ForeignKey(Sender,on_delete=models.CASCADE)
    #预计结束时间
    finish_date=models.DateField()
    #开始时间
    start_date=models.DateField(auto_now_add=True)
    #收样人
    sample_collectr=models.ForeignKey(User, on_delete=models.CASCADE)
    identification_cost=models.CharField('鉴定费用',max_length=10)
    ACTIVES = ((1, '是'), (2, '否'))
    payment_state=models.CharField('是否付款',max_length=10,default='是',choices=ACTIVES)
    objects = models.Manager()

#用户组权限
class UserPower(models.Model):
    id = models.AutoField(primary_key=True)
    user_group=models.ForeignKey(UserGroup,on_delete=models.CASCADE)
    module=models.ForeignKey(Module,on_delete=models.CASCADE)
    ACTIVES = (('是', '是'), ('否', '否'))
    is_readable = models.CharField('是否有浏览权限', max_length=32, default="non_active", choices=ACTIVES)
    is_editable = models.CharField('是否有编辑权限', max_length=32, default="non_active", choices=ACTIVES)
    is_forbidden = models.CharField('是否禁止访问', max_length=32, default="non_active", choices=ACTIVES)
    objects = models.Manager()


# 用户配置状态
class UserGroupStatus(models.Model):
    id = models.AutoField(primary_key=True)
    user_group = models.ForeignKey(UserGroup, on_delete=models.CASCADE)
    usergroup_status_values=models.CharField('配置状态',max_length=50)
    objects = models.Manager()


#单样表
class SingleSample(models.Model):
    gemstone_id=models.CharField('编号',max_length=20,primary_key=True)
    is_select_data = ((1, "无"), (2, "通过"), (3, "未通过"))
    is_select=models.CharField(default=1,choices=is_select_data,max_length=10)
    identification_id=models.ForeignKey(Sample,on_delete=models.CASCADE)
    SingleSample_status = models.CharField(default="收样",max_length=20 )
    verification_code=models.CharField('验证码',max_length=10,null=True)
    single_sample_name=models.CharField('样品名称',max_length=20)
    identification_result=models.CharField('鉴定结果',max_length=50,null=True)
    #证书
    sample_type_data = ((1, "大卡"), (2, "玉石"), (3, "钻石"), (4, "宝石"), (5, "小卡"), (6, "大报告"))
    sample_type = models.CharField(default=1, choices=sample_type_data, max_length=10)
    require = models.CharField('检测要求', max_length=50, blank=True)
    status = models.CharField('样品状况', max_length=50, blank=True)
    gemstone_appearance=models.FloatField('外观',max_length=20,null=True)
    gemstone_mass=models.FloatField('总质量',max_length=100000,null=True)
    gemstone_density=models.FloatField('密度',max_length=1000,null=True)
    refraction_index=models.FloatField('折射率',max_length=1000,null=True)
    light_characteristc=models.FloatField('光学特性',max_length=1000,null=True)
    observation_result=models.CharField('放大观察',max_length=50,null=True)
    heavy_metal=models.CharField('重金属检测',max_length=50,null=True)
    infrared=models.CharField('红外线检测',max_length=50,null=True)
    cut=models.CharField('琢型', max_length=50,null=True)
    color_level=models.FloatField('颜色级别',max_length=100,null=True)
    Cleanliness_level=models.FloatField('纯净级别',max_length=100,null=True)
    diamond_cut=models.CharField('切工', max_length=50,null=True)
    others=models.CharField('其他', max_length=50,null=True)
    remarks=models.TextField('备注',null=True)
    image=models.FileField('图片',null=True)
    objects = models.Manager()

#预设值表-新-无外键
class Preinstall(models.Model):
    id=models.AutoField(primary_key=True)
    sample_type=models.CharField('配置项目',max_length=50)
    type=models.CharField('配置类型',max_length=50)
    preinstall_value=models.CharField('预设值',max_length=50)
    objects = models.Manager()

#样品检测表
class Task(models.Model):
    id = models.AutoField(primary_key=True)
    gemstone_id=models.ForeignKey(SingleSample,on_delete=models.CASCADE)
    # 检测员
    identification_staff = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    # 任务状态
    identification_id = models.ForeignKey(Sample, on_delete=models.CASCADE)
    # 审核员
    examine_staff=models.CharField(max_length=20,null=True)
    objects = models.Manager()


class PrintSetting(models.Model):
    id = models.AutoField(primary_key=True)
    start_x=models.IntegerField()
    start_y=models.IntegerField()
    row_spacing=models.IntegerField()
    col_spacing=models.IntegerField()
    page_spacing=models.IntegerField()
    row_words=models.IntegerField()
    row_max=models.IntegerField()
    picture_x=models.IntegerField()
    picture_y = models.IntegerField()
    pic_sizex=models.IntegerField()
    pic_sizey = models.IntegerField()
    QR_X=models.IntegerField()
    QR_Y = models.IntegerField()
    QR_size=models.IntegerField()
    page_sizex=models.IntegerField()
    page_sizey = models.IntegerField()
    font=models.IntegerField()
    horizontal=models.IntegerField()
    name=models.CharField('表单名',max_length=20,default="1")
    objects = models.Manager()

class SystemSetting(models.Model):
    id=models.AutoField(primary_key=True)
    station_letter=models.CharField(max_length=2)
    station_num = models.IntegerField()
    now_position=models.CharField(max_length=5)
    now_number=models.IntegerField()
    feature_type=models.CharField(max_length=5)
    feature_digit=models.IntegerField()
    image_add=models.FilePathField()
    pic_size=models.CharField(max_length=20)
    QR_add=models.URLField()
    page_size=models.IntegerField()
    read_type=models.IntegerField()
    gorge=models.CharField(max_length=10)
    baud_rate=models.IntegerField()
    parity_check=models.IntegerField()
    data_bit=models.IntegerField()
    overtime=models.IntegerField()
    stop_bit=models.CharField(max_length=10)
    hand_control=models.IntegerField()
    objects = models.Manager()

class Copy(models.Model):
    id=models.AutoField(primary_key=True)
    copy_name=models.CharField(max_length=20)
    copy_date=models.DateField()
    copy_position=models.FilePathField()
    copyfile_name=models.CharField(max_length=50)
    copy_remarks=models.CharField(max_length=100,null=True)
    objects = models.Manager()

class CopySetting(models.Model):
    id = models.AutoField(primary_key=True)
    copy_method=models.IntegerField()
    copy_type=models.CharField(max_length=10)
    copy_cycle=models.IntegerField(null=True)
    copy_hour=models.IntegerField(null=True)
    starttime=models.DateTimeField()
    objects = models.Manager()



# Creating Django Signals

# It's like trigger in database. It will run only when Data is Added in CustomUser model

@receiver(post_save, sender=CustomUser)
# Now Creating a Function which will automatically insert data in HOD, Staff or Student
def create_user_profile(sender, instance, created, **kwargs):
    # if Created is true (Means Data Inserted)
    if created:
        # Check the user_type and insert the data in respective tables
        if instance.user_type == 1:
            AdminHOD.objects.create(admin=instance)
        if instance.user_type == 2:
            Staffs.objects.create(admin=instance)
        if instance.user_type == 3:
            Students.objects.create(admin=instance, course_id=Courses.objects.get(id=1),
                                    session_year_id=SessionYearModel.objects.get(id=1), address="", profile_pic="",
                                    gender="")


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.adminhod.save()
    if instance.user_type == 2:
        instance.staffs.save()
    if instance.user_type == 3:
        instance.students.save()



