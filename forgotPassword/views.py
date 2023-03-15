from django.shortcuts import render
from Signup.models import Users
# from models import UpdateUserDetails
from django.contrib import messages
from django.contrib.auth.hashers import make_password



def verify(request):
    if request.method == 'POST':
        userEmail = request.POST.get('email')
        print("&&& Entered email &&&: ", userEmail)
        data = Users.objects.all().filter(email = userEmail).values_list()

        # Verifying if the entered email is present or not
        if(len(data) == 0):
            print("user data:", data)
            messages.error(request, "Account not registered")
            return render(request, "forgotpassword.html")
        else:
            userData = data[0]
            # Getting the actual username and password saved in the "users" table
            actualUserName = userData[1]
            actualPassword = userData[2]
            data = {'username':actualUserName}
            return render(request, "resetpassword.html", data)
    else:
        return render(request, "forgotpassword.html")

def resetpassword(request):
    if request.method == 'POST':
        user_name = request.session['username']
        print("entered password for reset:",request.POST.get('password'))
        password_reset = make_password(request.POST.get('password'))
        # password_reset = request.POST.get('password')
        print("encrypted password for reset:",password_reset)


        data = Users.objects.all().filter(userName = user_name).update(password = password_reset)
        messages.error(request,"Password has been reset successfully.")
        return render(request, "login.html")
    else:
        return render(request, "login.html")
        



