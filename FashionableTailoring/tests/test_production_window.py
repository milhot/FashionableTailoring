import unittest
from unittest.mock import patch, MagicMock
from tkinter import Tk
from ui.orders_window import OrdersWindow

class TestOrdersWindow(unittest.TestCase):
    def setUp(self):
        self.root = Tk()
        self.user_info = (1, 'Admin', 'Admin User', 'admin', 'password', '1234567890')
        self.orders_window = OrdersWindow(self.root, self.user_info)

    def tearDown(self):
        self.root.destroy()

    @patch('orders_window.Database.execute_query')
    def test_load_orders(self, mock_execute_query):
        # Подготовка данных для теста
        mock_execute_query.return_value = [
            (1, 'User1', '2023-10-01 12:00:00', '2023-10-10 12:00:00', 'Completed'),
            (2, 'User2', '2023-10-02 12:00:00', '2023-10-11 12:00:00', 'Pending')
        ]

        # Вызов метода, который тестируем
        self.orders_window.load_orders()

        # Проверка, что данные были загружены в Treeview
        self.assertEqual(len(self.orders_window.tree.get_children()), 2)

    @patch('orders_window.Database.execute_query')
    def test_add_order(self, mock_execute_query):
        # Подготовка данных для теста
        mock_execute_query.return_value = None

        # Вызов метода, который тестируем
        self.orders_window.add_order()

        # Проверка, что данные были добавлены в базу данных
        mock_execute_query.assert_called_once()

    @patch('orders_window.Database.execute_query')
    def test_edit_order(self, mock_execute_query):
        # Подготовка данных для теста
        mock_execute_query.return_value = None

        # Вызов метода, который тестируем
        self.orders_window.edit_order()

        # Проверка, что данные были обновлены в базе данных
        mock_execute_query.assert_called_once()

    @patch('orders_window.Database.execute_query')
    def test_delete_order(self, mock_execute_query):
        # Подготовка данных для теста
        mock_execute_query.return_value = None

        # Вызов метода, который тестируем
        self.orders_window.delete_order()

        # Проверка, что данные были удалены из базы данных
        mock_execute_query.assert_called_once()

if __name__ == '__main__':
    unittest.main()