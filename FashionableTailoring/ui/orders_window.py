import tkinter as tk
from tkinter import ttk, messagebox
from database import Database
from datetime import datetime

class OrdersWindow:
    def __init__(self, root, user_info):
        self.root = root
        self.db = Database()
        self.window = tk.Toplevel(self.root)
        self.window.title("Заказы")
        self.window.geometry("800x600")
        self.user_info = user_info
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.window, text="Заказы", font=("Arial", 18)).pack(pady=20)

        # Создаем таблицу для отображения заказов
        self.tree = ttk.Treeview(self.window, columns=(
            "order_id", "full_name", "order_date", "period_of_execution", "order_status"), show="headings")

        # Определяем заголовки столбцов
        self.tree.heading("order_id", text="Номер заказа")
        self.tree.heading("full_name", text="Пользователь")
        self.tree.heading("order_date", text="Дата заказа")
        self.tree.heading("period_of_execution", text="Дата получения")
        self.tree.heading("order_status", text="Статус")

        # Устанавливаем ширину столбцов
        self.tree.column("order_id", width=100)
        self.tree.column("full_name", width=150)
        self.tree.column("order_date", width=150)
        self.tree.column("period_of_execution", width=150)
        self.tree.column("order_status", width=150)

        self.tree.pack(fill=tk.BOTH, expand=True)

        # Добавляем полосу прокрутки
        scrollbar = ttk.Scrollbar(self.window, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.load_orders()

        tk.Button(self.window, text="Добавить заказ", command=self.add_order).pack(pady=10)
        tk.Button(self.window, text="Редактировать заказ", command=self.edit_order).pack(pady=10)
        tk.Button(self.window, text="Удалить заказ", command=self.delete_order).pack(pady=10)

    def load_orders(self):
        # Очищаем таблицу
        for i in self.tree.get_children():
            self.tree.delete(i)

        # Загружаем заказы из базы данных
        orders = self.db.execute_query("SELECT \
            Orders.order_id, \
            Users.full_name, \
            Orders.order_date, \
            Orders.period_of_execution, \
            Orders.order_status \
            FROM Orders \
            JOIN Users ON Users.user_id = Orders.user_id")
        for order in orders:
            self.tree.insert("", "end", values=order)

    def add_order(self):
        # Создаем диалоговое окно для добавления заказа
        add_window = tk.Toplevel(self.window)
        add_window.title("Добавить заказ")
        add_window.geometry("400x300")

        tk.Label(add_window, text="Дата заказа:").pack(pady=5)
        order_date_entry = tk.Entry(add_window)
        order_date_entry.pack(pady=5)

        tk.Label(add_window, text="Дата получения:").pack(pady=5)
        period_of_execution_entry = tk.Entry(add_window)
        period_of_execution_entry.pack(pady=5)

        tk.Label(add_window, text="Статус:").pack(pady=5)
        order_status_entry = tk.Entry(add_window)
        order_status_entry.pack(pady=5)

        def save_order():
            order_date = order_date_entry.get()
            period_of_execution = period_of_execution_entry.get()
            order_status = order_status_entry.get()

            if not order_date or not period_of_execution or not order_status:
                messagebox.showerror("Ошибка", "Заполните все поля")
                return

            # Убедитесь, что даты передаются в правильном формате
            try:
                order_date = datetime.strptime(order_date, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")
                period_of_execution = datetime.strptime(period_of_execution, "%Y-%m-%d %H:%M:%S").strftime(
                    "%Y-%m-%d %H:%M:%S")
            except ValueError:
                messagebox.showerror("Ошибка", "Неверный формат даты. Используйте формат YYYY-MM-DD HH:MM:SS")
                return

            self.db.execute_query(
                "INSERT INTO Orders (order_date, user_id, period_of_execution, order_status) VALUES (%s, %s, %s, %s)",
                (order_date, self.user_info[0], period_of_execution, order_status), fetch=False)
            add_window.destroy()
            self.load_orders()

        tk.Button(add_window, text="Сохранить", command=save_order).pack(pady=10)

    def edit_order(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Ошибка", "Выберите заказ для редактирования")
            return

        order_id = self.tree.item(selected_item)['values'][0]
        order_date = self.tree.item(selected_item)['values'][2]
        period_of_execution = self.tree.item(selected_item)['values'][3]
        order_status = self.tree.item(selected_item)['values'][4]

        # Создаем диалоговое окно для редактирования заказа
        edit_window = tk.Toplevel(self.window)
        edit_window.title("Редактировать заказ")
        edit_window.geometry("400x300")

        tk.Label(edit_window, text="Дата заказа:").pack(pady=5)
        order_date_entry = tk.Entry(edit_window)
        order_date_entry.insert(0, order_date)
        order_date_entry.pack(pady=5)

        tk.Label(edit_window, text="Дата получения:").pack(pady=5)
        period_of_execution_entry = tk.Entry(edit_window)
        period_of_execution_entry.insert(0, period_of_execution)
        period_of_execution_entry.pack(pady=5)

        tk.Label(edit_window, text="Статус:").pack(pady=5)
        order_status_entry = tk.Entry(edit_window)
        order_status_entry.insert(0, order_status)
        order_status_entry.pack(pady=5)

        def update_order():
            new_order_date = order_date_entry.get()
            new_period_of_execution = period_of_execution_entry.get()
            new_order_status = order_status_entry.get()

            if not new_order_date or not new_period_of_execution or not new_order_status:
                messagebox.showerror("Ошибка", "Заполните все поля")
                return

            # Убедитесь, что даты передаются в правильном формате
            try:
                new_order_date = datetime.strptime(new_order_date, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")
                new_period_of_execution = datetime.strptime(new_period_of_execution, "%Y-%m-%d %H:%M:%S").strftime(
                    "%Y-%m-%d %H:%M:%S")
            except ValueError:
                messagebox.showerror("Ошибка", "Неверный формат даты. Используйте формат YYYY-MM-DD HH:MM:SS")
                return

            self.db.execute_query(
                "UPDATE Orders SET order_date = %s, period_of_execution = %s, order_status = %s WHERE order_id = %s",
                (new_order_date, new_period_of_execution, new_order_status, order_id), fetch=False)
            edit_window.destroy()
            self.load_orders()

        tk.Button(edit_window, text="Сохранить", command=update_order).pack(pady=10)

    def delete_order(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Ошибка", "Выберите заказ для удаления")
            return

        order_id = self.tree.item(selected_item)['values'][0]
        confirm = messagebox.askyesno("Подтверждение", f"Вы уверены, что хотите удалить заказ №{order_id}?")
        if confirm:
            self.db.execute_query("DELETE FROM Orders WHERE order_id = %s", (order_id,), fetch=False)
            self.load_orders()