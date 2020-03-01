from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, render_to_response
from django.contrib.auth.decorators import login_required
from timekeeping.models import dimemployees as de
from timekeeping.models import dimprojects
from timekeeping.models import timesheet_details
from urllib import request
import time
import datetime
from datetime import date
project_name_map={}
#date_day_map={}

"""
from googleapiclient import discovery
from oauth2client import tools
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.file import Storage
import httplib2
"""

def index(request):
    return render(request, 'index.html')
    # name_list = dimemployees.objects.order_by('name')[:5]
    # return render(request, 'timekeeping/index.html', {'name_list': name_list})

"""
def google_calendar_connection():
    flags = tools.argparser.parse_args([])
    FLOW = OAuth2WebServerFlow(
        client_id='xxxxxxxxxx-xxxxxxxxxxxxxxxxxxxxxxxxxx.apps.googleusercontent.com',
        client_secret='xxxxxx',
        scope='https://www.googleapis.com/auth/calendar',
        user_agent='<application name>'
        )
    storage = Storage('calendar.dat')
    credentials = storage.get()
    if credentials is None or credentials.invalid == True:
        credentials = tools.run_flow(FLOW, storage, flags)
    
    # Create an httplib2.Http object to handle our HTTP requests and authorize it
    # with our good Credentials.
    http = httplib2.Http()
    http = credentials.authorize(http)
    service = discovery.build('calendar', 'v3', http=http)
    
    return service
    

def form_valid(self, form):
        service = self.google_calendar_connection()
        
        event = {
          'summary': "new",
          'location': "london",
          'description': "anything",
          'start': {
            'date': "2015-09-02",
          },
          'end': {
            'date': "2015-09-02",
          },
                 
        }
        
        event = service.events().insert(calendarId='primary', body=event).execute()
        
        return CreateView.form_valid(self, form) 

""" 




def home(request):
	return render(request, 'home.html')

def Login(request):
	return render(request, 'login.html')

@login_required
def timesheet(request):
    #return render(request, 'timekeeping/timesheet.html',{"name":[x.name for x in de.objects.all()], "email":de.objects.get(id=1).email})
    print(" ".join(['<option value="Employee {}"> {} </option>'.format(ind+1,x.name) for ind,x in enumerate(de.objects.all())]))
    print(" ".join(['<option value="Project {}"> {} </option>'.format(ind+1,x.project_name) for ind,x in enumerate(dimprojects.objects.all())]))
    wkno=request.POST.get('weekno')
    for ind,x in enumerate(dimprojects.objects.all()):
        key_val="Project {}".format(ind+1)
        project_name_map[key_val]=x.project_name
    global current_user
    current_user=str(request.user)
    email_id=request.user.email
    current_user=current_user.replace(" ", "").rstrip(current_user[-16:])
    cal='<iframe src="https://calendar.google.com/calendar/embed?showPrint=0&amp;mode=WEEK&amp;height=600&amp;wkst=1&amp;bgcolor=%23ffffff&amp;src={}%40edgered.com.au&amp;color=%231B887A&amp;ctz=Australia%2FSydney" style="border:solid 1px #777" width="800" height="600" frameborder="0" scrolling="no"></iframe>'.format(current_user)
    #context['your_html_variable'] = "\n".join(['<option value="Employee {}"> {} </option>'.format(ind+1,x.name) for ind,x in enumerate(de.objects.all())])
    return render(request, 'timesheet.html',{"name":"\n".join(['<option value="Employee {}"> {} </option>'.format(ind+1,x.name) for ind,x in enumerate(de.objects.all())]), "email":de.objects.get(id=1).email,"wkno":wkno,"project_name":" ".join(['<option value="Project {}"> {} </option>'.format(ind+1,x.project_name) for ind,x in enumerate(dimprojects.objects.all())]),"current_user":current_user,"email_id":email_id,"cal":cal})

def email(request, dimemployees_id):
    return HttpResponse("You're looking at %s." % dimemployees_id)

def detail(request, dimemployees_id):
    employee = get_object_or_404(de, pk=dimemployees_id)
    return render(request, 'detail.html', {'employee': employee})

def test(request):
    return HttpResponse(de.objects.all())

def sub_func(request):
    global wkno
    global wkno_bkp
    wkno_bkp=request.GET.get('weekno','')
    wkno=wkno_bkp.split("-")[1].strip("W")
    yr=request.GET.get('weekno','').split("-")[0]
    yr=int(yr)
    #sun_hrs=request.GET.get('sun_hours','')
    sun_hrs= request.GET.getlist('sun_hours')
    sun_pn= request.GET.getlist('sun_pn')
    mon_hrs= request.GET.getlist('mon_hours')
    mon_pn= request.GET.getlist('mon_pn')
    tue_hrs= request.GET.getlist('tue_hours')
    tue_pn= request.GET.getlist('tue_pn')
    wed_hrs= request.GET.getlist('wed_hours')
    wed_pn= request.GET.getlist('wed_pn')
    thu_hrs= request.GET.getlist('thu_hours')
    thu_pn= request.GET.getlist('thu_pn')
    fri_hrs= request.GET.getlist('fri_hours')
    fri_pn= request.GET.getlist('fri_pn')
    sat_hrs= request.GET.getlist('sat_hours')
    sat_pn= request.GET.getlist('sat_pn')
    wkno=int(wkno)
    startdate = time.asctime(time.strptime('%d %d 1' %(yr, wkno), '%Y %W %w'))
    if date(yr, 1, 1).weekday()!=0:
        startdate = datetime.datetime.strptime(startdate, '%a %b %d %H:%M:%S %Y')- datetime.timedelta(days=7)
    else:
        startdate = datetime.datetime.strptime(startdate, '%a %b %d %H:%M:%S %Y')
    dates = [startdate]
    for i in range(1, 7):
        dates.append((startdate + datetime.timedelta(days=i)))
    dates_f=[str(date.date()) for date in dates]
    days=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    global date_day_map
    date_day_map={}
    for day_date in zip(days,dates_f):
        date_day_map[day_date[0]]=day_date[1]
    list_zip=[zip(["Monday" for i in range(0,len(mon_pn))],mon_pn,mon_hrs),zip(["Tuesday" for i in range(0,len(tue_pn))],tue_pn,tue_hrs),zip(["Wednesday" for i in range(0,len(wed_pn))],wed_pn,wed_hrs),zip(["Thursday" for i in range(0,len(thu_pn))],thu_pn,thu_hrs),zip(["Friday" for i in range(0,len(fri_pn))],fri_pn,fri_hrs),zip(["Saturday" for i in range(0,len(sat_pn))],sat_pn,sat_hrs),zip(["Sunday" for i in range(0,len(sun_pn))],sun_pn,sun_hrs)]
    global output_map
    output_map={"Monday":[],"Tuesday":[],"Wednesday":[],"Thursday":[],"Friday":[],"Saturday":[],"Sunday":[]}
    for zip_pn_hr in list_zip:
        for day_pn_hr in zip_pn_hr:
            pn_hr_str='%s|%s'%(project_name_map.get(day_pn_hr[1],''),day_pn_hr[2])
            output_map[day_pn_hr[0]].append(pn_hr_str)

    return render(request, 'week_display.html',{"wkno":wkno,"dates":dates_f, "mon_hrs":mon_hrs,"mon_pn":mon_pn, "tue_hrs":tue_hrs,"tue_pn":tue_pn, "wed_hrs":wed_hrs,"wed_pn":wed_pn, "thu_hrs":thu_hrs,"thu_pn":thu_pn, "fri_hrs":fri_hrs,"fri_pn":fri_pn, "sat_hrs":sat_hrs,"sat_pn":sat_pn,"sun_hrs":sun_hrs,"sun_pn":sun_pn,"project_name_map":project_name_map,"date_day_map":date_day_map,"Monday":date_day_map["Monday"],"Tuesday":date_day_map["Tuesday"],"Wednesday":date_day_map["Wednesday"],"Thursday":date_day_map["Thursday"],"Friday":date_day_map["Friday"],"Saturday":date_day_map["Saturday"],"Sunday":date_day_map["Sunday"],"output_map":output_map,"date_day_map":date_day_map})


def multibarhorizontalchart(request):
    for day in output_map.keys():
        timesheet_details.objects.create(username=current_user,day_value=day,date_value=date_day_map.get(day),week_no=wkno_bkp,projects_time=output_map.get(day))
        #timesheet_details
    xdata = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    all_projects_names=[x.project_name for x in dimprojects.objects.all()]
    #no_of_series=len(all_projects_names)
    #series_names=all_projects_names
    #proj_time_maps= {k: [] for k in all_projects_names}
    ydata_list=[]
    for pj_nm in all_projects_names:
        day_work_list=[]
        for day in xdata:
            #op_keys=output_map
            ydata_stg = output_map[day]
            for adayswork in ydata_stg:
                hours=0
                if adayswork.split("|")[0]==pj_nm:
                    hours=adayswork.split("|")[1]
                    break;
            day_work_list.append(hours)
        ydata_list.append(day_work_list)   
    extra_serie = {"tooltip": {"y_start": "", "y_end": " hours"}}
    chartdata ={'x': xdata}
    for series_num in range(1,len(all_projects_names)+1):
       nm='name%s'%(series_num)
       y='y%s'%(series_num)
       extra='extra%s'%(series_num)
       chartdata[nm]=all_projects_names[series_num-1]
       chartdata[y]=ydata_list[series_num-1]
       chartdata[extra]=extra_serie
    
    charttype = "multiBarHorizontalChart"
    chartcontainer = 'multibarhorizontalchart_container'  # container name
    data = {
        'charttype': charttype,
        'chartdata': chartdata,
        'chartcontainer': chartcontainer,
        'extra': {
            'x_is_date': False,
            'x_axis_format': '',
            'tag_script_js': True,
            'jquery_on_ready': True,
        },
         "wkno":wkno,
         "date_day_map":date_day_map,
         "output_map":output_map
    }
   # print(abc)
    return render_to_response('multibarhorizontalchart.html', data)
            #ydata_list.append([val.split("|")[1] if val.split("|")[0]==pj_nm else 0 for val in ydata_stg])
            
    #for day in xdata:
        
            
            
            
