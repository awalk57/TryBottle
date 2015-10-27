__author__ = "al walker"

import grequests
# from sqlalchemy import create_engine, Column, Boolean, Integer, String
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker


def exception_handler(request, exception):

    print "Request Failed for ->", exception.request.url, exception.message

# Base = declarative_base()
# engine = create_engine("sqlite:///urldb.db", echo=True)
# create_session = sessionmaker(bind=engine)
# read in urls from file
def get_checks():

    with open("urls.txt") as f:
        urls = f.read().splitlines()

    reqs = (grequests.get(u, timeout=0.50) for u in urls)
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

if __name__ == "__main__":
    get_checks()