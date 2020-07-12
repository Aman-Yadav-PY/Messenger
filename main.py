from tkcalendar import Calendar
from client import client
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from data_center import database, data
import socket
import tkinter as tk
import time
import csv



class messenger:


	def __init__(self, master):
		self.master = master
		self.notebook = ttk.Notebook(self.master)
		self.notebook.place(relx=0.018, rely=0.02, relheight=0.97, relwidth=0.97)

		self.Database = database('User data.db')
		self.Database.initialize()

	# login window
	def first_tab(self):
		self.img = ImageTk.PhotoImage(Image.open('ico.ico'))

		self.main_frame = tk.Frame(self.master)
		self.main_frame.pack()

		self.frame = tk.Frame(self.main_frame, background='#7ffc80')
		self.frame.place(relx=0.018, rely=0.02, relheight=0.97, relwidth=0.966)


		self.label1 = tk.Label(self.frame, image=self.img, background='#7ffc80')
		self.label1.place(relx=0.38, rely=0.02, relheight=0.27, relwidth=0.26)
		
		self.entry_login = ttk.Entry(self.frame, font = ['calibri', 20, 'bold'], foreground='grey')
		self.entry_login.insert(0, 'Username')
		self.entry_login.place(relx=0.18, rely=0.37, relheight=0.11, relwidth=0.7)


		self.entry_password = ttk.Entry(self.frame, font = ['calibri', 20, 'bold'], foreground='grey')
		self.entry_password.insert(0, 'Password')
		self.entry_password.place(relx=0.18, rely=0.5, relheight=0.11, relwidth=0.7)

		def sign_in():
			self.Top = tk.Toplevel()
			self.Top.geometry('600x500')
			self.top = tk.Frame(self.Top, background='green')
			self.top.place(relx=0, rely=0, relheight=1, relwidth=1)

			# name
			self.label_name = tk.Label(self.top, text='Name', font=20, background='green')
			self.label_name.place(relx=0.138, rely=0.035)
			
			self.name = ttk.Entry(self.top, font = ['calibri', 30, 'bold'])
			self.name.place(relx=0.14, rely=0.1, relheight=0.08, relwidth=0.77)

			# age
			def calendar():
				calendar_window = tk.Toplevel()
				date = Calendar(calendar_window)
				date.pack()

				def Date():
					self.DOB = date.get_date()
					m,d,y = self.DOB.split('/')

					D = time.gmtime()[0]

					self.age = ((D-2000)-int(y))
					self.calendar.config(text=self.DOB)

					date.destroy()
					calendar_window.destroy()

				date_getter = ttk.Button(calendar_window, text='Done', command=Date)
				date_getter.pack()

			self.calendar = ttk.Button(self.top, text='Birthday', command=calendar)
			self.calendar.place(relx=0.138, rely=0.20, relheight=0.11, relwidth=0.33)

			# gender
			self.label_gender = tk.Label(self.top, text='Gender', font=20, background='green')
			self.label_gender.place(relx=0.585, rely=0.2)
			
			self.gender = ttk.Combobox(self.top, value = ['Male', 'Female', 'Other'])
			self.gender.place(relx=0.586, rely=0.25, relheight=0.05, relwidth=0.33)

			# email
			self.label_email = tk.Label(self.top, text='Email', font=20, background='green')
			self.label_email.place(relx=0.13, rely=0.37)
			
			self.email = ttk.Entry(self.top, font = ['calibri', 30, 'bold'])
			self.email.place(relx=0.135, rely=0.43, relheight=0.08, relwidth=0.77)

			# passwordgender
			self.label_password = tk.Label(self.top, text='Password', font=20, background='green')
			self.label_password.place(relx=0.13, rely=0.56)
			
			self.password = ttk.Entry(self.top, font = ['calibri', 30, 'bold'])
			self.password.place(relx=0.135, rely=0.61, relheight=0.08, relwidth=0.77)

			# confirmation password
			self.label_cpassword = tk.Label(self.top, text='Confirm Password',font=20, background='green')
			self.label_cpassword.place(relx=0.13, rely=0.73)
			
			self.cpassword = ttk.Entry(self.top, font = ['calibri', 30, 'bold'])
			self.cpassword.place(relx=0.135, rely=0.78, relheight=0.08, relwidth=0.77)


			def runner():
				self.username = str(self.name.get())
				self.email_id = str(self.email.get())

				if self.password.get() == self.cpassword.get():
					self.passcode = str(self.cpassword.get())
					self.info = {'Name':self.username , 'Email':self.email_id, 'gender':self.gender.get(), 'age':self.age, 'birthdate':self.DOB, 'password':self.passcode}
					D = data(self.username, self.email_id, self.gender.get(), self.age, self.DOB, self.passcode)
					self.Database.insert_data(D)

					self.name.config(takefocus=True)
					self.Top.destroy()

				else:
					messagebox.showwarning(message='retype your password')
					length_password, length_cpassword = len(self.password.get()), len(self.cpassword.get())
					self.password.delete(0, length_password)
					self.cpassword.delete(0, length_cpassword)

					self.password.config(takefocus=True)


			self.create_btn = ttk.Button(self.top, text='Create Account', command=runner)
			self.create_btn.place(relx=0.155, rely=0.9, relheight=0.08, relwidth=0.7)


		def login():
		
			self.user = self.entry_login.get()
			password = self.entry_password.get()

			data = self.Database.fetcher(self.user)

			try:
				if self.user == data[0] or data[1]:
					if data[-1] == password:

						try:
							self.activator = client('127.0.0.1', 5050, self.label_messaging)
							self.activator.connector(data[0])


							self.notebook.select(self.all_tabs[1])

							if data[2] == 'Male':
								self.user_img = ImageTk.PhotoImage(Image.open(r'E:\neural networking\Projects\massenger\pics\USER.ico'))
							else:
								self.user_img = ImageTk.PhotoImage(Image.open(r'E:\neural networking\Projects\massenger\pics\USER1.ico'))

							self.canvas.create_image(100, 40, image=self.user_img)
							self.canvas.create_text(170, 40, text=data[0])

							self.label_conn.config(image = self.user_img)
						
						except:
							messagebox.showwarning('Connection Error', message = 'Connect to Internet.')

					else:
						self.entry_password.config(background='red')
						self.entry_password.delete(0, len(self.entry_password.get()))
			except Exception as e:
				print(e)

			else:
				self.entry_login.config(background='red')
				self.entry_login.delete(0, len(self.entry_login.get()))

		
				

		self.loginbtn = ttk.Button(self.frame, text='Login', command=login)
		self.loginbtn.place(relx=0.18, rely=0.63, relheight=0.11, relwidth=0.33)

		self.acount_btn = ttk.Button(self.frame, text='Sign in ', command=sign_in)
		self.acount_btn.place(relx=0.548, rely=0.63, relheight=0.11, relwidth=0.33)
		
		self.notebook.add(self.main_frame, text='Login')

	# contact window
	def second_tab(self):
		self.main_frame = tk.Frame(self.master)
		self.main_frame.pack()
		self.frame = tk.Frame(self.main_frame, background='blue', relief='raise')
		self.frame.place(relx=0.0, rely=0, relheight=0.3, relwidth=1)

		self.canvas = tk.Canvas(self.frame, background='#6cbdd5')
		# self.canvas.create_image(100, 40, image = self.img)
		# self.canvas.create_text(170, 40, text='User')
		self.canvas.place(relx=0, rely=0, relheight=1, relwidth=0.4)

		self.frame2 = tk.Frame(self.main_frame, background='green', relief='sunken')
		self.frame2.place(relx=0, rely=0.18, relheight=0.8, relwidth=1)

		self.label_conn = tk.Label(self.frame2, text='You are not connected to Internet!', font=35)
		self.label_conn.pack()


		self.notebook.add(self.main_frame, text='Contact')

	def third_tab(self):

		self.main_frame = tk.Frame(self.master)
		self.main_frame.pack()

		self.frame = tk.Frame(self.main_frame, background='green')
		self.frame.place(relx=0.018, rely=0.02, relheight=0.84, relwidth=0.966)

		self.frame2 = tk.Frame(self.main_frame, background='blue')
		self.frame2.place(relx=0.018, rely=0.865, relheight=0.13, relwidth=0.966)


		self.label_messaging = ttk.Label(self.frame, background='red')
		self.label_messaging.place(relx=0.018, rely=0.145, relheight=0.84, relwidth=0.966)

		self.notebook.add(self.main_frame, text='Send')
		# self.notebook.add(self.frame2)


	def operation(self):
		self.entry = ttk.Entry(self.frame2)
		self.entry.place(relx=0.01, rely = 0.1, relheight=0.8, relwidth=0.6)

		self.entry2 = ttk.Entry(self.frame2)
		# self.entry2.pack()

		def activate_code():
			msg = self.activator.info_exchanger(self.entry.get())
			self.label_messaging.config(text = msg)

		self.button = ttk.Button(self.frame2)
		self.button.config(command=activate_code, text='Send')
		self.button.place(relx=0.62, rely = 0.1, relheight=0.8, relwidth=0.18)

		self.button = ttk.Button(self.frame2)
		self.button.config(command=activate_code, text='Media')
		self.button.place(relx=0.81, rely = 0.1, relheight=0.8, relwidth=0.18)

		self.all_tabs = self.notebook.tabs()


root = tk.Tk()
root.geometry('600x500')
c = messenger(root)
c.first_tab()
c.second_tab()
c.third_tab()
c.operation()



root.mainloop()
