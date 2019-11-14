import requests
import json

session = requests.Session()
token = False
#session.verify = False
#session.proxies = { 'https': 'http://127.0.0.1:8080' }

def update_headers(func):
	global session, token
	if func == "init":
		session.headers.update(
			{
					"Meijer-Version": "iPhone/5.28.1",
					"Accept-Language": "en-US;q=1",
					"User-Agent": "Meijer/5.28.1 (iPhone; iOS 13.1.3; Scale/2.00)", 
					"Content-Type": "application/x-www-form-urlencoded",
					"Accept": "application/json",
					"Accept-Encoding": "gzip, deflate, br",
					"Authorization": "Basic bW1hOmRyQXFhczc2UmU3UmVrZUJhbmFNYU5FTWFoN3BhREU1"
			}
		)
		return()
	if func == "init":
		session.headers.update(
			{
					"Meijer-Version": "iPhone/5.28.1",
					"Accept-Language": "en-US;q=1",
					"User-Agent": "Meijer/5.28.1 (iPhone; iOS 13.1.3; Scale/2.00)", 
					"Content-Type": "application/x-www-form-urlencoded",
					"Accept": "application/json",
					"Accept-Encoding": "gzip, deflate, br",
					"Authorization": "Basic bW1hOmRyQXFhczc2UmU3UmVrZUJhbmFNYU5FTWFoN3BhREU1"
			}
		)
		return()
	if func == "get_account_properties":
		session.headers.update(
			{
					"Version": "5.28.1",
					"Accept-Language": "en-us",
					"User-Agent": "Meijer/504 CFNetwork/1107.1 Darwin/19.0.0", 
					"Content-Type": "application/json",
					"Accept": "application/vnd.meijer.digitalmperks.accountproperties-v1.0+json",
					"Accept-Encoding": "gzip, deflate, br",
					"Authorization": "Bearer " + token,
					"Build": "504",
					"Platform": "iOS"
			}
		)
		return()
	if func == "get_all_meijer_coupons":
		session.headers.update(
			{
					"Version": "5.28.1",
					"Accept-Language": "en-US;q=1",
					"User-Agent": "Meijer/5.28.1 (iPhone; iOS 13.1.3; Scale/2.00)", 
					"Content-Type": "application/vnd.meijer.digitalmperks.offers-v1.0+json",
					"Accept": "application/vnd.meijer.digitalmperks.offers-v1.0+json",
					"Accept-Encoding": "gzip, deflate, br",
					"Authorization": "Bearer " + token,
					"Build": "504",
					"Platform": "iOS",
					"Meijer-Version": "iPhone/5.28.1"
			}
		)
		return()
	if func == "clip_meijer_coupon":
		session.headers.update(
			{
					"Version": "5.28.1",
					"Accept-Language": "en-us",
					"User-Agent": "Meijer/504 CFNetwork/1107.1 Darwin/19.0.0", 
					"Content-Type": "application/vnd.meijer.digitalmperks.clip-v1.0+json",
					"Accept": "application/vnd.meijer.digitalmperks.clip-v1.0+json",
					"Accept-Encoding": "gzip, deflate, br",
					"Authorization": "Bearer " + token,
					"Build": "504",
					"Platform": "iOS",
					"Meijer-Version": "iPhone/5.28.1"
			}
		)
		return()
	if func == "unclip_meijer_coupon":
		session.headers.update(
			{
					"Version": "5.28.1",
					"Accept-Language": "en-us",
					"User-Agent": "Meijer/504 CFNetwork/1107.1 Darwin/19.0.0", 
					"Content-Type": "application/vnd.meijer.digitalmperks.unclip-v1.0+json",
					"Accept": "application/vnd.meijer.digitalmperks.unclip-v1.0+json",
					"Accept-Encoding": "gzip, deflate, br",
					"Authorization": "Bearer " + token,
					"Build": "504",
					"Platform": "iOS",
					"Meijer-Version": "iPhone/5.28.1"
			}
		)
		return()
	if token:
		session.headers.update(
			{
					"Meijer-Version": "iPhone/5.28.1",
					"Accept-Language": "en-US;q=1",
					"User-Agent": "Meijer/5.28.1 (iPhone; iOS 13.1.3; Scale/2.00)", 
					"Content-Type": "application/vnd.meijer.account.account-v1.0+json",
					"Accept": "application/vnd.meijer.account.updateConfirmation-v1.0+json",
					"Accept-Encoding": "gzip, deflate, br",
					"Authorization": "Bearer " + token
			}
		)
		return()


def create_meijer_account (phone, password, firstname, lastname, email, zipcode, storeId, pin):
	update_headers("create_meijer_account")
	global session
	createurl = 'https://mservices.meijer.com/dgtlmma/accounts/createAccountwithMperks'
	payload = {
									"phoneNumber":phone,
									"password":password,
									"firstName":firstname,
									"IsMeijerNewsEmailEnabled":"false",
									"isMperksTextEnabled":"false",
									"email":email,
									"zip":zipcode,
									"storeId":storeId,
									"enrollInPharmacy":"true",
									"pin":pin,
									"lastName":lastname
						}
	r = session.post(createurl, data=json.dumps(payload))
	rjson = r.json()
	if not rjson["success"]:
		print(rjson["errorMessage"])
		return (False)
	else:
		return(rjson["accountId"])

def init_meijer_connection_guest():
	global session, token
	update_headers("init")
	payload = { 'grant_type': 'client_credentials' }
	r = session.post('https://login.meijer.com/as/token.oauth2', data=payload)
	token = r.json()["access_token"]

def init_meijer_connection_user(username, password):
	global session, token
	update_headers("init")
	payload = { 
									"grant_type": "password",
									"password": password,
									"scope": "openid",
									"username": username
						 }
	r = session.post('https://login.meijer.com/as/token.oauth2', data=payload)
	if r.json().get("access_token"):
		token = r.json()["access_token"]
		return(True)
	else:
		print (r.json()["error_description"])
		return(False)

def get_account_properties():
	global session, token
	if not token:
		print("Please login first.")
		return(False)
	update_headers("get_account_properties")
	propertiesurl = 'https://mperksservices.meijer.com/dgtlmPerksMMA/api/customer/Account/Properties'
	r=session.get('https://mperksservices.meijer.com/dgtlmPerksMMA/api/customer/Account/Properties')
	return(r.json())

def get_all_meijer_coupons():
	global session, token
	if not token:
		print ("Must login first!")
		return(False)
	properties = get_account_properties()
	update_headers("get_all_meijer_coupons")
	zipcode = properties["zipCode"]
	storeId = properties["storeId"]
	couponurl = 'https://mperksservices.meijer.com/dgtlmPerksMMA/api/Offers'
	payload = {
								"sortType":"BySuggested",
								"offerClass":1,
								"storeId":storeId,
								"zip":zipcode,
								"pageSize":9999,
								"categoryId":"All",
								"showClippedCoupons": False	
	}
	r=session.post(couponurl, data=json.dumps(payload))
	rjson = r.json()
	coupons = rjson.get("listOfCoupons")
	if coupons:
		return(coupons)
	else:
		return(False)

def get_all_clipped_meijer_coupons():
	global session, token
	if not token:
		print ("Must login first!")
		return(False)
	properties = get_account_properties()
	update_headers("get_all_meijer_coupons")
	zipcode = properties["zipCode"]
	storeId = properties["storeId"]
	couponurl = 'https://mperksservices.meijer.com/dgtlmPerksMMA/api/Offers/ClippedOffers'
	payload = {
									"categoryId":"All",
									"pageSize":9999,
									"offerClass":1,
									"sortType":"ByDepartmentSuggested"
						}
	r=session.post(couponurl, data=json.dumps(payload))
	rjson = r.json()
	coupons = rjson.get("listOfCoupons")
	if coupons:
		return(coupons)
	else:
		return(False)

def clip_meijer_coupon(meijerOfferId):
	global session, token
	if not token:
		print("Must login first!")
		return(False)
	update_headers("clip_meijer_coupon")
	clipurl = 'https://mperksservices.meijer.com/dgtlmPerksMMA/api/offers/clip'
	payload = { "meijerOfferId": meijerOfferId }
	r=session.post(clipurl, data=json.dumps(payload))
	if r.json()["result"] == 'Success':
		return(True)
	else:
		return(r.json()["result"])
		
def unclip_meijer_coupon(meijerOfferId):
	global session, token
	if not token:
		print("Must login first!")
		return(False)
	update_headers("unclip_meijer_coupon")
	clipurl = 'https://mperksservices.meijer.com/dgtlmPerksMMA/api/offers/unclip'
	payload = { "meijerOfferId": meijerOfferId }
	r=session.post(clipurl, data=json.dumps(payload))
	if r.json()["result"] == 'Success':
		return(True)
	else:
		return(False)