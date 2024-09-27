import unittest
from unittest.mock import patch, MagicMock
from tkinter import messagebox
from ui.login_window import LoginWindow
from ui.main_window import MainWindow
import re

class TestMainWindow(unittest.TestCase):
    @patch('ui.main_window.OrdersWindow')
    @patch('ui.main_window.MainWindow.create_widgets')
    def test_open_orders(self, mock_create_widgets, mock_orders_window):
        # Создание экземпляра MainWindow
        main_window = MainWindow(MagicMock(), [(1, 'Администратор', 'Иван Иванов', 'admin', 'password', '1234567890')])

        # Вызов метода open_orders
        main_window.open_orders()

        # Проверка, что OrdersWindow был вызван с правильными аргументами
        mock_orders_window.assert_called_once_with(main_window.root, main_window.user_info)

    @patch('database.Database.execute_query')
    @patch('tkinter.messagebox.showerror')
    @patch('tkinter.Toplevel')
    @patch('ui.main_window.MainWindow.create_widgets')
    def test_track_order(self, mock_create_widgets, mock_toplevel, mock_showerror, mock_execute_query):
        # Подготовка данных для теста
        mock_execute_query.return_value = [
            (1, '2023-10-01', 'В обработке', 'ул. Ленина, 1', '1234567890', 'Иван Иванов', 'Продукт 1', '123456', 2, 100.0)
        ]

        # Создание экземпляра MainWindow
        main_window = MainWindow(MagicMock(), [(1, 'Администратор', 'Иван Иванов', 'admin', 'password', '1234567890')])

        # Мокирование ввода данных
        main_window.order_entry = MagicMock()
        main_window.order_entry.get.return_value = '1'

        # Вызов метода track_order
        main_window.track_order()

        # Проверка, что execute_query был вызван с правильными аргументами
        expected_query = re.compile(r"""
            SELECT\s+Orders\.order_date,\s+Orders\.period_of_execution,\s+Orders\.order_status,\s+
                   OrderLines\.quantity,\s+OrderLines\.total_price,\s+Products\.size,\s+Products\.color,\s+
                   ProductModels\.model_name,\s+ProductTypes\.type_name,\s+Materials\.material_name\s+
            FROM\s+Orders\s+
            JOIN\s+OrderLines\s+ON\s+Orders\.order_id\s+=\s+OrderLines\.order_id\s+
            JOIN\s+Products\s+ON\s+OrderLines\.product_id\s+=\s+Products\.product_id\s+
            JOIN\s+ProductModels\s+ON\s+Products\.model_id\s+=\s+ProductModels\.model_id\s+
            JOIN\s+ProductTypes\s+ON\s+Products\.type_id\s+=\s+ProductTypes\.type_id\s+
            JOIN\s+Materials\s+ON\s+Products\.material_id\s+=\s+Materials\.material_id\s+
            WHERE\s+Orders\.order_id\s+=\s+%s;
        """, re.VERBOSE)
        mock_execute_query.assert_called_once()
        self.assertRegex(mock_execute_query.call_args[0][0], expected_query)

        # Проверка, что showerror не был вызван
        mock_showerror.assert_not_called()

        # Проверка, что Toplevel был вызван
        mock_toplevel.assert_called_once()

    @patch('database.Database.execute_query')
    @patch('tkinter.messagebox.showerror')
    @patch('ui.main_window.MainWindow.create_widgets')
    def test_track_order_not_found(self, mock_create_widgets, mock_showerror, mock_execute_query):
        # Подготовка данных для теста
        mock_execute_query.return_value = []

        # Создание экземпляра MainWindow
        main_window = MainWindow(MagicMock(), [(1, 'Администратор', 'Иван Иванов', 'admin', 'password', '1234567890')])

        # Мокирование ввода данных
        main_window.order_entry = MagicMock()
        main_window.order_entry.get.return_value = '1'

        # Вызов метода track_order
        main_window.track_order()

        # Проверка, что execute_query был вызван с правильными аргументами
        expected_query = re.compile(r"""
            SELECT\s+Orders\.order_date,\s+Orders\.period_of_execution,\s+Orders\.order_status,\s+
                   OrderLines\.quantity,\s+OrderLines\.total_price,\s+Products\.size,\s+Products\.color,\s+
                   ProductModels\.model_name,\s+ProductTypes\.type_name,\s+Materials\.material_name\s+
            FROM\s+Orders\s+
            JOIN\s+OrderLines\s+ON\s+Orders\.order_id\s+=\s+OrderLines\.order_id\s+
            JOIN\s+Products\s+ON\s+OrderLines\.product_id\s+=\s+Products\.product_id\s+
            JOIN\s+ProductModels\s+ON\s+Products\.model_id\s+=\s+ProductModels\.model_id\s+
            JOIN\s+ProductTypes\s+ON\s+Products\.type_id\s+=\s+ProductTypes\.type_id\s+
            JOIN\s+Materials\s+ON\s+Products\.material_id\s+=\s+Materials\.material_id\s+
            WHERE\s+Orders\.order_id\s+=\s+%s;
        """, re.VERBOSE)
        mock_execute_query.assert_called_once()
        self.assertRegex(mock_execute_query.call_args[0][0], expected_query)

        # Проверка, что showerror был вызван с правильными аргументами
        mock_showerror.assert_called_once_with("Ошибка", "Заказ не найден")





if __name__ == '__main__':
    unittest.main()