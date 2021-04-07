#!/usr/bin/env python

#
#
# @author ChrisMCodes
# date: 2020-08-19
# purpose: A simple app to help CMs determine whether their clients meet the HUD
# income limits in Northern Arizona.

from tkinter import *
import string # to strip user input
import sys

global size
global county
global income
global hinc
global current_array # tracks current income input
global mainframe
global current_data
global freq

current_data = {}

# Create income calculator window
money = Tk()
money.title("Calculating income")

# Create grid for income
frame = Frame(money)
frame.grid(column=0,row=0, sticky=(N,W,E,S))
frame.columnconfigure(0, weight = 1)
frame.rowconfigure(0, weight = 10)
frame.pack(pady = 5, padx = 50)

# Get pay frequency
fr = StringVar(money)

# Options
pay_freq = ['Weekly', 'Biweekly', 'Monthly', 'Bimonthly']

pf = OptionMenu(frame, fr, *pay_freq)
Label(frame, text="Frequency of pay:").grid(row = 1, column = 1)
pf.grid(row = 2, column = 1)

def get_money(*args):
    freq = str(fr.get())
    m = str(pay.get())
    try:
        income = float(m)

        if freq == "Weekly":
            income *= 52
        elif freq == "Biweekly":
            income *= 26
        elif freq == "Monthly":
            income *= 12
        elif freq == "Bimonthly":
            income *= 6
        else:
            raise KeyError()
        current_data['income'] = income
        money.destroy()
    except:
        err = Tk()
        err.title("An error occurred")
        l = Label(err, text="Please restart the program and ensure you are entering valid data for all fields.")
        l.pack()
        btn = Button(err, text = "Exit and retry", command = err.destroy)
        btn.pack()
        err.mainloop()
        money.destroy()
        sys.exit(1)

Label(frame, text="Enter average pay per pay period. \n\tTake sum of all paystubs and divide by number of paystubs. \nUse only numbers; no symbols:").grid(row = 3, column = 1)
pay = Entry(money, width=10)
pay.pack()

but = Button(money, text= "Continue", command = get_money)
but.pack()

money.mainloop()
#
#
#
# Second window!
#
#
#

# Getting info about household size
persons = Tk()
persons.title("Household income")

# Creating grids
# persons
mainframe = Frame(persons)
mainframe.grid(column=0,row=0, sticky=(N,W,E,S) )
mainframe.columnconfigure(0, weight = 1)
mainframe.rowconfigure(0, weight = 1)
mainframe.pack(pady = 100, padx = 100)


# Create a Tkinter variable
tkvar = StringVar(persons)
cvar = StringVar(persons)
ivar = StringVar(persons)

# setting up the options
num_people = ['1', '2', '3', '4', '5', '6', '7', '8+']
regions = ['Apache', 'Coconino', 'Mohave', 'Navajo','Yavapai']

apache_inc = ['28950', '33100', '37250', '41350', '44700', '48000', '51300', '54600', '99999999']

coco_inc = ['42150', '48150', '54150', '60150','65000', '69800', '74600', '79400','99999999']

mohave_inc = ['31200', '35650', '40100', '44550','48150', '51700', '55250', '58850','99999999']

navajo_inc = ['29800', '34050', '38300', '42550','46000', '49400','52800', '56200', '99999999']

yava_inc = ['36200', '41400', '46550', '51700','55850', '60000', '64150', '68250','99999999']

# setting up the menus
# persons
household = OptionMenu(mainframe, tkvar, *num_people)
Label(mainframe, text="Number of people in household:").grid(row = 1, column = 1)
household.grid(row = 2, column = 1)

# county
cty = OptionMenu(mainframe, cvar, *regions)
Label(mainframe, text="County of residence:").grid(row = 3, column = 1)
cty.grid(row = 4, column = 1)
    


# event on value change
def change_household(*args):
    temp_size = tkvar.get()
    if temp_size == '8+':
        size = 8
    else:
        size = int(temp_size)
    current_data['size'] = size
        

def change_county(*args):
    county = cvar.get()
    gen_income(county)
    current_data['county'] = county

def gen_income(county):
    if county == "Apache":
        current_array = apache_inc
        
    elif county == "Coconino":
        current_array = coco_inc
        
    elif county == "Mohave":
        current_array = mohave_inc
        
    elif county == "Navajo":
        current_array = navajo_inc
        
    else:
        current_array = yava_inc
    current_data['array'] = current_array


def qualifies(current_data):
    income = current_data['income']
    for j in current_data['array']:
        if income < float(j):
            this_inc = current_data['array'].index(j) + 1
            break

    root = Tk()
    root.title("Results")
    this_size = int(current_data['size'])

    if this_inc <= this_size:
        label = Label(root, text="Annual income is ${:,.2f} \nThis client qualifies!".format(current_data['income']), fg = "green", font = "Arial 32 bold")
    else:
        label = Label(root, text="Annual income is ${:,.2f} \nSorry, this client is over income.".format(current_data['income']), fg = "red", font = "Arial 32 bold")

    label.pack()
    button = Button(root, text="Exit", command = root.destroy)
    button.pack()
    root.mainloop()
    


# event reader
tkvar.trace('w', change_household)
cvar.trace('w', change_county)

# The ever-important exit button!
exit_button = Button(persons, text="Click here when finished", command=persons.destroy)
exit_button.pack()

persons.mainloop()

try:
    if current_data['array'] != None and current_data['size'] != None and current_data['income'] != None:
        qualifies(current_data)
    else:
        raise KeyError("Invalid data found")
except KeyError:
    new = Tk()
    new.title("An error occurred")
    l = Label(new, text="Please restart the program and ensure you are entering valid data for all fields.")
    l.pack()
    btn = Button(new, text = "Exit and retry", command = new.destroy)
    btn.pack()
    new.mainloop()

