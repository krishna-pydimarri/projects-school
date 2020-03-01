from django.db import models, connections
from django.forms import ModelForm
from django.contrib.postgres.fields import ArrayField

# class Question(models.Model):
#     question_text = models.CharField(max_length=200)
#     pub_date = models.DateTimeField('date published')
    # def __str__(self):
    #   return self.question_text

# class Choice(models.Model):
#     question = models.ForeignKey(Question, on_delete=models.CASCADE)
#     choice_text = models.CharField(max_length=200)
#     votes = models.IntegerField(default=0)

class dimemployees(models.Model):
    name = models.CharField(max_length=50)
    active = models.CharField(max_length=1)
    email = models.EmailField(max_length=100)
    #def __str__(self):
    #    return self.name+"|"+self.active

class dimprojects(models.Model):
    project_id = models.IntegerField()
    client = models.CharField(max_length=200)
    project_name = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()

class edgered_timesheets(models.Model):
    date = models.DateField()
    hours_worked = models.IntegerField()
    timecode = models.IntegerField()
    name = models.CharField(max_length=50)
    islatest = models.IntegerField()
    date_changed = models.DateTimeField(auto_now=True)



class timesheet_details(models.Model):
    username=models.CharField(max_length=50)
    day_value=models.CharField(max_length=50)
    date_value=models.DateField()
    week_no=models.CharField(max_length=50)
    projects_time=ArrayField(models.CharField(max_length=500))
# import sys,os


# def dictfetchall(cursor):
#     "Return all rows from a cursor as a dict"
#     columns = [col[0] for col in cursor.description]
#     return [
#         dict(zip(columns, row))
#         for row in cursor.fetchall()
#     ]

# from collections import namedtuple

# def namedtuplefetchall(cursor):
#     "Return all rows from a cursor as a namedtuple"
#     desc = cursor.description
#     nt_result = namedtuple('Result', [col[0] for col in desc])
#     return [nt_result(*row) for row in cursor.fetchall()]

# result = namedtuplefetchall(cursor)
# # print(result[1][0])
# i = 0
# while i <= len(result):
#     print(result[i][0])
#     i += 1


# print(Dimemployees)
    # name = result[0]
    # active = result.active
    # email = result.email
    # print(name)
    # print(active)
    # print(email)

# employee = dimemployees.objects.raw('SELECT * FROM timesheets.dimemployees')
# print(employee)

# cnx.close()
# db_conn = connections['default']
