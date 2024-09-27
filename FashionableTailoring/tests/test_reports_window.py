import unittest
from unittest.mock import patch, MagicMock
from tkinter import Tk
from tkinter import ttk  # Добавьте этот импорт
from ui.reports_window import ReportsWindow

class TestReportsWindow(unittest.TestCase):

    def setUp(self):
        self.root = Tk()
        self.reports_window = ReportsWindow(self.root)

    def tearDown(self):
        self.root.destroy()

    @patch('ui.reports_window.Database.execute_query')
    def test_generate_orders_report(self, mock_execute_query):
        # Подготовка данных для теста
        mock_execute_query.return_value = [
            (1, 'User1', '2023-10-01 12:00:00', '2023-10-10 12:00:00', 'Completed'),
            (2, 'User2', '2023-10-02 12:00:00', '2023-10-11 12:00:00', 'Pending')
        ]

        # Вызов метода, который тестируем
        self.reports_window.generate_orders_report()

        # Проверка, что данные были загружены в Treeview
        report_window = self.root.winfo_children()[-1]
        tree = None
        for child in report_window.winfo_children():
            if isinstance(child, ttk.Treeview):
                tree = child
                break
        self.assertIsNotNone(tree, "Treeview не найден в окне отчета")
        self.assertEqual(len(tree.get_children()), 2)

    @patch('ui.reports_window.Database.execute_query')
    def test_generate_production_report(self, mock_execute_query):
        # Подготовка данных для теста
        mock_execute_query.return_value = [
            (1, 1, 'Performer1', '2023-10-10 12:00:00', 'Completed'),
            (2, 2, 'Performer2', '2023-10-11 12:00:00', 'Pending')
        ]

        # Вызов метода, который тестируем
        self.reports_window.generate_production_report()

        # Проверка, что данные были загружены в Treeview
        report_window = self.root.winfo_children()[-1]
        tree = None
        for child in report_window.winfo_children():
            if isinstance(child, ttk.Treeview):
                tree = child
                break
        self.assertIsNotNone(tree, "Treeview не найден в окне отчета")
        self.assertEqual(len(tree.get_children()), 2)

    @patch('ui.reports_window.Database.execute_query')
    def test_generate_materials_report(self, mock_execute_query):
        # Подготовка данных для теста
        mock_execute_query.return_value = [
            (1, 'Material1', 100),
            (2, 'Material2', 200)
        ]

        # Вызов метода, который тестируем
        self.reports_window.generate_materials_report()

        # Проверка, что данные были загружены в Treeview
        report_window = self.root.winfo_children()[-1]
        tree = None
        for child in report_window.winfo_children():
            if isinstance(child, ttk.Treeview):
                tree = child
                break
        self.assertIsNotNone(tree, "Treeview не найден в окне отчета")
        self.assertEqual(len(tree.get_children()), 2)

    @patch('ui.reports_window.Database.execute_query')
    def test_generate_products_report(self, mock_execute_query):
        # Подготовка данных для теста
        mock_execute_query.return_value = [
            (1, 'Model1', 'Type1', 'Red', 'M', 50),
            (2, 'Model2', 'Type2', 'Blue', 'L', 100)
        ]

        # Вызов метода, который тестируем
        self.reports_window.generate_products_report()

        # Проверка, что данные были загружены в Treeview
        report_window = self.root.winfo_children()[-1]
        tree = None
        for child in report_window.winfo_children():
            if isinstance(child, ttk.Treeview):
                tree = child
                break
        self.assertIsNotNone(tree, "Treeview не найден в окне отчета")
        self.assertEqual(len(tree.get_children()), 2)

if __name__ == '__main__':
    unittest.main()