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
    def __init__(self, task, status, urlstr, chk_status):
        """Constructor"""
        self.task = task
        self.status = status
        self.urlstr = urlstr
        self.chk_status = chk_status
        
#----------------------------------------------------------------------
def main():
    """
    Create the database and add data to it
    """
    Base.metadata.create_all(engine)
    create_session = sessionmaker(bind=engine)
    session = create_session()
    
    session.add_all([
        URLDB('State Web Page', 0, 'http://www.state.nj.us', '200'),
        URLDB('Python Library Blog', 1,'http://www.blog.pythonlibrary.org', ''),
        URLDB('Bottle Tutorial', 1, 'http://bottlepy.org/docs', ''),
        URLDB('Norwegian Cruise Lines', 0, 'http://www.ncl.com', '')
        ])
    session.commit()

if __name__ == "__main__":
    main()