"""PresagingTechnique URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from PresagingTechnique import  views as mainview
from users import views as usr
from cloud import views as cloud
from csp import views as csp
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',mainview.index,name='index'),
    path('index',mainview.index,name='index'),
    path('custRegistration/',mainview.custRegistration,name='custRegistration'),
    path('CustLogin/',mainview.CustLogin,name='CustLogin'),
    path('CloudLogin/',mainview.CloudLogin,name='CloudLogin'),
    path('CspLogin/',mainview.CspLogin,name='CspLogin'),
    path('Logout/',mainview.Logout,name='Logout'),

    ####Users URLS
    path('UserLoginCheck/',usr.UserLoginCheck,name='UserLoginCheck'),
    path('CustExploreService/',usr.CustExploreService,name='CustExploreService'),
    path('CustUploadData/',usr.CustUploadData,name='CustUploadData'),
    path('CustomerViewData/',usr.CustomerViewData,name='CustomerViewData'),
    path('CustDownload/',usr.CustDownload,name='CustDownload'),
    path('CustSuggestions/',usr.CustSuggestions,name='CustSuggestions'),


    ###Cloud All URL paths
    path('CloudLoginCheck/',cloud.CloudLoginCheck,name='CloudLoginCheck'),
    path('CloudCustomers/',cloud.CloudCustomers,name='CloudCustomers'),
    path('CloudActivateUsers/',cloud.CloudActivateUsers,name='CloudActivateUsers'),
    path('CloudCSPAdding/',cloud.CloudCSPAdding,name='CloudCSPAdding'),
    path('CloudCreateCsp/',cloud.CloudCreateCsp,name='CloudCreateCsp'),
    path('CloudDataView/',cloud.CloudDataView,name='CloudDataView'),


    ###CSP ALL URL Configurations
    path('CSPLoginCheck/',csp.CSPLoginCheck,name='CSPLoginCheck'),
    path('getCSPLoginDetails/',csp.getCSPLoginDetails,name='getCSPLoginDetails'),
    path('GetCSPLoginData/',csp.GetCSPLoginData,name='GetCSPLoginData'),
    path('CspDataView/',csp.CspDataView,name='CspDataView'),
    path('CspViewSuggested/',csp.CspViewSuggested,name='CspViewSuggested'),


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)