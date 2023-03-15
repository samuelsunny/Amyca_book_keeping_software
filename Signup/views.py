from django.shortcuts import render
from Signup.models import Users, Subscriptions
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.http import JsonResponse

data = {}
global planType
def signup(request):
    print("RECEIVED POST")

    if request.method == 'POST':
        # return render(request, "index.html")
        username = request.POST.get('name')
        useremail = request.POST.get('email')
        business_name = request.POST.get('businessName')
        contact_number = request.POST.get('contactNumber')
        password = request.POST.get('password')
        confirmed_password = request.POST.get('confirmedPassword')

        print("RECEIVED POST - enter", username, useremail, business_name, contact_number, password, confirmed_password)
        # if request.POST.get('name') and request.POST.get('email') and request.POST.get('businessName') and\
        #     request.POST.get('contactNumber') and request.POST.get('password') and request.POST.get('confirmPassword'):
        print("RECEIVED POST - got")
        # Checking whether the entered username is in the DB table or not
        username_in_db = Users.objects.all().filter(userName = username).values_list()

        # Checking whether the entered email is in the DB table or not
        email_in_db = Users.objects.all().filter(email = useremail).values_list()

        # print("Data in DB:", len(data_in_db))

        
            
        # If the entered user details are not already in DB table "users", then we store the entered details
        if len(email_in_db) == 0:
            # Checking if the entered username is already in the DB table "users"
            # If it is already present then we display a message
            if len(username_in_db) != 0:
                messages.error(request,"Username already exists. Choose another username.")
                return render(request, "signup.html")
            # If both the username and email are unique then the account is considered as unique and the details \
            # are registered in the "users" table
            else:
                saveRecord = Users()
                saveRecord.userName = username
                            
                # Encrypting the entered password before storing it.
                password = make_password(confirmed_password)
                saveRecord.password = password

                saveRecord.email = useremail
                saveRecord.businessName = business_name
                saveRecord.contactNumber = contact_number

                saveRecord.save()
                messages.error(request,"Account created successfully.")
                return render(request, "login.html")
        
        # If the user details are already present in the "users" table then we prompt them to login with their credentials
        else:
            messages.error(request,"Email already exists. Choose another one.")
            return render(request, "signup.html")

    # To handle the GET requests to signup page
    else:
        return render(request, "signup.html")

def homepage(request):
    if request.session['sessionId'] == "":
        return render(request, "homepage.html")
    else:
        username = request.session['username']
        data = {'username' : username}
        return render( request, "userhomepage.html", data)

def landing_page(request):
  
    # if request.session['sessionId'] == "":
    #     return render(request, "landingpage.html")
    # else:
    #     username = request.session['username']
    #     data = {'username' : username}
    #     return render( request, "userhomepage.html", data)
    
    try:
        if request.session['sessionId'] == "":
            return render(request, "landingpage.html")
        else:
            username = request.session['username']
            data = {'username' : username}
            return render( request, "userhomepage.html", data)
    except:
        request.session['sessionId'] = ""
        request.session['username'] = ""
        request.session['userId'] = ""
        request.session['subscriptionId'] = ""
        request.session['subscriptionPlan'] = ""
        if request.session['sessionId'] == "":
            return render(request, "landingpage.html")

def payment(request):
    if request.session['username']=='':
        print("inside")
        return render(request, "login.html")
    print("This iw ",request.session['username'])
    if request.method == "POST":
        selectedPlanType = request.session['planType']
        print("Plan type:", selectedPlanType)
        # Checking if the user has already subscribed to a plan
        subscribed_by_user= Subscriptions.objects.all().filter(userId = request.session['userId']).values_list()
        print("subscribed_by_user",len(subscribed_by_user))
        # If there is an existing subscription then we update it with newly upgraded subscription
        if len(subscribed_by_user) != 0:
            updating_user_subscription = Subscriptions.objects.all().filter(userId = request.session['userId']).update(planType = selectedPlanType)
        # Else we save the subscription details as a new entry into the subscriptions table
        else:
            saveSubcriptionRecord = Subscriptions()
            saveSubcriptionRecord.planType = selectedPlanType
            saveSubcriptionRecord.userId = request.session['userId']
            saveSubcriptionRecord.paymentMethod = "Credit/Debit card"
            saveSubcriptionRecord.save()
            # To get the subscriptionId of the newly added subscription details from the subscriptions table
            data = Subscriptions.objects.all().filter(userId = request.session['userId']).values_list()
            userdata = Users.objects.get(pk = request.session['userId']).__dict__
            print("User data:", userdata)
            newsubscriptionId = data[0][0]
            for i in range(len(data)):
                print(i,"th subscription Id:", data[i][0])
            user_name = request.session['username']
            updated_subscription_Id = Users.objects.all().filter(userName = user_name).update(subscriptionId = newsubscriptionId)

        data_to_template = {
            'username' :request.session['username'],
            'subscriptionId': request.session['subscriptionId'],
            'userId': request.session['userId'],
            'subscriptionPlan':request.session['subscriptionPlan']
        }
        

        return render( request, "payment_success.html", data_to_template)
    else:
        try:
            print(request.GET['planType'])
            request.session['planType'] = request.GET['planType']
            return render(request, "paymentpage.html")
        except:
            return render(request, "userHomePage.html")

def getAllUserNames(request):
        existingData = Users.objects.all().values()
        # print("this is existing data",existingData)
        return JsonResponse(list(existingData), safe=False)