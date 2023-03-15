"""Project_Amyca URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path,include, re_path
from Signup.views import signup,homepage,payment,landing_page,getAllUserNames
from Login.views import login,userHomePage,upload_csv, forgotpassword,logout,subscription_plans,subscription_payment,addCategory,addCategoryData,getReports
from forgotPassword.views import verify,resetpassword



urlpatterns = [
    path('admin/', admin.site.urls),
    path("", landing_page),
    re_path(r'.*signup/$', signup),
    re_path(r'.*login/$', login),
    re_path(r'.*payment/$', payment),
    re_path(r'.*homepage/$', homepage),
    re_path(r'.*subscription_plans/$', subscription_plans),
    re_path(r'.*subscription_payment/$', subscription_plans),
    # re_path(r'.*userHomePage/$', userHomePage),
    re_path(r'.*upload_csv/',upload_csv),
    re_path(r'.*forgot_password/$', forgotpassword),
    re_path(r'.*verify/$', verify),
    re_path(r'.*resetpassword/$', resetpassword),
    re_path(r'.*logout/$', logout),
    re_path(r'.*getAllUserNames',getAllUserNames),
    re_path(r'.*addCategory/',addCategory),
    re_path(r'.*addCategoryData/',addCategoryData),
    re_path(r'.*getReports/',getReports)


]
