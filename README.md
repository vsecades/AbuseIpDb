# AbuseIpDb - Wrapper around the Abuse IP DB service API

This was a project born of having to do this in an automated fashion for our
internal systems, and not finding a decent Python package worth installing.

The package supports APIv1 in full.

**Please note:** The APIv1 is deprecated by AbuseIpDb.  They set the sunset
date to 2020-02-01.

## Installing

```bash
pip install abuseipdb
```

## Usage

The package still supports the existing methods for the APIv1.  This enables
you to migrate gradually.  We will only describe the new usage below.

```python
from abuseipdb import AbuseIpDb
abuse = AbuseIpDb(api_key='APIv1key')
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

All the following calls result in the same call to AbuseIpDb.  If yyou pass in
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

## Project links

 * [AbuseIpDB Repository](https://github.com/vsecades/AbuseIpDb "AbuseIpDB Repository")
 * [Abuse IP DB APIv1 Documentation](https://www.abuseipdb.com/api.html)
 * [IPv4 Address Blocks Reserved for Documentation](https://tools.ietf.org/html/rfc5737)
----
