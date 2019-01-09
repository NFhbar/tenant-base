"""test file for correct execution"""
import logging
import main
LOG = logging.getLogger()
LOG.setLevel(logging.INFO)

class TestClass:

    @classmethod
    def setup_class(cls):
        LOG.info('Setup Tests')

    @classmethod
    def teardown_class(cls):
        LOG.info('Tear Down Tests')

    def test_lambda_handler_btc(self):
        """test correct execution"""
        main.main()
