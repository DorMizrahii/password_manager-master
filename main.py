from tkinter import *
from tkinter import messagebox
import pyperclip
import json
import random

FONT = ("Arial", 10, "bold")


# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_password():
    password_entry.delete(0, END)
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
               'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_letter = [random.choice(letters) for _ in range(nr_letters)]
    password_symbols = [random.choice(symbols) for _ in range(nr_symbols)]
    password_numbers = [random.choice(numbers) for _ in range(nr_numbers)]

    password_list = password_letter + password_numbers + password_symbols
    random.shuffle(password_list)

    password = "".join(password_list)

    password_entry.insert(0, password)
    pyperclip.copy(password)


# ----------------------------- Find Password ------------------------------#

def search():
    website = website_entry.get()
    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showerror(title="Search Error", message="No data file has been found.")
    else:
        try:
            email = data[website]['email']
            password = data[website]['password']
        except KeyError:
            messagebox.showerror(title="Search Error", message=f"No data on {website} has been found.")
        else:
            messagebox.showinfo(title=website,
                                message=f"Email: {email}\nPassword: {password}")


# ---------------------------- SAVE PASSWORD ------------------------------- #

def clear_data():
    password_entry.delete(0, END)
    password_entry.insert(0, "")
    website_entry.delete(0, END)
    website_entry.insert(0, "")


def save():
    password = password_entry.get()
    website = website_entry.get()
    email = user_name_entry.get()

    new_data = \
        {
            website:
                {
                    "email": email,
                    "password": password,
                }
        }

    if len(password) < 1 or len(website) < 1:
        messagebox.showerror(title="Invalid data", message="Please try again...")

    else:
        try:
            with open("data.json", "r") as data_file:
                data = json.load(data_file)
        except FileNotFoundError as msg:
            print(f"{msg}\nNew file 'data.json' has been created.")
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            data.update(new_data)
            with open("data.json", "w") as data_file:
                json.dump(data, data_file, indent=4)
        finally:
            messagebox.showinfo(title="Data Added", message="Data has been successfully added.")
            clear_data()


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager 😊")
# window.minsize(500, 500)
window.config(padx=50, pady=50)
logo_img = PhotoImage(file="logo.png")
canvas = Canvas(width=200, height=200)
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1)

# website
website_label = Label(text="Website:", font=FONT)
website_label.grid(row=1, column=0)
website_entry = Entry(width=35)
website_entry.focus()
website_entry.grid(columnspan=2, row=1, column=1)

# user_name
user_name_label = Label(text="Email/Username:", font=FONT)
user_name_label.grid(column=0, row=2)
user_name_entry = Entry(width=35)
user_name_entry.insert(END, "dormizrahi1209@gmail.com")
user_name_entry.grid(columnspan=2, row=2, column=1)

# password
password_label = Label(text="Password:", font=FONT)
password_label.grid(column=0, row=3)
password_entry = Entry(width=35)
password_entry.grid(columnspan=2, row=3, column=1)
generate_password_button = Button(text="Generate Password", font=FONT, command=generate_password)
generate_password_button.grid(row=3, column=3)

# add
add_button = Button(text="Add", font=FONT, width=25, command=save)
add_button.grid(row=4, columnspan=2, column=1)

# search

search_button = Button(text="Search", font=FONT, width=14, command=search)
search_button.grid(row=1, column=3)

window.mainloop()
