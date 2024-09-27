import tkinter as tk
from tkinter import ttk, messagebox
from database import Database

class WarehouseWindow:
    def __init__(self, root):
        self.root = root
        self.db = Database()
        self.window = tk.Toplevel(self.root)
        self.window.title("Склад")
        self.window.geometry("800x600")

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.window, text="Склад", font=("Arial", 18)).pack(pady=20)

        # Создаем таблицу для отображения данных склада
        self.tree = ttk.Treeview(self.window, columns=(
            "product_id", "quantity", "size", "color", "model_name", "type_name", "material_name"), show="headings")

        # Определяем заголовки столбцов
        self.tree.heading("product_id", text="ID товара")
        self.tree.heading("quantity", text="Количество")
        self.tree.heading("size", text="Размер")
        self.tree.heading("color", text="Цвет")
        self.tree.heading("model_name", text="Модель")
        self.tree.heading("type_name", text="Тип")
        self.tree.heading("material_name", text="Материал")

        # Устанавливаем ширину столбцов
        self.tree.column("product_id", width=100)
        self.tree.column("quantity", width=100)
        self.tree.column("size", width=100)
        self.tree.column("color", width=100)
        self.tree.column("model_name", width=100)
        self.tree.column("type_name", width=100)
        self.tree.column("material_name", width=100)

        self.tree.pack(fill=tk.BOTH, expand=True)

        # Добавляем полосу прокрутки
        scrollbar = ttk.Scrollbar(self.window, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.load_warehouse()

        tk.Button(self.window, text="Добавить материал/продукцию", command=self.add_item).pack(pady=10)
        tk.Button(self.window, text="Редактировать", command=self.edit_item).pack(pady=10)
        tk.Button(self.window, text="Удалить", command=self.delete_item).pack(pady=10)

    def load_warehouse(self):
        # Очищаем таблицу
        for i in self.tree.get_children():
            self.tree.delete(i)

        # Загружаем данные склада из базы данных
        items = self.db.execute_query("SELECT \
            Warehouse.product_id, \
            Warehouse.quantity, \
            Products.size, \
            Products.color, \
            ProductModels.model_name, \
            ProductTypes.type_name, \
            Materials.material_name \
            FROM Warehouse \
            JOIN Products ON Warehouse.product_id = Products.product_id \
            JOIN ProductModels ON Products.model_id = ProductModels.model_id \
            JOIN ProductTypes ON Products.type_id = ProductTypes.type_id \
            JOIN Materials ON Products.material_id = Materials.material_id")
        for item in items:
            self.tree.insert("", "end", values=item)

    def add_item(self):
        # Создаем диалоговое окно для добавления материала/продукции
        add_window = tk.Toplevel(self.window)
        add_window.title("Добавить материал/продукцию")
        add_window.geometry("400x300")

        tk.Label(add_window, text="ID товара:").pack(pady=5)
        product_id_entry = tk.Entry(add_window)
        product_id_entry.pack(pady=5)

        tk.Label(add_window, text="Количество:").pack(pady=5)
        quantity_entry = tk.Entry(add_window)
        quantity_entry.pack(pady=5)

        def save_item():
            product_id = product_id_entry.get()
            quantity = quantity_entry.get()

            if not product_id or not quantity:
                messagebox.showerror("Ошибка", "Заполните все поля")
                return

            self.db.execute_query(
                "INSERT INTO Warehouse (product_id, quantity) VALUES (%s, %s)",
                (product_id, quantity), fetch=False)
            add_window.destroy()
            self.load_warehouse()

        tk.Button(add_window, text="Сохранить", command=save_item).pack(pady=10)

    def edit_item(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Ошибка", "Выберите товар для редактирования")
            return

        product_id = self.tree.item(selected_item)['values'][0]
        quantity = self.tree.item(selected_item)['values'][1]

        # Создаем диалоговое окно для редактирования материала/продукции
        edit_window = tk.Toplevel(self.window)
        edit_window.title("Редактировать материал/продукцию")
        edit_window.geometry("400x300")

        tk.Label(edit_window, text="ID товара:").pack(pady=5)
        product_id_entry = tk.Entry(edit_window)
        product_id_entry.insert(0, product_id)
        product_id_entry.pack(pady=5)

        tk.Label(edit_window, text="Количество:").pack(pady=5)
        quantity_entry = tk.Entry(edit_window)
        quantity_entry.insert(0, quantity)
        quantity_entry.pack(pady=5)

        def update_item():
            new_product_id = product_id_entry.get()
            new_quantity = quantity_entry.get()

            if not new_product_id or not new_quantity:
                messagebox.showerror("Ошибка", "Заполните все поля")
                return

            self.db.execute_query(
                "UPDATE Warehouse SET quantity = %s WHERE product_id = %s",
                (new_quantity, new_product_id), fetch=False)
            edit_window.destroy()
            self.load_warehouse()

        tk.Button(edit_window, text="Сохранить", command=update_item).pack(pady=10)

    def delete_item(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Ошибка", "Выберите товар для удаления")
            return

        product_id = self.tree.item(selected_item)['values'][0]
        confirm = messagebox.askyesno("Подтверждение", f"Вы уверены, что хотите удалить товар №{product_id}?")
        if confirm:
            self.db.execute_query("DELETE FROM Warehouse WHERE product_id = %s", (product_id,), fetch=False)
            self.load_warehouse()