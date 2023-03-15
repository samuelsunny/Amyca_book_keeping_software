from django.shortcuts import render
from Signup.models import Users, Subscriptions
from Login.models import Income, Expense, Keywords
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.views.decorators.csrf import csrf_exempt

from io import StringIO
import pandas as pd
import json, os

def login(request):
	print("LOGIN")
	if request.method == 'POST':
		# Checking if the user is in session
		try:
			if(request.session['sessionId'] == ""):
				username = request.POST.get('userName')
				password = request.POST.get('password')
				print("&&& LOGIN &&&: ", username, password)

				# Getting the user details
				data = Users.objects.all().filter(userName = username).values_list()
				print("Data: ", data[0])
				if(len(data) == 0):
					messages.error(request,"Account not registered.")
					return render(request, "login.html")

				else:
					userData = data[0]
					print("User details: ",userData)
					# Getting the actual username and password
					userId = userData[0]
					actualUserName = userData[1]
					actualPassword = userData[2]
					subscriptionId = userData[6]
					print("subId", subscriptionId)
					if subscriptionId == None:
						subscriptionPlan = "None"
					else:
						sub_data = Subscriptions.objects.all().filter(subscriptionId = subscriptionId).values_list()
						print("subscription details:", sub_data)
						subscriptionPlan = sub_data[0][2]

					# 	print("sub_data",sub_data[0])
					# 	try:
					# 		subscriptionPlan = sub_data[0][2]
					# 		print("Subscription plan:", subscriptionPlan)
					# 	except:
					# 		print("sub problem")
					# 	print("subplan", subscriptionPlan)


					# Checking whether the entered passowrd and the stored encrypted password are correct or not
					passwordIsCorrect = check_password(password, actualPassword)


					print("Encrypted password:",actualPassword, check_password(password, actualPassword), passwordIsCorrect)

					print("USER DETAILS: ", list(userData), "correct?", passwordIsCorrect)
				
					if(username == actualUserName and passwordIsCorrect):
						# Using encrypted password as the session Id
						request.session['sessionId'] = actualPassword
						request.session['username'] = actualUserName
						request.session['userId'] = userId
						request.session['subscriptionId'] = subscriptionId
						request.session['subscriptionPlan'] = subscriptionPlan


						
						print("Right credentials")
						data_to_template = {
							'username' :request.session['username'],
							'subscriptionId': request.session['subscriptionId'],
							'userId': request.session['userId'],
							'subscriptionPlan':request.session['subscriptionPlan']
						}
						return render( request, "userhomepage.html", data_to_template)
					else:
						messages.error(request,"Incorrect password. Enter right credentials.")
						return render(request, "login.html")
					
			# If thes user is not in the session directing the user to the login page
			else:
				print("in else")
				request.session['sessionId'] = ""
				request.session['username'] = ""
				request.session['userId'] = ""
				request.session['subscriptionId'] = ""
				request.session['subscriptionPlan'] = ""
				print("session:", request.session['sessionId'])
				return render(request, "login.html")
		except:
			print("in excpet")
			request.session['sessionId'] = ""
			request.session['username'] = ""
			request.session['userId'] = ""
			request.session['subscriptionId'] = "None"
			request.session['subscriptionPlan'] = "None"
			print("session:", request.session['sessionId'])
			messages.error(request,"Incorrect username. Please check.")
			return render(request, "login.html")
			 
	# For handling GET request to '/login/'
	else:
		# If the user is not in the session then directing the user to the login page
		if(request.session['sessionId'] == ""):
			request.session['sessionId'] = ""
			request.session['username'] = ""
			request.session['userId'] = ""
			request.session['subscriptionId'] = ""
			request.session['subscriptionPlan'] = ""
			print("session:", request.session['sessionId'])
			return render(request, "login.html")
		# If the user is in the session then directing the requests to "/" to the homepage
		else:
			print("session:", request.session['sessionId'])
			data = {'username' : request.session['username']}
			return render( request, "userhomepage.html", data)

# To handle logout
def logout(request):
	request.session['sessionId'] = ""
	request.session['username'] = ""
	request.session['userId'] = ""
	request.session['subscriptionId'] = ""
	request.session['subscriptionPlan'] = ""
	os.remove("tempTransactionData.json")

	print(request.path)
	messages.error(request,"Logged out successfully.")
	return render(request, "landingpage.html")

def userHomePage(request):
	return render(request, "userHomePage.html")

def forgotpassword(request):
	return render(request, "forgotpassword.html")

def subscription_plans(request):
	# Getting the subscription plan details of the logged in user
	data = Users.objects.all().filter(userName = request.session['username']).values_list()
	userData = data[0]
	print("User details: ",userData)
	subscriptionId = userData[6]
	print("subId for subscription plan: ", subscriptionId)
	if subscriptionId == None:
		subscriptionPlan = "None"
	else:
		sub_data = Subscriptions.objects.all().filter(subscriptionId = subscriptionId).values_list()
		print("subscription details of subscription plan:", sub_data)
		subscriptionPlan = sub_data[0][2]

		# 	print("sub_data",sub_data[0])
		# 	try:
		# 		subscriptionPlan = sub_data[0][2]
		# 		print("Subscription plan:", subscriptionPlan)
		# 	except:
		# 		print("sub problem")
		# 	print("subplan", subscriptionPlan)
		request.session['subscriptionPlan'] = subscriptionPlan

	data_to_template = {
							'username' :request.session['username'],
							'subscriptionId': request.session['subscriptionId'],
							'userId': request.session['userId'],
							'subscriptionPlan':request.session['subscriptionPlan']
						}

	print("Data template: ", data_to_template)
	return render(request, "subscription_plans.html", data_to_template)

def subscription_payment(request):
	print("inside subcription")
	# return render( request, "payment_success.html")

	if request.method == 'POST':
		print("INSIDE SUBSCRIPTION post")

		# Checking if the user is in session
		try:
			if(request.session['sessionId'] == ""):
				return render(request, "login.html")
			else:
				return render(request, "payment_success.html")
		except:
			request.session['sessionId'] = ""
			print("session:", request.session['sessionId'])
			return render(request, "login.html")
	else:
		print("INSIDE SUBSCRIPTION get")

		# If the user is not in the session then directing the user to the login page
		if(request.session['sessionId'] == ""):
			request.session['sessionId'] = ""
			print("session:", request.session['sessionId'])
			return render(request, "login.html")
		# If the user is in the session then directing the requests to "/" to the homepage
		else:
			print("session:", request.session['sessionId'])
			data = {'username' : request.session['username']}
			return render( request, "paymentpage.html", data)
			   
	

def upload_csv(request):
	totalData={}
	
	if request.method == "GET":
		try:
			if(request.session['sessionId'] != ""):
				data_to_template = {
						'username' :request.session['username'],
						'subscriptionId': request.session['subscriptionId'],
						'userId': request.session['userId'],
						'subscriptionPlan':request.session['subscriptionPlan']
					}
				return render(request, "userhomepage.html", data_to_template)
			else:
				print("in else")
				request.session['sessionId'] = ""
				request.session['username'] = ""
				request.session['userId'] = ""
				request.session['subscriptionId'] = "None"
				request.session['subscriptionPlan'] = "None"
				print("session at addCategory():", request.session['sessionId'])
				return render(request, "login.html")
		except:
			print("in excpet")
			request.session['sessionId'] = ""
			request.session['username'] = ""
			request.session['userId'] = ""
			request.session['subscriptionId'] = "None"
			request.session['subscriptionPlan'] = "None"
			print("session at addCategory():", request.session['sessionId'])
			return render(request, "login.html")
	# if it is a POST, then proceed
	else:
		try:
			if(request.session['sessionId'] != ""):
				csv_file = request.FILES.getlist('csv_file')

				file_name=""
			
				i=0
				for file in csv_file:
					i+=1
					temp='data'
					temp+=temp+str(i)
					check=temp
					temp={}
					income_data = []
					expenditure_data  = []
					expenditure_amount = []
					income_amount = []
					file_name = file.name
				# if not csv_file.name.endswith('.csv'):
				# 	messages.error(request,'File is not CSV type')
				# 	return render(request, "userhomepage.html")
				#if file is too large, return
					if file.multiple_chunks():
						messages.error(request,"Uploaded file is too big (%.2f MB)." % (file.size/(1000*1000),))
						return HttpResponseRedirect(reverse("myapp:upload_csv"))

					file_data = file.read().decode("utf-8")		
					# data = pd.read_csv(file_data)
					lines = file_data.split("\n")
				
					# print(lines[0], type(lines[0]))
					d = lines[0]
					headers = d.split(",")
					# print("HEADERS:", headers)1
					for i in range(len(headers)):
						header = headers[i].replace("\r","")
						# print("print header ",header)
						temp[header] = []

					for each_line in range(1,len(lines)-1):
						# print(lines[each_line])2
						row_data = lines[each_line].split(",")
						# for value in row_data:
						# 	print("Each value: ", value)

						temp['Details'].append(row_data[0])
						temp['Posting Date'].append(row_data[1])
						temp['Description'].append(row_data[2])
						temp['Amount'].append(row_data[3])
						temp['Type'].append(row_data[4].replace("\r",""))
					# print("This is check",check)
					
					# print("THIS is TEmp ......",temp)
					# totalData[check]=temp
					# talData",totalData)
					df = pd.DataFrame(temp)
					all_transactions = df["Details"].tolist()
					# print(df, df.loc[0,"Details"], len(df))
					for transaction_number in range(len(all_transactions)):
						if df.loc[transaction_number,"Details"] == "DEBIT":
							expenditure_amount.append(float(df.loc[transaction_number,"Amount"]))
							expenditure_data.append(df.loc[transaction_number].tolist())
						elif df.loc[transaction_number,"Details"] == "CREDIT":
							income_amount.append(float(df.loc[transaction_number,"Amount"]))
							income_data.append(df.loc[transaction_number].tolist())

					data_to_store = { file_name:{
						'profit_data':income_data,
						'loss_data' :expenditure_data,
						'total_income' : sum(income_amount),
						'total_expenditure' : sum(expenditure_amount),
						'username' :request.session['username'],
						'subscriptionId': request.session['subscriptionId'],
						'userId': request.session['userId'],
						'subscriptionPlan':request.session['subscriptionPlan']}
					}

					# Storing the processed data temporarily in tempTransactionData.json
					
					try:
						# 1. Read file contents
						with open("tempTransactionData.json", "r") as file:
							data = json.load(file)
							print("Existing data:", data)
						# 2. Update the existing json data
						data.update(data_to_store)
						print("Updated data:", data)

						# 3. Write data "tempTransactionData.json" file
						with open("tempTransactionData.json", "w") as file:
							json.dump(data, file)

					except:
						# An exception occurs when there is no "tempTransactionData.json" present,
						# "w" creates the json file it is not aalready created.
						# After this we write the processed data to "tempTransactionData.json" file
						with open("tempTransactionData.json", "w") as file:
							json.dump(data_to_store, file)

					
					# print("Expenditue and income: ", sum(expenditure_amount), sum(income_amount), expenditure_data,income_data)
					# Passing data to the template(HTML page)
					keywords = Keywords.objects.values_list('sub_category', flat=True)
					data_to_template = {
						'profit_data':income_data,
						'loss_data' :expenditure_data,
						'total_income' : sum(income_amount),
						'total_expenditure' : sum(expenditure_amount),
						'username' :request.session['username'],
						'subscriptionId': request.session['subscriptionId'],
						'userId': request.session['userId'],
						'subscriptionPlan':request.session['subscriptionPlan'],
						'keywords': keywords,
						'filename':file_name
					}
				request.session['file_name'] = file_name
				# return render(request,"report.html",data_to_template)
				return render(request,"addcategory.html",data_to_template)
				# pd_data = StringIO(file_data)
				# df = pd.DataFrame(pd_data)
				# df.columns=df.iloc[0]
				# header_row = df.iloc[0]
				# processed_csv_data = pd.DataFrame(df.values[1:],columns=header_row)
				# processed_csv_data = df.rename(columns=df.iloc[0]).loc[1:]
				# new_df  = pd.DataFrame(df.values[1:], columns=header_row)
				# print(processed_csv_data['Details,Posting Date,Description,Amount,Type\r\n'], len(processed_csv_data))
				# print("Number of lines", len(lines))
				# file_data.replace('\r',"")
				# print(file_data, type(file_data))
				# for line in lines:
				# 	line.replace("\r","")
				# 	print(line)
				# print(lines)
			else:
				print("in excpet")
				request.session['sessionId'] = ""
				request.session['username'] = ""
				request.session['userId'] = ""
				request.session['subscriptionId'] = "None"
				request.session['subscriptionPlan'] = "None"
				print("session at addCategory():", request.session['sessionId'])
				return render(request, "login.html")
		except:
			print("in excpet")
			request.session['sessionId'] = ""
			request.session['username'] = ""
			request.session['userId'] = ""
			request.session['subscriptionId'] = "None"
			request.session['subscriptionPlan'] = "None"
			print("session at addCategory():", request.session['sessionId'])
			return render(request, "login.html")


def addCategory(request):
	if request.method == 'POST':
		try:
			if(request.session['sessionId'] != ""):
				print("Add category posted details:", request.POST.get('selected_category'), request.POST.get('given_sub_category'))
				category = request.POST.get('selected_category')
				given_sub_category = request.POST.get('given_sub_category')
				# If the category is "income" then adding the sub-category to income (category/account type) table
				if category == "income":
					subCategory_exists = Income.objects.all().filter(incomeCategory = given_sub_category).exists()
					print("DATA EXISTS:", subCategory_exists)
					if subCategory_exists != True:
						addingIncomeCategory = Income()
						addingIncomeCategory.incomeCategory = given_sub_category
						addingIncomeCategory.save()
						
						category_data = Income.objects.all().filter(incomeCategory = given_sub_category).values_list()
						print("FOR KEY WORDS:",category_data[0][0],category_data[0][1])
						# Adding to the "keywords" table for accessing them in the UI
						addingKeywords = Keywords()
						addingKeywords.category = "income"
						addingKeywords.categoryID = category_data[0][0]
						addingKeywords.sub_category = category_data[0][1]
						addingKeywords.save()

						# Getting all the keywords and passing them to the addcategory.html page for accessing them in the UI
						# keywordsData = Keywords.objects.all().values_list()
						# Getting a list of all the keywords
						keywords = Keywords.objects.values_list('sub_category', flat=True)

						print("All the keywords:", list(keywords))
						data_to_template = {
									'username' :request.session['username'],
									'subscriptionId': request.session['subscriptionId'],
									'userId': request.session['userId'],
									'subscriptionPlan':request.session['subscriptionPlan'],
									'keywords':keywords
								}
						return render(request,"addcategory.html", data_to_template)
					else:
						messages.error(request,"Sub-category already exists. Please choose form the list.")
						keywords = Keywords.objects.values_list('sub_category', flat=True)

						print("All the keywords:", list(keywords))
						data_to_template = {
									'username' :request.session['username'],
									'subscriptionId': request.session['subscriptionId'],
									'userId': request.session['userId'],
									'subscriptionPlan':request.session['subscriptionPlan'],
									'keywords':keywords
								}
						return render(request,"addcategory.html", data_to_template)
				elif category == "expense":
					subCategory_exists = Expense.objects.all().filter(expenseCategory = given_sub_category).exists()
					if subCategory_exists != True:
						addingExpenseCategory = Expense()
						addingExpenseCategory.expenseCategory = given_sub_category
						addingExpenseCategory.save()
						category_data = Expense.objects.all().filter(expenseCategory = given_sub_category).values_list()
						print("FOR KEY WORDS:",category_data[0][0],category_data[0][1])
						# Adding to the "keywords" table for accessing them in the UI
						addingKeywords = Keywords()
						addingKeywords.category = "expense"
						addingKeywords.categoryID = category_data[0][0]
						addingKeywords.sub_category = category_data[0][1]
						addingKeywords.save()

						# Getting all the keywords and passing them to the addcategory.html page for accessing them in the UI
						# keywordsData = Keywords.objects.all().values_list()
						# Getting a list of all the keywords
						keywords = Keywords.objects.values_list('sub_category', flat=True)

						print("All the keywords:", list(keywords))
						data_to_template = {
									'username' :request.session['username'],
									'subscriptionId': request.session['subscriptionId'],
									'userId': request.session['userId'],
									'subscriptionPlan':request.session['subscriptionPlan'],
									'keywords':keywords
								}
						return render(request,"addcategory.html", data_to_template)
					else:
						messages.error(request,"Sub-category already exists. Please choose form the list.")
						keywords = Keywords.objects.values_list('sub_category', flat=True)

						print("All the keywords:", list(keywords))
						data_to_template = {
									'username' :request.session['username'],
									'subscriptionId': request.session['subscriptionId'],
									'userId': request.session['userId'],
									'subscriptionPlan':request.session['subscriptionPlan'],
									'keywords':keywords
								}
						return render(request,"addcategory.html", data_to_template)
		except:
			print("in excpet")
			request.session['sessionId'] = ""
			request.session['username'] = ""
			request.session['userId'] = ""
			request.session['subscriptionId'] = "None"
			request.session['subscriptionPlan'] = "None"
			print("session at addCategory():", request.session['sessionId'])
			return render(request, "login.html")
		
	# For handling GET requests to addcategory.html
	else:
		try:
			if(request.session['sessionId'] != ""):
				print("In GET for add Category")
				# Getting all the keywords and passing them to the addcategory.html page for accessing them in the UI
				keywordsData = Keywords.objects.all().values_list()
				keywords = Keywords.objects.values_list('sub_category', flat=True)

				print("All the keywords:", keywordsData,list(keywords))
				data_to_template = {
							'username' :request.session['username'],
							'subscriptionId': request.session['subscriptionId'],
							'userId': request.session['userId'],
							'subscriptionPlan':request.session['subscriptionPlan'],
							'keywords':keywords
						}
				return render(request,"addcategory.html", data_to_template)
			else:
				print("in excpet")
				request.session['sessionId'] = ""
				request.session['username'] = ""
				request.session['userId'] = ""
				request.session['subscriptionId'] = "None"
				request.session['subscriptionPlan'] = "None"
				print("session at addCategory():", request.session['sessionId'])
				return render(request, "login.html")
		except:
			print("in excpet")
			request.session['sessionId'] = ""
			request.session['username'] = ""
			request.session['userId'] = ""
			request.session['subscriptionId'] = "None"
			request.session['subscriptionPlan'] = "None"
			print("session at addCategory():", request.session['sessionId'])
			return render(request, "login.html")

# @csrf_exempt		
def addCategoryData(request):
	# print("Inside add category", request.POST)
	# return render(request, "login.html")
	if request.method == 'POST':
		fileName = request.session['file_name']
		getCategory = request.POST.get('sel_category')
		getSubCategory = request.POST.get('sel_sub_category')
		print(fileName,getCategory,getSubCategory)
		existing_data={}
		with open("tempTransactionData.json", "r") as file:
			existing_data = json.load(file)
			print("Existing data:", existing_data)
		selectedCategory = {'selectedCategory' : getCategory}
		selectedSubCategory = {'selectedSubCategory' : getSubCategory}

		existing_data[fileName].update(selectedCategory) 
		existing_data[fileName].update(selectedSubCategory) 

		with open("tempTransactionData.json", "w") as file:
			json.dump(existing_data, file)

		# print("FILE CONTENTS:", existing_data[fileName]['selectedCategory'])
		data_to_template = {
							'username' :request.session['username'],
							'subscriptionId': request.session['subscriptionId'],
							'userId': request.session['userId'],
							'subscriptionPlan':request.session['subscriptionPlan']
						}
		return render(request, "uploadmore.html",data_to_template)


def getReports(request):
	if request.method == 'GET':
		file = request.GET.getlist("file")
		if len(file) != 0:
			fileName = file[0]
			with open("tempTransactionData.json", "r") as file:
				existing_data = json.load(file)
				print("Existing data:", existing_data)

			fileReport = existing_data[fileName]

			data_to_template = {
									'username' :request.session['username'],
									'subscriptionId': request.session['subscriptionId'],
									'userId': request.session['userId'],
									'subscriptionPlan':request.session['subscriptionPlan'],
									'profitData' : fileReport['profit_data'],
									'lossData'   : fileReport['loss_data'],
									'Total_Income': fileReport['total_income'],
									'Total_Expense' : abs(fileReport['total_expenditure']),
									'filename' : fileName
								}
			
			return render(request, "report.html",data_to_template)
		else:
			print("File:",request.GET.getlist("file"))
			with open("tempTransactionData.json", "r") as file:
					existing_data = json.load(file)
					# print("Existing data:", existing_data)
			files = existing_data.keys()
			data_to_template = {
									'username' :request.session['username'],
									'subscriptionId': request.session['subscriptionId'],
									'userId': request.session['userId'],
									'subscriptionPlan':request.session['subscriptionPlan'],
									'uploadedFiles' : files
								}
			
			return render(request, "getreport.html",data_to_template)

	# else:
	# 	return render(request, "login.html")

