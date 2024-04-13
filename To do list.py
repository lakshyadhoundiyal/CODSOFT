import tkinter
import tkinter.messagebox
import pickle

#colors
co0 = "#ffffff" 
co1 = "#000000"
co2 = "#4456f0"

#window
window = tkinter.Tk()
window.title("To do list")
window.geometry("450x500")  
window.resizable(width=False , height=False)



def task_adding():
    todo = task_add.get()
    if todo != "":
        todo_box.insert(tkinter.END, todo)
        task_add.delete(0, tkinter.END)
    else:
        tkinter.messagebox.showwarning(title="Attention!", message="To add a task, please enter the task.")

def task_removing():
    try:
        index_todo = todo_box.curselection()[0]
        todo_box.delete(index_todo)
    except:
        tkinter.messagebox.showwarning(title="Attention!", message="To delete the task, please select the task.")

def task_load():
    try:
        tasks = pickle.load(open("tasks.dat", "rb"))
        todo_box.delete(0, tkinter.END)
        for todo in tasks:
            todo_box.insert(tkinter.END, todo)
    except:
        tkinter.messagebox.showwarning(title="Attention!", message="Cannot find tasks.dat")

def task_save():
    todo_list = todo_box.get(0, tkinter.END)
    try:
        pickle.dump(todo_list, open("tasks.dat", "wb"))
        tkinter.messagebox.showinfo("Success", "Tasks saved successfully!")
    except Exception as e:
        tkinter.messagebox.showerror("Error", f"Failed to save tasks: {e}")

def task_clear():
    todo_box.delete(0, tkinter.END)



list_frame = tkinter.Frame(window)
list_frame.pack()

todo_box = tkinter.Listbox(list_frame, height=20, width=50)
todo_box.pack(side=tkinter.LEFT)

scroller = tkinter.Scrollbar(list_frame)
scroller.pack(side=tkinter.RIGHT, fill=tkinter.Y)

todo_box.config(yscrollcommand=scroller.set)
scroller.config(command=todo_box.yview)

task_add = tkinter.Entry(window, width=70)
task_add.pack()

add_task_button = tkinter.Button(window, text="CLICK TO ADD TASK", font=("Ivy 8 bold", 10, "bold"), bg=co2, width=30, command=task_adding)
add_task_button.pack()

remove_task_button = tkinter.Button(window, text="CLICK TO REMOVE TASK", font=("Ivy 8 bold", 10, "bold"), bg="pink", width=30, command=task_removing)
remove_task_button.pack()

load_task_button = tkinter.Button(window, text="CLICK TO LOAD TASK", font=("Ivy 8 bold", 10, "bold"), bg=co2, width=30, command=task_load)
load_task_button.pack()

save_task_button = tkinter.Button(window, text="CLICK TO SAVE TASK", font=("Ivy 8 bold", 10, "bold"), bg="pink", width=30, command=task_save)
save_task_button.pack()

clear_task_button = tkinter.Button(window, text="CLICK TO CLEAR SCREEN", font=("Ivy 8 bold", 10, "bold"), bg=co2, width=30, command=task_clear)
clear_task_button.pack()

window.mainloop()
