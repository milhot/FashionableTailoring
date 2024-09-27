import tkinter as tk
from tkinter import ttk, messagebox
from database import Database
from datetime import datetime

class ProductionWindow:
    def __init__(self, root, user_info):
        self.root = root
        self.db = Database()
        self.window = tk.Toplevel(self.root)
        self.window.title("Производство")
        self.window.geometry("800x600")
        self.user_info = user_info

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.window, text="Производство", font=("Arial", 18)).pack(pady=20)

        # Создаем таблицу для отображения заданий
        self.tree = ttk.Treeview(self.window, columns=(
            "target_id", "order_id", "performer_name", "period_of_execution", "target_status"), show="headings")

        # Определяем заголовки столбцов
        self.tree.heading("target_id", text="Номер задания")
        self.tree.heading("order_id", text="Номер заказа")
        self.tree.heading("performer_name", text="Исполнитель")
        self.tree.heading("period_of_execution", text="Дата получения")
        self.tree.heading("target_status", text="Статус")

        # Устанавливаем ширину столбцов
        self.tree.column("target_id", width=100)
        self.tree.column("order_id", width=100)
        self.tree.column("performer_name", width=150)
        self.tree.column("period_of_execution", width=300)
        self.tree.column("target_status", width=150)

        self.tree.pack(fill=tk.BOTH, expand=True)

        # Добавляем полосу прокрутки
        scrollbar = ttk.Scrollbar(self.window, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.load_targets()

        tk.Button(self.window, text="Добавить задание", command=self.add_target).pack(pady=10)
        tk.Button(self.window, text="Редактировать задание", command=self.edit_target).pack(pady=10)
        tk.Button(self.window, text="Удалить задание", command=self.delete_target).pack(pady=10)

    def load_targets(self):
        # Очищаем таблицу
        for i in self.tree.get_children():
            self.tree.delete(i)

        # Загружаем задания из базы данных
        targets = self.db.execute_query("SELECT \
            ProductionTargets.target_id, \
            ProductionTargets.order_id, \
            Users.full_name AS performer_name, \
            ProductionTargets.period_of_execution, \
            ProductionTargets.target_status \
            FROM ProductionTargets \
            JOIN Users ON Users.user_id = ProductionTargets.performer_id")
        for target in targets:
            self.tree.insert("", "end", values=target)

    def add_target(self):
        # Создаем диалоговое окно для добавления задания
        add_window = tk.Toplevel(self.window)
        add_window.title("Добавить задание")
        add_window.geometry("400x300")

        tk.Label(add_window, text="Номер заказа:").pack(pady=5)
        order_id_entry = tk.Entry(add_window)
        order_id_entry.pack(pady=5)

        tk.Label(add_window, text="Дата получения:").pack(pady=5)
        period_of_execution_entry = tk.Entry(add_window)
        period_of_execution_entry.pack(pady=5)

        tk.Label(add_window, text="Статус:").pack(pady=5)
        target_status_entry = tk.Entry(add_window)
        target_status_entry.pack(pady=5)

        def save_target():
            order_id = order_id_entry.get()
            performer_id = self.user_info[0]
            period_of_execution = period_of_execution_entry.get()
            target_status = target_status_entry.get()

            if not order_id or not performer_id or not period_of_execution or not target_status:
                messagebox.showerror("Ошибка", "Заполните все поля")
                return

            try:
                period_of_execution = datetime.strptime(period_of_execution, "%Y-%m-%d %H:%M:%S").strftime(
                    "%Y-%m-%d %H:%M:%S")
            except ValueError:
                messagebox.showerror("Ошибка", "Неверный формат даты. Используйте формат YYYY-MM-DD HH:MM:SS")
                return

            self.db.execute_query(
                "INSERT INTO ProductionTargets (order_id, performer_id, period_of_execution, target_status) VALUES (%s, %s, %s, %s)",
                (order_id, performer_id, period_of_execution, target_status), fetch=False)
            add_window.destroy()
            self.load_targets()

        tk.Button(add_window, text="Сохранить", command=save_target).pack(pady=10)

    def edit_target(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Ошибка", "Выберите задание для редактирования")
            return

        target_id = self.tree.item(selected_item)['values'][0]
        order_id = self.tree.item(selected_item)['values'][1]
        performer_id = self.user_info[0]
        period_of_execution = self.tree.item(selected_item)['values'][3]
        target_status = self.tree.item(selected_item)['values'][4]

        # Создаем диалоговое окно для редактирования задания
        edit_window = tk.Toplevel(self.window)
        edit_window.title("Редактировать задание")
        edit_window.geometry("400x300")

        tk.Label(edit_window, text="Номер заказа:").pack(pady=5)
        order_id_entry = tk.Entry(edit_window)
        order_id_entry.insert(0, order_id)
        order_id_entry.pack(pady=5)


        tk.Label(edit_window, text="Дата получения:").pack(pady=5)
        period_of_execution_entry = tk.Entry(edit_window)
        period_of_execution_entry.insert(0, period_of_execution)
        period_of_execution_entry.pack(pady=5)

        tk.Label(edit_window, text="Статус:").pack(pady=5)
        target_status_entry = tk.Entry(edit_window)
        target_status_entry.insert(0, target_status)
        target_status_entry.pack(pady=5)

        def update_target():
            new_order_id = order_id_entry.get()
            new_period_of_execution = period_of_execution_entry.get()
            new_target_status = target_status_entry.get()

            if not new_order_id or not performer_id or not new_period_of_execution or not new_target_status:
                messagebox.showerror("Ошибка", "Заполните все поля")
                return

            try:
                new_period_of_execution = datetime.strptime(new_period_of_execution, "%Y-%m-%d %H:%M:%S").strftime(
                    "%Y-%m-%d %H:%M:%S")
            except ValueError:
                messagebox.showerror("Ошибка", "Неверный формат даты. Используйте формат YYYY-MM-DD HH:MM:SS")
                return

            self.db.execute_query(
                "UPDATE ProductionTargets SET order_id = %s, performer_id = %s, period_of_execution = %s, target_status = %s WHERE target_id = %s",
                (new_order_id, performer_id, new_period_of_execution, new_target_status, target_id), fetch=False)
            edit_window.destroy()
            self.load_targets()

        tk.Button(edit_window, text="Сохранить", command=update_target).pack(pady=10)

    def delete_target(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Ошибка", "Выберите задание для удаления")
            return

        target_id = self.tree.item(selected_item)['values'][0]
        confirm = messagebox.askyesno("Подтверждение", f"Вы уверены, что хотите удалить задание №{target_id}?")
        if confirm:
            self.db.execute_query("DELETE FROM ProductionTargets WHERE target_id = %s", (target_id,), fetch=False)
            self.load_targets()