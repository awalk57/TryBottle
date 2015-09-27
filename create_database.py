from sqlalchemy import create_engine, Column, Boolean, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = create_engine("sqlite:///todo.db", echo=True)

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
def main():
    """
    Create the database and add data to it
    """
    Base.metadata.create_all(engine)
    create_session = sessionmaker(bind=engine)
    session = create_session()
    
    session.add_all([
        TODO('Read Google News', 0),
        TODO('Visit the Python website', 1),
        TODO('See how flask differs from bottle', 1),
        TODO('Watch the latest from the Slingshot Channel', 0)
        ])
    session.commit()

if __name__ == "__main__":
    main()