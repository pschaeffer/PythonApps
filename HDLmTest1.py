# Start the first set of tests class. Note that no instances of this class
# are ever created (actually I don't know how Python unit testing works).

from   deepdiff import DeepDiff
from   HDLmUrl  import *
import json 
import unittest
import urllib.request

class Test_HDLmTest1(unittest.TestCase):
  # Run a set of URL parsing tests
  def test_runUrlTests(self):
    # The array below contains all of the URL tests. For each test, we have an input 
    # string (a URL), an output string (the return value converted to JSON), and an
    # error message string 
    urlTests = [  
                 [ 'https://192.168.a.1/',
                   '{"fragment": null, \
                     "hostParts": ["192", "168", "a", "1"], \
                     "hostString": "192.168.a.1", \
                     "hostType": "HDLmHostTypes.standard", \
                     "originalUrl": "https://192.168.a.1/", \
                     "pathParts": [], \
                     "pathString": "/", \
                     "portNumber": null, \
                     "queryParts": null, \
                     "queryString": null, \
                     "scheme": "https", \
                     "userInfo": null}',
                   '' ],
                 [ 'https://192.256.1.1/',
                   '{"fragment": null, \
                     "hostParts": ["192", "256", "1", "1"], \
                     "hostString": "192.256.1.1", \
                     "hostType": "HDLmHostTypes.standard", \
                     "originalUrl": "https://192.256.1.1/", \
                     "pathParts": [], \
                     "pathString": "/", \
                     "portNumber": null, \
                     "queryParts": null, \
                     "queryString": null, \
                     "scheme": "https", \
                     "userInfo": null}',
                   '' ],
                 [ 'https://192.168.1/',
                   '{"fragment": null, \
                     "hostParts": ["192", "168", "1"], \
                     "hostString": "192.168.1", \
                     "hostType": "HDLmHostTypes.standard", \
                     "originalUrl": "https://192.168.1/", \
                     "pathParts": [], \
                     "pathString": "/", \
                     "portNumber": null, \
                     "queryParts": null, \
                     "queryString": null, \
                     "scheme": "https", \
                     "userInfo": null}',
                   '' ],               
                 [ 'https://0:25/a//b//?x123=123y&x456=aabb',
                   '{"fragment": null, \
                     "hostParts": ["0"], \
                     "hostString": "0", \
                     "hostType": "HDLmHostTypes.standard", \
                     "originalUrl": "https://0:25/a//b//?x123=123y&x456=aabb", \
                     "pathParts": ["a", "", "b", ""], \
                     "pathString": "/a//b//", \
                     "portNumber": 25, \
                     "queryParts": {"x123": "123y", "x456": "aabb"}, \
                     "queryString": "x123=123y&x456=aabb", \
                     "scheme": "https", \
                     "userInfo": null}',
                   '' ],
                 [ 'https://a:25/a//b//?x123=123y&x456=aabb',
                   '{"fragment": null, \
                     "hostParts": ["a"], \
                     "hostString": "a", \
                     "hostType": "HDLmHostTypes.standard", \
                     "originalUrl": "https://a:25/a//b//?x123=123y&x456=aabb", \
                     "pathParts": ["a", "", "b", ""], \
                     "pathString": "/a//b//", \
                     "portNumber": 25, \
                     "queryParts": {"x123": "123y", "x456": "aabb"}, \
                     "queryString": "x123=123y&x456=aabb", \
                     "scheme": "https", \
                     "userInfo": null}',
                   '' ],
                 [ 'https://0-a.1.2',
                   '{"fragment": null, \
                     "hostParts": ["0-a", "1", "2"], \
                     "hostString": "0-a.1.2", \
                     "hostType": "HDLmHostTypes.standard", \
                     "originalUrl": "https://0-a.1.2", \
                     "pathParts": [], \
                     "pathString": "", \
                     "portNumber": null, \
                     "queryParts": null, \
                     "queryString": null, \
                     "scheme": "https", \
                     "userInfo": null}',
                   '' ],
                 [ 'https://0-a.b.c',
                   '{"fragment": null, \
                     "hostParts": ["0-a", "b", "c"], \
                     "hostString": "0-a.b.c", \
                     "hostType": "HDLmHostTypes.standard", \
                     "originalUrl": "https://0-a.b.c", \
                     "pathParts": [], \
                     "pathString": "", \
                     "portNumber": null, \
                     "queryParts": null, \
                     "queryString": null, \
                     "scheme": "https", \
                     "userInfo": null}',
                   '' ], 
                 [ 'https://0a.b.c',
                   '{"fragment": null, \
                     "hostParts": ["0a", "b", "c"], \
                     "hostString": "0a.b.c", \
                     "hostType": "HDLmHostTypes.standard", \
                     "originalUrl": "https://0a.b.c", \
                     "pathParts": [], \
                     "pathString": "", \
                     "portNumber": null, \
                     "queryParts": null, \
                     "queryString": null, \
                     "scheme": "https", \
                     "userInfo": null}',
                   '' ], 
                 [ 'https://[00ff::]:25/a//b//?x123=123y&x456=aabb',
                   '{"fragment": null, \
                     "hostParts": [255, null], \
                     "hostString": "00ff::", \
                     "hostType": "HDLmHostTypes.ipv6", \
                     "originalUrl": "https://[00ff::]:25/a//b//?x123=123y&x456=aabb", \
                     "pathParts": ["a", "", "b", ""], \
                     "pathString": "/a//b//", \
                     "portNumber": 25, \
                     "queryParts": {"x123": "123y", "x456": "aabb"}, \
                     "queryString": "x123=123y&x456=aabb", \
                     "scheme": "https", \
                     "userInfo": null}',
                   '' ],     
                 [ 'https://[00ff::]/a//b//?x123=123y&x456=aabb',
                   '{"fragment": null, \
                     "hostParts": [255, null], \
                     "hostString": "00ff::", \
                     "hostType": "HDLmHostTypes.ipv6", \
                     "originalUrl": "https://[00ff::]/a//b//?x123=123y&x456=aabb", \
                     "pathParts": ["a", "", "b", ""], \
                     "pathString": "/a//b//", \
                     "portNumber": null, \
                     "queryParts": {"x123": "123y", "x456": "aabb"}, \
                     "queryString": "x123=123y&x456=aabb", \
                     "scheme": "https", \
                     "userInfo": null}',
                   '' ],   
                 [ 'https://00ff::/a//b//?x123=123y&x456=aabb',
                   '{"fragment": null, \
                     "hostParts": [255, null], \
                     "hostString": "00ff::", \
                     "hostType": "HDLmHostTypes.ipv6", \
                     "originalUrl": "https://00ff::/a//b//?x123=123y&x456=aabb", \
                     "pathParts": ["a", "", "b", ""], \
                     "pathString": "/a//b//", \
                     "portNumber": null, \
                     "queryParts": {"x123": "123y", "x456": "aabb"}, \
                     "queryString": "x123=123y&x456=aabb", \
                     "scheme": "https", \
                     "userInfo": null}',
                   '' ],    
                 [ 'https://ff00::/a//b//?x123=123y&x456=aabb',
                   '{"fragment": null, \
                     "hostParts": [65280, null], \
                     "hostString": "ff00::", \
                     "hostType": "HDLmHostTypes.ipv6", \
                     "originalUrl": "https://ff00::/a//b//?x123=123y&x456=aabb", \
                     "pathParts": ["a", "", "b", ""], \
                     "pathString": "/a//b//", \
                     "portNumber": null, \
                     "queryParts": {"x123": "123y", "x456": "aabb"}, \
                     "queryString": "x123=123y&x456=aabb", \
                     "scheme": "https", \
                     "userInfo": null}',
                   '' ],            
                 [ 'https://a:25/a//b//?x123=123y&x456=aabb',
                   '{"fragment": null, \
                     "hostParts": ["a"], \
                     "hostString": "a", \
                     "hostType": "HDLmHostTypes.standard", \
                     "originalUrl": "https://a:25/a//b//?x123=123y&x456=aabb", \
                     "pathParts": ["a", "", "b", ""], \
                     "pathString": "/a//b//", \
                     "portNumber": 25, \
                     "queryParts": {"x123": "123y", "x456": "aabb"}, \
                     "queryString": "x123=123y&x456=aabb", \
                     "scheme": "https", \
                     "userInfo": null}',
                   '' ],
                 [ 'https://[ffff]:25/a//b//?x123=123y&x456=aabb',
                   '{"fragment": null, \
                     "hostParts": [65535], \
                     "hostString": "ffff", \
                     "hostType": "HDLmHostTypes.ipv6", \
                     "originalUrl": "https://[ffff]:25/a//b//?x123=123y&x456=aabb", \
                     "pathParts": ["a", "", "b", ""], \
                     "pathString": "/a//b//", \
                     "portNumber": 25, \
                     "queryParts": {"x123": "123y", "x456": "aabb"}, \
                     "queryString": "x123=123y&x456=aabb", \
                     "scheme": "https", \
                     "userInfo": null}',
                   '' ],
                 [ 'https://ffff/a//b//?x123=123y&x456=aabb',
                   '{"fragment": null, \
                     "hostParts": ["ffff"], \
                     "hostString": "ffff", \
                     "hostType": "HDLmHostTypes.standard", \
                     "originalUrl": "https://ffff/a//b//?x123=123y&x456=aabb", \
                     "pathParts": ["a", "", "b", ""], \
                     "pathString": "/a//b//", \
                     "portNumber": null, \
                     "queryParts": {"x123": "123y", "x456": "aabb"}, \
                     "queryString": "x123=123y&x456=aabb", \
                     "scheme": "https", \
                     "userInfo": null}',
                   '' ],
                 [ 'https://192.168.1.1:25/a//b//?x123=123y&x456=aabb',
                   '{"fragment": null, \
                     "hostParts": [192, 168, 1, 1], \
                     "hostString": "192.168.1.1", \
                     "hostType": "HDLmHostTypes.ipv4", \
                     "originalUrl": "https://192.168.1.1:25/a//b//?x123=123y&x456=aabb", \
                     "pathParts": ["a", "", "b", ""], \
                     "pathString": "/a//b//", \
                     "portNumber": 25, \
                     "queryParts": {"x123": "123y", "x456": "aabb"}, \
                     "queryString": "x123=123y&x456=aabb", \
                     "scheme": "https", \
                     "userInfo": null}',
                   '' ],
                 [ 'https://[2010:836B:4179::836B:4179]:25/a/b//c/d?x123=123y;x456=aabb',
                   '{"fragment": null, \
                     "hostParts": [8208, 33643, 16761, null, 33643, 16761], \
                     "hostString": "2010:836b:4179::836b:4179", \
                     "hostType": "HDLmHostTypes.ipv6", \
                     "originalUrl": "https://[2010:836B:4179::836B:4179]:25/a/b//c/d?x123=123y;x456=aabb", \
                     "pathParts": ["a", "b", "", "c", "d"], \
                     "pathString": "/a/b//c/d", \
                     "portNumber": 25, \
                     "queryParts": {"x123": "123y", "x456": "aabb"}, \
                     "queryString": "x123=123y;x456=aabb", \
                     "scheme": "https", \
                     "userInfo": null}',
                   '' ],
                 [ 'https://2010:836B:4179::836B:4179/a/b//c/d?x123=123y;x456=aabb',
                   '{"fragment": null, \
                     "hostParts": [8208, 33643, 16761, null, 33643, 16761], \
                     "hostString": "2010:836b:4179::836b:4179", \
                     "hostType": "HDLmHostTypes.ipv6", \
                     "originalUrl": "https://2010:836B:4179::836B:4179/a/b//c/d?x123=123y;x456=aabb", \
                     "pathParts": ["a", "b", "", "c", "d"], \
                     "pathString": "/a/b//c/d", \
                     "portNumber": null, \
                     "queryParts": {"x123": "123y", "x456": "aabb"}, \
                     "queryString": "x123=123y;x456=aabb", \
                     "scheme": "https", \
                     "userInfo": null}',
                   '' ],
                 [ 'http://abc.def#123',
                   '{"fragment": "123", \
                     "hostParts": ["abc", "def"], \
                     "hostString": "abc.def", \
                     "hostType": "HDLmHostTypes.standard", \
                     "originalUrl": "http://abc.def#123", \
                     "pathParts": [], \
                     "pathString": "", \
                     "portNumber": null, \
                     "queryParts": null, \
                     "queryString": null, \
                     "scheme": "http", \
                     "userInfo": null}',
                   '' ],
                 [ 'http://[::1]#123',
                   '{"fragment": "123", \
                     "hostParts": [null, 1], \
                     "hostString": "::1", \
                     "hostType": "HDLmHostTypes.ipv6", \
                     "originalUrl": "http://[::1]#123", \
                     "pathParts": [], \
                     "pathString": "", \
                     "portNumber": null, \
                     "queryParts": null, \
                     "queryString": null, \
                     "scheme": "http", \
                     "userInfo": null}',
                   '' ],
                 [ 'http://::1#123',
                   '{"fragment": "123", \
                     "hostParts": [null, 1], \
                     "hostString": "::1", \
                     "hostType": "HDLmHostTypes.ipv6", \
                     "originalUrl": "http://::1#123", \
                     "pathParts": [], \
                     "pathString": "", \
                     "portNumber": null, \
                     "queryParts": null, \
                     "queryString": null, \
                     "scheme": "http", \
                     "userInfo": null}',
                   '' ],
                 [ 'https://[::FF23:129.144.52.38]:25/',
                   '{"fragment": null, \
                     "hostParts": [null, 65315, 129, 144, 52, 38], \
                     "hostString": "::ff23:129.144.52.38", \
                     "hostType": "HDLmHostTypes.ipv6", \
                     "originalUrl": "https://[::FF23:129.144.52.38]:25/", \
                     "pathParts": [], \
                     "pathString": "/", \
                     "portNumber": 25, \
                     "queryParts": null, \
                     "queryString": null, \
                     "scheme": "https", \
                     "userInfo": null}',
                   '' ],
                 [ 'https://::FF23:129.144.52.38/',
                   '{"fragment": null, \
                     "hostParts": [null, 65315, 129, 144, 52, 38], \
                     "hostString": "::ff23:129.144.52.38", \
                     "hostType": "HDLmHostTypes.ipv6", \
                     "originalUrl": "https://::FF23:129.144.52.38/", \
                     "pathParts": [], \
                     "pathString": "/", \
                     "portNumber": null, \
                     "queryParts": null, \
                     "queryString": null, \
                     "scheme": "https", \
                     "userInfo": null}',
                   '' ],
                 [ 'https://[::]:25/',
                   '{"fragment": null, \
                     "hostParts": [null], \
                     "hostString": "::", \
                     "hostType": "HDLmHostTypes.ipv6", \
                     "originalUrl": "https://[::]:25/", \
                     "pathParts": [], \
                     "pathString": "/", \
                     "portNumber": 25, \
                     "queryParts": null, \
                     "queryString": null, \
                     "scheme": "https", \
                     "userInfo": null}',
                   '' ],
                 [ 'https://::/',
                   '{"fragment": null, \
                     "hostParts": [null], \
                     "hostString": "::", \
                     "hostType": "HDLmHostTypes.ipv6", \
                     "originalUrl": "https://::/", \
                     "pathParts": [], \
                     "pathString": "/", \
                     "portNumber": null, \
                     "queryParts": null, \
                     "queryString": null, \
                     "scheme": "https", \
                     "userInfo": null}',
                   '' ],
                 [ 'https://[::]/',
                   '{"fragment": null, \
                     "hostParts": [null], "hostString": "::", \
                     "hostType": "HDLmHostTypes.ipv6", \
                     "originalUrl": "https://[::]/", \
                     "pathParts": [], "pathString": "/", \
                     "portNumber": null, \
                     "queryParts": null, \
                     "queryString": null, \
                     "scheme": "https", \
                     "userInfo": null}',
                   '' ],
                 [ 'https://::/',
                   '{"fragment": null, \
                     "hostParts": [null], "hostString": "::", \
                     "hostType": "HDLmHostTypes.ipv6", \
                     "originalUrl": "https://::/", \
                     "pathParts": [], "pathString": "/", \
                     "portNumber": null, \
                     "queryParts": null, \
                     "queryString": null, \
                     "scheme": "https", \
                     "userInfo": null}',
                   '' ],
                 [ 'https://[::ffff]:25/',
                   '{"fragment": null, \
                     "hostParts": [null, 65535], \
                     "hostString": "::ffff", \
                     "hostType": "HDLmHostTypes.ipv6", \
                     "originalUrl": "https://[::ffff]:25/", \
                     "pathParts": [], \
                     "pathString": "/", \
                     "portNumber": 25, \
                     "queryParts": null, \
                     "queryString": null, \
                     "scheme": "https", \
                     "userInfo": null}',
                   '' ],
                 [ 'https://::ffff/',
                   '{"fragment": null, \
                     "hostParts": [null, 65535], \
                     "hostString": "::ffff", \
                     "hostType": "HDLmHostTypes.ipv6", \
                     "originalUrl": "https://::ffff/", \
                     "pathParts": [], \
                     "pathString": "/", \
                     "portNumber": null, \
                     "queryParts": null, \
                     "queryString": null, \
                     "scheme": "https", \
                     "userInfo": null}',
                   '' ],
                 [ 'https://[ffff::]:25/',
                   '{"fragment": null, \
                     "hostParts": [65535, null], \
                     "hostString": "ffff::", \
                     "hostType": "HDLmHostTypes.ipv6", \
                     "originalUrl": "https://[ffff::]:25/", \
                     "pathParts": [], \
                     "pathString": "/", \
                     "portNumber": 25, \
                     "queryParts": null, \
                     "queryString": null, \
                     "scheme": "https", \
                     "userInfo": null}',
                   '' ],
                 [ 'https://ffff::/',
                   '{"fragment": null, \
                     "hostParts": [65535, null], \
                     "hostString": "ffff::", \
                     "hostType": "HDLmHostTypes.ipv6", \
                     "originalUrl": "https://ffff::/", \
                     "pathParts": [], \
                     "pathString": "/", \
                     "portNumber": null, \
                     "queryParts": null, \
                     "queryString": null, \
                     "scheme": "https", \
                     "userInfo": null}',
                   '' ],
                 [ 'https://[FEDC:BA98:7654:3210:FEDC:BA98:7654:3210]:25/',
                   '{"fragment": null, \
                     "hostParts": [65244, 47768, 30292, 12816, 65244, 47768, 30292, 12816], \
                     "hostString": "fedc:ba98:7654:3210:fedc:ba98:7654:3210", \
                     "hostType": "HDLmHostTypes.ipv6", \
                     "originalUrl": "https://[FEDC:BA98:7654:3210:FEDC:BA98:7654:3210]:25/", \
                     "pathParts": [], \
                     "pathString": "/", \
                     "portNumber": 25, \
                     "queryParts": null, \
                     "queryString": null, \
                     "scheme": "https", \
                     "userInfo": null}',
                   '' ],
                 [ 'https://FEDC:BA98:7654:3210:FEDC:BA98:7654:3210/',
                   '{"fragment": null, \
                     "hostParts": [65244, 47768, 30292, 12816, 65244, 47768, 30292, 12816], \
                     "hostString": "fedc:ba98:7654:3210:fedc:ba98:7654:3210", \
                     "hostType": "HDLmHostTypes.ipv6", \
                     "originalUrl": "https://FEDC:BA98:7654:3210:FEDC:BA98:7654:3210/", \
                     "pathParts": [], \
                     "pathString": "/", \
                     "portNumber": null, \
                     "queryParts": null, \
                     "queryString": null, \
                     "scheme": "https", \
                     "userInfo": null}',
                   '' ],
                 [ 'https://[1080:0:0:0:8:800:200C:4171]:25/',
                   '{"fragment": null, \
                     "hostParts": [4224, 0, 0, 0, 8, 2048, 8204, 16753], \
                     "hostString": "1080:0:0:0:8:800:200c:4171", \
                     "hostType": "HDLmHostTypes.ipv6", \
                     "originalUrl": "https://[1080:0:0:0:8:800:200C:4171]:25/", \
                     "pathParts": [], \
                     "pathString": "/", \
                     "portNumber": 25, \
                     "queryParts": null, \
                     "queryString": null, \
                     "scheme": "https", \
                     "userInfo": null}',
                   '' ],
                 [ 'https://1080:0:0:0:8:800:200C:4171/',
                   '{"fragment": null, \
                     "hostParts": [4224, 0, 0, 0, 8, 2048, 8204, 16753], \
                     "hostString": "1080:0:0:0:8:800:200c:4171", \
                     "hostType": "HDLmHostTypes.ipv6", \
                     "originalUrl": "https://1080:0:0:0:8:800:200C:4171/", \
                     "pathParts": [], \
                     "pathString": "/", \
                     "portNumber": null, \
                     "queryParts": null, \
                     "queryString": null, \
                     "scheme": "https", \
                     "userInfo": null}',
                   '' ],
                 [ 'https://[3ffe:2a00:100:7031::1]:25/',
                   '{"fragment": null, \
                     "hostParts": [16382, 10752, 256, 28721, null, 1], \
                     "hostString": "3ffe:2a00:100:7031::1", \
                     "hostType": "HDLmHostTypes.ipv6", \
                     "originalUrl": "https://[3ffe:2a00:100:7031::1]:25/", \
                     "pathParts": [], \
                     "pathString": "/", \
                     "portNumber": 25, \
                     "queryParts": null, \
                     "queryString": null, \
                     "scheme": "https", \
                     "userInfo": null}',
                   '' ],
                 [ 'https://3ffe:2a00:100:7031::1/',
                   '{"fragment": null, \
                     "hostParts": [16382, 10752, 256, 28721, null, 1], \
                     "hostString": "3ffe:2a00:100:7031::1", \
                     "hostType": "HDLmHostTypes.ipv6", \
                     "originalUrl": "https://3ffe:2a00:100:7031::1/", \
                     "pathParts": [], \
                     "pathString": "/", \
                     "portNumber": null, \
                     "queryParts": null, \
                     "queryString": null, \
                     "scheme": "https", \
                     "userInfo": null}',
                   '' ],
                 [ 'https://[1080::8:800:200C:417A]:25/',
                   '{"fragment": null, \
                     "hostParts": [4224, null, 8, 2048, 8204, 16762], \
                     "hostString": "1080::8:800:200c:417a", \
                     "hostType": "HDLmHostTypes.ipv6", \
                     "originalUrl": "https://[1080::8:800:200C:417A]:25/", \
                     "pathParts": [], \
                     "pathString": "/", \
                     "portNumber": 25, \
                     "queryParts": null, \
                     "queryString": null, \
                     "scheme": "https", \
                     "userInfo": null}',
                   '' ],
                 [ 'https://1080::8:800:200C:417A/',
                   '{"fragment": null, \
                     "hostParts": [4224, null, 8, 2048, 8204, 16762], \
                     "hostString": "1080::8:800:200c:417a", \
                     "hostType": "HDLmHostTypes.ipv6", \
                     "originalUrl": "https://1080::8:800:200C:417A/", \
                     "pathParts": [], \
                     "pathString": "/", \
                     "portNumber": null, \
                     "queryParts": null, \
                     "queryString": null, \
                     "scheme": "https", \
                     "userInfo": null}',
                   '' ],
                 [ 'https://[::192.9.5.5]:25/',
                   '{"fragment": null, \
                     "hostParts": [null, 192, 9, 5, 5], \
                     "hostString": "::192.9.5.5", \
                     "hostType": "HDLmHostTypes.ipv6", \
                     "originalUrl": "https://[::192.9.5.5]:25/", \
                     "pathParts": [], \
                     "pathString": "/", \
                     "portNumber": 25, \
                     "queryParts": null, \
                     "queryString": null, \
                     "scheme": "https", \
                     "userInfo": null}',
                   '' ],
                 [ 'https://::192.9.5.5/',
                   '{"fragment": null, \
                     "hostParts": [null, 192, 9, 5, 5], \
                     "hostString": "::192.9.5.5", \
                     "hostType": "HDLmHostTypes.ipv6", \
                     "originalUrl": "https://::192.9.5.5/", \
                     "pathParts": [], \
                     "pathString": "/", \
                     "portNumber": null, \
                     "queryParts": null, \
                     "queryString": null, \
                     "scheme": "https", \
                     "userInfo": null}',
                   '' ],
                 [ 'https://[::FFFF:129.144.52.38]:25/',
                   '{"fragment": null, \
                     "hostParts": [null, 65535, 129, 144, 52, 38], \
                     "hostString": "::ffff:129.144.52.38", \
                     "hostType": "HDLmHostTypes.ipv6", \
                     "originalUrl": "https://[::FFFF:129.144.52.38]:25/", \
                     "pathParts": [], \
                     "pathString": "/", \
                     "portNumber": 25, \
                     "queryParts": null, \
                     "queryString": null, \
                     "scheme": "https", \
                     "userInfo": null}',
                   '' ],
                 [ 'https://::FFFF:129.144.52.38/',
                   '{"fragment": null, \
                     "hostParts": [null, 65535, 129, 144, 52, 38], \
                     "hostString": "::ffff:129.144.52.38", \
                     "hostType": "HDLmHostTypes.ipv6", \
                     "originalUrl": "https://::FFFF:129.144.52.38/", \
                     "pathParts": [], \
                     "pathString": "/", \
                     "portNumber": null, \
                     "queryParts": null, \
                     "queryString": null, \
                     "scheme": "https", \
                     "userInfo": null}',
                   '' ],
                 [ 'https://[2010:836B:4179::836B:4179]:25/a/b//c/d?x123=123y;x456=aabb',
                   '{"fragment": null, \
                     "hostParts": [8208, 33643, 16761, null, 33643, 16761], \
                     "hostString": "2010:836b:4179::836b:4179", \
                     "hostType": "HDLmHostTypes.ipv6", \
                     "originalUrl": "https://[2010:836B:4179::836B:4179]:25/a/b//c/d?x123=123y;x456=aabb", \
                     "pathParts": ["a", "b", "", "c", "d"], \
                     "pathString": "/a/b//c/d", \
                     "portNumber": 25, \
                     "queryParts": {"x123": "123y", "x456": "aabb"}, \
                     "queryString": "x123=123y;x456=aabb", \
                     "scheme": "https", \
                     "userInfo": null}',
                   '' ],
                 [ 'https://[2010:836B:4179::836B:4179]:25/a/b//c/d?x123=123y&x456=aabb',
                   '{"fragment": null, \
                     "hostParts": [8208, 33643, 16761, null, 33643, 16761], \
                     "hostString": "2010:836b:4179::836b:4179", \
                     "hostType": "HDLmHostTypes.ipv6", \
                     "originalUrl": "https://[2010:836B:4179::836B:4179]:25/a/b//c/d?x123=123y&x456=aabb", \
                     "pathParts": ["a", "b", "", "c", "d"], \
                     "pathString": "/a/b//c/d", \
                     "portNumber": 25, \
                     "queryParts": {"x123": "123y", "x456": "aabb"}, \
                     "queryString": "x123=123y&x456=aabb", \
                     "scheme": "https", \
                     "userInfo": null}',
                   '' ],
                 [ 'https://[2010:836B:4179::836B:4179]:25/a/b//c/d/?x123=123y&x456=aabb',
                   '{"fragment": null, \
                     "hostParts": [8208, 33643, 16761, null, 33643, 16761], \
                     "hostString": "2010:836b:4179::836b:4179", \
                     "hostType": "HDLmHostTypes.ipv6", \
                     "originalUrl": "https://[2010:836B:4179::836B:4179]:25/a/b//c/d/?x123=123y&x456=aabb", \
                     "pathParts": ["a", "b", "", "c", "d"], \
                     "pathString": "/a/b//c/d/", \
                     "portNumber": 25, \
                     "queryParts": {"x123": "123y", "x456": "aabb"}, \
                     "queryString": "x123=123y&x456=aabb", \
                     "scheme": "https", \
                     "userInfo": null}',
                   '' ],
                 [ 'https://[2010:836B:4179::836B:4179]:25/a/b//?x123=123y&x456=aabb',
                   '{"fragment": null, \
                     "hostParts": [8208, 33643, 16761, null, 33643, 16761], \
                     "hostString": "2010:836b:4179::836b:4179", \
                     "hostType": "HDLmHostTypes.ipv6", \
                     "originalUrl": "https://[2010:836B:4179::836B:4179]:25/a/b//?x123=123y&x456=aabb", \
                     "pathParts": ["a", "b", ""], \
                     "pathString": "/a/b//", \
                     "portNumber": 25, \
                     "queryParts": {"x123": "123y", "x456": "aabb"}, \
                     "queryString": "x123=123y&x456=aabb", \
                     "scheme": "https", \
                     "userInfo": null}',
                   '' ],
                 [ 'https://[2010:836B:4179::836B:4179]:25/a//b//?x123=123y&x456=aabb',
                   '{"fragment": null, \
                     "hostParts": [8208, 33643, 16761, null, 33643, 16761], \
                     "hostString": "2010:836b:4179::836b:4179", \
                     "hostType": "HDLmHostTypes.ipv6", \
                     "originalUrl": "https://[2010:836B:4179::836B:4179]:25/a//b//?x123=123y&x456=aabb", \
                     "pathParts": ["a", "", "b", ""], \
                     "pathString": "/a//b//", \
                     "portNumber": 25, \
                     "queryParts": {"x123": "123y", "x456": "aabb"}, \
                     "queryString": "x123=123y&x456=aabb", \
                     "scheme": "https", \
                     "userInfo": null}',
                   '' ],
                 [ 'https://[2010:836B:4179::836B:4179]:25/a//b//?x123=123y&x456=aabb',
                   '{"fragment": null, \
                     "hostParts": [8208, 33643, 16761, null, 33643, 16761], \
                     "hostString": "2010:836b:4179::836b:4179", \
                     "hostType": "HDLmHostTypes.ipv6", \
                     "originalUrl": "https://[2010:836B:4179::836B:4179]:25/a//b//?x123=123y&x456=aabb", \
                     "pathParts": ["a", "", "b", ""], \
                     "pathString": "/a//b//", \
                     "portNumber": 25, \
                     "queryParts": {"x123": "123y", "x456": "aabb"}, \
                     "queryString": "x123=123y&x456=aabb", \
                     "scheme": "https", \
                     "userInfo": null}',
                   '' ],
                 [ 'https://[2011:836B:4179::836B:4179]:25/a//b//?x123=123y&x456=aabb',
                   '{"fragment": null, \
                     "hostParts": [8209, 33643, 16761, null, 33643, 16761], \
                     "hostString": "2011:836b:4179::836b:4179", \
                     "hostType": "HDLmHostTypes.ipv6", \
                     "originalUrl": "https://[2011:836B:4179::836B:4179]:25/a//b//?x123=123y&x456=aabb", \
                     "pathParts": ["a", "", "b", ""], \
                     "pathString": "/a//b//", \
                     "portNumber": 25, \
                     "queryParts": {"x123": "123y", "x456": "aabb"}, \
                     "queryString": "x123=123y&x456=aabb", \
                     "scheme": "https", \
                     "userInfo": null}',
                   '' ],
                 [ 'https://2010:836B:4179::836B:4179/a/b//c/d?x123=123y;x456=aabb',
                   '{"fragment": null, \
                     "hostParts": [8208, 33643, 16761, null, 33643, 16761], \
                     "hostString": "2010:836b:4179::836b:4179", \
                     "hostType": "HDLmHostTypes.ipv6", \
                     "originalUrl": "https://2010:836B:4179::836B:4179/a/b//c/d?x123=123y;x456=aabb", \
                     "pathParts": ["a", "b", "", "c", "d"], \
                     "pathString": "/a/b//c/d", \
                     "portNumber": null, \
                     "queryParts": {"x123": "123y", "x456": "aabb"}, \
                     "queryString": "x123=123y;x456=aabb", \
                     "scheme": "https", \
                     "userInfo": null}',
                   '' ],
                 [ 'https://2010:836B:4179::836B:4179/a/b//c/d?x123=123y&x456=aabb',
                   '{"fragment": null, \
                     "hostParts": [8208, 33643, 16761, null, 33643, 16761], \
                     "hostString": "2010:836b:4179::836b:4179", \
                     "hostType": "HDLmHostTypes.ipv6", \
                     "originalUrl": "https://2010:836B:4179::836B:4179/a/b//c/d?x123=123y&x456=aabb", \
                     "pathParts": ["a", "b", "", "c", "d"], \
                     "pathString": "/a/b//c/d", \
                     "portNumber": null, \
                     "queryParts": {"x123": "123y", "x456": "aabb"}, \
                     "queryString": "x123=123y&x456=aabb", \
                     "scheme": "https", \
                     "userInfo": null}',
                   '' ],
                 [ 'https://2010:836B:4179::836B:4179/a/b//c/d/?x123=123y&x456=aabb',
                   '{"fragment": null, \
                     "hostParts": [8208, 33643, 16761, null, 33643, 16761], \
                     "hostString": "2010:836b:4179::836b:4179", \
                     "hostType": "HDLmHostTypes.ipv6", \
                     "originalUrl": "https://2010:836B:4179::836B:4179/a/b//c/d/?x123=123y&x456=aabb", \
                     "pathParts": ["a", "b", "", "c", "d"], \
                     "pathString": "/a/b//c/d/", \
                     "portNumber": null, \
                     "queryParts": {"x123": "123y", "x456": "aabb"}, \
                     "queryString": "x123=123y&x456=aabb", \
                     "scheme": "https", \
                     "userInfo": null}',
                   '' ],
                 [ 'https://2010:836B:4179::836B:4179/a/b//?x123=123y&x456=aabb',
                   '{"fragment": null, \
                     "hostParts": [8208, 33643, 16761, null, 33643, 16761], \
                     "hostString": "2010:836b:4179::836b:4179", \
                     "hostType": "HDLmHostTypes.ipv6", \
                     "originalUrl": "https://2010:836B:4179::836B:4179/a/b//?x123=123y&x456=aabb", \
                     "pathParts": ["a", "b", ""], \
                     "pathString": "/a/b//", \
                     "portNumber": null, \
                     "queryParts": {"x123": "123y", "x456": "aabb"}, \
                     "queryString": "x123=123y&x456=aabb", \
                     "scheme": "https", \
                     "userInfo": null}',
                   '' ],
                 [ 'https://2010:836B:4179::836B:4179/a//b//?x123=123y&x456=aabb',
                   '{"fragment": null, \
                     "hostParts": [8208, 33643, 16761, null, 33643, 16761], \
                     "hostString": "2010:836b:4179::836b:4179", \
                     "hostType": "HDLmHostTypes.ipv6", \
                     "originalUrl": "https://2010:836B:4179::836B:4179/a//b//?x123=123y&x456=aabb", \
                     "pathParts": ["a", "", "b", ""], \
                     "pathString": "/a//b//", \
                     "portNumber": null, \
                     "queryParts": {"x123": "123y", "x456": "aabb"}, \
                     "queryString": "x123=123y&x456=aabb", \
                     "scheme": "https", \
                     "userInfo": null}',
                   '' ],
                 [ 'https://2010:836B:4179::836B:4179/a//b//?x123=123y&x456=aabb',
                   '{"fragment": null, \
                     "hostParts": [8208, 33643, 16761, null, 33643, 16761], \
                     "hostString": "2010:836b:4179::836b:4179", \
                     "hostType": "HDLmHostTypes.ipv6", \
                     "originalUrl": "https://2010:836B:4179::836B:4179/a//b//?x123=123y&x456=aabb", \
                     "pathParts": ["a", "", "b", ""], \
                     "pathString": "/a//b//", \
                     "portNumber": null, \
                     "queryParts": {"x123": "123y", "x456": "aabb"}, \
                     "queryString": "x123=123y&x456=aabb", \
                     "scheme": "https", \
                     "userInfo": null}',
                   '' ],
                 [ 'https://2011:836B:4179::836B:4179/a//b//?x123=123y&x456=aabb',
                   '{"fragment": null, \
                     "hostParts": [8209, 33643, 16761, null, 33643, 16761], \
                     "hostString": "2011:836b:4179::836b:4179", \
                     "hostType": "HDLmHostTypes.ipv6", \
                     "originalUrl": "https://2011:836B:4179::836B:4179/a//b//?x123=123y&x456=aabb", \
                     "pathParts": ["a", "", "b", ""], \
                     "pathString": "/a//b//", \
                     "portNumber": null, \
                     "queryParts": {"x123": "123y", "x456": "aabb"}, \
                     "queryString": "x123=123y&x456=aabb", \
                     "scheme": "https", \
                     "userInfo": null}',
                   '' ],
                 [ 'https://192.168.1.1:25/a//b//?x123=123y&x456=aabb',
                   '{"fragment": null, \
                     "hostParts": [192, 168, 1, 1], \
                     "hostString": "192.168.1.1", \
                     "hostType": "HDLmHostTypes.ipv4", \
                     "originalUrl": "https://192.168.1.1:25/a//b//?x123=123y&x456=aabb", \
                     "pathParts": ["a", "", "b", ""], \
                     "pathString": "/a//b//", \
                     "portNumber": 25, \
                     "queryParts": {"x123": "123y", "x456": "aabb"}, \
                     "queryString": "x123=123y&x456=aabb", \
                     "scheme": "https", \
                     "userInfo": null}',
                   '' ],
                 [ 'https://[::ffff]:25/a//b//?x123=123y&x456=aabb',
                   '{"fragment": null, \
                     "hostParts": [null, 65535], \
                     "hostString": "::ffff", \
                     "hostType": "HDLmHostTypes.ipv6", \
                     "originalUrl": "https://[::ffff]:25/a//b//?x123=123y&x456=aabb", \
                     "pathParts": ["a", "", "b", ""], \
                     "pathString": "/a//b//", \
                     "portNumber": 25, \
                     "queryParts": {"x123": "123y", "x456": "aabb"}, \
                     "queryString": "x123=123y&x456=aabb", \
                     "scheme": "https", \
                     "userInfo": null}',
                   '' ],
                 [ 'https://[::]:25/a//b//?x123=123y&x456=aabb',
                   '{"fragment": null, \
                     "hostParts": [null], \
                     "hostString": "::", \
                     "hostType": "HDLmHostTypes.ipv6", \
                     "originalUrl": "https://[::]:25/a//b//?x123=123y&x456=aabb", \
                     "pathParts": ["a", "", "b", ""], \
                     "pathString": "/a//b//", \
                     "portNumber": 25, \
                     "queryParts": {"x123": "123y", "x456": "aabb"}, \
                     "queryString": "x123=123y&x456=aabb", \
                     "scheme": "https", \
                     "userInfo": null}',
                   '' ],
                 [ 'https://[ffff]:25/a//b//?x123=123y&x456=aabb',
                   '{"fragment": null, \
                     "hostParts": [65535], \
                     "hostString": "ffff", \
                     "hostType": "HDLmHostTypes.ipv6", \
                     "originalUrl": "https://[ffff]:25/a//b//?x123=123y&x456=aabb", \
                     "pathParts": ["a", "", "b", ""], \
                     "pathString": "/a//b//", \
                     "portNumber": 25, \
                     "queryParts": {"x123": "123y", "x456": "aabb"}, \
                     "queryString": "x123=123y&x456=aabb", \
                     "scheme": "https", \
                     "userInfo": null}',
                   '' ],
                 [ 'https://[ffff:ffff]:25/a//b//?x123=123y&x456=aabb',
                   '{"fragment": null, \
                     "hostParts": [65535, 65535], \
                     "hostString": "ffff:ffff", \
                     "hostType": "HDLmHostTypes.ipv6", \
                     "originalUrl": "https://[ffff:ffff]:25/a//b//?x123=123y&x456=aabb", \
                     "pathParts": ["a", "", "b", ""], \
                     "pathString": "/a//b//", \
                     "portNumber": 25, \
                     "queryParts": {"x123": "123y", "x456": "aabb"}, \
                     "queryString": "x123=123y&x456=aabb", \
                     "scheme": "https", \
                     "userInfo": null}',
                   '' ],
                 [ 'https://[ffff::ffff]:25/a//b//?x123=123y&x456=aabb',
                   '{"fragment": null, \
                     "hostParts": [65535, null, 65535], \
                     "hostString": "ffff::ffff", \
                     "hostType": "HDLmHostTypes.ipv6", \
                     "originalUrl": "https://[ffff::ffff]:25/a//b//?x123=123y&x456=aabb", \
                     "pathParts": ["a", "", "b", ""], \
                     "pathString": "/a//b//", \
                     "portNumber": 25, \
                     "queryParts": {"x123": "123y", "x456": "aabb"}, \
                     "queryString": "x123=123y&x456=aabb", \
                     "scheme": "https", \
                     "userInfo": null}',
                   '' ],
                 [ 'https://[ffff::]:25/a//b//?x123=123y&x456=aabb',
                   '{"fragment": null, \
                     "hostParts": [65535, null], \
                     "hostString": "ffff::", \
                     "hostType": "HDLmHostTypes.ipv6", \
                     "originalUrl": "https://[ffff::]:25/a//b//?x123=123y&x456=aabb", \
                     "pathParts": ["a", "", "b", ""], \
                     "pathString": "/a//b//", \
                     "portNumber": 25, \
                     "queryParts": {"x123": "123y", "x456": "aabb"}, \
                     "queryString": "x123=123y&x456=aabb", \
                     "scheme": "https", \
                     "userInfo": null}',
                   '' ],
                 [ 'https://[00ff::]:25/a//b//?x123=123y&x456=aabb',
                   '{"fragment": null, \
                     "hostParts": [255, null], \
                     "hostString": "00ff::", \
                     "hostType": "HDLmHostTypes.ipv6", \
                     "originalUrl": "https://[00ff::]:25/a//b//?x123=123y&x456=aabb", \
                     "pathParts": ["a", "", "b", ""], \
                     "pathString": "/a//b//", \
                     "portNumber": 25, \
                     "queryParts": {"x123": "123y", "x456": "aabb"}, \
                     "queryString": "x123=123y&x456=aabb", \
                     "scheme": "https", \
                     "userInfo": null}',
                   '' ],
                 [ 'https://::ffff/a//b//?x123=123y&x456=aabb',
                   '{"fragment": null, \
                     "hostParts": [null, 65535], \
                     "hostString": "::ffff", \
                     "hostType": "HDLmHostTypes.ipv6", \
                     "originalUrl": "https://::ffff/a//b//?x123=123y&x456=aabb", \
                     "pathParts": ["a", "", "b", ""], \
                     "pathString": "/a//b//", \
                     "portNumber": null, \
                     "queryParts": {"x123": "123y", "x456": "aabb"}, \
                     "queryString": "x123=123y&x456=aabb", \
                     "scheme": "https", \
                     "userInfo": null}',
                   '' ],
                 [ 'https://::/a//b//?x123=123y&x456=aabb',
                   '{"fragment": null, \
                     "hostParts": [null], \
                     "hostString": "::", \
                     "hostType": "HDLmHostTypes.ipv6", \
                     "originalUrl": "https://::/a//b//?x123=123y&x456=aabb", \
                     "pathParts": ["a", "", "b", ""], \
                     "pathString": "/a//b//", \
                     "portNumber": null, \
                     "queryParts": {"x123": "123y", "x456": "aabb"}, \
                     "queryString": "x123=123y&x456=aabb", \
                     "scheme": "https", \
                     "userInfo": null}',
                   '' ],
                 [ 'https://ffff/a//b//?x123=123y&x456=aabb',
                   '{"fragment": null, \
                     "hostParts": ["ffff"], \
                     "hostString": "ffff", \
                     "hostType": "HDLmHostTypes.standard", \
                     "originalUrl": "https://ffff/a//b//?x123=123y&x456=aabb", \
                     "pathParts": ["a", "", "b", ""], \
                     "pathString": "/a//b//", \
                     "portNumber": null, \
                     "queryParts": {"x123": "123y", "x456": "aabb"}, \
                     "queryString": "x123=123y&x456=aabb", \
                     "scheme": "https", \
                     "userInfo": null}',
                   '' ],
                 [ 'https://ffff:ffff/a//b//?x123=123y&x456=aabb',
                   '{"fragment": null, \
                     "hostParts": [65535, 65535], \
                     "hostString": "ffff:ffff", \
                     "hostType": "HDLmHostTypes.ipv6", \
                     "originalUrl": "https://ffff:ffff/a//b//?x123=123y&x456=aabb", \
                     "pathParts": ["a", "", "b", ""], \
                     "pathString": "/a//b//", \
                     "portNumber": null, \
                     "queryParts": {"x123": "123y", "x456": "aabb"}, \
                     "queryString": "x123=123y&x456=aabb", \
                     "scheme": "https", \
                     "userInfo": null}',
                   '' ],
                 [ 'https://ffff::ffff/a//b//?x123=123y&x456=aabb',
                   '{"fragment": null, \
                     "hostParts": [65535, null, 65535], \
                     "hostString": "ffff::ffff", \
                     "hostType": "HDLmHostTypes.ipv6", \
                     "originalUrl": "https://ffff::ffff/a//b//?x123=123y&x456=aabb", \
                     "pathParts": ["a", "", "b", ""], \
                     "pathString": "/a//b//", \
                     "portNumber": null, \
                     "queryParts": {"x123": "123y", "x456": "aabb"}, \
                     "queryString": "x123=123y&x456=aabb", \
                     "scheme": "https", \
                     "userInfo": null}',
                   '' ],
                 [ 'https://ffff::/a//b//?x123=123y&x456=aabb',
                   '{"fragment": null, \
                     "hostParts": [65535, null], \
                     "hostString": "ffff::", \
                     "hostType": "HDLmHostTypes.ipv6", \
                     "originalUrl": "https://ffff::/a//b//?x123=123y&x456=aabb", \
                     "pathParts": ["a", "", "b", ""], \
                     "pathString": "/a//b//", \
                     "portNumber": null, \
                     "queryParts": {"x123": "123y", "x456": "aabb"}, \
                     "queryString": "x123=123y&x456=aabb", \
                     "scheme": "https", \
                     "userInfo": null}',
                   '' ],
                 [ 'https://00ff::/a//b//?x123=123y&x456=aabb',
                   '{"fragment": null, \
                     "hostParts": [255, null], \
                     "hostString": "00ff::", \
                     "hostType": "HDLmHostTypes.ipv6", \
                     "originalUrl": "https://00ff::/a//b//?x123=123y&x456=aabb", \
                     "pathParts": ["a", "", "b", ""], \
                     "pathString": "/a//b//", \
                     "portNumber": null, \
                     "queryParts": {"x123": "123y", "x456": "aabb"}, \
                     "queryString": "x123=123y&x456=aabb", \
                     "scheme": "https", \
                     "userInfo": null}',
                   '' ],
                 [ 'https://192.168.1.1:25/a//b//?x123=123y&x456=aabb',
                   '{"fragment": null, \
                     "hostParts": [192, 168, 1, 1], \
                     "hostString": "192.168.1.1", \
                     "hostType": "HDLmHostTypes.ipv4", \
                     "originalUrl": "https://192.168.1.1:25/a//b//?x123=123y&x456=aabb", \
                     "pathParts": ["a", "", "b", ""], \
                     "pathString": "/a//b//", \
                     "portNumber": 25, \
                     "queryParts": {"x123": "123y", "x456": "aabb"}, \
                     "queryString": "x123=123y&x456=aabb", \
                     "scheme": "https", \
                     "userInfo": null}',
                   '' ],
                 [ 'https://[::192.168.1.1]:25/a//b//?x123=123y&x456=aabb',
                   '{"fragment": null, \
                     "hostParts": [null, 192, 168, 1, 1], \
                     "hostString": "::192.168.1.1", \
                     "hostType": "HDLmHostTypes.ipv6", \
                     "originalUrl": "https://[::192.168.1.1]:25/a//b//?x123=123y&x456=aabb", \
                     "pathParts": ["a", "", "b", ""], \
                     "pathString": "/a//b//", \
                     "portNumber": 25, \
                     "queryParts": {"x123": "123y", "x456": "aabb"}, \
                     "queryString": "x123=123y&x456=aabb", \
                     "scheme": "https", \
                     "userInfo": null}',
                   '' ],
                 [ 'https://[f:f]:25/a//b//?x123=123y&x456=aabb',
                   '{"fragment": null, \
                     "hostParts": [15, 15], \
                     "hostString": "f:f", \
                     "hostType": "HDLmHostTypes.ipv6", \
                     "originalUrl": "https://[f:f]:25/a//b//?x123=123y&x456=aabb", \
                     "pathParts": ["a", "", "b", ""], \
                     "pathString": "/a//b//", \
                     "portNumber": 25, \
                     "queryParts": {"x123": "123y", "x456": "aabb"}, \
                     "queryString": "x123=123y&x456=aabb", \
                     "scheme": "https", \
                     "userInfo": null}',
                   '' ],
                 [ 'https://[f:f:f:f:f:f:f:f]:25/a//b//?x123=123y&x456=aabb',
                   '{"fragment": null, \
                     "hostParts": [15, 15, 15, 15, 15, 15, 15, 15], \
                     "hostString": "f:f:f:f:f:f:f:f", \
                     "hostType": "HDLmHostTypes.ipv6", \
                     "originalUrl": "https://[f:f:f:f:f:f:f:f]:25/a//b//?x123=123y&x456=aabb", \
                     "pathParts": ["a", "", "b", ""], \
                     "pathString": "/a//b//", \
                     "portNumber": 25, \
                     "queryParts": {"x123": "123y", "x456": "aabb"}, \
                     "queryString": "x123=123y&x456=aabb", \
                     "scheme": "https", \
                     "userInfo": null}',
                   '' ],
                 [ 'https://[f:f:f::f:f:f:f]:25/a//b//?x123=123y&x456=aabb',
                   '{"fragment": null, \
                     "hostParts": [15, 15, 15, null, 15, 15, 15, 15], \
                     "hostString": "f:f:f::f:f:f:f", \
                     "hostType": "HDLmHostTypes.ipv6", \
                     "originalUrl": "https://[f:f:f::f:f:f:f]:25/a//b//?x123=123y&x456=aabb", \
                     "pathParts": ["a", "", "b", ""], \
                     "pathString": "/a//b//", \
                     "portNumber": 25, \
                     "queryParts": {"x123": "123y", "x456": "aabb"}, \
                     "queryString": "x123=123y&x456=aabb", \
                     "scheme": "https", \
                     "userInfo": null}',
                   '' ],
                 [ 'https://::192.168.1.1/a//b//?x123=123y&x456=aabb',
                   '{"fragment": null, \
                     "hostParts": [null, 192, 168, 1, 1], \
                     "hostString": "::192.168.1.1", \
                     "hostType": "HDLmHostTypes.ipv6", \
                     "originalUrl": "https://::192.168.1.1/a//b//?x123=123y&x456=aabb", \
                     "pathParts": ["a", "", "b", ""], \
                     "pathString": "/a//b//", \
                     "portNumber": null, \
                     "queryParts": {"x123": "123y", "x456": "aabb"}, \
                     "queryString": "x123=123y&x456=aabb", \
                     "scheme": "https", \
                     "userInfo": null}',
                   '' ],
                 [ 'https://f:f/a//b//?x123=123y&x456=aabb',
                   '{"fragment": null, \
                     "hostParts": [15, 15], \
                     "hostString": "f:f", \
                     "hostType": "HDLmHostTypes.ipv6", \
                     "originalUrl": "https://f:f/a//b//?x123=123y&x456=aabb", \
                     "pathParts": ["a", "", "b", ""], \
                     "pathString": "/a//b//", \
                     "portNumber": null, \
                     "queryParts": {"x123": "123y", "x456": "aabb"}, \
                     "queryString": "x123=123y&x456=aabb", \
                     "scheme": "https", \
                     "userInfo": null}',
                   '' ],
                 [ 'https://f:f:f:f:f:f:f:f/a//b//?x123=123y&x456=aabb',
                   '{"fragment": null, \
                     "hostParts": [15, 15, 15, 15, 15, 15, 15, 15], \
                     "hostString": "f:f:f:f:f:f:f:f", \
                     "hostType": "HDLmHostTypes.ipv6", \
                     "originalUrl": "https://f:f:f:f:f:f:f:f/a//b//?x123=123y&x456=aabb", \
                     "pathParts": ["a", "", "b", ""], \
                     "pathString": "/a//b//", \
                     "portNumber": null, \
                     "queryParts": {"x123": "123y", "x456": "aabb"}, \
                     "queryString": "x123=123y&x456=aabb", \
                     "scheme": "https", \
                     "userInfo": null}',
                   '' ],
                 [ 'https://f:f:f::f:f:f:f/a//b//?x123=123y&x456=aabb',
                   '{"fragment": null, \
                     "hostParts": [15, 15, 15, null, 15, 15, 15, 15], \
                     "hostString": "f:f:f::f:f:f:f", \
                     "hostType": "HDLmHostTypes.ipv6", \
                     "originalUrl": "https://f:f:f::f:f:f:f/a//b//?x123=123y&x456=aabb", \
                     "pathParts": ["a", "", "b", ""], \
                     "pathString": "/a//b//", \
                     "portNumber": null, \
                     "queryParts": {"x123": "123y", "x456": "aabb"}, \
                     "queryString": "x123=123y&x456=aabb", \
                     "scheme": "https", \
                     "userInfo": null}',
                   '' ],
                 [ 'https://a:25/a//b//?x123=123y&x456=aabb',
                   '{"fragment": null, \
                     "hostParts": ["a"], \
                     "hostString": "a", \
                     "hostType": "HDLmHostTypes.standard", \
                     "originalUrl": "https://a:25/a//b//?x123=123y&x456=aabb", \
                     "pathParts": ["a", "", "b", ""], \
                     "pathString": "/a//b//", \
                     "portNumber": 25, \
                     "queryParts": {"x123": "123y", "x456": "aabb"}, \
                     "queryString": "x123=123y&x456=aabb", \
                     "scheme": "https", \
                     "userInfo": null}',
                   '' ],
                 [ 'https://x1:25/a//b//?x123=123y&x456=aabb',
                   '{"fragment": null, \
                     "hostParts": ["x1"], \
                     "hostString": "x1", \
                     "hostType": "HDLmHostTypes.standard", \
                     "originalUrl": "https://x1:25/a//b//?x123=123y&x456=aabb", \
                     "pathParts": ["a", "", "b", ""], \
                     "pathString": "/a//b//", \
                     "portNumber": 25, \
                     "queryParts": {"x123": "123y", "x456": "aabb"}, \
                     "queryString": "x123=123y&x456=aabb", \
                     "scheme": "https", \
                     "userInfo": null}',
                   '' ],
                 [ 'https://x1.x2:25/a//b//?x123=123y&x456=aabb',
                   '{"fragment": null, \
                     "hostParts": ["x1", "x2"], \
                     "hostString": "x1.x2", \
                     "hostType": "HDLmHostTypes.standard", \
                     "originalUrl": "https://x1.x2:25/a//b//?x123=123y&x456=aabb", \
                     "pathParts": ["a", "", "b", ""], \
                     "pathString": "/a//b//", \
                     "portNumber": 25, \
                     "queryParts": {"x123": "123y", "x456": "aabb"}, \
                     "queryString": "x123=123y&x456=aabb", \
                     "scheme": "https", \
                     "userInfo": null}',
                   '' ],
                 [ 'https://x1.x2.x3:25/a//b//?x123=123y&x456=aabb',
                   '{"fragment": null, \
                     "hostParts": ["x1", "x2", "x3"], \
                     "hostString": "x1.x2.x3", \
                     "hostType": "HDLmHostTypes.standard", \
                     "originalUrl": "https://x1.x2.x3:25/a//b//?x123=123y&x456=aabb", \
                     "pathParts": ["a", "", "b", ""], \
                     "pathString": "/a//b//", \
                     "portNumber": 25, \
                     "queryParts": {"x123": "123y", "x456": "aabb"}, \
                     "queryString": "x123=123y&x456=aabb", \
                     "scheme": "https", \
                     "userInfo": null}',
                   '' ],
                 [ 'https://x1.x2.x3:25',
                   '{"fragment": null, \
                     "hostParts": ["x1", "x2", "x3"], \
                     "hostString": "x1.x2.x3", \
                     "hostType": "HDLmHostTypes.standard", \
                     "originalUrl": "https://x1.x2.x3:25", \
                     "pathParts": [], \
                     "pathString": "", \
                     "portNumber": 25, \
                     "queryParts": null, \
                     "queryString": null, \
                     "scheme": "https", \
                     "userInfo": null}',
                   '' ],
                 [ 'https://x1.x2.x3:25/',
                   '{"fragment": null, \
                     "hostParts": ["x1", "x2", "x3"], \
                     "hostString": "x1.x2.x3", \
                     "hostType": "HDLmHostTypes.standard", \
                     "originalUrl": "https://x1.x2.x3:25/", \
                     "pathParts": [], \
                     "pathString": "/", \
                     "portNumber": 25, \
                     "queryParts": null, \
                     "queryString": null, \
                     "scheme": "https", \
                     "userInfo": null}',
                   '' ],
                 [ 'https://x1.x2.x3:25/a',
                   '{"fragment": null, \
                     "hostParts": ["x1", "x2", "x3"], \
                     "hostString": "x1.x2.x3", \
                     "hostType": "HDLmHostTypes.standard", \
                     "originalUrl": "https://x1.x2.x3:25/a", \
                     "pathParts": ["a"], \
                     "pathString": "/a", \
                     "portNumber": 25, \
                     "queryParts": null, \
                     "queryString": null, \
                     "scheme": "https", \
                     "userInfo": null}',
                   '' ],
                 [ 'https://x1.x2.x3:25/a/',
                   '{"fragment": null, \
                     "hostParts": ["x1", "x2", "x3"], \
                     "hostString": "x1.x2.x3", \
                     "hostType": "HDLmHostTypes.standard", \
                     "originalUrl": "https://x1.x2.x3:25/a/", \
                     "pathParts": ["a"], \
                     "pathString": "/a/", \
                     "portNumber": 25, \
                     "queryParts": null, \
                     "queryString": null, \
                     "scheme": "https", \
                     "userInfo": null}',
                   '' ],
                 [ 'https://x1.x2.x3:25/a/b',
                   '{"fragment": null, \
                     "hostParts": ["x1", "x2", "x3"], \
                     "hostString": "x1.x2.x3", \
                     "hostType": "HDLmHostTypes.standard", \
                     "originalUrl": "https://x1.x2.x3:25/a/b", \
                     "pathParts": ["a", "b"], \
                     "pathString": "/a/b", \
                     "portNumber": 25, \
                     "queryParts": null, \
                     "queryString": null, \
                     "scheme": "https", \
                     "userInfo": null}',
                   '' ],
                 [ 'https://x1.x2.x3:25/a/b/',
                   '{"fragment": null, \
                     "hostParts": ["x1", "x2", "x3"], \
                     "hostString": "x1.x2.x3", \
                     "hostType": "HDLmHostTypes.standard", \
                     "originalUrl": "https://x1.x2.x3:25/a/b/", \
                     "pathParts": ["a", "b"], \
                     "pathString": "/a/b/", \
                     "portNumber": 25, \
                     "queryParts": null, \
                     "queryString": null, \
                     "scheme": "https", \
                     "userInfo": null}',
                   '' ],
                 [ 'https://x1.x2.x3:25/a/b/?x123=123y&x456=aabb',
                   '{"fragment": null, \
                     "hostParts": ["x1", "x2", "x3"], \
                     "hostString": "x1.x2.x3", \
                     "hostType": "HDLmHostTypes.standard", \
                     "originalUrl": "https://x1.x2.x3:25/a/b/?x123=123y&x456=aabb", \
                     "pathParts": ["a", "b"], \
                     "pathString": "/a/b/", \
                     "portNumber": 25, \
                     "queryParts": {"x123": "123y", "x456": "aabb"}, \
                     "queryString": "x123=123y&x456=aabb", \
                     "scheme": "https", \
                     "userInfo": null}',
                   '' ],
                 [ 'https://x1.x2.x3:25/a/b?x123=123y&x456=aabb',
                   '{"fragment": null, \
                     "hostParts": ["x1", "x2", "x3"], \
                     "hostString": "x1.x2.x3", \
                     "hostType": "HDLmHostTypes.standard", \
                     "originalUrl": "https://x1.x2.x3:25/a/b?x123=123y&x456=aabb", \
                     "pathParts": ["a", "b"], \
                     "pathString": "/a/b", \
                     "portNumber": 25, \
                     "queryParts": {"x123": "123y", "x456": "aabb"}, \
                     "queryString": "x123=123y&x456=aabb", \
                     "scheme": "https", \
                     "userInfo": null}',
                   '' ],
                 [ 'https://x1.x2.x3:25/a?x123=123y&x456=aabb',
                   '{"fragment": null, \
                     "hostParts": ["x1", "x2", "x3"], \
                     "hostString": "x1.x2.x3", \
                     "hostType": "HDLmHostTypes.standard", \
                     "originalUrl": "https://x1.x2.x3:25/a?x123=123y&x456=aabb", \
                     "pathParts": ["a"], \
                     "pathString": "/a", \
                     "portNumber": 25, \
                     "queryParts": {"x123": "123y", "x456": "aabb"}, \
                     "queryString": "x123=123y&x456=aabb", \
                     "scheme": "https", \
                     "userInfo": null}',
                   '' ],
                 [ 'https://x1.x2.x3:25/?x123=123y&x456=aabb',
                   '{"fragment": null, \
                     "hostParts": ["x1", "x2", "x3"], \
                     "hostString": "x1.x2.x3", \
                     "hostType": "HDLmHostTypes.standard", \
                     "originalUrl": "https://x1.x2.x3:25/?x123=123y&x456=aabb", \
                     "pathParts": [], \
                     "pathString": "/", \
                     "portNumber": 25, \
                     "queryParts": {"x123": "123y", "x456": "aabb"}, \
                     "queryString": "x123=123y&x456=aabb", \
                     "scheme": "https", \
                     "userInfo": null}',
                   '' ],
                 [ 'https://x1.x2.x3:25?x123=123y&x456=aabb',
                   '{"fragment": null, \
                     "hostParts": ["x1", "x2", "x3"], \
                     "hostString": "x1.x2.x3", \
                     "hostType": "HDLmHostTypes.standard", \
                     "originalUrl": "https://x1.x2.x3:25?x123=123y&x456=aabb", \
                     "pathParts": [], \
                     "pathString": "", \
                     "portNumber": 25, \
                     "queryParts": {"x123": "123y", "x456": "aabb"}, \
                     "queryString": "x123=123y&x456=aabb", \
                     "scheme": "https", \
                     "userInfo": null}',
                   '' ],
                 # This is the Chinese URL using punycode (http://例子.卷筒纸)
                 [ 'http://xn--fsqu00a.xn--3lr804guic/?x123=123y&x456=aabb',
                   '{"fragment": null, \
                     "hostParts": ["xn--fsqu00a", "xn--3lr804guic"], \
                     "hostString": "xn--fsqu00a.xn--3lr804guic", \
                     "hostType": "HDLmHostTypes.standard", \
                     "originalUrl": "http://xn--fsqu00a.xn--3lr804guic/?x123=123y&x456=aabb", \
                     "pathParts": [], \
                     "pathString": "/", \
                     "portNumber": null, \
                     "queryParts": {"x123": "123y", "x456": "aabb"}, \
                     "queryString": "x123=123y&x456=aabb", \
                     "scheme": "http", \
                     "userInfo": null}',
                   '' ],
                 # This is the Japanese URL (http://example.com/引き割り.html)
                 [ 'http://example.com/%E5%BC%95%E3%81%8D%E5%89%B2%E3%82%8A.html',
                   '{"fragment": null, \
                     "hostParts": ["example", "com"], \
                     "hostString": "example.com", \
                     "hostType": "HDLmHostTypes.standard", \
                     "originalUrl": "http://example.com/%E5%BC%95%E3%81%8D%E5%89%B2%E3%82%8A.html", \
                     "pathParts": ["引き割り.html"], \
                     "pathString": "/%E5%BC%95%E3%81%8D%E5%89%B2%E3%82%8A.html", \
                     "portNumber": null, \
                     "queryParts": null, \
                     "queryString": null, \
                     "scheme": "http", \
                     "userInfo": null}',
                   '' ],
                 [ 'http://[::]/',
                   '{"fragment": null, \
                     "hostParts": [null], \
                     "hostString": "::", \
                     "hostType": "HDLmHostTypes.ipv6", \
                     "originalUrl": "http://[::]/", \
                     "pathParts": [], \
                     "pathString": "/", \
                     "portNumber": null, \
                     "queryParts": null, \
                     "queryString": null, \
                     "scheme": "http", \
                     "userInfo": null}',
                   '' ],
                 [ 'http://[::]',
                   '{"fragment": null, \
                     "hostParts": [null], \
                     "hostString": "::", \
                     "hostType": "HDLmHostTypes.ipv6", \
                     "originalUrl": "http://[::]", \
                     "pathParts": [], \
                     "pathString": "", \
                     "portNumber": null, \
                     "queryParts": null, \
                     "queryString": null, \
                     "scheme": "http", \
                     "userInfo": null}',
                   '' ],
                 [ 'http://[::1]/',
                   '{"fragment": null, \
                     "hostParts": [null, 1], \
                     "hostString": "::1", \
                     "hostType": "HDLmHostTypes.ipv6", \
                     "originalUrl": "http://[::1]/", \
                     "pathParts": [], \
                     "pathString": "/", \
                     "portNumber": null, \
                     "queryParts": null, \
                     "queryString": null, \
                     "scheme": "http", \
                     "userInfo": null}',
                   '' ],
                 [ 'http://[::1]',
                   '{"fragment": null, \
                     "hostParts": [null, 1], \
                     "hostString": "::1", \
                     "hostType": "HDLmHostTypes.ipv6", \
                     "originalUrl": "http://[::1]", \
                     "pathParts": [], \
                     "pathString": "", \
                     "portNumber": null, \
                     "queryParts": null, \
                     "queryString": null, \
                     "scheme": "http", \
                     "userInfo": null}',
                   '' ],
                 [ 'http://[::1]#123',
                   '{"fragment": "123", \
                     "hostParts": [null, 1], \
                     "hostString": "::1", \
                     "hostType": "HDLmHostTypes.ipv6", \
                     "originalUrl": "http://[::1]#123", \
                     "pathParts": [], \
                     "pathString": "", \
                     "portNumber": null, \
                     "queryParts": null, \
                     "queryString": null, \
                     "scheme": "http", \
                     "userInfo": null}',
                   '' ],
                 [ 'http://::/',
                   '{"fragment": null, \
                     "hostParts": [null], \
                     "hostString": "::", \
                     "hostType": "HDLmHostTypes.ipv6", \
                     "originalUrl": "http://::/", \
                     "pathParts": [], \
                     "pathString": "/", \
                     "portNumber": null, \
                     "queryParts": null, \
                     "queryString": null, \
                     "scheme": "http", \
                     "userInfo": null}',
                   '' ],
                 [ 'http://::',
                   '{"fragment": null, \
                     "hostParts": [null], \
                     "hostString": "::", \
                     "hostType": "HDLmHostTypes.ipv6", \
                     "originalUrl": "http://::", \
                     "pathParts": [], \
                     "pathString": "", \
                     "portNumber": null, \
                     "queryParts": null, \
                     "queryString": null, \
                     "scheme": "http", \
                     "userInfo": null}',
                   '' ],
                 [ 'http://::1/',
                   '{"fragment": null, \
                     "hostParts": [null, 1], \
                     "hostString": "::1", \
                     "hostType": "HDLmHostTypes.ipv6", \
                     "originalUrl": "http://::1/", \
                     "pathParts": [], \
                     "pathString": "/", \
                     "portNumber": null, \
                     "queryParts": null, \
                     "queryString": null, \
                     "scheme": "http", \
                     "userInfo": null}',
                   '' ],
                 [ 'http://::1',
                   '{"fragment": null, \
                     "hostParts": [null, 1], \
                     "hostString": "::1", \
                     "hostType": "HDLmHostTypes.ipv6", \
                     "originalUrl": "http://::1", \
                     "pathParts": [], \
                     "pathString": "", \
                     "portNumber": null, \
                     "queryParts": null, \
                     "queryString": null, \
                     "scheme": "http", \
                     "userInfo": null}',
                   '' ],
                 [ 'http://::1#123',
                   '{"fragment": "123", \
                     "hostParts": [null, 1], \
                     "hostString": "::1", \
                     "hostType": "HDLmHostTypes.ipv6", \
                     "originalUrl": "http://::1#123", \
                     "pathParts": [], \
                     "pathString": "", \
                     "portNumber": null, \
                     "queryParts": null, \
                     "queryString": null, \
                     "scheme": "http", \
                     "userInfo": null}',
                   '' ],
                 [ '//x1.x2.x3:25/',
                   '{"fragment": null, \
                     "hostParts": ["x1", "x2", "x3"], \
                     "hostString": "x1.x2.x3", \
                     "hostType": "HDLmHostTypes.standard", \
                     "originalUrl": "//x1.x2.x3:25/", \
                     "pathParts": [], \
                     "pathString": "/", \
                     "portNumber": 25, \
                     "queryParts": null, \
                     "queryString": null, \
                     "scheme": null, \
                     "userInfo": null}',
                   '',
                   {"prUrlOk": True},
                 ],
                 [ '/',
                   '{"fragment": null, \
                     "hostParts": null, \
                     "hostString": null, \
                     "hostType": null, \
                     "originalUrl": "/", \
                     "pathParts": [], \
                     "pathString": "/", \
                     "portNumber": null, \
                     "queryParts": null, \
                     "queryString": null, \
                     "scheme": null, \
                     "userInfo": null}',
                   '',
                   {"prUrlOk": True, "relativeUrl": True},
                 ],
                 [ '/abc',
                   '{"fragment": null, \
                     "hostParts": null, \
                     "hostString": null, \
                     "hostType": null, \
                     "originalUrl": "/abc", \
                     "pathParts": ["abc"], \
                     "pathString": "/abc", \
                     "portNumber": null, \
                     "queryParts": null, \
                     "queryString": null, \
                     "scheme": null, \
                     "userInfo": null}',
                   '',
                   {"prUrlOk": True, "relativeUrl": True},
                 ],
                 [ '/abc/def',
                   '{"fragment": null, \
                     "hostParts": null, \
                     "hostString": null, \
                     "hostType": null, \
                     "originalUrl": "/abc/def", \
                     "pathParts": ["abc", "def"], \
                     "pathString": "/abc/def", \
                     "portNumber": null, \
                     "queryParts": null, \
                     "queryString": null, \
                     "scheme": null, \
                     "userInfo": null}',
                   '',
                   {"prUrlOk": True, "relativeUrl": True},
                 ],
                 # The error tests start here 
                 [ '/',
                   '',
                   'URL does not appear to contain a valid host name',
                   {"prUrlOk": True} ],
                 [ 'https://[:::]:25/',
                   '',
                   'IPv6 host name is not valid' ],
                 [ 'https://:::/',
                   '',
                   'IPv6 host name is not valid' ],
                 [ 'https://[2010:836B:4179::836B:4179]:25/a/b//c/d?x123=123y;x123=aabb',
                   '',
                   'URL query string is invalid' ],
                 [ 'https://2010:836B:4179::836B:4179/a/b//c/d?x123=123y;x123=aabb',
                   '',
                   'URL query string is invalid' ],
                 [ 'httpxyz://[2010:836B:4179::836B:4179]:25/a/b//c/d?x123=123y;x123=aabb',
                   '',
                   'Scheme value from the URL is not valid' ],
                 [ 'httpxyz://2010:836B:4179::836B:4179/a/b//c/d?x123=123y;x123=aabb',
                   '',
                   'Scheme value from the URL is not valid' ],
                 [ 'httpxyz//[2010:836B:4179::836B:4179]:25/a/b//c/d?x123=123y;x123=aabb',
                   '',
                   'Colon after URL scheme missing' ],
                 [ 'httpxyz//2010:836B:4179::836B:4179/a/b//c/d?x123=123y;x123=aabb',
                   '',
                   'Colon after URL scheme missing' ],
                 [ 'httpxyz',
                   '',
                   'URL does not appear to contain a valid scheme' ],
                 [ 'https:',
                   '',
                   'URL does not appear to contain a valid host name' ],
                 [ 'https:/',
                   '',
                   'URL does not appear to contain a valid host name' ],
                 [ 'https://',
                   '',
                   'Host name is missing from the URL' ],
                 [ 'https://[ffff',
                   '',
                   'Right square bracket not found the URL' ],
                 [ 'https://+ffff',
                   '',
                   'URL has an invalid host name value' ],
                 [ 'https://[ffff]:a',
                   '',
                   'URL port number is invalid or missing' ],
                 [ 'https://[ffff]:ab',
                   '',
                   'URL port number is invalid or missing' ],
                 [ 'https:///',
                   '',
                   'URL has an invalid host name value' ],
                 [ 'https://192.168 1.1/',
                   '',
                   'IPv4 host name is not valid' ],
                 [ 'https://[]/',
                   '',
                   'IPv6 host name is not valid' ],
                 [ 'https:///',
                   '',
                   'URL has an invalid host name value' ],
                 [ 'https://[ffff ffff]/',
                   '',
                   'IPv6 host name is not valid' ],
                 [ 'https://ffff ffff/',
                   '',
                   'Standard host name is not valid' ],
                 [ 'https://[fff+]/',
                   '',
                   'IPv6 host name is not valid' ],
                 [ 'https://fff+/',
                   '',
                   'URL has an invalid host name value' ],
                 [ 'https://[fffff]/',
                   '',
                   'IPv6 host name is not valid' ],
                 [ 'https://[fffg]/',
                   '',
                   'IPv6 host name is not valid' ],
                 [ 'https://[f:f:f:f:f:f:f:f:f]/',
                   '',
                   'IPv6 host name is not valid' ],
                 [ 'https://f:f:f:f:f:f:f:f:f/',
                   '',
                   'IPv6 host name is not valid' ],
                 [ 'https://f:f:f:f:f:f:f:f:f/',
                   '',
                   'IPv6 host name is not valid' ],
                 [ 'https://[f:f::f:f:f:f::f:f]/',
                   '',
                   'IPv6 host name is not valid' ],
                 [ 'https://f:f::f:f:f:f::f:f/',
                   '',
                   'IPv6 host name is not valid' ],
                 [ 'https://+/',
                   '',
                   'URL has an invalid host name value' ],
                 [ 'https://./',
                   '',
                   'URL has an invalid host name value' ],
                 [ 'https://a./',
                   '',
                   'Standard host name is not valid' ],
                 [ 'https://a..b/',
                   '',
                   'Standard host name is not valid' ],
                 [ 'https://-a.b/',
                   '',
                   'Standard host name is not valid' ],
                 [ 'https://a-.b/',
                   '',
                   'Standard host name is not valid' ],
                 # Domain names can only contain valid ASCII characters, 
                 # digits, and the hyphen (minus) character. The domain
                 # name below is not valid.
                 [ 'https://a.bÀ/',
                   '',
                   'Standard host name is not valid' ],
                 # Domain names can only contain valid ASCII characters, 
                 # digits, and the hyphen (minus) character. The domain
                 # name below is not valid.
                 [ 'https://a.bÀ/',
                   '',
                   'Standard host name is not valid' ],
                 [ 'https://x1.x2.x3:25?x123',
                   '',
                   'URL query string is invalid' ],
                 [ 'https://x1.x2.x3:25?x123&',
                   '',
                   'URL query string is invalid' ],
                 [ 'https://x1.x2.x3:25?=',
                   '',
                   'URL query string is invalid' ],
                 [ 'https://x1.x2.x3:25?x123=',
                   '',
                   'URL query string is invalid' ],
                 [ 'https://x1.x2.x3:25?x123==',
                   '',
                   'URL query string is invalid' ],
                 [ 'https://x1.x2.x3:25?x123=&',
                   '',
                   'URL query string is invalid' ],
                 [ 'https://x1.x2.x3:25?x123=x456&x123=x456',
                   '',
                   'URL query string is invalid' ],
                 [ 'https://x1.x2.x3:25?',
                   '',
                   'URL query string is invalid' ],
               ]
    # Get the count of the number of tests and run each test 
    tests = urlTests
    testCount = len(tests)
    for i in range(testCount): 
      # Get the current test
      curTest = tests[i]
      curTestLen = len(curTest)
      curInput = curTest[0]
      # Check if any additional keyword values were specified 
      curKeywords = dict()
      if curTestLen > 3:
        curKeywords = curTest[3]
      # Get the expected JSON output and convert it to a dictionary
      # if possible
      curExpectedOutputJson = curTest[1]
      # Convert the expected JSON output to a dictionary (if possible)
      if curExpectedOutputJson != '':
        curExpectedOutputDict = json.loads(curExpectedOutputJson)
        # We need to fix one of the entries in the dictionary. The entry is 
        # the host type. The host type must be an enum.
        enumType = 'hostType'
        enumStr = curExpectedOutputDict[enumType]
        # Convert the enum string to an enum value
        if enumStr != None:
          enumIndex = enumStr.find('.')
          enumStr = enumStr[enumIndex+1:]
          enumValue = HDLmHostTypes[enumStr]
          curExpectedOutputDict[enumType] = enumValue
      # If the expected JSON is an empty string, create an empty dictionary
      else:
        curExpectedOutputDict = dict()
      # Get the current expected error message (if any)
      curErrorMessage = curTest[2]
      # Try running the actual test. The test may throw an exception. If the
      # test does not throw an exception, it will produce output. We need to
      # check the output.
      try:
        # print(f'Test {i} {curInput} started') 
        actualOutputObject = HDLmUrl(curInput, **curKeywords)
        actualOutputDict = actualOutputObject.__dict__
        diff = DeepDiff(actualOutputDict, curExpectedOutputDict, ignore_order=True)
        diffLen = len(diff)
        # Check if the actual dictionary matches the expected dictionary
        if diffLen > 0:
          testMessage = f'Test {i} {curInput} failed - Invalid output'
          self.fail(testMessage)
      # The test threw an exception. The exception may have been expected. 
      except Exception as e:
        actualErrorMessage = str(e)
        if actualErrorMessage != curErrorMessage:
          testMessage = f'Test {i} {curInput} failed - {actualErrorMessage}'
          self.fail(testMessage)
  # Run a set of string tokenization tests
  def test_runTokensTests(self):
    # The array below contains all of the string tokenization tests. For each
    # test, we have an input string (that will be hopefully tokenized), an 
    # output list of tokens, and (possibly) an error message string. 
    tokenTests = [                          
                   [ 'abc',
                     '[ \
                        [0, "HDLmTokenTypes.identifier", "abc" ], \
                        [3, "HDLmTokenTypes.end", "" ] \
                      ]',
                     '',
                   ],
                   [ '',
                     '[ \
                        [0, "HDLmTokenTypes.end", ""] \
                      ]',
                     '',
                   ],
                   [ 'a',
                     '[ \
                        [0, "HDLmTokenTypes.identifier", "a"], \
                        [1, "HDLmTokenTypes.end", ""] \
                      ]',
                     '',
                   ],
                   [ 'b',
                     '[ \
                        [0, "HDLmTokenTypes.identifier", "b"], \
                        [1, "HDLmTokenTypes.end", ""] \
                      ]',
                     '',
                   ],
                   [ 'ab',
                     '[ \
                        [0, "HDLmTokenTypes.identifier", "ab"], \
                        [2, "HDLmTokenTypes.end", ""] \
                      ]',
                     '',
                   ],
                   [ 'ab ',
                     '[ \
                        [0, "HDLmTokenTypes.identifier", "ab"], \
                        [2, "HDLmTokenTypes.space", " "], \
                        [3, "HDLmTokenTypes.end", ""] \
                      ]',
                     '',
                   ],
                   [ 'ab  ',
                     '[ \
                        [0, "HDLmTokenTypes.identifier", "ab"], \
                        [2, "HDLmTokenTypes.space", "  "], \
                        [4, "HDLmTokenTypes.end", ""] \
                      ]',
                     '',
                   ],
                   [ 'a  b',
                     '[ \
                        [0, "HDLmTokenTypes.identifier", "a"], \
                        [1, "HDLmTokenTypes.space", "  "], \
                        [3, "HDLmTokenTypes.identifier", "b"], \
                        [4, "HDLmTokenTypes.end", ""] \
                      ]',
                     '',
                   ],
                   [ 'a  b 12',
                     '[ \
                        [0, "HDLmTokenTypes.identifier", "a"], \
                        [1, "HDLmTokenTypes.space", "  "], \
                        [3, "HDLmTokenTypes.identifier", "b"], \
                        [4, "HDLmTokenTypes.space", " "], \
                        [5, "HDLmTokenTypes.integer", "12"], \
                        [7, "HDLmTokenTypes.end", ""] \
                      ]',
                     '',
                   ],
                   [ 'a  b 12 +',
                     '[ \
                        [0, "HDLmTokenTypes.identifier", "a"], \
                        [1, "HDLmTokenTypes.space", "  "], \
                        [3, "HDLmTokenTypes.identifier", "b"], \
                        [4, "HDLmTokenTypes.space", " "], \
                        [5, "HDLmTokenTypes.integer", "12"], \
                        [7, "HDLmTokenTypes.space", " "], \
                        [8, "HDLmTokenTypes.operator", "+"], \
                        [9, "HDLmTokenTypes.end", ""] \
                      ]',
                     '',
                   ],
                   [ 'a  b 12 + \'\'',
                     '[ \
                        [0, "HDLmTokenTypes.identifier", "a"], \
                        [1, "HDLmTokenTypes.space", "  "], \
                        [3, "HDLmTokenTypes.identifier", "b"], \
                        [4, "HDLmTokenTypes.space", " "], \
                        [5, "HDLmTokenTypes.integer", "12"], \
                        [7, "HDLmTokenTypes.space", " "], \
                        [8, "HDLmTokenTypes.operator", "+"], \
                        [9, "HDLmTokenTypes.space", " "], \
                        [10, "HDLmTokenTypes.quoted", ""], \
                        [12, "HDLmTokenTypes.end", ""] \
                      ]',
                     '',
                   ],
                   [ 'a  b 12 + \'cde\'',
                     '[ \
                        [0, "HDLmTokenTypes.identifier", "a"], \
                        [1, "HDLmTokenTypes.space", "  "], \
                        [3, "HDLmTokenTypes.identifier", "b"], \
                        [4, "HDLmTokenTypes.space", " "], \
                        [5, "HDLmTokenTypes.integer", "12"], \
                        [7, "HDLmTokenTypes.space", " "], \
                        [8, "HDLmTokenTypes.operator", "+"], \
                        [9, "HDLmTokenTypes.space", " "], \
                        [10, "HDLmTokenTypes.quoted", "cde"], \
                        [15, "HDLmTokenTypes.end", ""] \
                      ]',
                     '',
                   ],
                   [ 'a  b 12 + \'c\'\'de\'',
                     '[ \
                        [0, "HDLmTokenTypes.identifier", "a"], \
                        [1, "HDLmTokenTypes.space", "  "], \
                        [3, "HDLmTokenTypes.identifier", "b"], \
                        [4, "HDLmTokenTypes.space", " "], \
                        [5, "HDLmTokenTypes.integer", "12"], \
                        [7, "HDLmTokenTypes.space", " "], \
                        [8, "HDLmTokenTypes.operator", "+"], \
                        [9, "HDLmTokenTypes.space", " "], \
                        [10, "HDLmTokenTypes.quoted", "c\'de"], \
                        [17, "HDLmTokenTypes.end", ""] \
                      ]',
                     '',
                   ],
                   [ 'a  b 12 + \'c\'\'de\' À',
                     '[ \
                        [0, "HDLmTokenTypes.identifier", "a"], \
                        [1, "HDLmTokenTypes.space", "  "], \
                        [3, "HDLmTokenTypes.identifier", "b"], \
                        [4, "HDLmTokenTypes.space", " "], \
                        [5, "HDLmTokenTypes.integer", "12"], \
                        [7, "HDLmTokenTypes.space", " "], \
                        [8, "HDLmTokenTypes.operator", "+"], \
                        [9, "HDLmTokenTypes.space", " "], \
                        [10, "HDLmTokenTypes.quoted", "c\'de"], \
                        [17, "HDLmTokenTypes.space", " "], \
                        [18, "HDLmTokenTypes.unknown", "À"], \
                        [19, "HDLmTokenTypes.end", ""] \
                      ]',
                     '',
                   ],
                   [ 'a  b 12 + ' + '\'' + 'cd' + '\\' + '\'' + 'e' + '\'',
                     '[ \
                        [0, "HDLmTokenTypes.identifier", "a"], \
                        [1, "HDLmTokenTypes.space", "  "], \
                        [3, "HDLmTokenTypes.identifier", "b"], \
                        [4, "HDLmTokenTypes.space", " "], \
                        [5, "HDLmTokenTypes.integer", "12"], \
                        [7, "HDLmTokenTypes.space", " "], \
                        [8, "HDLmTokenTypes.operator", "+"], \
                        [9, "HDLmTokenTypes.space", " "], \
                        [10, "HDLmTokenTypes.quoted", "cd\'e"], \
                        [17, "HDLmTokenTypes.end",       ""] \
                      ]',
                     '',
                   ],
                   # The error tests start here                         
                   [ 'a  b 12 + \'cde\'\' À',
                     '',
                     'A quote string token is not complete' ],
                   [ 'a  b 12 + ' + '\'' + 'cd' + '\\',
                     '',
                     'Quoted string has an escape at the end' ],
                 ]
    # Get the count of the number of tests and run each test 
    tests = tokenTests
    testCount = len(tests)
    for i in range(testCount): 
      # Get the current test
      curTest = tests[i]
      curTestLen = len(curTest)
      curInput = curTest[0]
      # Get the expected JSON output and convert it to a list
      # if possible
      curExpectedOutputJson = curTest[1]
      # Check if any additional keyword values were specified 
      curKeywords = dict()
      if curTestLen > 3:
        curKeywords = curTest[3]
      # Convert the expected JSON output to a list (if possible)
      if len(curExpectedOutputJson) > 0: 
        curExpectedOutputDict = json.loads(curExpectedOutputJson)
      # If the expected JSON is an empty string, create an empty list
      else:
        curExpectedOutputDict = dict()
      # The list must be processed at this point. Each entry in the 
      # list is somewhat wrong. The entry in each list is a token
      # type string. We need convert each token type string to a
      # token type enum.
      tempTokenList = []
      for curList in curExpectedOutputDict:
        # Get the string value that is the actual token type
        curTypeStr = curList[1]
        curTypeIndex = curTypeStr.find('.')
        curTypeStr = curTypeStr[curTypeIndex+1:]
        # Convert the string value to an enum value
        curTypeEnum = HDLmTokenTypes[curTypeStr]
        # Build a temporary token from the values we have
        tempToken = Token(curTypeEnum, curList[0], curList[2])
        tempTokenList.append(tempToken) 
      # Get the current expected error message (if any)
      curErrorMessage = curTest[2]
      # Try running the actual test. The test may throw an exception. If the
      # test does not throw an exception, it will produce output. We need to
      # check the output.
      try:
        actualOutputList = HDLmString.getTokens(curInput, **curKeywords)
        for listEntry in actualOutputList:
          if hasattr(listEntry, 'originalValue'):
            del listEntry.originalValue 
          if hasattr(listEntry, 'back'):
            del listEntry.back 
          if hasattr(listEntry, 'quote'):
            del listEntry.quote 
        diff = DeepDiff(actualOutputList, tempTokenList, ignore_order=True)
        diffLen = len(diff)
        # Check if the actual list matches the expected list
        if diffLen > 0:
          testMessage = f'Test {i} {curInput} failed - Invalid output'
          self.fail(testMessage)
      # The test threw an exception. The exception may have been expected. 
      except Exception as e:
        actualErrorMessage = str(e)
        if actualErrorMessage != curErrorMessage:
          testMessage = f'Test {i} {curInput} failed - {actualErrorMessage}'
          self.fail(testMessage)

# Actual starting point
if __name__ == '__main__':
  unittest.main()