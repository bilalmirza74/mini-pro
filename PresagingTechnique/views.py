from django.shortcuts import  render,HttpResponseRedirect
from django.contrib import messages
from .forms import CustomerRegistrationForm
def index(request):
    return render(request,'index.html',{})

def custRegistration(request):
    if request.method=='POST':

        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            print('Data is Valid')
            form.save()
            messages.success(request, 'You have been successfully registered')
            #return HttpResponseRedirect('./CustLogin')
            form = CustomerRegistrationForm()
            return render(request, 'registrations.html', {'form': form})
        else:
            print("Invalid form")
    else:
        form = CustomerRegistrationForm()
    return render(request,'registrations.html',{'form':form})

def CustLogin(request):
    return render(request,"CustomerLogin.html",{})
def CloudLogin(request):
    return render(request,'CloudLogin.html',{})
def CspLogin(request):
    return render(request,"CspLogin.html",{})
def Logout(request):
    return render(request,'index.html',{})