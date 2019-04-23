from VK import User
from unittest import TestCase, main
from unittest.mock import patch, Mock

class UserTests(TestCase):

    def setUp(self):
        self.user = {
            'bdate': '28.1.2002',
            'first_name': 'Александр',
            'id': 187509567,
            'last_name': 'Зайцев',
            'sex': 2,
            'city': {'id': 1}}


    def test_get_sity(self):
        self.assertIsInstance(User.get_city(self.user), dict)
        self.assertIsInstance(User.get_city(self.user)['id'], int)
        self.assertGreater(User.get_city(self.user)['id'], 0)

    def test_get_age(self):
        self.assertRaises(ValueError, User.get_age, 'строка')
        self.assertRaises(ValueError, User.get_age, 12345)
        self.assertRaises(ValueError, User.get_age, [1, 2, 'строка'])
        self.assertGreater(User.get_age(self.user), 0)

    def test_get_seatch_sex(self):
        self.assertIsInstance(User.get_seatch_sex(self.user), int)
        self.assertGreater(User.get_seatch_sex(self.user), -1)
        self.assertLess(User.get_seatch_sex(self.user), 3)

class TestBlog(TestCase):
    @patch('VK.Main')
    def test_search_peoples(self, mock_peoples):
        peoples = mock_peoples()

        peoples.search_peoples.return_value = [
            {
                "id":242444423,
                'about': "очень интересно",
                'books': 'инфа'
            }
        ]

        response = peoples.search_peoples()
        self.assertIsNotNone(response)
        self.assertIsInstance(response[0], dict)
        self.assertIsInstance(response, list)

    @patch('VK.Main')
    def test_get_top3_photo(self, mock_photos):
        photos = mock_photos()

        photos.get_top3_photo.return_value = [
            {
                'photo': "photoUrl",
                'likes': 123
            }
        ]


        response = photos.get_top3_photo()
        self.assertIsNotNone(response)
        self.assertIsInstance(response[0], dict)
        self.assertIsInstance(response, list)
        self.assertIsInstance(response[0]['photo'], str)
        

if __name__ == "__main__":
    main()


