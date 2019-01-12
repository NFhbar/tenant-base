# -*- coding: utf-8 -*-
"""test file for correct execution"""
from os import system
import logging
import mock
import main
import helpers
from pymemcache.client import Client

LOG = logging.getLogger()
LOG.setLevel(logging.INFO)
KeyValueHelper = helpers.KeyValueHelper
mock_database_path = 'tests/test.sqlite'

class TestClass:

    @classmethod
    def setup_class(cls):
        LOG.info('Setup Tests')
        cls.mock_database = mock_database_path
        cls.db_conn = KeyValueHelper(cls.mock_database)
        main.run_command('memcached -d -p 1234')
        cls.client = Client(('localhost', 1234))

    @classmethod
    def teardown_class(cls):
        for key, value in cls.db_conn:
            del cls.db_conn[key]

        cls.client.delete('testkey1')
        cls.client.delete('testkey2')


    def test_main_exit(self, monkeypatch):
        """test correct execution for exit option"""
        monkeypatch.setattr('builtins.input', lambda x: 'exit')
        main.main(['-s', self.mock_database])

    def test_run_command(self):
        """test run_command function"""
        try:
            main.run_command('fake_command')
            assert False
        except Exception:
            assert True

        try:
            main.run_command('ls')
            assert True
        except Exception:
            assert False

    def test_main_show(self):
        """test correct execution of -show flag"""
        main.main(['-sh', self.mock_database])

    def test_value_operations(self):
        """test set_value function for different cases"""
        # Case 1 - set value through set_value and check it is in
        # memcached and DB
        input = ['set', 'testkey1', 'testvalue1']

        result = main.set_value(input, self.client, self.mock_database)
        memcahed_expected = self.client.get('testkey1')
        assert result[1] == memcahed_expected.decode('utf-8')


        db_expected = self.db_conn['testkey1']
        assert result[1] == db_expected

        # Case 2a - Get a value that is only in the DB
        user_input = ['get', 'testkey2']
        self.db_conn[user_input[1]] = 'testvalue2'
        response = self.client.get(user_input[1])
        assert response == None
        result = main.get_value(user_input, self.client, self.mock_database)
        # assert result.decode('utf-8') == 'testvalue2'
        LOG.info('TEST')
        LOG.info(result)

        # Case 2b -  Get a value that does not exist at all
        user_input[1] = 'does_not_exist'
        result = main.get_value(user_input, self.client, self.mock_database)
        assert result == None

        # Case 3 - Delete a value
        user_input[0] = 'delete'
        user_input[1] = 'testkey2'
        result = main.delete_value(user_input, self.client, self.mock_database)
        assert result == True
        # Let's try to delete again
        result = main.delete_value(user_input, self.client, self.mock_database)
        assert result == False

if __name__ == '__main__':
    pytest.main()
