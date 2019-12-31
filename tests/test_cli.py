from argparse import Namespace
from unittest import TestCase

try:
    from unittest.mock import MagicMock, patch
except ImportError:
    from mock import MagicMock, patch

from abuseipdb import AbuseIpDb
from abuseipdb.cli import main as abuseipdb_cli


@patch('abuseipdb.cli._read_api_key_and_subscriber_status', return_value=("SomeAPIkey", False))
class CommandLineTestCase(TestCase):
    # Only testing the invocation of AbuseIpDb.
    # The functionality itself is tested in the test modules for the API
    # version.  Likewise we check for valid parameters in the tests for the
    # generic API.
    # We also rely on argparse to report missing or unknown parameters

    # IP addresses from TEST-NET-1 according to RFC 5737
    TEST_IP_ADDRESS = '192.0.2.123'
    TEST_CIDR_NETWORK = '192.0.2.0/24'

    def call_command(self, **kwargs):
        """Mocking argparse, as we assume it works correctly"""
        defaults = dict(
            api_version=2,
            config_file="/etc/abiseipdb",
        )
        defaults.update(**kwargs)
        with patch('abuseipdb.cli._parse_parameter', return_value=Namespace(**defaults)):
            with patch('abuseipdb.AbuseIpDb.{}'.format(kwargs['action'])) as mock:
                abuseipdb_cli()
        return mock

    def test_blacklist__without_any_optional_parameter(self, api_key_mock):
        mock = self.call_command(action='blacklist')
        mock.assert_called_once_with()

    def test_blacklist__with_confidence_minimum(self, api_key_mock):
        mock = self.call_command(action='blacklist', confidence_minimum=99)
        mock.assert_called_once_with(confidence_minimum=99)

    def test_blacklist__with_confidence_minimum_and_limit(self, api_key_mock):
        mock = self.call_command(action='blacklist', confidence_minimum=99, limit=999)
        mock.assert_called_once_with(confidence_minimum=99, limit=999)

    def test_blacklist__with_limit(self, api_key_mock):
        mock = self.call_command(action='blacklist', limit=999)
        mock.assert_called_once_with(limit=999)

    def test_bulk_report__without_any_optional_parameter(self, api_key_mock):
        mock = self.call_command(action='bulk_report', report_file='report.csv')
        mock.assert_called_once_with(file_name='report.csv')

    def test_check__without_any_optional_parameter(self, api_key_mock):
        mock = self.call_command(action='check', ip_address=self.TEST_IP_ADDRESS)
        mock.assert_called_once_with(ip_address=self.TEST_IP_ADDRESS)

    def test_check__with_max_age_in_days(self, api_key_mock):
        mock = self.call_command(action='check', ip_address=self.TEST_IP_ADDRESS, max_age_in_days=90)
        mock.assert_called_once_with(ip_address=self.TEST_IP_ADDRESS, max_age_in_days=90)

    def test_check_block__without_any_optional_parameter(self, api_key_mock):
        mock = self.call_command(action='check_block', cidr_network=self.TEST_CIDR_NETWORK)
        mock.assert_called_once_with(cidr_network=self.TEST_CIDR_NETWORK)

    def test_check_block__with_max_age_in_days(self, api_key_mock):
        mock = self.call_command(action='check_block', cidr_network=self.TEST_CIDR_NETWORK, max_age_in_days=90)
        mock.assert_called_once_with(cidr_network=self.TEST_CIDR_NETWORK, max_age_in_days=90)

    def test_report__without_any_optional_parameter(self, api_key_mock):
        mock = self.call_command(action='report', ip_address=self.TEST_IP_ADDRESS, categories=[15, 'SSH'])
        mock.assert_called_once_with(ip_address=self.TEST_IP_ADDRESS, categories='15,SSH')

    def test_report__with_comment(self, api_key_mock):
        mock = self.call_command(action='report', ip_address=self.TEST_IP_ADDRESS, categories=[15, 'SSH'], comment=['a', 'comment'])
        mock.assert_called_once_with(ip_address=self.TEST_IP_ADDRESS, categories='15,SSH', comment='a comment')
