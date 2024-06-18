import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import DateEntry, Calendar
import os
import json
from datetime import datetime

class Task:
    def __init__(self, title, deadline, details, status="未着手"):
        self.title = title
        self.deadline = deadline
        self.details = details
        self.status = status

    def to_dict(self):
        return {
            "title": self.title,
            "deadline": self.deadline,
            "details": self.details,
            "status": self.status
        }

    @staticmethod
    def from_dict(data):
        return Task(
            data["title"],
            data["deadline"],
            data["details"],
            data.get("status", "未着手")  # デフォルト値を設定
        )

class TaskDialog(tk.Toplevel):
    def __init__(self, parent, task=None, date=None):
        super().__init__(parent)
        self.title("タスク追加" if task is None else "タスク編集")
        self.geometry("400x350")
        self.configure(bg="#f0f0f0")

        self.title_label = tk.Label(self, text="タイトル:", bg="#f0f0f0")
        self.title_label.pack(pady=5)
        self.title_entry = tk.Entry(self, width=40)
        self.title_entry.pack(pady=5)

        self.deadline_label = tk.Label(self, text="期限:", bg="#f0f0f0")
        self.deadline_label.pack(pady=5)
        self.deadline_entry = DateEntry(self, width=37, date_pattern="yyyy-mm-dd")
        self.deadline_entry.pack(pady=5)

        self.details_label = tk.Label(self, text="詳細:", bg="#f0f0f0")
        self.details_label.pack(pady=5)
        self.details_entry = tk.Entry(self, width=40)
        self.details_entry.pack(pady=5)

        self.status_label = tk.Label(self, text="ステータス:", bg="#f0f0f0")
        self.status_label.pack(pady=5)
        self.status_var = tk.StringVar()
        self.status_combobox = ttk.Combobox(self, textvariable=self.status_var, values=["未着手", "進行中", "完了"])
        self.status_combobox.pack(pady=5)
        self.status_combobox.current(0)  # デフォルトで "未着手" を選択

        self.add_button = tk.Button(self, text="保存", command=self.on_save_task, bg="#4CAF50", fg="white")
        self.add_button.pack(pady=10)

        self.task = task

        if task:
            self.title_entry.insert(0, task.title)
            self.deadline_entry.set_date(task.deadline)
            self.details_entry.insert(0, task.details)
            self.status_combobox.set(task.status)
        elif date:
            self.deadline_entry.set_date(date)

    def on_save_task(self):
        title = self.title_entry.get()
        deadline = self.deadline_entry.get()
        details = self.details_entry.get()
        status = self.status_var.get()
        if title:
            self.task = Task(title, deadline, details, status)
            self.destroy()
        else:
            messagebox.showwarning("警告", "タイトルは必須です。")

    def show(self):
        self.grab_set()
        self.wait_window()
        return self.task

class TaskManager:
    def __init__(self, root):
        self.root = root
        self.root.title("タスク管理")
        self.root.geometry("1000x600")
        
        self.style = ttk.Style()
        self.style.configure("Treeview.Heading", font=("Arial", 12, "bold"))
        self.style.configure("Treeview", font=("Arial", 10), rowheight=25)
        self.style.configure("TButton", font=("Arial", 10), padding=10)
        
        self.tasks = []
        self.load_tasks()

        self.left_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        self.calendar = Calendar(self.left_frame, selectmode='day', date_pattern='yyyy-mm-dd', background="white", foreground="black", selectbackground="#4CAF50")
        self.calendar.pack(pady=10)
        self.calendar.bind("<<CalendarSelected>>", self.on_date_select)

        self.button_frame = tk.Frame(self.left_frame, bg="#f0f0f0")
        self.button_frame.pack(pady=10, fill=tk.X)
        
        self.add_button = tk.Button(self.button_frame, text="タスク追加", command=self.add_task, bg="#4CAF50", fg="white")
        self.add_button.pack(fill=tk.X, pady=5)

        self.edit_button = tk.Button(self.button_frame, text="タスク編集", command=self.edit_task, bg="#2196F3", fg="white")
        self.edit_button.pack(fill=tk.X, pady=5)
        
        self.delete_button = tk.Button(self.button_frame, text="タスク削除", command=self.delete_task, bg="#f44336", fg="white")
        self.delete_button.pack(fill=tk.X, pady=5)

        self.show_all_button = tk.Button(self.button_frame, text="全てのタスクを表示", command=self.show_all_tasks, bg="#9E9E9E", fg="white")
        self.show_all_button.pack(fill=tk.X, pady=5)

        self.tree_frame = tk.Frame(self.root)
        self.tree_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.tree = ttk.Treeview(self.tree_frame, columns=("Title", "Deadline", "Details", "Status"), show="headings")
        self.tree.heading("Title", text="タイトル")
        self.tree.heading("Deadline", text="期限")
        self.tree.heading("Details", text="詳細")
        self.tree.heading("Status", text="ステータス")
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        self.tree.bind('<Double-1>', self.on_tree_select)

        self.update_task_list()
    
    def add_task(self):
        selected_date = self.calendar.get_date()
        dialog = TaskDialog(self.root, date=selected_date)
        task = dialog.show()
        if task:
            self.tasks.append(task)
            self.update_task_list()
            self.save_tasks()

    def edit_task(self):
        selected_item = self.tree.selection()
        if selected_item:
            task_index = self.tree.index(selected_item[0])
            task = self.tasks[task_index]
            dialog = TaskDialog(self.root, task)
            updated_task = dialog.show()
            if updated_task:
                self.tasks[task_index] = updated_task
                self.update_task_list()
                self.save_tasks()
        else:
            messagebox.showwarning("警告", "編集するタスクを選択してください。")
    
    def delete_task(self):
        selected_item = self.tree.selection()
        if selected_item:
            response = messagebox.askyesno("確認", "選択したタスクを削除してもよろしいですか？")
            if response:
                for item in selected_item:
                    task_index = self.tree.index(item)
                    del self.tasks[task_index]
                self.update_task_list()
                self.save_tasks()
        else:
            messagebox.showwarning("警告", "削除するタスクを選択してください。")
    
    def on_date_select(self, event):
        selected_date = self.calendar.get_date()
        self.update_task_list(selected_date)

    def show_all_tasks(self):
        self.update_task_list()

    def update_task_list(self, selected_date=None):
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.calendar.calevent_remove('all')
        for task in self.tasks:
            task_deadline = datetime.strptime(task.deadline, "%Y-%m-%d").date()
            self.calendar.calevent_create(task_deadline, task.title, "task")
            if selected_date is None or task.deadline == selected_date:
                self.tree.insert("", tk.END, values=(task.title, task.deadline, task.details, task.status))

    def save_tasks(self):
        with open("tasks.json", "w") as file:
            tasks_data = [task.to_dict() for task in self.tasks]
            json.dump(tasks_data, file)
    
    def load_tasks(self):
        if os.path.exists("tasks.json"):
            with open("tasks.json", "r") as file:
                try:
                    tasks_data = json.load(file)
                    self.tasks = [Task.from_dict(task_data) for task_data in tasks_data]
                except json.JSONDecodeError:
                    self.tasks = []

    def on_tree_select(self, event):
        item_id = self.tree.identify_row(event.y)
        column_id = self.tree.identify_column(event.x)
        if column_id == "#4":  # "Status"列の場合
            self.show_status_combobox(item_id)

    def show_status_combobox(self, item_id):
        x, y, width, height = self.tree.bbox(item_id, "Status")
        status_var = tk.StringVar()
        status_combobox = ttk.Combobox(self.tree_frame, textvariable=status_var, values=["未着手", "進行中", "完了"])
        status_combobox.place(x=x, y=y + self.tree_frame.winfo_y(), width=width, height=height)
        status_combobox.set(self.tree.set(item_id, "Status"))
        status_combobox.bind("<<ComboboxSelected>>", lambda event: self.on_status_change(event, item_id, status_combobox))

    def on_status_change(self, event, item_id, combobox):
        new_status = combobox.get()
        self.tree.set(item_id, "Status", new_status)
        task_index = self.tree.index(item_id)
        self.tasks[task_index].status = new_status
        self.save_tasks()
        combobox.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    task_manager = TaskManager(root)
    root.mainloop()
