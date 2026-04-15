import unittest
from unittest.mock import patch, MagicMock
from db_manager import save_user_profile, filter_locations

class TestN3DatabaseManager(unittest.TestCase):
    @patch('db_manager._get_connection')
    def test_save_user_profile(self, mock_get_conn):
        # Giả lập kết nối và con trỏ PostgreSQL
        mock_conn = MagicMock()
        mock_cur = MagicMock()
        mock_get_conn.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cur
        
        # Chạy hàm thật
        res = save_user_profile({"user_id": "U01", "vector": [0.1, 0.2, 0.3, 0.4, 0.5]})
        
        # Kiểm tra kết quả
        self.assertEqual(res["status"], "success")
        self.assertEqual(res["user_id"], "U01")

    @patch('db_manager._get_connection')
    def test_filter_locations_logic(self, mock_get_conn):
        # Giả lập kết nối và con trỏ PostgreSQL
        mock_conn = MagicMock()
        mock_cur = MagicMock()
        mock_get_conn.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cur
        
        # Giả lập dữ liệu SQL trả về từ hàm fetchall()
        mock_cur.fetchall.return_value = [
            {"location_id": "loc_001", "vector": "[0.1, 0.2]", "metadata": {}, "geo": {}}
        ]
        
        # Chạy hàm thật
        res = filter_locations(budget=1000, duration=1)
        
        # Kiểm tra kết quả
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]["location_id"], "loc_001")

if __name__ == '__main__':
    unittest.main()