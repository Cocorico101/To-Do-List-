from tkinter import *

class EmptyListError(Exception):
    """Raised when trying to remove from an empty list"""
    pass

class ToDoList:
    """Represents to do list GUI to display tasks to complete
    Also update text file as GUI changes"""
    def __init__(self, root):
        self.root = root
        self.root.title("To Do List")
        self.root.geometry('1000x500+365+250')
        self.root.resizable(True, True)
        self.action = []

        #self.root.rowconfigure(1,weight=1)
        self.root.columnconfigure(0,weight=1)
        #self.root.columnconfigure(1, weight=1)

        #Create label for app
        self.label = Label(self.root, text='To Do List App', font='ariel, 25 bold', width=15, bd=5, bg='grey', fg='black')

        self.label.grid(row=0, columnspan=4, sticky=EW)

        #Label for task list
        self.labeltask = Label(self.root, text="Tasks List", font='ariel, 15 bold', width=10, bd=10, bg='khaki1', fg="black")
        self.labeltask.grid(row=1, column=0)

        #================TEXT FIELD TO ENTER TASK===========#

        self.task_field = Text(self.root, height=2, width=22, font='ariel, 12', bd=5, highlightcolor='blue', undo=True)
        #self.task_field = Text(self.root)
        self.task_field.grid(row=2, column=1, sticky=N)

        #Create frame for task list and scrollbar
        self.frame = Frame(self.root)
        self.frame.grid(row=2, column=0, sticky=E+W+N+S)
        #self.frame.rowconfigure(0,weight=1)
        self.frame.columnconfigure(0,weight=1)

        #self.task_list = Listbox(self.frame, height=25, width=40, font='ariel, 12', bd=5, highlightcolor='blue', cursor='arrow')
        self.task_list = Listbox(self.frame, font='ariel, 12')
        #self.task_list.pack(side=LEFT, fill=Y, expand=True)
        self.task_list.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')

        task_list_scrollbar = Scrollbar(self.frame, orient='vertical')
        #task_list_scrollbar.pack(side=RIGHT, fill=Y)
        task_list_scrollbar.grid(row=0, column=1, sticky='ns')
        task_list_scrollbar.config(command=self.task_list.yview)

        self.task_list.config(yscrollcommand=task_list_scrollbar.set)

        #===============ADD TASK FUNCTION================#
        def add_task():
            """Method to add task to GUI and text file"""
            if len(self.task_field.get(1.0, 'end-1c')) == 0:
                print("Cannot have empty input")
                return
            content = self.task_field.get(1.0, END)
            self.task_list.insert(END, content)

            #Write content in the seperate file
            with open('data.txt', 'a') as file:
                file.write(content)
                file.seek(0)
            #Make it disappear from the text box after it is added to the task list
            self.task_field.delete(1.0, END)

        #===============DELETE TASK FUNCTION===============#
        def delete_task():
            """"Method to remove task one at a time from GUI and text file. EmptyListError exception is thrown if GUI is empty"""
            #delete = self.task_list.curselection()
            try:
                if self.task_list.size() == 0:
                    raise EmptyListError
                if len(self.task_list.curselection()) == 0:
                    raise EmptyListError
                delete = self.task_list.curselection()
                look = self.task_list.get(delete)
                #Remove from text file
                with open('data.txt', 'r+') as f:
                    new_f = f.readlines()
                    f.seek(0)
                    for line in new_f:
                        item = str(look)
                        check_tuple = isinstance(look, tuple)
                        if check_tuple is True:
                            item = ' '.join(look)
                        #first_item = item[0]
                        if item not in line:
                            f.write(line)
                        f.truncate()
            #Remove from GUI
                self.task_list.delete(delete)
            except EmptyListError:
                print("Empty List Exception occurred: Cannot remove from an empty list")

        with open('data.txt', 'r') as file:
            #Get each line in a seperated line
            file_line = file.readlines()
            for i in file_line:
                ready = i.split()
                self.task_list.insert(END, ready)
            file.close()

        #================ADD/REMOVE BUTTONS===============#
        self.add_button = Button(self.root, text="Add Task", font='ariel, 15 bold italic', width=10, bd=5, bg='orange', fg='black', command=add_task)
        self.add_button.grid(row=1, column=1, padx=5, pady=5)

        self.delete_button = Button(self.root, text="Remove Task", font='ariel, 15 bold italic', width=10, bd=5, bg='orange', fg='black', command=delete_task)
        self.delete_button.grid(row=1, column=2, padx=10, pady=5)

        def clear_task():
            """Clear all tasks in GUI and text file"""
            #Clear tasks in GUI
            self.task_list.delete(0, END)

            #Clear tasks in text file
            with open('data.txt', 'r+') as file:
                file.truncate(0)

        #============CLEAR BUTTON==============#
        self.clear_button = Button(self.root, text="Clear all ", font='ariel, 15 bold italic', width=10, bd=5, bg='orange', fg='black', command=clear_task)
        self.clear_button.grid(row=1, column=3, padx=10)

        def clear_all_but_selected():
            """"Clear all task and only keep the selected in GUI and text file. Empty List Error exception is thrown if list empty"""
            #Clear tasks in the GUI
            try:
                if self.task_list.size() == 0:
                    raise EmptyListError
                store_current()

                if len(self.task_list.curselection()) == 0:
                    raise EmptyListError
                do_not_clear_this = self.task_list.curselection()
                look = self.task_list.get(do_not_clear_this)

                #Remove from text file
                with open('data.txt', 'r+') as f:
                    new_f = f.readlines()
                    f.seek(0)
                    for line in new_f:
                        #Check to see if each line is a tuple, if it is, join them. Ignore if not tuple.
                        item = str(look)
                        check_tuple = isinstance(look, tuple)
                        if check_tuple is True:
                            item = ' '.join(look)
                        #Remove everything but the selected line.
                        if item in line:
                            f.truncate()
                            f.write(item)

                #Remove from GUI
                self.task_list.delete(0, do_not_clear_this[0] -1)
                self.task_list.delete(1, END)
            except EmptyListError:
                print("Empty List Exception occurred: Cannot remove from an empty list")

        # ============CLEAR ALL BUT SELECTED BUTTON==============#
        self.clear_all_but_selected_button = Button(self.root, text="Clear all but selected", font='ariel, 15 bold italic', width=18, bd=5,bg='orange', fg='black', command=clear_all_but_selected)
        self.clear_all_but_selected_button.grid(row=2, column=3, padx=10)

        def store_current():
            """Store current contents of the list"""
            file = open("data.txt", "r")
            data = file.readlines()
            file.seek(0)
            self.action.clear()
            for line in data:
                self.action.append(line.strip())
            print(self.action)
            file.close()

        def undo_clear_all_but_selected():
            """Undo the action of clear all but selected"""
            #Update the GUI to display store_current() contents
            look = self.task_list.curselection()
            self.task_list.delete(look)
            for item in self.action:
                self.task_list.insert(END, item)

            #Update text file to store_current() contents
            with open ("data.txt", 'w') as file:
                for item in self.action:
                    file.write("%s\n" % item)

        #==================UNDO-CLEAR-ALL-BUT-SELECTED-BUTTON================#
        self.undo_clear_all_selected = Button(self.root, text="Undo Clear all but selected", font='ariel, 15 bold italic', width=22, bd=5,bg='orange', fg='black', command=undo_clear_all_but_selected)
        self.undo_clear_all_selected.grid(row=3, column=3, padx=10)

def main():
    """Start up GUI of to do list"""
    root = Tk()
    ui_window = ToDoList(root)
    #Keep making it appearing
    root.mainloop()
    #Run main
if __name__ == "__main__":
        main()