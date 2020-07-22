import sqlite3
import os

class database:
	def __init__(self, filename):
		self.filename = filename
		
	def initialize(self):
		self.connection = sqlite3.connect(self.filename)
		self.navigate = self.connection.cursor()

		database_name = 'user data.db'
		# if database_name in [x for x in os.listdir()]: 
		self.navigate.execute("""CREATE TABLE userdata(
			Name text, 
			Email text, 
			Gender text, 
			age integer, 
			birthday text,
			password text

			)""")
		# else:
		# 	pass

	def insert_data(self, data):
		with self.connection:
			self.navigate.execute("""INSERT INTO userdata VALUES(
				:Name, :Email, :Gender, :age, :birthday, :password)""",
				{'Name':data.name, 'Email':data.email, 'Gender':data.gender, 
				'age':data.age, 'birthday':data.birthday, 'password':data.password})

	def fetcher(self, name):
		self.navigate.execute("SELECT * FROM userdata WHERE Name=:Name", {'Name':name})
		self.retrived_data = self.navigate.fetchone()
		return self.retrived_data

if __name__ == '__main__':
	def test():
		db = database(":memory:")
		db.initialize()
		class data:
			def __init__(self, name, email, gender, age, birthday, password):
				self.name = name
				self.email = email
				self.gender = gender
				self.age = age
				self.birthday = birthday
				self.password = password
		user1 = data('Aman', 'aman1234@gmail.com', 'male', 17, '20 April 2003', '1234')
		user2 = data('Kuldeep', 'kuldeep2032004@gmail.com', 'male', 17, '20 March 2003', '12345')

		db.insert_data(user1)
		db.insert_data(user2)

		print(db.fetcher('Kuldeep Yadav'))
		
	test()



		
