from django.db import models

# Create your models here.


class job_hunting(models.Model):  # 求職
    name = models.CharField(max_length=255, default="")  # 聯絡人
    minSalary = models.CharField(max_length=255, default="")  # 期望薪資
    maxSalary = models.CharField(max_length=255, default="")  # 期望薪資
    address = models.CharField(max_length=255, default="")  # 期望工作地點
    Phone = models.CharField(max_length=255, default="")  # 聯絡電話
    remark = models.CharField(max_length=255, default="")  # 聯絡電話
    lineId = models.CharField(
        max_length=255, default="", primary_key=True)  # lineId


class company(models.Model):  # 公司
    name = models.CharField(max_length=255, default="")  # 聯絡人
    salary = models.IntegerField(default="")  # 給付薪資
    address = models.CharField(max_length=255, default="")  # 工作地點
    Phone = models.CharField(max_length=255, default="")  # 聯絡電話
    assistant = models.CharField(max_length=255, default="")  # 是否有助理
    overtime_pay = models.CharField(max_length=255, default="")  # 是否有加班費
