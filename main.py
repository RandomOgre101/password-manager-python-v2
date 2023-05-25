from tkinter import *
from tkinter import messagebox
from random import randint, choice, shuffle
import pyperclip
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    pass_letters = [choice(letters) for _ in range(randint(8, 10))]
    pass_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    pass_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = pass_letters + pass_symbols + pass_numbers
    shuffle(password_list)
    password = "".join(password_list)

    password_input.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_password():
    web = website_input.get()
    emus = emailuser_input.get()
    passw = password_input.get()
    new_data = {
        web:{
            "email": emus,
            "password": passw,  
        }
    }

    if len(web) == 0 or len(emus) == 0 or len(passw) == 0:
        messagebox.showwarning(title="Invalid Input", message="Please fill out all the fields.")

    else:
        ok = messagebox.askokcancel(title=web, message=f"Email/Username: {emus}\nPassword: {passw}\n\nIs it okay to save?")

        if ok:
            try:
                with open('data.json', mode='r') as data_file:
                    data = json.load(data_file)
                    

            except FileNotFoundError:
                with open('data.json', mode='w') as data_file:
                    json.dump(new_data, data_file, indent=4)

            else:
                data.update(new_data)

                with open('data.json', mode='w') as data_file:
                    json.dump(data, data_file, indent=4)
                messagebox.showinfo(title="Success", message="Successfully saved.")

            finally:
                website_input.delete(0, END)
                password_input.delete(0, END)


def search():
    web = website_input.get()
    try:
        with open('data.json', mode='r') as data_file:
            data = json.load(data_file)
                    
    except FileNotFoundError:
        messagebox.showerror(title="Error", message="No Data File Found")

    finally:
        if web in data:
            em = data[web]['email']
            passw = data[web]['password']
            messagebox.showinfo(title=web, message=f"Email/Username: {em}\n\nPassword: {passw}")
            pyperclip.copy(passw)
        else:
            messagebox.showerror(title="Error", message=f"No Details for {web} Exists")

        
        

# ---------------------------- UI SETUP ------------------------------- #
## Basic Setup
window = Tk()
window.title("Password Manager")
window.config(padx=20, pady=20)

canvas = Canvas(width=200, height=200, highlightthickness=0)
img = PhotoImage(file='logo.png')
canvas.create_image(100,100,image=img)
canvas.grid(column=1, row=0)

## Labels
website_label = Label(text="Website: ")
website_label.grid(column=0, row=1)

emailuser_label = Label(text="Email/Username: ")
emailuser_label.grid(column=0, row=2)

password_label = Label(text="Password: ")
password_label.grid(column=0, row=3)

##Inputs
website_input = Entry(width=21)
website_input.grid(column=1, row=1, columnspan=1)
website_input.focus()

emailuser_input = Entry(width=35)
emailuser_input.insert(0, "abc@gmail.com")
emailuser_input.grid(column=1, row=2, columnspan=2)

password_input = Entry(width=21)
password_input.grid(column=1, row=3)

## Buttons
generate_button = Button(text="Generate Password", command=generate)
generate_button.grid(column=2, row=3)

add_button = Button(text="Add", width=28, command=save_password)
add_button.grid(column=1, row=4, columnspan=2)

search_button = Button(text="Search", command=search, width=15)
search_button.grid(column=2, row=1)

window.mainloop()