import unittest
from unittest.mock import patch, MagicMock
from tkinter import messagebox
from ui.login_window import LoginWindow
from ui.main_window import MainWindow
import re

class TestLoginWindow(unittest.TestCase):
    @patch('database.Database.execute_query')
    @patch('tkinter.messagebox.showinfo')
    @patch('tkinter.Tk.destroy')
    @patch('ui.login_window.LoginWindow.open_main_window')  # Замокать метод, который открывает главное окно
    def test_login_success(self, mock_open_main_window, mock_destroy, mock_showinfo, mock_execute_query):
        # Подготовка данных для теста
        mock_execute_query.return_value = [(1, 'Администратор', 'Иван Иванов', 'admin', 'password', '1234567890')]

        # Создание экземпляра LoginWindow
        login_window = LoginWindow(MagicMock())

        # Мокирование полей ввода
        login_window.entry_login = MagicMock()
        login_window.entry_password = MagicMock()

        # Установка side_effect для метода get
        login_window.entry_login.get.side_effect = lambda: 'admin'
        login_window.entry_password.get.side_effect = lambda: 'password'

        # Вызов метода login
        login_window.login()

        # Проверка ожидаемых результатов
        expected_query = re.compile(r"SELECT\s+Users\.user_id,\s+Roles\.role_name,\s+Users\.full_name,\s+Users\.login,\s+Users\.password,\s+Users\.phone\s+FROM\s+Users\s+JOIN\s+Roles\s+ON\s+Users\.role_id\s+=\s+Roles\.role_id\s+WHERE\s+login\s+=\s+'admin'\s+and\s+password\s+=\s+'password'")
        mock_execute_query.assert_called_once()
        self.assertRegex(mock_execute_query.call_args[0][0], expected_query)
        mock_showinfo.assert_called_once_with("Успех", "Авторизация прошла успешно!")
        # mock_destroy.assert_called_once()  # Проверка, что метод destroy был вызван
        mock_open_main_window.assert_called_once()  # Проверка, что метод открытия главного окна был вызван

    @patch('database.Database.execute_query')
    @patch('tkinter.messagebox.showerror')
    def test_login_failure(self, mock_showerror, mock_execute_query):
        # Подготовка данных для теста
        mock_execute_query.return_value = []

        # Создание экземпляра LoginWindow
        login_window = LoginWindow(MagicMock())

        # Мокирование полей ввода
        login_window.entry_login = MagicMock()
        login_window.entry_password = MagicMock()

        # Установка side_effect для метода get
        login_window.entry_login.get.side_effect = lambda: 'invalid_user'
        login_window.entry_password.get.side_effect = lambda: 'wrong_password'

        # Вызов метода login
        login_window.login()

        # Проверка ожидаемых результатов
        expected_query = re.compile(r"SELECT\s+Users\.user_id,\s+Roles\.role_name,\s+Users\.full_name,\s+Users\.login,\s+Users\.password,\s+Users\.phone\s+FROM\s+Users\s+JOIN\s+Roles\s+ON\s+Users\.role_id\s+=\s+Roles\.role_id\s+WHERE\s+login\s+=\s+'invalid_user'\s+and\s+password\s+=\s+'wrong_password'")
        mock_execute_query.assert_called_once()
        self.assertRegex(mock_execute_query.call_args[0][0], expected_query)
        mock_showerror.assert_called_once_with("Ошибка", "Неверный логин или пароль")






if __name__ == '__main__':
    unittest.main()