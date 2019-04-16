from VK import User
import unittest

class UserTests(unittest.TestCase):

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

if __name__ == "__main__":
    unittest.main()


