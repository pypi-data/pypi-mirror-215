import hashlib
import sys
from time import strftime, gmtime


if sys.version_info.major == 2:
    from urlparse import urlparse, urlunparse
    from urllib import quote, unquote

else:
    from urllib.parse import urlparse, urlunparse, quote, unquote


def current_time():
    time_format = "%a, %d %b %Y %H:%M:%S GMT"
    return strftime(time_format, gmtime())


def url_quote(o):
    scheme, netloc, path, params, query, fragment = urlparse(
        o, allow_fragments=False
    )
    path = quote(unquote(path))
    o = urlunparse((scheme, netloc, path, params, query, fragment))
    return o


def should_url_quote(key):
    should_url_quote_list = ["x-qs-fetch-source"]
    return key in should_url_quote_list


def should_quote(key):
    should_quote_list = ["x-qs-copy-source", "x-qs-move-source"]
    return key in should_quote_list


def md5_digest(input_str):
    m = hashlib.md5()
    m.update(input_str)
    return m.digest()
