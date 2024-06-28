import requests
from bs4 import BeautifulSoup
import re
import random
import time

t = time.process_time()

url = "https://tcioe.edu.np"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")
text_content = soup.get_text()
words = text_content.split()

filtered_words = [word for word in words if len(word) >= 3]

substitutions = {
	'a': '@',
	'e': '3',
	'i': '1',
	'o': '0',
	's': '$'
}

password_list = []
for word in filtered_words:
	password_list.append(word.lower())
	password_list.append(word.lower() + "123")
	password_list.append(word.lower() + "@123")


	for other_word in filtered_words:
    	if other_word != word:
        	password_list.append(word + other_word.lower())
        	password_list.append(word.lower() + other_word.lower())
        	password_list.append(word.lower() + "@" + other_word.lower())
        	converted_word = ''.join([substitutions.get(char.lower(), char) for char in word])
        	password_list.append(converted_word + other_word)

password_list = list(set(password_list))
password_list = [pwd for pwd in password_list if len(pwd) >= 8 and pwd.isascii()]
password_list = [password for password in password_list if not re.search(r'[,().]', password)]
random.shuffle(password_list)
output_file = "password_list.txt"
with open(output_file, "w") as file:
	file.write("\n".join(password_list))

print("Password list generated and saved to", output_file)
