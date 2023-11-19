from tkinter import *
from tkinter import messagebox
from pathlib import Path
import random
import pyperclip
import json

path = Path("data.txt")

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
# Password Generator Project

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
           'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
           'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

nr_letters = random.randint(8, 10)
nr_symbols = random.randint(2, 4)
nr_numbers = random.randint(2, 4)

password_list = []

[password_list.append(random.choice(letters)) for char in range(nr_letters)]
[password_list.append(random.choice(symbols)) for char in range(nr_symbols)]
[password_list.append(random.choice(numbers)) for char in range(nr_numbers)]

random.shuffle(password_list)

password = "".join(password_list)


def generate_password():
    entry_pswd.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def get_values():
    hold_website = entry_website.get().title()
    hold_email = entry_email.get()
    hold_password = entry_pswd.get()

    len_email = len(hold_email)
    len_website = len(hold_website)
    len_password = len(hold_password)

    data = {
        hold_website: {
            "email": hold_email,
            "password": hold_password
        }
    }
    if len_email == 0 or len_password == 0 or len_website == 0:
        messagebox.showerror(title="field left empty", message="You left some field empty")

    else:
        is_ok = messagebox.askokcancel(title=hold_website,
                                       message=f"These are the details entered \nEmail: {hold_email}\n"
                                               f"Password: {hold_password}\nIs it okay to save?")
        if is_ok:
            try:
                with open("data.json", mode='r') as file:
                    content = json.load(file)
            except (json.decoder.JSONDecodeError, FileNotFoundError):
                with open("data.json", mode='w') as file:
                    json.dump(data, file, indent=4)
            else:
                content.update(data)
                with open("data.json", mode='w') as file:
                    json.dump(content, file, indent=4)
            finally:
                entry_website.delete(0, END)
                entry_pswd.delete(0, END)


# ---------------------------- SEARCH DATA ------------------------------- #

def search():
    hold_website = entry_website.get().title()
    if len(hold_website) == 0:
        messagebox.showerror(title="Field value requires!", message="Website field is left empty! "
                                                                    "Please provide a valid website to search")
    else:
        try:
            with open("data.json", mode='r') as file:
                content = json.load(file)
        except FileNotFoundError:
            messagebox.showerror(title="Error", message="File not Found")
        else:
            try:
                retrived_email = content[hold_website]['email']
                retrived_password = content[hold_website]['password']
            except KeyError:
                messagebox.showerror(title="Website not found", message="The website that you searched doesn't exists")
            else:
                messagebox.askokcancel(title=hold_website,
                                       message=f"Credentials for your searched website \n\n"
                                               f"Email: {retrived_email}\n"
                                               f"Password: {retrived_password}\n\n"
                                               f"The password is copied to clipboard!!")

                pyperclip.copy(content[hold_website]['password'])


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password-Manager")
window.config(padx=50, pady=50, bg='white')
canvas = Canvas(width=200, height=200, bg='white', highlightthickness=0)
main_image = PhotoImage(file='logo.png')
canvas.create_image(100, 100, image=main_image)
canvas.grid(row=0, column=1)

label_website = Label(text="Website:", bg='white')
label_website.grid(row=1, column=0)
entry_website = Entry(width=21)
entry_website.focus()
entry_website.grid(row=1, column=1)

label_email = Label(text="Email/Username:", bg='white')
label_email.grid(row=2, column=0)
entry_email = Entry(width=39)
entry_email.insert(0, "sheikhtahamaroof@gmail.com")
entry_email.grid(row=2, column=1, columnspan=2)

label_pswd = Label(text="Password:", bg='white')
label_pswd.grid(row=3, column=0)
entry_pswd = Entry(width=21)
entry_pswd.grid(row=3, column=1)

btn_search = Button(text="Search", width=15, command=search)
btn_search.grid(row=1, column=2)

btn_gn_pswd = Button(text="Generate Password", bg='white', command=generate_password)
btn_gn_pswd.grid(row=3, column=2)

btn_add = Button(text="Add", width=34, command=get_values)
btn_add.grid(row=4, column=1, columnspan=2)

window.mainloop()
