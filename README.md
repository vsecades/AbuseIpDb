# AbuseIpDb - Wrapper around the Abuse IP DB service API

The package supports APIv2.  No other API is currently available.  Uploading a
CSV report of abusive IP addresses is not yet implemented.

## Installing

```bash
pip install abuseipdb
```

## Usage as a python module

To choose between the API versions, you pass the version as the second
parameter.  Use the string APIv2 to select the API version.  This is currently
the only API supported by AbuseIPDB.

```python
from abuseipdb import AbuseIpDb
abuse_v2 = AbuseIpDb(api_key='APIv2key', api_version='APIv2')  # Using API v2
abuse = AbuseIpDb(api_key='APIv2key')                          # Also using API v2
```

If you have a subscription plan with Abuse IP DB, you can indicate this with an
additional parameter.

```python
from abuseipdb import AbuseIpDb
abuse = AbuseIpDb(api_key='APIv2key', subscriber=True)
```

### Checking a single IP address

```python
abuse.check(ip_address="192.0.2.123")
abuse.check(ip_address="192.0.2.123", max_age_in_days=90)
```

### Checking for a CIDR network block

```python
abuse.check_block(cidr_network="192.0.2.0/24")
abuse.check_block(cidr_network="192.0.2.0/24", max_age_in_days=90)
```

### Report an abusive IP address

All the following calls result in the same call to AbuseIpDb.  If you pass in
an unkonwn category, it will raise a `ValueError`.


```python
abuse.report(ip_address="192.0.2.123", categories="15,22")
abuse.report(ip_address="192.0.2.123", categories="15, 22")
abuse.report(ip_address="192.0.2.123", categories="HACKING, SSH")
abuse.report(ip_address="192.0.2.123", categories=(15, 22))
abuse.report(ip_address="192.0.2.123", categories=("15", "22"))
abuse.report(ip_address="192.0.2.123", categories=[15, "SSH"])
```

This adds a comment to the report.

```python
abuse.report(ip_address="192.0.2.123", categories=("13", "22"),
             comment="Some comment about the abusive IP address")
```

### Report a list of abusive IP addresses

Please refer to [IP Bulk Reporter](https://www.abuseipdb.com/bulk-report)
for the exact specification of the CSV file.

```python
abuse.bulk_report(file_name="report.csv")
```

**NOTE:** This is currently not implemented.

### Retrieve a list of abusive IP addresses

```python
abuse.blacklist()
abuse.blacklist(limit=10)             # Only get 10 entries
abuse.blacklist(confidence_level=90)  # Only available for subscribers
```

## Usage on the command line

You can invoke the module on the command line.  It supports all the commands
listed above.  For the explicit syntax and the required configuration call it
with the `--help` parameter.

```bash
abuseipdb --help
```

### fail2ban

The CLI was developed for usage with *fail2ban*.  Use the following action
instead of *wget* or *curl*:

```
actionban = abuseipdb -s report -c "<abuseipdb_category>" "<ip>" "<matches>"
actionban = abuseipdb --mask-sensitive-data report --category "<abuseipdb_category>" "<ip>" "<matches>"
```

The lines do the same.  Of course you can leave out the masking of sensitive
data, but it is a bad idea.  It will replace your own hostname with `*host*`,
any existing user with `*user*` and any email address with `*email*`.  This
will prevent any information leakage about your system and reduce the attack
surface a little bit.

## Project links

 * [AbuseIpDB Repository](https://github.com/vsecades/AbuseIpDb "AbuseIpDB Repository")
 * [Abuse IP DB APIv1 Documentation](https://www.abuseipdb.com/api.html)
 * [Abuse IP DB APIv2 Documentation](https://docs.abuseipdb.com/)
 * [IPv4 Address Blocks Reserved for Documentation](https://tools.ietf.org/html/rfc5737)
----
