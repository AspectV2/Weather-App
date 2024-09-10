import tkinter as tk
from tkinter import *
from customtkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
import pyrebase
from dotenv import load_dotenv
import os
import firebase


load_dotenv()


firebaseConfig = firebase.api_key

api_key = os.getenv('api_key')


firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()


def weather():
    global weather_window, weather_data, entry_field
    weather_window = Toplevel()
    weather_window.geometry("540x540")
    weather_window.title("Weather page")

    entry_field = CTkEntry(master=weather_window)
    entry_field.place(relx=0.3, rely=0.1, anchor=CENTER)
    get_weather_button = CTkButton(master=weather_window, text="Get weather", command=weather_data_labels, corner_radius=32, fg_color='#003185', hover_color='#024950')
    get_weather_button.place(relx=0.8, rely=0.1, anchor=E)


def weather_data_labels():
    global weather_data
    fp1 = "https://api.openweathermap.org/data/2.5/weather?q="
    fp2 = entry_field.get()
    fp3 = "&appid="
    fp4 = api_key
    fp5 = "&units=imperial"

    weather_data = requests.get(fp1 + fp2 + fp3 + fp4 + fp5)

    weather = weather_data.json()["weather"][0]["main"]
    temperature = weather_data.json()["main"]["temp"]
    description = weather_data.json()['weather'][0]['description']
    icon_id = weather_data.json()['weather'][0]['icon']

    icon_url = f"https://openweathermap.org/img/wn/{icon_id}@2x.png"

    weather_label = Label(weather_window, text=weather)
    weather_label.place(relx=0.5, rely=0.7, anchor=CENTER)
    temperature_label = Label(weather_window, text=str(temperature) + '°F', font="40")
    temperature_label.place(relx=0.5, rely=0.3, anchor=CENTER)

    image = Image.open(requests.get(icon_url, stream=True).raw)
    icon = ImageTk.PhotoImage(image, width=300, height=300)
    icon_label = tk.Label(weather_window)
    icon_label.configure(image=icon)
    icon_label.image = icon

    icon_label.place(relx=0.5, rely=0.5, anchor=CENTER)


def sign_up_page():
    global sign_up_username, sign_up_password
    sign_up = Toplevel()
    sign_up.geometry("540x540")
    sign_up.title("Sign up page")

    sign_up_username = CTkEntry(sign_up)

    sign_up_username.place(relx=0.5, rely=0.4, anchor=CENTER)
    sign_up_username_label = Label(sign_up, text="Email")
    sign_up_username_label.place(relx=0.5, rely=0.35, anchor=CENTER)
    sign_up_password = CTkEntry(sign_up, show="*")
    sign_up_password_label = Label(sign_up, text="Password")
    sign_up_password.place(relx=0.5, rely=0.55, anchor=CENTER)
    sign_up_password_label.place(relx=0.5, rely=0.5, anchor=CENTER)

    sign_up_button = CTkButton(sign_up, text="Sign Up", corner_radius=32, fg_color='#003185', hover_color='#024950', command=sign_up_task)
    sign_up_button.place(relx=0.5, rely=0.7, anchor=CENTER)


def sign_up_task():
    try:
        user = auth.create_user_with_email_and_password(sign_up_username.get(), sign_up_password.get())
        weather()
    except:
        messagebox.showerror("Error", "Invalid email or Email already made")


def login_task():
    try:
        login_user = auth.sign_in_with_email_and_password(login.get(), password.get())
        weather()
    except:
        messagebox.showerror("Error", "Incorrect email or password")


login_page = Tk()
login_page.title("Login Page")
login_page.geometry("540x540")

login = CTkEntry(login_page)
password = CTkEntry(login_page, show="*")
enter = CTkButton(login_page, text="Login", command=login_task, corner_radius=32, fg_color='#003185', hover_color='#024950')
sign_up = CTkButton(login_page, text="Don't have an account? Sign Up!", font=('Arial', 10), command=sign_up_page, fg_color='#003185', hover_color='#024950')
# CHANGE FONT

email = Label(login_page, text="Email")
password_label = Label(login_page, text="Password")

check_button = Checkbutton(login, text="show_password")
sign_up.place(relx=0.03, rely=0.7, anchor=W)
enter.place(relx=0.5, rely=0.7, anchor=CENTER)
email.place(relx=0.5, rely=0.35, anchor=CENTER)
password_label.place(relx=0.5, rely=0.5, anchor=CENTER)
password.place(relx=0.5, rely=0.55, anchor=CENTER)
login.place(relx=0.5, rely=0.4, anchor=CENTER)

login_page.mainloop()
