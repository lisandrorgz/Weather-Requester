import unittest
from unittest.mock import MagicMock, patch
from export import ExportAPIData
from db import WeatherTables, PostgresDB

class TestExportAPIData(unittest.TestCase):
    def test_to_postgres(self):
        data_list = [
            {'dt': 12345, 'cod': 200, 'city': 'City', 'temperature': 25},
            {'dt': 67890, 'cod': 200, 'city': 'City2', 'temperature': 28}
        ]
        database_mock = MagicMock(PostgresDB)
        session_mock = MagicMock()
        database_mock.get_session.return_value = session_mock

        ExportAPIData.to_postgres(data_list)

        self.assertTrue(session_mock.add.called)
        self.assertTrue(session_mock.commit.called)
        self.assertTrue(session_mock.close.called)

    @patch('os.path.exists', return_value=True)
    @patch('pandas.DataFrame.to_csv')
    @patch('json.dump')
    @patch('json.load')
    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    
    def test_to_csv(self, mock_open, mock_load, mock_dump, mock_to_csv, mock_exists):
        df_mock = MagicMock()
        df_mock['dt'].iloc[0] = 12345

        ExportAPIData.to_csv(df_mock)

        mock_exists.assert_called_once()
        mock_open.assert_called_with(ExportAPIData._CONFIG_FILE, 'r')
        mock_load.assert_called_once()
        mock_to_csv.assert_called_once()

    def test_get_date(self):
        df_mock = MagicMock()
        df_mock['dt'].iloc[0] = 12345

        result = ExportAPIData.get_date(df_mock)

        self.assertEqual(result, '1970-01-01')

    @patch('json.dump')
    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    def test_save_csv_cont(self, mock_open, mock_dump):
        ExportAPIData._CSV_CONT = 42
        ExportAPIData._save_csv_cont()

        mock_open.assert_called_with(ExportAPIData._CONFIG_FILE, 'w')
        mock_dump.assert_called_once_with({'csv_cont': 42}, mock_open())

    @patch('json.load')
    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    def test_load_csv_cont(self, mock_open, mock_load):
        mock_load.return_value = {'csv_cont': 42}
        ExportAPIData._load_csv_cont()

        mock_open.assert_called_with(ExportAPIData._CONFIG_FILE, 'r')
        self.assertEqual(ExportAPIData._CSV_CONT, 42)

if __name__ == "__main__":
    unittest.main()
