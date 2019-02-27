import unittest
import sys
import re
import os
from app import App
from helpers.config import Config
a = Config()


class Mytests(unittest.TestCase):
    def setUp(self):
        self.app = App()

    def test_config_class(self):
        self.assertIsInstance(self.app.config, Config)

    @unittest.skipIf(not ('win' in sys.platform), 'Тест запущен не в Windows')
    def test_path(self):
        config = Config()
        self.assertIn('C:\\', config.config_paths[1])

    def test_init_env_config_path(self):
        func_result = Config.init_env_config_path()
        self.assertIsInstance(func_result, list)
        num_of_matches = len(re.findall('[A-Z]{1}:\\\\\w*', func_result[1]))
        self.assertGreater(num_of_matches, 0)

    def test_get_windows_system_disk(self):
        self.assertEqual(os.getenv("SystemDrive"), Config.get_windows_system_disk())

    def test_get_windows_system_disk(self):
        self.assertRaises(TypeError, Config.get_windows_system_disk, 123)


if __name__ == '__main__':
    unittest.main()
