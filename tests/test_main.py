# -*- coding: utf-8 -*-
"""test file for correct execution"""
from os import system
import logging
import main
log = logging.getLogger()
log.setLevel(logging.INFO)

class TestClass:

    @classmethod
    def setup_class(cls):
        log.info('Setup Tests')
        cls.mock_database = 'mock.sqlite'

    @classmethod
    def teardown_class(cls):
        log.info('Stopping memcached server')
        exit_code = system('killall memcached')
        log.info(exit_code)

    def test_main_serve_argument(self):
        """test correct execution"""
        main.main(['-s', self.mock_database])

if __name__ == '__main__':
    pytest.main()
