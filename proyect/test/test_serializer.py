import unittest
from unittest.mock import MagicMock, patch
from serializer import RequesterSerializer
from params import api_key

class TestRequesterSerializer(unittest.TestCase):
    def test_json_to_df_csv(self):
        json_data = [{"key": "value"}, {"key": "value"}]
        df = RequesterSerializer.json_to_df_csv(json_data)
        self.assertTrue(isinstance(df, pd.DataFrame))
    
    def test_json_to_df_postgres(self):
        json_data = {
            "list": [{"main.temp": 20, "dt": 12345, "cod": 200, "city": {"name": "City"}}]
        }
        df = RequesterSerializer.json_to_df_postgres(json_data)
        self.assertEqual(len(df), 1)
        self.assertIn("temperature", df[0])
    
    def test_normalize_to_df(self):
        json_data = [{"key": "value"}, {"key": "value"}]
        df = RequesterSerializer.normalize_to_df(json_data)
        self.assertTrue(isinstance(df, pd.DataFrame))
    
    def test_elem_list_to_a_dicc(self):
        element = "param1=value1&param2=value2"
        api_key = api_key
        result = RequesterSerializer.elem_list_to_a_dicc(element, api_key)
        expected_result = {
            "param1": "value1",
            "param2": "value2",
            "appid": api_key
        }
        self.assertEqual(result, expected_result)

if __name__ == "__main__":
    unittest.main()
