from unittest import TestCase

try:
    from unittest.mock import patch
except ImportError:
    from mock import patch

import abuseipdb
from abuseipdb.parameters import Parameters



class LegacyTestCase(TestCase):

    # IP addresses from TEST-NET-1 according to RFC 5737
    TEST_IP_ADDRESS = '192.0.2.123'
    TEST_CIDR_NETWORK = '192.0.2.0/24'

    def reset_configuration(self):
        # This is required to test the configuration isolated
        Parameters.configuration = {}

    def test_configure_api_key__key_provided(self):
        self.reset_configuration()
        abuseipdb.configure_api_key('some_API_key')
        assert Parameters.get_config() == {'API_KEY': 'some_API_key'}

    def test_configure_api_key__no_key_provided(self):
        self.reset_configuration()
        with self.assertRaises(ValueError):
            abuseipdb.configure_api_key(None)

    def test_check_ip__no_api_key_configured(self):
        self.reset_configuration()
        with self.assertRaises(KeyError):
            abuseipdb.check_ip(ip=self.TEST_IP_ADDRESS)

    def test_check_ip__no_ip_address_provided(self):
        self.reset_configuration()
        abuseipdb.configure_api_key('some_API_key')
        with self.assertRaises(ValueError):
            abuseipdb.check_ip()

    @patch('requests.request')

    def test_check_ip(self, mock):
        self.reset_configuration()
        abuseipdb.configure_api_key('some_API_key')
        abuseipdb.check_ip(ip=self.TEST_IP_ADDRESS)
        mock.assert_called_once_with(
            'GET', 'https://www.abuseipdb.com/check/192.0.2.123/json?key=some_API_key&days=30')

    @patch('requests.request')

    def test_check_ip__with_different_days(self, mock):
        self.reset_configuration()
        abuseipdb.configure_api_key('some_API_key')
        abuseipdb.check_ip(ip=self.TEST_IP_ADDRESS, days='90')
        mock.assert_called_once_with(
            'GET', 'https://www.abuseipdb.com/check/192.0.2.123/json?key=some_API_key&days=90')

    def test_check_cidr__no_api_key_configured(self):
        self.reset_configuration()
        with self.assertRaises(KeyError):
            abuseipdb.check_cidr(cidr=self.TEST_CIDR_NETWORK)

    def test_check_cidr__no_cidr_network_provided(self):
        self.reset_configuration()
        abuseipdb.configure_api_key('some_API_key')
        with self.assertRaises(ValueError):
            abuseipdb.check_cidr()

    @patch('requests.request')

    def test_check_cidr(self, mock):
        self.reset_configuration()
        abuseipdb.configure_api_key('some_API_key')
        abuseipdb.check_cidr(cidr=self.TEST_CIDR_NETWORK)
        # This URL looks wrong, but the APIv1 documentation doesn't indicate,
        # that the / needs to be encoded.
        mock.assert_called_once_with(
            'GET', 'https://www.abuseipdb.com/check-block/json?key=some_API_key&network=192.0.2.0/24&days=30')

    @patch('requests.request')

    def test_check_cidr__with_different_days(self, mock):
        self.reset_configuration()
        abuseipdb.configure_api_key('some_API_key')
        abuseipdb.check_cidr(cidr=self.TEST_CIDR_NETWORK, days='90')
        # This URL looks wrong, but the APIv1 documentation doesn't indicate,
        # that the / needs to be encoded.
        mock.assert_called_once_with(
            'GET', 'https://www.abuseipdb.com/check-block/json?key=some_API_key&network=192.0.2.0/24&days=90')


    def test_report_ip__no_api_key_configured(self):
        self.reset_configuration()
        with self.assertRaises(KeyError):
            abuseipdb.report_ip(ip=self.TEST_IP_ADDRESS, categories="22")

    def test_report_ip__no_ip_address_provided(self):
        self.reset_configuration()
        abuseipdb.configure_api_key('some_API_key')
        with self.assertRaises(ValueError):
            abuseipdb.report_ip(categories="22")

    def test_report_ip__no_categories_provided(self):
        self.reset_configuration()
        abuseipdb.configure_api_key('some_API_key')
        with self.assertRaises(ValueError):
            abuseipdb.report_ip(ip=self.TEST_IP_ADDRESS)

    @patch('requests.request')

    def test_report_ip(self, mock):
        self.reset_configuration()
        abuseipdb.configure_api_key('some_API_key')
        abuseipdb.report_ip(ip=self.TEST_IP_ADDRESS, categories="22")
        mock.assert_called_once_with(
            'GET', 'https://www.abuseipdb.com/report/json?key=some_API_key&category=22&comment=&ip=192.0.2.123')

    @patch('requests.request')

    def test_report_ip__with_some_comment(self, mock):
        self.reset_configuration()
        abuseipdb.configure_api_key('some_API_key')
        abuseipdb.report_ip(ip=self.TEST_IP_ADDRESS, categories="22", comment="Some comment")
        # This URL looks wrong, but the APIv1 documentation doesn't indicate,
        # that the comment needs to be encoded.
        mock.assert_called_once_with(
            'GET', 'https://www.abuseipdb.com/report/json?key=some_API_key&category=22&comment=Some comment&ip=192.0.2.123')

