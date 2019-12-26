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
        abuseipdb.configure_api_key('some_API_key')
        assert Parameters.get_config() == {'API_KEY': 'some_API_key'}

    def test_configure_api_key__no_key_provided(self):
        self.reset_configuration()
        abuseipdb.configure_api_key(None)
        assert Parameters.get_config() == {}

    def test_check_ip__no_api_key_configured(self):
        self.reset_configuration()
        with self.assertRaises(KeyError):
            abuseipdb.check_ip(ip='192.0.2.123')

    def test_check_cidr__no_api_key_configured(self):
        self.reset_configuration()
        with self.assertRaises(KeyError):
            abuseipdb.check_cidr(cidr='192.0.2.123')

    def test_report_ip__no_api_key_configured(self):
        self.reset_configuration()
        with self.assertRaises(KeyError):
            abuseipdb.report_ip(ip='192.0.2.123', categories="22")
