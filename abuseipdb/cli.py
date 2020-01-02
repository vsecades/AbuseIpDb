import argparse
import json
import os
import stat
from configparser import ConfigParser, NoOptionError

from abuseipdb import AbuseIpDb


def main():
    args = _parse_parameter()
    api = _create_api(args)
    kwargs = _create_kwargs_from_args(args)
    result = _call_action(api, args.action, **kwargs)
    _print_result(result)


def _call_action(api, action, **kwargs):
    return getattr(api, action)(**kwargs)


def _print_result(result):
    print(json.dumps(result, indent=4, sort_keys=True))


def _create_kwargs_from_args(args):
    def to_unicode(s):
        try:
            return s.decode('utf-8')
        except:
            return s

    if args.action == "blacklist":
        filter_for_keys = ("confidence_minimum", "limit")
    elif args.action == "bulk_report":
        filter_for_keys = ("file_name")
        args.file_name = args.report_file
    elif args.action == "check":
        filter_for_keys = ("ip_address", "max_age_in_days")
    elif args.action == "check_block":
        filter_for_keys = ("cidr_network", "max_age_in_days")
    elif args.action == "report":
        filter_for_keys = ("ip_address", "categories", "comment")
    else:
        filter_for_keys = ()

    # only pass on the relevant parameters
    kwargs = {k: v for k, v in vars(args).items() if k in filter_for_keys}

    # argparse stores the following parameters as a list
    if "categories"in kwargs.keys():
        kwargs["categories"] = ",".join(str(c) for c in kwargs["categories"])
    if "comment"in kwargs.keys():
        kwargs["comment"] = " ".join(str(c) for c in kwargs["comment"])
    # Needed for Python 2.7
    if "ip_address"in kwargs.keys():
        kwargs["ip_address"] = to_unicode(kwargs["ip_address"])
    if "cidr_network"in kwargs.keys():
        kwargs["cidr_network"] = to_unicode(kwargs["cidr_network"])
    return kwargs


def _create_api(args):
    api_version = "APIv{}".format(args.api_version)
    api_key, subscriber = _read_api_key_and_subscriber_status(args.config_file)
    subscriber = False
    return AbuseIpDb(api_key=api_key, api_version=api_version, subscriber=subscriber)


def _read_api_key_and_subscriber_status(file_name):
    # Need to be a separate method to be able to mock it.
    if os.stat(file_name).st_mode & (stat.S_IRWXG | stat.S_IRWXO):
        raise OSError('Security issue!  Configuration readable by others than the owner!')
    config = ConfigParser()
    config.read(file_name)
    api_key = config.get('AbuseIPDB', 'api_key')
    try:
        subscriber = config.get('AbuseIPDB', 'subscriber')
    except NoOptionError:
        subscriber = False
    return api_key, subscriber


def _parse_parameter():
    parser = argparse.ArgumentParser(
        prog="abusipdb",
        description=description_text,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("-a", "--api-version",
                        type=int,
                        default=2,
                        choices=[1, 2],
                        help="choose the API version")
    parser.add_argument("-f", "--config-file",
                        default="/etc/abuseipdb",
                        metavar="FILE",
                        help="specify a different configuration file")
    subparsers = parser.add_subparsers(
        title="subcommands",
        description=subparsers_description,
        dest="action",
        help="execute the specified command")

    blacklist = subparsers.add_parser(
        "blacklist", add_help=False,
        usage="abusipdb blacklist [{-l,--limit} LIMIT] [{-m,--confidence_minimum} MINIMUM]")
    blacklist.add_argument(
        "-m", "--confidence_minimum",
        type=int,
        default=100,
        help="lower the confidence minimum to this percentage (subscribers only)")
    blacklist.add_argument(
        "-l", "--limit",
        type=int,
        default=10000,
        help="limit the number of entries in the blacklist")

    bulk_report = subparsers.add_parser(
        "bulk_report", add_help=False,
        usage="abusipdb bulk_report FILE")
    bulk_report.add_argument(
        "report_file",
        help="file containing the bulk report")

    check = subparsers.add_parser(
        "check", add_help=False,
        usage="abusipdb check [{-d,--max-age-in-days] DAYS] IP_ADDRESS")
    check.add_argument(
        "ip_address",
        help="check or report IP address")
    check.add_argument(
        "-d", "--max-age-in-days",
        type=int,
        help="only consider reports up to this age during checks")

    check_block = subparsers.add_parser(
        "check_block", add_help=False,
        usage="abusipdb check_block [{-d,--max-age-in-days} DAYS] NETWORK")
    check_block.add_argument(
        "cidr_network",
        help="check CIDR network")
    check_block.add_argument(
        "-d", "--max-age-in-days",
        type=int,
        help="only consider reports up to this age during checks")

    report = subparsers.add_parser(
        "report", add_help=False,
        usage="abusipdb report {-c,--category} CATEGORY [{-c,--category} CATEGORY [...]] IP_ADDRESS [COMMENT]")
    report.add_argument(
        "ip_address",
        help="check or report IP address")
    report.add_argument(
        "-c", "--category",
        action="append",
        dest="categories",
        required=True,
        help="specify the category for the report (multiple times)")
    report.add_argument(
        "comment",
        nargs=argparse.REMAINDER,
        help="comment for the report")

    args = parser.parse_args()
    return args


description_text = """
description:

  Interact with the Abuse IP DB on the command line

  You need an API key for https://www.abuseipdb.com/ to use this program.
  Please visit https://www.abuseipdb.com/register to receive one.

  You must place this API key in a configuration file.  The default
  configuration file is /etc/abuseipdb on UNIX systems. You can change
  this path with the --config-file option.  It contains a single line
  with the following format:

    [AbuseIPDB]
    api_key = YourValidAPIkeyforAbuseIpDb
    subscriber = False

  You can omit the configuration for subscriber.  It defaults to False.

  There is no parameter to specify the API key, because it would show up in
  the global process list.  The configuration file must only be readable
  by the executing user.  This decision was made to protect the API key.
"""

subparsers_description = """For an explanation of the commands please visit https://docs.abuseipdb.com/.

abusipdb blacklist [{-l,--limit} LIMIT] [{-m,--confidence_minimum} MINIMUM]
abusipdb bulk_report FILE
abusipdb check [{-d,--max-age-in-days} DAYS] IP_ADDRESS
abusipdb check_block [{-d,--max-age-in-days} DAYS] NETWORK
abusipdb report {-c,--category} CATEGORY [{-c,--category} CATEGORY [...]]
                IP_ADDRESS [COMMENT]
"""
