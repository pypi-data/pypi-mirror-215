# +-------------------------------------------------------------------------
# | Copyright (C) 2016 Yunify, Inc.
# +-------------------------------------------------------------------------
# | Licensed under the Apache License, Version 2.0 (the "License");
# | you may not use this work except in compliance with the License.
# | You may obtain a copy of the License in the LICENSE file, or at:
# |
# | http://www.apache.org/licenses/LICENSE-2.0
# |
# | Unless required by applicable law or agreed to in writing, software
# | distributed under the License is distributed on an "AS IS" BASIS,
# | WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# | See the License for the specific language governing permissions and
# | limitations under the License.
# +-------------------------------------------------------------------------
# -*- coding: utf-8 -*-

import hmac
import base64
import logging
import hashlib
import time
import sys
# from pytz import timezone
# from datetime import datetime
if sys.version_info.major == 2:
    from urllib import quote, unquote, urlencode, quote_plus
    from urlparse import urlparse, parse_qs, urlunparse
else:
    from urllib.parse import quote, unquote, urlencode, quote_plus, urlparse, parse_qs, urlunparse
from qingcloud_hpc.build_request import Builder
from qingcloud_hpc.cli_utils.helper import url_quote

ISO8601 = '%Y-%m-%dT%H:%M:%SZ'


def process_canonical_request(request):
    hex_encode = hex_encode_md5_hash(request.data)
    parsed_url = urlparse(request.url)
    canonical_uri = process_canonical_uri(parsed_url[2])
    canonical_query_string = process_canonical_query_string(parse_qs(parsed_url[4]))
    return "%s\n%s\n%s\n%s" % (request.method.upper(), canonical_uri, canonical_query_string, hex_encode)


def process_canonical_query_string(query):
    # print "process_canonical_query_string query [%s:%s] " % (type(query), query)
    params = []
    for param in query:
        params.append(param)
    params.sort()

    canonical_query_param = []
    for key in params:
        value = query[key]
        k = quote(key)
        if type(value) is list:
            value.sort()
            for v in value:
                # print "k,v [%s:%s], type(v) = %s " % (k, v, type(v))
                kv = k + "=" + quote(str(v))
                canonical_query_param.append(kv)
        else:
            kv = k + "=" + quote(str(value))
            canonical_query_param.append(kv)

    return '&'.join(canonical_query_param)


def process_canonical_uri(path):
    pattens = unquote(path).split('/')
    uri = []
    for v in pattens:
        uri.append(quote(v))
    url_path = "/".join(uri)

    if url_path[-1] != '/':
        url_path = url_path + "/"

    return url_path


def hex_encode_md5_hash(data):
    if sys.version_info.major == 2:
        if not data:
            data = ""
    else:
        if not data:
            data = "".encode("utf-8")
        else:
            data = data.encode("utf-8")
    md5 = hashlib.md5()
    md5.update(data)
    return md5.hexdigest()


class Request:

    def __init__(self, config, operation):
        self.req = Builder(config, operation).parse()
        self.access_key_id = config.qy_access_key_id
        self.secret_access_key = config.qy_secret_access_key
        self.zone = config.zone
        self.logger = logging.getLogger("hpc-sdk")
        # print self.req.method
        # print self.req.url
        # print self.req.headers
        # print self.req.files
        # print self.req.data
        # print self.req.json
        # print self.req.params
        # print self.req.auth
        # print self.req.cookies

    def __repr__(self):
        return "<Request %s>" % self.req.method

    def sign(self):
        parsed_url = list(urlparse(self.req.url))
        query = {"version": "1",
                 "signature_version": "1",
                 "signature_method": "HmacSHA256",
                 "access_key_id": self.access_key_id,
                 "timestamp": time.strftime(ISO8601, time.gmtime())}

        if len(parsed_url[4]) == 0:
            parsed_url[4] = urlencode(query)
        else:
            if parsed_url[4].find("timestamp=") != -1:
                del query["timestamp"]
            parsed_url[4] = parsed_url[4] + "&" + urlencode(query)

        self.req.url = urlunparse(parsed_url)
        print(self.req.url )

        sign = {"signature": self.calc_sign()}
        parsed_url[4] = parsed_url[4] + "&" + urlencode(sign)
        self.req.url = urlunparse(parsed_url)

        self.logger.debug(self.req.url)

        prepared = self.req.prepare()
        prepared.url = url_quote(prepared.url)

        # print "prepared.method = %s" % prepared.method
        # print "prepared.url = %s" % prepared.url
        # print "prepared.headers = %s" % prepared.headers
        # print "prepared._cookies = %s" % prepared._cookies
        # print "prepared.body = %s" % prepared.body

        return prepared

    def calc_sign(self):
        string_to_sign = process_canonical_request(self.req)
        # print "string_to_sign: %s" % string_to_sign
        print(string_to_sign)
        if sys.version_info.major == 2:
            h = hmac.new(
                self.secret_access_key,
                string_to_sign,
                digestmod=hashlib.sha256
            )
            signature = base64.b64encode(h.digest()).strip()
            return quote_plus(signature)
        else:
            h = hmac.new(self.secret_access_key.encode(encoding="utf-8"), digestmod=hashlib.sha256)
            h.update(string_to_sign.encode(encoding="utf-8"))
            sign = base64.b64encode(h.digest()).strip()
            signature = quote_plus(sign.decode())
            # signature = quote_plus(signature)
            print(signature)
            return signature

