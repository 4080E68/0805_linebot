from django.db import models

# Create your models here.


class job_hunting(models.Model):  # 求職
    name = models.CharField(max_length=255, default="")  # 聯絡人
    job_type = models.CharField(max_length=255, default="")  # 工作類型
    minSalary = models.IntegerField(default="")  # 期望薪資
    maxSalary = models.IntegerField(default="")  # 期望薪資
    address = models.CharField(max_length=255, default="")  # 期望工作地點
    Phone = models.CharField(max_length=255, default="")  # 聯絡電話
    remark = models.CharField(max_length=255, default="")  # 備註
    lineId = models.CharField(max_length=255, default="")  # lineId
    job_title = models.CharField(max_length=255, default="")  # 負責人
    job_title2 = models.CharField(max_length=255, default="")  # 負責人2


class company(models.Model):  # 公司
    companyName = models.CharField(max_length=255, default="")
    name = models.CharField(max_length=255, default="")  # 聯絡人
    job_type = models.CharField(max_length=255, default="")  # 工作類型
    minSalary = models.IntegerField(default="")  # 期望薪資
    maxSalary = models.IntegerField(default="")  # 期望薪資
    address = models.CharField(max_length=255, default="")  # 工作地點
    Phone = models.CharField(max_length=255, default="")  # 聯絡電話
    remark = models.CharField(max_length=255, default="")  # 備註
    assistant = models.CharField(max_length=255, default="")  # 是否有助理
    overtime_pay = models.CharField(max_length=255, default="")  # 是否有加班費
    welfare = models.CharField(max_length=255, default="")  # 是否有加班費
    lineId = models.CharField(max_length=255, default="")  # lineId
