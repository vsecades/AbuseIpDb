from argparse import Namespace
from unittest import TestCase
from unittest.mock import patch

from abuseipdb.cli import main as abuseipdb_cli


class CommandLineTestHelper(object):
    """Providing common functionality to all test cases"""

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
        with patch('abuseipdb.cli._print_result'):
            with patch('abuseipdb.cli._parse_parameter', return_value=Namespace(**defaults)):
                with patch('abuseipdb.AbuseIpDb.{}'.format(kwargs['action'])) as mock:
                    abuseipdb_cli()
        return mock


@patch('abuseipdb.cli._read_api_key_and_subscriber_status', return_value=("SomeAPIkey", False))
class CommandLineTestCase(CommandLineTestHelper, TestCase):
    # Only testing the invocation of AbuseIpDb.
    # The functionality itself is tested in the test modules for the API
    # version.  Likewise we check for valid parameters in the tests for the
    # generic API.
    # We also rely on argparse to report missing or unknown parameters

    def test_blacklist__without_any_optional_parameter(self, api_key_mock):
        mock = self.call_command(
            action='blacklist')
        mock.assert_called_once_with()

    def test_blacklist__with_confidence_minimum(self, api_key_mock):
        mock = self.call_command(
            action='blacklist', confidence_minimum=99)
        mock.assert_called_once_with(confidence_minimum=99)

    def test_blacklist__with_confidence_minimum_and_limit(self, api_key_mock):
        mock = self.call_command(
            action='blacklist', confidence_minimum=99, limit=999)
        mock.assert_called_once_with(confidence_minimum=99, limit=999)

    def test_blacklist__with_limit(self, api_key_mock):
        mock = self.call_command(
            action='blacklist', limit=999)
        mock.assert_called_once_with(limit=999)

    def test_bulk_report__without_any_optional_parameter(self, api_key_mock):
        mock = self.call_command(
            action='bulk_report', report_file='report.csv')
        mock.assert_called_once_with(file_name='report.csv')

    def test_categories(self, api_key_mock):
        defaults = dict(
            action='list_categories',
            api_version=2,
            config_file="/etc/abiseipdb",
        )
        with patch('abuseipdb.cli._parse_parameter', return_value=Namespace(**defaults)):
            abuseipdb_cli()

    def test_check__without_any_optional_parameter(self, api_key_mock):
        mock = self.call_command(
            action='check', ip_address=self.TEST_IP_ADDRESS)
        mock.assert_called_once_with(ip_address=self.TEST_IP_ADDRESS)

    def test_check__with_max_age_in_days(self, api_key_mock):
        mock = self.call_command(
            action='check', ip_address=self.TEST_IP_ADDRESS, max_age_in_days=90)
        mock.assert_called_once_with(ip_address=self.TEST_IP_ADDRESS, max_age_in_days=90)

    def test_check_block__without_any_optional_parameter(self, api_key_mock):
        mock = self.call_command(
            action='check_block', cidr_network=self.TEST_CIDR_NETWORK)
        mock.assert_called_once_with(cidr_network=self.TEST_CIDR_NETWORK)

    def test_check_block__with_max_age_in_days(self, api_key_mock):
        mock = self.call_command(
            action='check_block', cidr_network=self.TEST_CIDR_NETWORK, max_age_in_days=90)
        mock.assert_called_once_with(cidr_network=self.TEST_CIDR_NETWORK, max_age_in_days=90)

    def test_report__without_any_optional_parameter(self, api_key_mock):
        mock = self.call_command(
            action='report', ip_address=self.TEST_IP_ADDRESS, categories=[15, 'SSH'])
        mock.assert_called_once_with(ip_address=self.TEST_IP_ADDRESS, categories='15,SSH')

    def test_report__with_comment(self, api_key_mock):
        mock = self.call_command(
            action='report', ip_address=self.TEST_IP_ADDRESS, categories=[15, 'SSH'], comment=['a', 'comment'])
        mock.assert_called_once_with(ip_address=self.TEST_IP_ADDRESS, categories='15,SSH', comment='a comment')

    def test_report__with_quoted_comment(self, api_key_mock):
        mock = self.call_command(
            action='report', ip_address=self.TEST_IP_ADDRESS, categories=[15, 'SSH'], comment=['a comment'])
        mock.assert_called_once_with(ip_address=self.TEST_IP_ADDRESS, categories='15,SSH', comment='a comment')

    def test_report__with_sensitive_comment(self, mock):
        with patch('pwd.getpwall', return_value=[('username',)]):
            with patch('socket.gethostname', return_value='hostname'):
                mock = self.call_command(
                    action='report', ip_address=self.TEST_IP_ADDRESS, categories=[15, 'SSH'], mask_sensitive_data=True,
                    comment=["Some", "email@example.com", "hostname", "and", "username", "butnothostname",
                             "andnotusername"])
        mock.assert_called_once_with(
            ip_address=self.TEST_IP_ADDRESS, categories='15,SSH',
            comment='Some *email* *host* and *user* butnothostname andnotusername')

    def test_report__with_sensitive_quoted_comment(self, mock):
        with patch('pwd.getpwall', return_value=[('username',)]):
            with patch('socket.gethostname', return_value='hostname'):
                mock = self.call_command(
                    action='report', ip_address=self.TEST_IP_ADDRESS, categories=[15, 'SSH'], mask_sensitive_data=True,
                    comment=["Some email@example.com hostname and username butnothostname andnotusername"])
        mock.assert_called_once_with(
            ip_address=self.TEST_IP_ADDRESS, categories='15,SSH',
            comment='Some *email* *host* and *user* butnothostname andnotusername')

    def test_report__with_extremly_long_comment(self, api_key_mock):
        long_comm = 'a' * 1000
        mock = self.call_command(
            action='report', ip_address=self.TEST_IP_ADDRESS, categories=[15, 'SSH'], comment=[long_comm, 'comment'])
        mock.assert_called_once_with(ip_address=self.TEST_IP_ADDRESS, categories='15,SSH', comment=long_comm + '\n...')
