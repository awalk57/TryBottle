from bottle import Bottle, route, run, debug
from bottle import redirect, request, template
from bottle.ext import sqlalchemy

from sqlalchemy import create_engine, Column, Boolean, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# --------------------------------
# Add SQLAlchemy app
# --------------------------------
app = Bottle()

Base = declarative_base()
engine = create_engine("sqlite:///todo.db", echo=True)
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
class TODO(Base):
    """
    TODO database class
    """
    __tablename__ = "todo"
    id = Column(Integer, primary_key=True)
    task = Column(String, nullable=False)
    status = Column(Boolean, nullable=False)

    #----------------------------------------------------------------------
    def __init__(self, task, status):
        """Constructor"""
        self.task = task
        self.status = status
        
    #----------------------------------------------------------------------
    def __repr__(self):
        """"""
        return "<TODO (task: %s, status: %s" % (self.task,
                                                self.status)
    
# --------------------------------
# Bottle specific code starts here
# --------------------------------

#----------------------------------------------------------------------
@route('/edit/<no:int>', method='GET')
def edit_item(no):
    """
    Edit a TODO item
    """
    session = create_session()
    result = session.query(TODO).filter(TODO.id==no).first()
    
    if request.GET.get('save','').strip():
        task = request.GET.get('task','').strip()
        status = request.GET.get('status','').strip()

        if status == 'open':
            status = 1
        else:
            status = 0
        
        result.task = task
        result.status = status
        session.commit()

        redirect("/")
    else:
        return template('edit_task', old=result, no=no)
    
#----------------------------------------------------------------------
@route("/new", method="GET")
def new_item():
    """
    Add a new TODO item
    """
    if request.GET.get("save", "").strip():
        task = request.GET.get("task", "").strip()
        status = 1
        
        session = create_session()
        new_task = TODO(task, status)
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
    result = session.query(TODO).filter(TODO.status==0).all()
    
    output = template("show_done", rows=result)
    return output
    
#----------------------------------------------------------------------
@route("/")
@route("/todo")
def todo_list():
    """
    Show the main page which is the current TODO list
    """
    session = create_session()
    result = session.query(TODO).filter(TODO.status==1).all()
    myResultList = [(item.id, item.task) for item in result]
    output = template("make_table", rows=myResultList)
    return output

#----------------------------------------------------------------------
if __name__ == "__main__":
    debug(True)
    run()