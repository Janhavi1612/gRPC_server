import unittest
from unittest.mock import MagicMock
import inventory_client
import library_pb2
import get_book_titles

# create mock client API
mock_api = inventory_client.InventoryClient("", "")
mock_return_value = library_pb2.GetBookResponse()
mock_return_value.ISBN = "101"
mock_return_value.title = "test1"
mock_api.getBook = MagicMock(return_value=mock_return_value)


class TestClient(unittest.TestCase):
    # test business logic
    def test_get_title_logic_with_mock_api(self):
        print("\n***test for mock client API***")
        expected_title_list = ["test1"]
        actual_title_list = get_book_titles.get_titles(mock_api, ["101"])
        assert expected_title_list == actual_title_list

    # test live server
    def test_live_server(self):
        print("\n***test for live server***")
        expected_title_list = ["girl on a blue train", "The royals"]

        # initialize actual client
        client_api = inventory_client.InventoryClient("localhost", "50051")
        actual_title_list = get_book_titles.get_titles(client_api, ["1", "2"])
        assert expected_title_list == actual_title_list


if __name__ == "__main__":
    unittest.main()
