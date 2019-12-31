import argparse
import sys


def main():
    args = parse_parameter()


def parse_parameter():
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
        "bulk-report", add_help=False,
        usage="abusipdb bulk-report FILE")
    bulk_report.add_argument(
        "report-file",
        help="file containing the bulk report")

    check = subparsers.add_parser(
        "check", add_help=False,
        usage="abusipdb check [{-d,--max-age-in-days] DAYS] IP_ADDRESS")
    check.add_argument(
        "ip-address",
        help="check or report IP address")
    check.add_argument(
        "-d", "--max-age-in-days",
        type=int,
        help="only consider reports up to this age during checks")

    check_block = subparsers.add_parser(
        "check-block", add_help=False,
        usage="abusipdb check-block [{-d,--max-age-in-days} DAYS] NETWORK")
    check_block.add_argument(
        "cidr-network",
        help="check CIDR network")
    check_block.add_argument(
        "-d", "--max-age-in-days",
        type=int,
        help="only consider reports up to this age during checks")

    report = subparsers.add_parser(
        "report", add_help=False,
        usage="abusipdb report {-c,--category} CATEGORY [{-c,--category} CATEGORY [...]] IP_ADDRESS [COMMENT]")
    report.add_argument(
        "ip-address",
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
    print(vars(args))
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

    api_key = "YourValidAPIkeyforAbuseIpDb"

  There is no parameter to specify the API key, because it would show up in
  the global process list.  The configuration file must only be readable
  by the executing user.  This decision was made to protect the API key.
"""

subparsers_description = """For an explanation of the commands please visit https://docs.abuseipdb.com/.

abusipdb blacklist [{-l,--limit} LIMIT] [{-m,--confidence_minimum} MINIMUM]
abusipdb bulk-report FILE
abusipdb check [{-d,--max-age-in-days} DAYS] IP_ADDRESS
abusipdb check-block [{-d,--max-age-in-days} DAYS] NETWORK
abusipdb report {-c,--category} CATEGORY [{-c,--category} CATEGORY [...]]
                IP_ADDRESS [COMMENT]
"""
