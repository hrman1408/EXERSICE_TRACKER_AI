import os
import requests
from tkinter import messagebox
from datetime import datetime
from tkinter import *
from dotenv import load_dotenv

load_dotenv()

now = datetime.now()
today = now.strftime("%d-%m-%Y")
time = now.strftime("%X")

#FIRSTLY, CREATE ACCOUNT ON GOOGLE SHEET EXCEL THEN CLICK ON SHARE🔒 AND COPY LINK
#SECONDLY, SIGN UP ON SHEETY SITE THEN CREATE PROJECT AND PASTE COPY LINK IN URL BLANK BUT REMEMBER GET & POST COLUMN ALSO ENABLE
#MAINLY, REMEMBER EXCEL AND SHEETY THEY BOTH ARE SIGN UP WITH SAME ID
#REMEBER WRITE DATE, TIME, EXERCISE, DURATION , CALORIES IN 5 DIFFERENT COLUMNS
SHEETY_ENDPOINT = os.getenv("OPENAI_SHEET_URL")
EXERCISE_ENDPOINT = "https://trackapi.nutritionix.com/v2/natural/exercise"

#GET NUTRITION API BY NUTRITIONIX
#IF YOU'RE UNABLE TO CREATE ACCOUNT ON NUTRITIONIX THEN YOU SHOULD EMAIL ON <api@nutritionix.com> AND THEY ACTIVATE YOUR ACCOUNT
APP_ID = os.getenv("OPENAI_APP_ID")
API_KEY = os.getenv("OPENAI_KEY_API")

exercise_header = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
}
#--------------------------------------LOGIC-----------------------------------------------#
def internet():
    try:
        requests.get(EXERCISE_ENDPOINT, timeout=5)
        return True
    except requests.exceptions.RequestException:
        messagebox.showinfo(title="Error", message="Please check your internet connection")
        return False

def add_row():
    if not internet():
        return

    query = enter_entry.get()
    gender = gender_entry.get()
    weight = weight_entry.get()
    height = height_entry.get()
    age = age_entry.get()

    if not all([query, gender, weight, height, age]):
        messagebox.showinfo(title="Empty", message="Fill all entries carefully")
        return

    try:
        exercise_parameter = {
            "query": query,
            "gender": gender,
            "weight_kg": float(weight),
            "height_cm": float(height),
            "age": int(age),
        }

        responses = requests.post(url=EXERCISE_ENDPOINT, json=exercise_parameter, headers=exercise_header)
        responses.raise_for_status()
        result = responses.json()

        for exercise in result['exercises']:
            sheety = {
                "sheet1": {
                    "date": today,
                    "time": time,
                    "exercise": exercise['user_input'].title(),
                    "duration": f"{exercise['duration_min']} minutes",
                    "calories": f"{exercise['nf_calories']} calories"
                }
            }
            requests.post(url=SHEETY_ENDPOINT, json=sheety)
            messagebox.showinfo(title="Successful", message=f"WOW! Today, you did {exercise['user_input'].title()} "
                                                            f"for {exercise['duration_min']} minutes.\n You burned "
                                                            f"{exercise['nf_calories']} calories.")
    except requests.exceptions.HTTPError as http_err:
        messagebox.showinfo(title="Error", message=f"HTTP error occurred: {http_err}")

#-------------------------------------------------GUI------------------------------------------------------#
window = Tk()
window.title("WORKOUT TRACKER")
window.minsize(height=500, width=600)
window.config(bg="teal", pady=20, padx=20)

canvas = Canvas(width=400, height=400, highlightthickness=0, bg="teal")
yog = PhotoImage(file="yog.png")
canvas.create_image(200, 200, image=yog)
canvas.grid(row=7, column=0, columnspan=2)

title_label = Label(text="WORKOUT TRACKER", font=("Castaller", 16, "bold"), fg="ivory", bg="teal")
title_label.grid(row=0, column=0, columnspan=2)

gender_label = Label(text="GENDER: ", font=("Castaller", 12, "bold"), fg="ivory", bg="teal")
gender_label.grid(row=1, column=0)

age_label = Label(text="AGE: ", font=("Castaller", 12, "bold"), fg="ivory", bg="teal")
age_label.grid(row=2, column=0)

height_label = Label(text="HEIGHT_CM: ", font=("Castaller", 12, "bold"), fg="ivory", bg="teal")
height_label.grid(row=3, column=0)

weight_label = Label(text="WEIGHT_KG: ", font=("Castaller", 12, "bold"), fg="ivory", bg="teal")
weight_label.grid(row=4, column=0)

entry_label = Label(text="ENTER EXERCISE YOU DID (ONLY 1):       ", font=("Castaller", 12, "bold"), fg="ivory",
                    bg="teal")
entry_label.grid(row=5, column=0)

gender_entry = Entry(font=("System", 10, "bold"))
gender_entry.grid(row=1, column=1)

age_entry = Entry(font=("System", 10, "bold"))
age_entry.grid(row=2, column=1)

height_entry = Entry(font=("System", 10, "bold"))
height_entry.grid(row=3, column=1)

weight_entry = Entry(font=("System", 10, "bold"))
weight_entry.grid(row=4, column=1)

enter_entry = Entry(font=("System", 10, "bold"), width=40)
enter_entry.grid(row=5, column=1)

today_label = Label(text=f"CURRENTLY:  {time} ({today})", font=("Castaller", 12, "bold"), fg="ivory", bg="teal")
today_label.grid(row=8, column=0, columnspan=2)

add_button = Button(text="ADD", font=("Castaller", 12, "bold"), fg="ivory", bg="teal", highlightthickness=0, width=5,
                    command=add_row)
add_button.grid(row=6, column=0, columnspan=2)

window.mainloop()
