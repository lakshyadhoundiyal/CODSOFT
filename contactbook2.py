import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pickle

co0 = "#ffffff"
co1 = "#000000"
co2 = "#4456f0"

window = tk.Tk()
window.title("Contact book")
window.geometry('495x455')
window.configure(background=co0)
window.resizable(width=False, height=False)


frame_up = tk.Frame(window, width=500, height=50, bg=co2)
frame_up.grid(row=0, column=0, padx=0, pady=1)

frame_down = tk.Frame(window, width=500, height=150, bg=co0)
frame_down.grid(row=1, column=0, padx=0, pady=1)

frame_table = tk.Frame(window, width=500, height=100, bg=co0, relief='flat')
frame_table.grid(row=2, column=0, columnspan=2, padx=10, pady=1, sticky=tk.NW)



data_list = []


def label_entry(frame, labelText, position):
    label = tk.Label(frame, text=labelText, width=20, height=1, font=('Ivy 10'), bg=co0, anchor=tk.NW)
    label.place(x=position[0], y=position[1])
    
    if labelText == 'Address':
        entry = tk.Entry(frame, width=25, justify='left',highlightthickness=1, relief="solid")
        entry.place(x=position[2], y=position[3])
        return label, entry
    else:
        entry = tk.Entry(frame, width=25, justify='left',highlightthickness=1, relief="solid")
        entry.place(x=position[2], y=position[3])
        return label, entry

l_name, e_name = label_entry(frame_down, "Name", [10, 20, 80, 20])
l_Address, e_Address = label_entry(frame_down, "Address", [10, 50, 80, 50])
l_telephone, e_telephone = label_entry(frame_down, "Telephone", [10, 80, 80, 80])
l_email, e_email = label_entry(frame_down, "Email", [10, 110, 80, 110])

def create_treeview(frame):
    treeview = ttk.Treeview(frame)
    treeview["columns"] = ("Name", "Address", "Telephone", "Email")
    treeview.column("#0", width=0, stretch=False)
    treeview.column("Name", width=100)
    treeview.column("Address", width=100)
    treeview.column("Telephone", width=100)
    treeview.column("Email", width=180)

    treeview.heading("#0",text="")
    treeview.heading("Name",text="Name")
    treeview.heading("Address",text="Address")
    treeview.heading("Telephone",text="Telephone")
    treeview.heading("Email",text="Email") 

    treeview.pack(side=tk.LEFT, fill=tk.Y)
    return treeview

scrollbar_x = tk.Scrollbar(frame_table, orient=tk.HORIZONTAL)
scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)

scrollbar_y = tk.Scrollbar(frame_table, orient=tk.VERTICAL)
scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)

tree = create_treeview(frame_table)

tree.config(xscrollcommand=scrollbar_x.set, yscrollcommand=scrollbar_y.set)
scrollbar_x.config(command=tree.xview)
scrollbar_y.config(command=tree.yview)

def add_data():
    Name = e_name.get()
    Address = e_Address.get()
    Telephone = e_telephone.get()
    Email = e_email.get()

    if Name and Address and Telephone and Email:
        data_list.append({"Name":Name,"Address":Address, "Telephone":Telephone, "Email":Email})
        tree.insert("", "end", values=(Name, Address, Telephone, Email))
        messagebox.showinfo('Success', 'Data added successfully')
        e_name.delete(0, 'end')
        e_Address.set('')
        e_telephone.delete(0, 'end')
        e_email.delete(0, 'end')
       
        with open('data.pkl', 'wb') as f:
            pickle.dump(data_list, f)
    else:
        messagebox.showinfo('Failure', 'Please fill all the fields')

def load_data():
    global data_list
    try:
       
        with open('data.pkl', 'rb') as f:
            data_list = pickle.load(f)
            for child in tree.get_children():
                tree.delete(child)
            for data in data_list:
                tree.insert("", "end", values=(data["Name"], data["Address"], data["Telephone"], data["Email"]))
    except Exception as e:
        pass

def search_data():
    if e_search.get():
        for child in tree.get_children():
            tree.delete(child) 
        for data in data_list:
            if data["Name"].startswith(e_search.get()):
                tree.insert("", "end", values=(data["Name"], data["Address"], data["Telephone"], data["Email"]))
    else:
        for child in tree.get_children():
            tree.delete(child) 
        for data in data_list:
            tree.insert("", "end", values=(data["Name"], data["Address"], data["Telephone"], data["Email"]))

def select_item(event):
    selected_item = tree.selection()[0]
    values = tree.item(selected_item)["values"]
    e_name.delete(0, 'end')
    e_name.insert(0, values[0])
    e_Address.set(values[1])
    e_telephone.delete(0, 'end')
    e_telephone.insert(0, values[2])
    e_email.delete(0, 'end')
    e_email.insert(0, values[3])

def update_data():
    selected_item = tree.selection()[0]
    values = tree.item(selected_item)["values"]
    for data in data_list:
        if data['Name'] == values[0]:
            data['Address'] = e_Address.get()
            data['Telephone'] = e_telephone.get()
            data['Email'] = e_email.get()
            tree.item(selected_item, values=(e_name.get(), e_Address.get(), e_telephone.get(), e_email.get()))
          
            with open('data.pkl', 'wb') as f:
                pickle.dump(data_list, f)
    messagebox.showinfo('Success', 'Data updated successfully')

def delete_data():
    selected_item = tree.selection()[0]
    values = tree.item(selected_item)["values"]
    for data in data_list:
        if data['Name'] == values[0]:
            data_list.remove(data)
            tree.delete(selected_item)
            e_name.delete(0, 'end')
            e_Address.set('')
            e_telephone.delete(0, 'end')
            e_email.delete(0, 'end')
         
            with open('data.pkl', 'wb') as f:
                pickle.dump(data_list, f)
    messagebox.showinfo('Success', 'Data deleted successfully')


#buttons

b_add = tk.Button(frame_down, text="Add", height=1, bg=co2, fg=co0, font=('Ivy 8 bold'), width=10, command=add_data)
b_add.place(x=400, y=50)

b_load = tk.Button(frame_down, text="Load", height=1, bg=co2, fg=co0, font=('Ivy 8 bold'), width=10, command=load_data)
b_load.place(x=250, y=50)

b_update = tk.Button(frame_down, text="Update", height=1, bg=co2, fg=co0, font=('Ivy 8 bold'), width=10, command=update_data)
b_update.place(x=400, y=80)

b_delete = tk.Button(frame_down, text="Delete", height=1, bg=co2, fg=co0, font=('Ivy 8 bold'), width=10, command=delete_data)
b_delete.place(x=400, y=110)

b_search = tk.Button(frame_down, text="Search", height=1, bg=co2, fg=co0, font=('Ivy 8 bold'), width=10, command=search_data)
b_search.place(x=250, y=20)

e_search = tk.Entry(frame_down, width=16, justify='left', font=('Ivy', 11), highlightthickness=1, relief="solid")
e_search.place(x=347, y=20)

tree.bind('<ButtonRelease-1>', select_item)

window.mainloop()
