import sqlite3
import os
print(os.getcwd())

connection = sqlite3.connect('user_data.db')

navigation = connection.cursor()
navigation.execute("""CREATE TABLE userdata(
					Name text, 
					Email text, 
					Gender text, 
					age integer, 
					birthday text,
					password text
	                              )""")
def insert_data(data):
	with connection:
		navigation.execute("""INSERT INTO userdata VALUES(:Name, :Email, :Gender, :age, :birthday, :password)""",
			{'Name':data.name, 'Email':data.email, 'Gender':data.gender, 'age':data.age, 'birthday':data.birthday,'password':data.password})

def fetcher(data):
	navigation.execute("SELECT * FROM userdata WHERE Name= :Name", {'Name':data})
	x = navigation.fetchone()
	return x

class data:
	def __init__(self, name, email, gender, age, birthday, password):
		self.name = name
		self.email = email
		self.gender = gender
		self.age = age
		self.birthday = birthday
		self.password = password

user1 = data('Aman Yadav', 'assassins2032004@gmail.com', 'male', 17, '20 April 2003', '1234')
user2 = data('Kuldeep Yadav', 'kuldeep2032004@gmail.com', 'male', 17, '20 March 2003', '12345')

insert_data(user1)
insert_data(user2)

print(fetcher('Kuldeep Yadav')[1])

connection.close()



