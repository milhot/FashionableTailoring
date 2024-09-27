import tkinter as tk
from tkinter import ttk, messagebox
from database import Database

class ReportsWindow:
    def __init__(self, root):
        self.root = root
        self.db = Database()
        self.window = tk.Toplevel(self.root)
        self.window.title("Отчеты")
        self.window.geometry("800x600")

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.window, text="Отчеты", font=("Arial", 18)).pack(pady=20)

        self.report_type = tk.StringVar(value="orders")
        tk.Radiobutton(self.window, text="Заказы", variable=self.report_type, value="orders").pack(pady=5)
        tk.Radiobutton(self.window, text="Производство", variable=self.report_type, value="production").pack(pady=5)
        tk.Radiobutton(self.window, text="Материалы", variable=self.report_type, value="materials").pack(pady=5)
        tk.Radiobutton(self.window, text="Готовая продукция", variable=self.report_type, value="products").pack(pady=5)

        tk.Button(self.window, text="Сформировать отчет", command=self.generate_report).pack(pady=20)

    def generate_report(self):
        report_type = self.report_type.get()
        if report_type == "orders":
            self.generate_orders_report()
        elif report_type == "production":
            self.generate_production_report()
        elif report_type == "materials":
            self.generate_materials_report()
        elif report_type == "products":
            self.generate_products_report()

    def generate_orders_report(self):
        report_window = tk.Toplevel(self.window)
        report_window.title("Отчет по заказам")
        report_window.geometry("800x600")

        tree = ttk.Treeview(report_window, columns=(
            "order_id", "full_name", "order_date", "period_of_execution", "order_status"), show="headings")

        tree.heading("order_id", text="Номер заказа")
        tree.heading("full_name", text="Пользователь")
        tree.heading("order_date", text="Дата заказа")
        tree.heading("period_of_execution", text="Дата получения")
        tree.heading("order_status", text="Статус")

        tree.column("order_id", width=100)
        tree.column("full_name", width=150)
        tree.column("order_date", width=150)
        tree.column("period_of_execution", width=150)
        tree.column("order_status", width=150)

        tree.pack(fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(report_window, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        orders = self.db.execute_query("SELECT \
            Orders.order_id, \
            Users.full_name, \
            Orders.order_date, \
            Orders.period_of_execution, \
            Orders.order_status \
            FROM Orders \
            JOIN Users ON Users.user_id = Orders.user_id")
        for order in orders:
            tree.insert("", "end", values=order)

    def generate_production_report(self):
        report_window = tk.Toplevel(self.window)
        report_window.title("Отчет по производству")
        report_window.geometry("800x600")

        tree = ttk.Treeview(report_window, columns=(
            "target_id", "order_id", "performer_name", "period_of_execution", "target_status"), show="headings")

        tree.heading("target_id", text="Номер задания")
        tree.heading("order_id", text="Номер заказа")
        tree.heading("performer_name", text="Исполнитель")
        tree.heading("period_of_execution", text="Дата выполнения")
        tree.heading("target_status", text="Статус")

        tree.column("target_id", width=100)
        tree.column("order_id", width=100)
        tree.column("performer_name", width=150)
        tree.column("period_of_execution", width=150)
        tree.column("target_status", width=150)

        tree.pack(fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(report_window, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        targets = self.db.execute_query("SELECT \
            ProductionTargets.target_id, \
            ProductionTargets.order_id, \
            Users.full_name AS performer_name, \
            ProductionTargets.period_of_execution, \
            ProductionTargets.target_status \
            FROM ProductionTargets \
            JOIN Users ON Users.user_id = ProductionTargets.performer_id")
        for target in targets:
            tree.insert("", "end", values=target)

    def generate_materials_report(self):
        report_window = tk.Toplevel(self.window)
        report_window.title("Отчет по материалам")
        report_window.geometry("800x600")

        tree = ttk.Treeview(report_window, columns=(
            "material_id", "material_name", "quantity"), show="headings")

        tree.heading("material_id", text="ID материала")
        tree.heading("material_name", text="Название материала")
        tree.heading("quantity", text="Количество")

        tree.column("material_id", width=100)
        tree.column("material_name", width=300)
        tree.column("quantity", width=100)

        tree.pack(fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(report_window, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        materials = self.db.execute_query("SELECT \
            Materials.material_id, \
            Materials.material_name, \
            Warehouse.quantity \
            FROM Materials \
            JOIN Warehouse ON Materials.material_id = Warehouse.product_id")
        for material in materials:
            tree.insert("", "end", values=material)

    def generate_products_report(self):
        report_window = tk.Toplevel(self.window)
        report_window.title("Отчет по готовой продукции")
        report_window.geometry("800x600")

        tree = ttk.Treeview(report_window, columns=(
            "product_id", "model_name", "type_name", "color", "size", "quantity"), show="headings")

        tree.heading("product_id", text="ID продукта")
        tree.heading("model_name", text="Модель")
        tree.heading("type_name", text="Тип")
        tree.heading("color", text="Цвет")
        tree.heading("size", text="Размер")
        tree.heading("quantity", text="Количество")

        tree.column("product_id", width=100)
        tree.column("model_name", width=150)
        tree.column("type_name", width=150)
        tree.column("color", width=100)
        tree.column("size", width=100)
        tree.column("quantity", width=100)

        tree.pack(fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(report_window, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        products = self.db.execute_query("SELECT \
            Products.product_id, \
            ProductModels.model_name, \
            ProductTypes.type_name, \
            Products.color, \
            Products.size, \
            Warehouse.quantity \
            FROM Products \
            JOIN ProductModels ON Products.model_id = ProductModels.model_id \
            JOIN ProductTypes ON Products.type_id = ProductTypes.type_id \
            JOIN Warehouse ON Products.product_id = Warehouse.product_id")
        for product in products:
            tree.insert("", "end", values=product)