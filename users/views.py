from django.shortcuts import render, HttpResponse, redirect
from PresagingTechnique.models import CustomerRegistrationModel
from django.contrib import messages
from .models import CustomerCloudData,KNNSuggestionModel
from django.core.files.storage import FileSystemStorage
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_iris
from cloud.models import CspRegisterModel
from django.db.models import Sum, Count, Avg
import matplotlib.pyplot as plt
import numpy as np
import os
from django.conf import settings
from django.http import HttpResponse, Http404
from .KnnAlgorithm import KnnRecommender
from django.conf import settings

sujjdict = {}

# Create your views here.

def UserLoginCheck(request):
    if request.method == "POST":
        loginid = request.POST.get('loginname')
        pswd = request.POST.get('pswd')
        print("Login ID = ", loginid, ' Password = ', pswd)
        try:
            check = CustomerRegistrationModel.objects.get(loginid=loginid, password=pswd)
            status = check.status
            print('Status is = ', status)
            if status == "activated":
                request.session['id'] = check.id
                request.session['loggeduser'] = check.name
                request.session['loginid'] = loginid
                request.session['email'] = check.email
                print("User id At", check.id, status)
                return render(request, 'users/CustomerPage.html', {})
            else:
                messages.success(request, 'Your Account Not at activated')
                return render(request, 'CustomerLogin.html')
            # return render(request, 'user/userpage.html',{})
        except Exception as e:
            print('Exception is ', str(e))
            pass
        messages.success(request, 'Invalid Login id and password')
    return render(request, 'CustomerLogin.html', {})


def CustExploreService(request):
    email = request.session['email']
    # knnalgorithm()
    global knnDict
    results = CspRegisterModel.objects.filter().values('service').annotate(price=Avg('price')).order_by("service")
    # print(results,type(results))
    dict = {}
    list = []
    for x in results:
        # print(x['service'],"===",x['price'])
        dict.update({x['service']: x['price']})
        list.append([x['price']])
    # print(dict)
    dpnt = []
    # print(list)
    for d in list:
        if d[0] < 500000:
            dpnt.append(1)
        else:
            dpnt.append(0)
    # print(dpnt)
    test = [[560000], [890000], [589444], [695870], [458962], [698745], [365500]]
    # test = [[1], [0], [1], [1], [1], [0], [0]]
    knn = KNeighborsClassifier(n_neighbors=1)

    # x = np.reshape(list,(-1,1)).T

    knn.fit(list, dpnt)
    rs = knn.predict(test)

    #for rslt in rs:
       # print(rslt)
    custname = request.session['loginid']
    # hstr = CustomerCloudData.objects.filter(custname=custname).values('servicename').distinct()
    hstr = CustomerCloudData.objects.filter(custname=custname).values('servicename').distinct().annotate(
        count=Count('servicename')).order_by("servicename")
    #print("Hello ", hstr)
    hisDict = {}
    mylist = []
    for x in hstr:
        hisDict.update({x['servicename']: x['count']})
    #knnDict = {}
    if len(hisDict) != 0:
        for keys, values in hisDict.items():
            print(keys, "==", values)
            knnDict = knnalgorithm(keys)
            for kk,vv in knnDict.items():
                #print(keys,"==",kk,"==",vv)
                KNNSuggestionModel.objects.create(username=custname,email=email,servicename=keys,knnsuggestions=kk,distance=vv)
                #Store Suggestions In database
            mylist.append(knnDict)
            # if knnSu is not None:
            # knnDict.update({knnSu:distVal})
    #print('Ram=',knnDict)
    #print('Alex List=', mylist)

    for list in mylist:
        print('List Dict ',list)
        for xy,yz in list.items():
            knnDict.update({xy:yz})

    # knnalgorithm('Microsoft Office')
    return render(request, 'users/ServiceExplore.html', {'dict': dict, 'hisDict': hisDict})


def CustUploadData(request):
    if request.method == 'POST':
        datatype = request.POST.get('datatype')
        location = request.POST.get('location')
        servicename = request.POST.get('service')
        # filename = request.POST.get('file')
        custname = request.session['loginid']
        email = request.session['email']
        myfile = request.FILES['file']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        CustomerCloudData.objects.create(custname=custname, datatype=datatype, email=email, location=location,
                                         servicename=servicename, filename=filename, file=uploaded_file_url)
        messages.success(request, 'Data uploaded to Cloud')

    return redirect('CustExploreService')


def CustomerViewData(request):
    custname = request.session['loginid']
    data = CustomerCloudData.objects.filter(custname=custname)
    return render(request, 'users/CustViewData.html', {'data': data})

def CustSuggestions(request):
    custname = request.session['loginid']
    data = KNNSuggestionModel.objects.filter(username=custname)
    return render(request,'users/CustSuggetions.html',{'data':data})

def CustDownload(request):
    path = request.GET.get('uid')
    file_path = os.path.join("/", path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            print('Path ', path)
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404


def knnalgorithm(movie_name):
    # get args
    # args = parse_args()
    # data_path = args.path
    movies_filename = settings.MEDIA_ROOT + "\\" + 'movies.csv'
    ratings_filename = settings.MEDIA_ROOT + "\\" + 'ratings.csv'
    movie_name = movie_name #'Microsoft Office'
    top_n = 1  # args.top_n
    # initial recommender system
    recommender = KnnRecommender(
        os.path.join('', movies_filename),
        os.path.join('', ratings_filename))
    # set params
    recommender.set_filter_params(50, 50)
    recommender.set_model_params(20, 'brute', 'cosine', -1)
    # make recommendations
    rslt = recommender.make_recommendations(movie_name, top_n)
    #print('X value is =', x)
    #print('Y value is =', y)
    return rslt
