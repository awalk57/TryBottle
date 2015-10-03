from sqlalchemy import create_engine, Column, Boolean, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = create_engine("sqlite:///urldb.db", echo=True)

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
def main():
    """
    Create the database and add data to it
    """
    Base.metadata.create_all(engine)
    create_session = sessionmaker(bind=engine)
    session = create_session()
    
    session.add_all([
        URLDB('State Web Page', 'http://www.state.nj.us', '200', 0),
        URLDB('Python Library Blog', 'http://www.blog.pythonlibrary.org', '', 1),
        URLDB('Bottle Tutorial', 'http://bottlepy.org/docs', '', 1),
        URLDB('Norwegian Cruise Lines', 'http://www.ncl.com', '', 0)
        ])
    session.commit()

if __name__ == "__main__":
    main()