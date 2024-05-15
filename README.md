# AbuseIpDb - Wrapper around the Abuse IP DB service API

The package supports APIv2.  No other API is currently available.  Uploading a
CSV report of abusive IP addresses is not yet implemented, but is in the plans to do so.

## Installing

Installation is planned to be done around Composer. Please be sure to NOT try to clone this repository and try your luck with getting it working. 
```bash
composer install AbuseIpDb
```

## Usage as a Composer package

We only support APIv2 to select the API version (this can be passed in as a parameter or is used as the default).  Newer values will be provided when the API is updated and our group has time to implement.  This is currently the only API supported by AbuseIPDB.

```php
TBD, still in implementation phase
```

If you have a subscription plan with Abuse IP DB, you can indicate this with an
additional parameter.

```php
TBD, still in implementation phase
```

### Checking a single IP address

```php
TBD, still in implementation phase
```

### Checking for a CIDR network block

```php
TBD, still in implementation phase
```

### Report an abusive IP address

All the following calls result in the same call to AbuseIpDb.  If you pass in
an unkonwn category, it will raise a `ValueError`.


```php
TBD, still in implementation phase
```

This adds a comment to the report.

```php
TBD, still in implementation phase
```

### Report a list of abusive IP addresses

Please refer to [IP Bulk Reporter](https://www.abuseipdb.com/bulk-report)
for the exact specification of the CSV file.

```php
TBD, still in implementation phase
```

**NOTE:** This is currently not implemented.

### Retrieve a list of abusive IP addresses

```php
TBD, still in implementation phase
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
TBD, still in implementation phase
```

The lines do the same.  Of course you can leave out the masking of sensitive
data, but it is a bad idea.  It will replace your own hostname with `*host*`,
any existing user with `*user*` and any email address with `*email*`.  This
will prevent any information leakage about your system and reduce the attack
surface a little bit.

## Project links

 * [AbuseIpDB Repository](https://github.com/vsecades/AbuseIpDb "AbuseIpDB Repository")
 * [Abuse IP DB APIv2 Documentation](https://docs.abuseipdb.com/)
 * [IPv4 Address Blocks Reserved for Documentation](https://tools.ietf.org/html/rfc5737)
----
