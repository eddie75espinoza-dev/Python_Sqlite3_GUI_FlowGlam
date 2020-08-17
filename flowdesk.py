# -*- mode: python ; coding: utf-8 -*-
'''
GUI desarrollada en Python 3, usando las librerías de Tkinter y SQLite3, para emprendimiento personal a través de
redes sociales según los requerimientos de la empresa FlowGlam.
Uso de base de datos SQLite

Esta GUI permite registrar ua persona con nombre y username de la red social, mediante CRUD, permite la creación
de tareas o turnos para cada usuario, mediante una fecha, hora, establece un nombre y un precio a cada tarea.

Desarrollador: Eddie Espinoza
Version: 1.0

'''
import sys, os

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mbox
from tkinter import *
import sqlite3

# Class Definition 
class User:
    # Data Base
    db_name = "flowdb.db"

    def __init__(self, window):
        self.wind = window
        self.wind.title('Flow Glam')
        self.wind.geometry('640x500')
        self.wind.minsize(640,500)
        self.wind.maxsize(640, 500)
        # Colors
        bg_colorBack = '#FFC8FB'
        fg_colorDanger = '#D7263D'

        self.img_logo = PhotoImage(file="logoFlow.png")
        Label(bg = bg_colorBack, image = self.img_logo).place(x = 60, y = 20)
        # Creating a Frame container
        frame = LabelFrame(bg = bg_colorBack, text = "Customer Registration")
        frame.grid(row = 0, column = 0, pady = 16)

        # Name input
        Label(frame, bg = bg_colorBack, text = "Name: ").grid(row = 1, column = 0)
        self.name = Entry(frame)
        self.name.grid(row = 1, column = 1)
        self.name.focus()

        # UserName input
        Label(frame, bg = bg_colorBack, text = "User: ").grid(row = 2, column = 0)
        self.user_name = Entry(frame)
        self.user_name.grid(row = 2, column = 1)

        # Email input
        Label(frame, bg = bg_colorBack, text = "E-mail: ").grid(row = 3, column = 0)
        self.email = Entry(frame)
        self.email.grid(row = 3, column = 1)
        self.email.focus()

        # Phone input
        Label(frame, bg = bg_colorBack, text = "Phone: ").grid(row = 4, column = 0)
        self.phone = Entry(frame)
        self.phone.grid(row = 4, column = 1)

        # Button back
        btnBack = tk.Button(text = '<--', command = self.get_clients)
        btnBack.place(x = 10, y = 10)

        # Button add
        self.btnSave = tk.Button(text = '  Save Client  ', command = self.add_client)
        self.btnSave.place(x = 408, y = 25)

        # Button Task
        self.btnTurn = tk.Button(text = '    Add Turn   ', command = self.add_turn)
        self.btnTurn.place(x = 408, y = 60)

        # Button Consult by User name
        self.btnByName = tk.Button(text = ' Consult by Name ', command = self.consult_name)
        self.btnByName.place(x = 408, y = 95)

        # Button Consult by User name
        self.btnByUser = tk.Button(text = ' Consult by User ', command = self.consult_user)
        self.btnByUser.place(x = 522, y = 95)

        # Button Edit
        self.btnEdit = tk.Button(text = '   Edit Client  ', command = self.edit_client)
        self.btnEdit.place(x = 540, y = 25)

        # Button Delete
        self.btnDelete = tk.Button(text = 'Delete  Client', command = self.del_client)
        self.btnDelete.place(x = 540, y = 60)
        self.btnDelete.config(fg = fg_colorDanger)

        # Button Consult by Date
        self.btnConsult = tk.Button(text = ' General Consult ', command = self.get_tasks)
        self.btnConsult.place(x = 162, y = 440)

        # Button Consult by Date
        Label(bg = bg_colorBack, text = "(yyyy-mm-dd)").place(x = 40, y = 410)
        self.date = Entry()
        self.date.place(x = 20, y = 430)
        self.btnByDate = tk.Button(text = '     Consult By Date     ', command = self.get_day)
        self.btnByDate.place(x = 20, y = 455)

        # Delete Task
        self.btnDeltask = tk.Button(text = '   Delete task   ', fg = fg_colorDanger, command = self.del_task)

        # Interaction message
        self.message = Label(bg = bg_colorBack, text = "", fg = fg_colorDanger)
        self.message.grid(row = 6, column = 0, columnspan = 2, sticky = W + E)

        # Table
        self.tree = ttk.Treeview(columns = ('#1','#2','#3', '#4'), selectmode = 'browse', height = 10, padding = 8)
        self.tree.grid(row = 12, column = 0)
        # Scrollbar
        self.vsb = ttk.Scrollbar(window, orient = 'vertical', command = self.tree.yview)
        self.vsb.place(x= 620, y=159, height = 238)
        self.tree.configure(yscrollcommand = self.vsb.set)

        # Get DB Client
        self.get_clients()

    # Query and Connection
    def db_query(self, query, parameters=()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result

    # Cleaning table
    def cleaning(self):
        self.name.delete(0, END)
        self.user_name.delete(0, END)
        self.email.delete(0, END)
        self.phone.delete(0, END)
        self.date.delete(0, END)
        self.name.focus()

        # Cleaning table
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)

    # Get customer table data
    def get_clients(self):
        self.btnSave.config(state = NORMAL)
        self.btnTurn.config(state = NORMAL)
        self.btnEdit.config(state = NORMAL)
        self.btnDelete.config(state = NORMAL)
        self.btnByName.config(state = NORMAL)
        self.btnByUser.config(state = NORMAL)
        self.btnDeltask.place_forget()

        self.cleaning()
        #
        self.tree.column('#0', width = 40, minwidth = 40, stretch = NO)
        self.tree.column('#1', width = 120, minwidth = 120)
        self.tree.column('#2', width = 120, minwidth = 120)
        self.tree.column('#3', width = 200, minwidth = 120)
        self.tree.column('#4', width = 120, minwidth = 120)
        self.tree.heading('#0', text = 'ID', anchor = W)
        self.tree.heading('#1', text = 'Name', anchor = CENTER)
        self.tree.heading('#2', text = ' User Name', anchor = CENTER)
        self.tree.heading('#3', text = 'Email', anchor = CENTER)
        self.tree.heading('#4', text = 'Phone', anchor = CENTER)
        # Consulting table
        query = 'SELECT * FROM users ORDER BY login DESC'
        db_rows = self.db_query(query)
        # filling data
        for row in db_rows:
            self.tree.insert('', 0, text = row[0], values = (row[1], row[2], row[3], row[4]))

    # Disabled buttons
    def btn_disabled(self):
        self.btnSave.config(state = DISABLED)
        self.btnTurn.config(state = DISABLED)
        self.btnEdit.config(state = DISABLED)
        self.btnDelete.config(state = DISABLED)
        self.btnByName.config(state = DISABLED)
        self.btnByUser.config(state = DISABLED)

    # Consult by name
    def consult_name(self):
        id_click = self.tree.item(self.tree.selection())['text']
        id_text = self.name.get()

        if id_click == "" and id_text == "":
            self.message['text'] = 'Select a Name'
        else:
            if id_click != "": self.get_user_click()
            if id_text != "": self.get_name_text(id_text)

    # Consult by name
    def consult_user(self):
        id_click = self.tree.item(self.tree.selection())['text']
        id_text = self.user_name.get()

        if id_click == "" and id_text == "":
            self.message['text'] = 'Select a User Name'
        else:
            if id_click != "": self.get_user_click()
            if id_text != "": self.get_user_text(id_text)

    # Heading Table User
    def table_consult_user(self):
        self.tree = ttk.Treeview(columns = ('#1', '#2', '#3', '#4', '#5'), selectmode = 'browse', height = 10,
                                 padding = 8)
        self.tree.grid(row = 12, column = 0)
        self.tree.column('#0', width = 100, minwidth = 40, stretch = NO)
        self.tree.column('#1', width = 80, minwidth = 60)
        self.tree.column('#2', width = 80, minwidth = 40)
        self.tree.column('#3', width = 200, minwidth = 120)
        self.tree.column('#4', width = 80, minwidth = 60)
        self.tree.column('#5', width = 60, minwidth = 40)
        self.tree.heading('#0', text = 'Name', anchor = W)
        self.tree.heading('#1', text = 'Date', anchor = CENTER)
        self.tree.heading('#2', text = 'Schedule', anchor = CENTER)
        self.tree.heading('#3', text = 'Service', anchor = CENTER)
        self.tree.heading('#4', text = 'Amount', anchor = CENTER)
        self.tree.heading('#5', text = 'Turn', anchor = CENTER)
        # Scrollbar
        self.vsb = ttk.Scrollbar(window, orient = 'vertical', command = self.tree.yview)
        self.vsb.place(x = 620, y = 159, height = 238)
        self.tree.configure(yscrollcommand = self.vsb.set)

    # Consult by user name (text)
    def get_name_text(self, id_text):
        self.btn_disabled()
        text_id = id_text+'%'
        # Consulting table
        parameters = (text_id,)
        query = 'SELECT users.id, users.name, tasks.date, tasks.hour, tasks.title, tasks.amount, tasks.turn, users.login FROM users INNER JOIN tasks ON users.id = tasks.id_users WHERE users.name LIKE ? ORDER BY tasks.date ASC'
        db_rows = self.db_query(query, parameters)
        # Cleaning table
        self.cleaning()
        # table
        self.table_consult_user()
        # filling data
        for row in db_rows:
            global idUser
            idUser = row[0]
            self.tree.insert('', 0, text = row[1], values = (row[2], row[3], row[4], row[5], row[6]))
        # Display Btn Delete task
        self.btnDeltask.place(x = 520, y = 408)

    # Consult by user name (text)
    def get_user_text(self, id_text):
        self.btn_disabled()
        # Consulting table
        parameters = ((id_text,))
        query = 'SELECT users.id, users.name, tasks.date, tasks.hour, tasks.title, tasks.amount, tasks.turn, users.login FROM users INNER JOIN tasks ON users.id = tasks.id_users WHERE users.login = ? ORDER BY tasks.date ASC'
        db_rows = self.db_query(query, parameters)
        # Cleaning table
        self.cleaning()
        # table
        self.table_consult_user()
        # filling data
        for row in db_rows:
            global idUser
            idUser = row[0]
            self.tree.insert('', 0, text = row[1], values = (row[2], row[3], row[4], row[5], row[6]))
        # Display Btn Delete task
        self.btnDeltask.place(x = 520, y = 408)

    # Consult by user name(selection)
    def get_user_click(self):
        self.message['text'] = ''
        try:
            id_user = self.tree.item(self.tree.selection())['text']
            val = self.tree.item(self.tree.selection())['values'][0]
        except IndexError as e:
            self.message['text'] = 'Select a Name'
            return
        self.btn_disabled()
        # Consulting table
        # self.tree.item(self.tree.selection())['text']
        id_user_task = self.tree.item(self.tree.selection())['text']
        parameters = (id_user, id_user_task)
        query = 'SELECT users.id, users.name, tasks.date, tasks.hour, tasks.title, tasks.amount, tasks.turn FROM users INNER JOIN tasks WHERE users.id = ? AND tasks.id_users = ? ORDER BY tasks.date ASC'
        db_rows = self.db_query(query, parameters)
        # Cleaning table
        self.cleaning()
        # table
        self.table_consult_user()

        # filling data
        for row in db_rows:
            global idUser
            idUser = row[0]
            self.tree.insert('', 0, text = row[1], values = (row[2], row[3], row[4], row[5], row[6]))

        #Display Btn Delete task
        self.btnDeltask.place(x = 520, y = 408)

    # Validation data entry
    def validation(self):
        return len(self.name.get()) != 0 and len(self.user_name.get()) != 0

    # Add Client
    def add_client(self):
        if self.validation():
            query = 'INSERT INTO users VALUES (NULL, ?, ?, ?, ?)'
            parameters = (self.name.get(), self.user_name.get(), self.email.get(), self.phone.get())
            self.db_query(query, parameters)
            self.message['text'] = 'Registered {} correctly'.format(self.name.get())
            self.name.delete(0, END)
            self.user_name.delete(0, END)
            self.email.delete(0, END)
            self.phone.delete(0, END)
        else:
            self.message['text'] = 'Name and User required'
        self.name.focus()
        self.get_clients()

    # Edit records
    def edit_client(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['values'][0]
        except IndexError as e:
            self.message['text'] = 'Select a record to edit'
            return
        name = self.tree.item(self.tree.selection())['values'][0]
        old_user_name = self.tree.item(self.tree.selection())['values'][1]
        self.edit_wind = Toplevel()

        # Creating a Frame container for Edit Client
        read_frame = LabelFrame(self.edit_wind, text = "Edit Client")
        read_frame.grid(row = 0, column = 0, padx = 8, pady = 8)

        # Read only Registro actual de cliente
        Label(read_frame, text = "Name: ").grid(row = 1, column = 0)
        Entry(read_frame, textvariable = StringVar(self.edit_wind, value = name), state = 'readonly').grid(row = 1,
                                                                                                           column = 1)
        # Read Only User_Name input
        Label(read_frame, text = "User Name: ").grid(row = 2, column = 0)
        Entry(read_frame, textvariable = StringVar(self.edit_wind, value = old_user_name), state = 'readonly').grid(
            row = 2, column = 1)

        # New record
        # Creating a Frame container for Edit Client
        edit_frame = LabelFrame(self.edit_wind, text = "New Record")
        edit_frame.grid(row = 4, column = 0, padx = 8, pady = 8)

        # Editing only Registro actual de cliente
        Label(edit_frame, text = "(New) Name: ").grid(row = 5, column = 0)
        new_name = Entry(edit_frame)
        new_name.grid(row = 5, column = 1)

        # Editing Only User_Name input
        Label(edit_frame, text = "(New) User Name: ").grid(row = 6, column = 0)
        new_user_name = Entry(edit_frame)
        new_user_name.grid(row = 6, column = 1)

        # Editing Only Email input
        Label(edit_frame, text = "(New) Email: ").grid(row = 7, column = 0)
        new_email = Entry(edit_frame)
        new_email.grid(row = 7, column = 1)

        # Editing Only Phone input
        Label(edit_frame, text = "(New) Phone: ").grid(row = 8, column = 0)
        new_phone = Entry(edit_frame)
        new_phone.grid(row = 8, column = 1)

        # Button Update
        Button(self.edit_wind, text = 'Update',
               command = lambda: self.update_client(new_name.get(), new_user_name.get(), new_email.get(), new_phone.get(), name, old_user_name)).grid(
            row = 8, column = 9, columnspan = 2, padx = 24, pady = 8)

    # Update Client
    def update_client(self, new_name, new_user_name, new_email, new_phone, name, old_user_name):
        if len(new_name) != 0 and len(new_user_name) != 0:
            query = 'UPDATE users SET name = ?, login = ?, email = ?, phone = ? WHERE name = ? AND login = ?'
            parameters = (new_name, new_user_name, new_email, new_phone, name, old_user_name)
            self.db_query(query, parameters)
            self.edit_wind.destroy()
            self.message['text'] = 'Update {} RegistrationData'.format(name)
            self.get_clients()
        else:
            self.message['text'] = 'Data Required'
            return

    # Delete records to client
    def del_client(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['values'][0]
        except IndexError as e:
            self.message['text'] = 'Select a record to delete'
            return
        msgBox = mbox.askokcancel('Delete record','Are you sure you want to Delete {}?'.format(self.tree.item(self.tree.selection())['values'][0]))
        if msgBox:
            self.message['text'] = ''
            user = self.tree.item(self.tree.selection())['values'][0]
            query = 'DELETE FROM users WHERE name = ?'
            self.db_query(query, (user,))
            self.message['text'] = 'Record {} deleted'.format(user)
            self.get_clients()

    # Register turn (tasks)
    def add_turn(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['values'][0]
        except IndexError as e:
            self.message['text'] = 'Select a record'
            return
        name = self.tree.item(self.tree.selection())['values'][0]
        user_name = self.tree.item(self.tree.selection())['values'][1]
        id_user = self.tree.item(self.tree.selection())['text']

        self.edit_wind = Toplevel()

        # Creating a Frame container for Edit Client
        read_frame = LabelFrame(self.edit_wind, text = "Add turn Client")
        read_frame.grid(row = 0, column = 0, padx = 8, pady = 8)

        # Read only Registro actual de cliente
        Label(read_frame, text = "Name: ").grid(row = 1, column = 0)
        Entry(read_frame, textvariable = StringVar(self.edit_wind, value = name), state = 'readonly').grid(row = 1,
                                                                                                                   column = 1)

        # Read Only User_Name input
        Label(read_frame, text = "User Name: ").grid(row = 2, column = 0)
        Entry(read_frame, textvariable = StringVar(self.edit_wind, value = user_name), state = 'readonly').grid(
            row = 2, column = 1)

        # New record to turn

        # Creating a Frame container for Add turn
        edit_frame = LabelFrame(self.edit_wind, text = "Add Turn")
        edit_frame.grid(row = 4, column = 0, padx = 8, pady = 8)

        # Creating a task for client input
        Label(edit_frame, text = "Service: ").grid(row = 5, column = 0)
        service = Entry(edit_frame)
        service.grid(row = 5, column = 1)

        # Creating a task for date input
        Label(edit_frame, text = "Date (yyyy-mm-dd): ").grid(row = 6, column = 0)
        date = Entry(edit_frame)
        date.grid(row = 6, column = 1)

        # Creating a task for hour input
        Label(edit_frame, text = "Hour (24:00): ").grid(row = 7, column = 0)
        hour = Entry(edit_frame)
        hour.grid(row = 7, column = 1)

        # Creating a task for Phone input
        Label(edit_frame, text = "Amount: ").grid(row = 8, column = 0)
        amount = Entry(edit_frame)
        amount.grid(row = 8, column = 1)

        # Creating a task number input
        Label(edit_frame, text = "Number turn: ").grid(row = 9, column = 0)
        nunTask = Entry(edit_frame)
        nunTask.grid(row = 9, column = 1)

        service.focus()

        # Button Add Tasks
        Button(self.edit_wind, text = '   Save   ', command = lambda: self.add_task(service.get(), date.get(), hour.get(), amount.get(), nunTask.get(), id_user)).grid(row = 10, column = 2, columnspan = 2, padx = 24, pady = 8)

    # Add Turn
    def add_task(self, service, date, hour, amount, turn, id_user):
        if len(service) != 0 and len(date) != 0 and len(hour) != 0:
            query = ' INSERT INTO tasks VALUES (NULL, ?, ?, ?, ?, ?, ?)'
            parameters = (service, date, hour, amount, turn, id_user)
            self.db_query(query, parameters)
            self.edit_wind.destroy()
            self.message['text'] = 'Register {} Successfully'.format(service)
            self.get_clients()
        else:
            self.message['text'] = 'Data required'
            self.name.focus()
            self.get_clients()

    # Delete tasks (Turn)
    def del_task(self):
        self.message['text'] = ''
        try:
            delTurn = self.tree.item(self.tree.selection())['values'][4]
            delTask = self.tree.item(self.tree.selection())['text']
        except IndexError as e:
            self.message['text'] = 'Select a record to delete'
            return
        msgBox = mbox.askokcancel('Delete task', 'Are you sure you want to Delete task to {}?'.format(delTask))
        if msgBox:
            self.message['text'] = ''
            self.tree.item(self.tree.selection())['text']
            query = 'DELETE FROM tasks WHERE tasks.id_users = ? AND tasks.turn = ?'   #DELETE FROM tasks WHERE tasks.turn = 3 AND tasks.id_users = 6
            self.db_query(query, (idUser, delTurn))
            self.message['text'] = 'Turn for {} deleted'.format(delTask)
        self.get_clients()

    # Heading Table by date
    def table_consult_date(self):
        self.tree = ttk.Treeview(columns = ('#1', '#2', '#3', '#4', '#5'), selectmode = 'browse', height = 10,
                                 padding = 8)
        self.tree.grid(row = 12, column = 0)
        self.tree.column('#0', width = 140, minwidth = 40, stretch = NO)
        self.tree.column('#1', width = 80, minwidth = 80)
        self.tree.column('#2', width = 80, minwidth = 60)
        self.tree.column('#3', width = 160, minwidth = 120)
        self.tree.column('#4', width = 80, minwidth = 60)
        self.tree.column('#5', width = 60, minwidth = 40)
        self.tree.heading('#0', text = 'User Name', anchor = CENTER)
        self.tree.heading('#1', text = 'Date', anchor = CENTER)
        self.tree.heading('#2', text = ' Schedule', anchor = CENTER)
        self.tree.heading('#3', text = 'Service', anchor = CENTER)
        self.tree.heading('#4', text = 'Amount', anchor = CENTER)
        self.tree.heading('#5', text = 'Turn', anchor = CENTER)
        # Scrollbar
        self.vsb = ttk.Scrollbar(window, orient = 'vertical', command = self.tree.yview)
        self.vsb.place(x = 620, y = 159, height = 238)
        self.tree.configure(yscrollcommand = self.vsb.set)

    # Consult tasks by date
    def get_tasks(self):
        self.message['text'] = ''
        # Cleaning table
        self.cleaning()
        # Disabled Buttons
        self.btn_disabled()
        self.btnDeltask.place_forget()
        # table
        self.table_consult_date()
        # Consulting table
        query = 'SELECT users.login, tasks.date, tasks.hour, tasks.title, tasks.amount, tasks.turn FROM users INNER JOIN tasks WHERE users.id = tasks.id_users  ORDER BY tasks.date DESC, tasks.hour DESC'
        db_rows = self.db_query(query)
        # filling data
        for row in db_rows:
            self.tree.insert('', 0, text = row[0], values = (row[1], row[2], row[3], row[4], row[5]))

    # Consult by day
    def get_day(self):
        self.message['text'] = ''
        dateCons = self.date.get()
        if len(dateCons) == 0:
            self.message['text'] = 'Date is required'
        else:
            self.btn_disabled()
            self.btnDeltask.place_forget()
            # Cleaning table
            self.cleaning()
            # table
            self.table_consult_date()
            # Consulting table
            query = 'SELECT users.login, tasks.date, tasks.hour, tasks.title, tasks.amount, tasks.turn FROM users INNER JOIN tasks ON users.id = tasks.id_users WHERE tasks.date = ? ORDER BY tasks.hour DESC'
            parameters = (dateCons,)
            db_rows = self.db_query(query, parameters)
            # filling data
            for row in db_rows:
                self.tree.insert('', 0, text = row[0], values = (row[1], row[2], row[3], row[4], row[5]))


if __name__ == '__main__':
    window = tk.Tk()
    sp = (os.path.dirname(__file__))  #Icon root
    # Icon
    img_icon = PhotoImage(file = os.path.join(sp, 'diamante.png'))
    window.tk.call('wm', 'iconphoto', window._w, img_icon)
    application = User(window)
    window['bg'] = '#ffc8fb' #Window color background
    window.mainloop()