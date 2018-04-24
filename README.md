# AbuseIpDb
### Wrapper around the AbuseIPDb service API

This was a project born of having to do this in an automated fashion for our internal systems, and not finding a decent Python 2.7 package worth installing.

In order to use it, all you need to do is:

```python
import abuseipdb
```
Once imported into your project, configure the API key for further use (you need to sign up for a webmaster account for this):

```python
abuseipdb.configure_api_key("[API KEY]")
```
This just updates the internal api key value in use.  Update that as needed if you need to report into multiple accounts over the course of your script.

Following that, there are 3 main methods for use within the module.  They are modelled  against the AbuseIPDb API.  These methods are:

check_ip
```python
abuseip.check_ip(ip="[IP]",days="[DAYS]")
```

check_cidr
```python
check_cidr(cidr="[CIDR]",days="[DAYS]")
```

report_ip
```python
report_ip(categories="[CATEGORIES]", comment="[OPTIONAL COMMENT]", ip="[IP]")
```
Out of these 3 methods, the parameters follow the rules set forth by AbuseIPDb posted here:

[Abuse IP DB API](https://www.abuseipdb.com/api.html "Abuse IP DB API")

| Field | Required  |  Default |  Example | Description  |
| ------------ | ------------ | ------------ | ------------ | ------------ |
| [IP]  |  Y |  NA | 8.8.8.8  | IPv4 Address  |
|  [DAYS] | N  | 30  |  30 |  Check for IP Reports in the last 30 days.  |
| [CIDR]  |  Y | NA  |  207.126.144.0/20 |  IPv4 Address Block in CIDR notation |
|  [CATEGORIES] | Y  | NA  | 10,12,15  | Comma delineated list of category IDs  |
| [OPTIONAL COMMENT] |  N | NA  |  This is a comment. |  Describe the type of malicious activity |
|  [API KEY] | Y  |  NA | Tzmp1...quWvaiO  | Your API key.  |


Source code can be found here:

####[AbuseIpDB Repository](https://github.com/vsecades/AbuseIpDb "AbuseIpDB Repository")
----