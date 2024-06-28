scope 
    \*.sunstone.ctfio.com
found a subdomain data.sunstone.ctfio.com

got a flag by visiting data sub [^FLAG^E78DEBBFDFBEAFF1336B599B0724A530^FLAG^]

found on main website
/login (301) -> redirects to /denied (401) : Access denied for my ip

found on data subdomain
/users (200) -> a list of users and got a flag [^FLAG^25032EB0D322F7330182507FBAA1A55F^FLAG^]


used curl to access /login on main site and got found another endpoint
/lawyers-only(302) -> redirects to lawyers-only-login and also a flag [^FLAG^FB52470E40F47559EBA87252B2D4CF67^FLAG^]

made a bruteforce script in python and got 

    jaskaran.lowe@vulnlawyers.ctf
    summer
logged in and found a flag [^FLAG^7F1ED1F306FC4E3399CEE15DF4B0AE3C^FLAG^]
there is a manager by name Shayne Cairns who can update the running case

there is also /lawyers-only-profile endpoint which shows the current user's profile details. Checked the source of this page and found a jquery that is getting json from /lawyers-only-profile-details/4

assuming 4 to be the current userid

bruh this also returns the password of the given user id

made a script to iterate through all the ids and got all user's passwords and a flag [^FLAG^938F5DC109A1E9B4FF3E3E92D29A56B3^FLAG^]

logged in as shayne and deleted the case and got the final flag [^FLAG^B38BAE0B8B804FCB85C730F10B3B5CB5^FLAG^]
