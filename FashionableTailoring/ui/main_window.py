import tkinter as tk
from tkinter import messagebox, ttk
import psycopg2
from ui.orders_window import OrdersWindow
from ui.production_window import ProductionWindow
from ui.warehouse_window import WarehouseWindow
from ui.reports_window import ReportsWindow
from ui.administration_window import AdministrationWindow
from database import Database

class MainWindow:
    def __init__(self, root, user_info):
        self.root = root
        self.db = Database()
        self.root.title("Главная")
        self.root.geometry("800x600")
        self.user_info = user_info[0]

        self.create_widgets()

    def create_widgets(self):
        # Создаем фрейм для шапки
        header_frame = tk.Frame(self.root)
        header_frame.pack(side=tk.TOP, fill=tk.X)

        # Заголовок слева от шапки
        tk.Label(header_frame, text="Модный пошив", font=("Arial", 24)).pack(side=tk.LEFT, padx=10, pady=10)

        # Получаем роль пользователя
        role_name = self.user_info[1]

        # Создаем кнопки в шапке в зависимости от роли
        if role_name == "Администратор":
            tk.Button(header_frame, text="Заказы", command=self.open_orders).pack(side=tk.LEFT, padx=10, pady=10)
            tk.Button(header_frame, text="Производство", command=self.open_production).pack(side=tk.LEFT, padx=10, pady=10)
            tk.Button(header_frame, text="Склад", command=self.open_warehouse).pack(side=tk.LEFT, padx=10, pady=10)
            tk.Button(header_frame, text="Отчеты", command=self.open_reports).pack(side=tk.LEFT, padx=10, pady=10)
            tk.Button(header_frame, text="Администрирование", command=self.open_administration).pack(side=tk.LEFT, padx=10, pady=10)
        elif role_name == "Менеджер по продажам":
            tk.Button(header_frame, text="Заказы", command=self.open_orders).pack(side=tk.LEFT, padx=10, pady=10)
        elif role_name == "Мастер цеха":
            tk.Button(header_frame, text="Производство", command=self.open_production).pack(side=tk.LEFT, padx=10, pady=10)
        elif role_name == "Кладовщик":
            tk.Button(header_frame, text="Склад", command=self.open_warehouse).pack(side=tk.LEFT, padx=10, pady=10)

        # Создаем фрейм для основного содержимого
        main_frame = tk.Frame(self.root)
        main_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Картинка человечка (профиль аккаунта)
        profile_image = tk.PhotoImage(file="profile.png")  # Замените на путь к вашей картинке
        profile_image = profile_image.subsample(5, 5)  # Уменьшаем изображение в 5 раз
        profile_label = tk.Label(main_frame, image=profile_image)
        profile_label.image = profile_image  # Сохраняем ссылку на изображение, чтобы оно не удалялось сборщиком мусора
        profile_label.pack(pady=10)

        # Имя и фамилия
        tk.Label(main_frame, text=f"Имя: {self.user_info[2]}", font=("Arial", 12)).pack(pady=5)

        # Роль
        tk.Label(main_frame, text=f"Роль: {role_name}", font=("Arial", 12)).pack(pady=5)

        # Логин через @
        tk.Label(main_frame, text=f"Логин: @{self.user_info[3]}", font=("Arial", 12)).pack(pady=5)

        # Поле "Отследить заказ"
        tk.Label(main_frame, text="Отследить заказ:", font=("Arial", 16)).pack(pady=10)
        self.order_entry = tk.Entry(main_frame, font=("Arial", 12))
        self.order_entry.pack(pady=10)
        tk.Button(main_frame, text="Отследить", command=self.track_order).pack(pady=10)

    def open_orders(self):
        OrdersWindow(self.root, self.user_info)

    def open_production(self):
        ProductionWindow(self.root, self.user_info)

    def open_warehouse(self):
        WarehouseWindow(self.root)

    def open_reports(self):
        ReportsWindow(self.root)

    def open_administration(self):
        AdministrationWindow(self.root)

    def track_order(self):
        order_id = self.order_entry.get()
        if not order_id:
            messagebox.showerror("Ошибка", "Введите номер заказа")
            return

        try:
            # Запрос к базе данных
            query = """
            SELECT Orders.order_date, Orders.period_of_execution, Orders.order_status, 
                   OrderLines.quantity, OrderLines.total_price, Products.size, Products.color, 
                   ProductModels.model_name, ProductTypes.type_name, Materials.material_name
            FROM Orders
            JOIN OrderLines ON Orders.order_id = OrderLines.order_id
            JOIN Products ON OrderLines.product_id = Products.product_id
            JOIN ProductModels ON Products.model_id = ProductModels.model_id
            JOIN ProductTypes ON Products.type_id = ProductTypes.type_id
            JOIN Materials ON Products.material_id = Materials.material_id
            WHERE Orders.order_id = %s;
            """
            orders = self.db.execute_query(query, (order_id,))

            if orders:
                self.display_order_details(orders)
            else:
                messagebox.showerror("Ошибка", "Заказ не найден")

        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка подключения к базе данных: {e}")

    def display_order_details(self, orders):
        # Создаем новое окно для отображения деталей заказа
        order_window = tk.Toplevel(self.root)
        order_window.title("Детали заказа")
        order_window.geometry("800x600")

        # Создаем таблицу для отображения данных
        tree = ttk.Treeview(order_window, columns=(
            "order_date", "period_of_execution", "order_status", "quantity", "total_price", "size", "color",
            "model_name", "type_name", "material_name"), show="headings")

        # Определяем заголовки столбцов
        tree.heading("order_date", text="Дата заказа")
        tree.heading("period_of_execution", text="Дата получения")
        tree.heading("order_status", text="Статус")
        tree.heading("quantity", text="Количество")
        tree.heading("total_price", text="Общая цена")
        tree.heading("size", text="Размер")
        tree.heading("color", text="Цвет")
        tree.heading("model_name", text="Модель")
        tree.heading("type_name", text="Тип")
        tree.heading("material_name", text="Материал")

        # Устанавливаем ширину столбцов
        tree.column("order_date", width=100)
        tree.column("period_of_execution", width=100)
        tree.column("order_status", width=100)
        tree.column("quantity", width=100)
        tree.column("total_price", width=100)
        tree.column("size", width=100)
        tree.column("color", width=100)
        tree.column("model_name", width=100)
        tree.column("type_name", width=100)
        tree.column("material_name", width=100)

        # Вставляем данные в таблицу
        for order in orders:
            tree.insert("", "end", values=order)

        # Добавляем полосу прокрутки
        scrollbar = ttk.Scrollbar(order_window, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        tree.pack(fill=tk.BOTH, expand=True)