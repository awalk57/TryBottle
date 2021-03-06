from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from bottle import Bottle, route, run, debug
from bottle import redirect, request, template
from bottle.ext import sqlalchemy


from rq import Connection, Queue, Worker

from sqlalchemy import create_engine, Column, Boolean, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# --------------------------------
# Add SQLAlchemy app
# --------------------------------
srvstate = 1

app = Bottle()


Base = declarative_base()
engine = create_engine("sqlite:///urldb.db", echo=True)
create_session = sessionmaker(bind=engine)

plugin = sqlalchemy.Plugin(
        engine,
        Base.metadata,
        keyword='db',
        create=True,
        commit=True,
        use_kwargs=False
)

app.install(plugin)

########################################################################
class URLDB(Base):
    """
    URLDB database class
    """
    __tablename__ = "urldb"
    id = Column(Integer, primary_key=True)
    task = Column(String, nullable=False)
    urlstr = Column(String, nullable=False)
    chk_status = Column(String, nullable=True)
    status = Column(Boolean, nullable=False)

    #----------------------------------------------------------------------
    def __init__(self, task, urlstr, chk_status, status):
        """Constructor"""
        self.task = task
        self.urlstr = urlstr
        self.chk_status = chk_status
        self.status = status

        
    #----------------------------------------------------------------------
    def __repr__(self):
        """"""
        return "<URLDB (task: %s, urlstr: %s, chk_status: %s, status: %s" % (self.task,
                                                self.urlstr,
                                                self.chk_status,
                                                self.status)
    
# --------------------------------
# Bottle specific code starts here
# --------------------------------

#----------------------------------------------------------------------
@route('/edit/<no:int>', method='GET')
def edit_item(no):
    """
    Edit a URLDB item
    """
    session = create_session()
    result = session.query(URLDB).filter(URLDB.id==no).first()
    
    if request.GET.get('save','').strip():
        task = request.GET.get('task','').strip()
        urlstr = request.GET.get('urlstr', '').strip()
        chk_status = request.GET.get('chk_status', '').strip()
        status = request.GET.get('status','').strip()

        if status == 'open':
            status = 1
        else:
            status = 0
        
        result.task = task
        result.urlstr = urlstr
        result.chk_status = chk_status
        result.status = status
        session.commit()

        redirect("/")
    else:
        return template('edit_task', old=result, no=no)
    
#----------------------------------------------------------------------
@route("/new", method="GET")
def new_item():
    """
    Add a new URLDB item
    """
    if request.GET.get('save', '').strip():
        task = request.GET.get('task', '').strip()
        urlstr = request.GET.get('urlstr', '').strip()
        chk_status = request.GET.get('chk_status', '').strip()
        status = 1
        
        session = create_session()
        new_task = URLDB(task, urlstr, chk_status, status)
        session.add(new_task)
        session.commit()
        
        redirect("/")
    else:
        return template("new_task.tpl")
    
#----------------------------------------------------------------------
@route("/done")
def show_done():
    """
    Show all items that are done
    """
    session = create_session()
    result = session.query(URLDB).filter(URLDB.status==0).all()
    
    output = template("show_done", rows=result)
    return output
    
#----------------------------------------------------------------------
@route("/")
@route("/list")
def URLDB_list():
    """
    Show the main page which is the current URLDB list
    """
    session = create_session()
    result = session.query(URLDB).filter(URLDB.status==1).order_by(URLDB.task).all()
    UrlList = [(item.id, item.task, item.urlstr) for item in result]
    output = template("make_table", rows=UrlList)
    return output

#----------------------------------------------------------------------
@route("/status")
def status():
    if srvstate:
        output = template("server_status", status='Running')
        return output
    else:
        output = template("server_status", status='Offline')
        return output

@route("/control")
def control():
    if srvstate:
        srvstate = 0
    else:
        srvstate = 1
    output = template("server_status")
    return output

if __name__ == "__main__":
    with Connection():
        q = Queue()
        Worker(q).work()


    run_example()
    debug(True)
    run()