from django.shortcuts import render,HttpResponse,redirect
from django.contrib import messages
from PresagingTechnique.models import CustomerRegistrationModel
from faker import Faker
from .models import  CspRegisterModel
from users.models import CustomerCloudData
# Create your views here.

def CloudLoginCheck(request):
    if request.method == 'POST':
        usrid = request.POST.get('loginname')
        pswd = request.POST.get('pswd')
        print("User ID is = ", usrid)
        if usrid == 'admin' and pswd == 'admin':
            return render(request, 'clouds/CloudHome.html')
        elif usrid == 'cloud' and pswd == 'cloud':
            return render(request, 'clouds/CloudHome.html')
        else:
            messages.success(request, 'Please Check Your Login Details')
    return render(request, 'CloudLogin.html')


def CloudCustomers(request):
    cust = CustomerRegistrationModel.objects.all()
    return render(request,'clouds/CloudCust.html',{'cust':cust})

def CloudActivateUsers(request):
    if request.method == 'GET':
        id = request.GET.get('uid')
        status = 'activated'
        print("PID = ", id, status)
        CustomerRegistrationModel.objects.filter(id=id).update(status=status)
        cust = CustomerRegistrationModel.objects.all()
        return render(request,'clouds/CloudCust.html',{'cust':cust})
def CloudCSPAdding(request):
    csp = CspRegisterModel.objects.all()
    return render(request,'clouds/CloudCSP.html',{'csp':csp})

def CloudCreateCsp(request):
    if request.method=='POST':
        cspname = request.POST.get('cspname')
        loginid = request.POST.get('loginid')
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        location = request.POST.get('location')
        service = request.POST.get('service')
        faker = Faker()
        password = faker.password()
        price = faker.random_int(50000, 1000000)
        try:
            CspRegisterModel.objects.create(name=cspname,loginid=loginid,password=password,mobile=mobile,email=email,locality=location,service=service,price=price)
            s = 'CSP Created Success for '+service
            messages.success(request, s)
        except Exception as ex:
            print('Error Message ',str(ex))
            ermsg = 'CSP with mobile '+mobile+ ' and email '+email+' already exist'
            messages.success(request, ermsg)
            return render(request, 'clouds/CloudCSP.html', {})

    return redirect('CloudCSPAdding')


def CloudDataView(request):
    data = CustomerCloudData.objects.all()
    return render(request, 'clouds/CloudDataView.html', {'data': data})
