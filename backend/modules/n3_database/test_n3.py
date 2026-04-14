import unittest
from unittest.mock import patch, MagicMock
from db_manager import save_user_profile, filter_locations

class TestN3DatabaseManager(unittest.TestCase):
    @patch('db_manager._get_db')
    def test_save_user_profile(self, mock_get_db):
        mock_db = MagicMock()
        mock_get_db.return_value = mock_db
        mock_db.users.insert_one.return_value = MagicMock(inserted_id="123")
        
        res = save_user_profile({"user_id": "U01", "vector": [0.1]})
        self.assertEqual(res["status"], "success")

    @patch('db_manager._get_db')
    def test_filter_locations_logic(self, mock_get_db):
        mock_db = MagicMock()
        mock_get_db.return_value = mock_db
        mock_db.locations.find.return_value = [{"name": "Sapa"}]
        
        res = filter_locations(budget=1000, duration=1)
        self.assertEqual(len(res), 1)

if __name__ == '__main__':
    unittest.main()