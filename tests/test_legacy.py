from unittest import TestCase

import abuseipdb
from abuseipdb.parameters import Parameters
from mock import patch


class LegacyTestCase(TestCase):

    def reset_configuration(self):
        # This is required to test the configuration isolated
        Parameters.configuration = {}

    def test_configure_api_key__key_provided(self):
        self.reset_configuration()
        abuseipdb.configure_api_key('some API key')
        assert Parameters.get_config() == {'API_KEY': 'some API key'}

    def test_configure_api_key__no_key_provided(self):
        self.reset_configuration()
        abuseipdb.configure_api_key(None)
        assert Parameters.get_config() == {}
