from VK import User
import unittest

class UserTests(unittest.TestCase):

    def setUp(self):
        print("Для проведения тестов, требуется авторизация в вконтакте")
        # login = input("Введите логин: ")
        # password = input("Введите пароль: ")
        # id = int(input("Введите id: "))

        self.user = User('+79653417551', 'zxcvbnm12.', 187509567)

    def test_id(self):
        self.assertEqual(self.user.user['id'], self.user.id,)

    def test_user_class(self):
        self.assertIsInstance(self.user.user, dict)

    def test_age(self):
        self.assertIn('age', self.user.user)
        self.assertIsInstance(self.user.user['age'], int)
        self.assertGreater(self.user.user['age'], 0)

    def test_groups(self):
        self.assertIn('groups', self.user.user)
        self.assertIsInstance(self.user.user['groups'], list)

    def test_search_sex(self):
        self.assertIn('search_sex', self.user.user)
        self.assertIsInstance(self.user.user['search_sex'], int)
        self.assertGreater(self.user.user['search_sex'], -1)
        self.assertLess(self.user.user['search_sex'], 3)

    def test_get_age(self):
        self.assertRaises(ValueError, self.user.get_age, 'строка')
        self.assertRaises(ValueError, self.user.get_age, 12345)
        self.assertRaises(ValueError, self.user.get_age, [1, 2, 'строка'])
        self.assertIsInstance(self.user.get_age(self.user.user), int)

    def test_get_groups(self):
        self.assertRaises(ValueError, self.user.get_groups, 'строка')
        self.assertRaises(ValueError, self.user.get_groups, 12345)
        self.assertRaises(ValueError, self.user.get_groups, [1, 2, 'строка'])
        self.assertIsInstance(self.user.get_groups(self.user.user), list)

    def test_get_seatch_sex(self):
        self.assertIsInstance(self.user.get_seatch_sex(self.user.user), int)
        self.assertGreater(self.user.get_seatch_sex(self.user.user), -1)
        self.assertLess(self.user.get_seatch_sex(self.user.user), 3)

if __name__ == "__main__":
    unittest.main()


