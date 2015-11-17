__author__ = "al walker"

import grequests


def exception_handler(request, exception):

    print "Request Failed for ->", exception.request.url, exception.message
#    errlist = [exception.request.url, exception.message]
    request.response = '999'
    print request

# read in urls from file
#errlist = []
with open("urls.txt") as f:
    urls = f.read().splitlines()

reqs = (grequests.get(u, timeout=5.00) for u in urls)

resp = grequests.map(reqs, False, 5, exception_handler = exception_handler)



listresult = list(resp)

print listresult
for x in listresult:
    rurl = x.url
    rtext = x.content
    rstat = x.status_code
    rtime = x.elapsed.microseconds / 1000.
    print "+++Url -> ", rurl, " Status -> ", rstat, "  Elapsed Time -> ", rtime, "milliseconds \n"
    #    print "   Content -> ", rtext
    print "--- \n"

