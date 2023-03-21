# external imports
from sqlalchemy import create_engine, Column, MetaData, Table
from sqlalchemy import insert, select, update, delete

# from sqlalchemy_utils import database_exists, create_database
from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import declarative_base



Base = declarative_base()
Metadata = MetaData()

Users = Table(
    "users",
    Metadata,
    Column("_id", Integer, primary_key=True),
    Column("uuid", Integer, unique=True),
    Column("activate", Boolean),
    Column("horoscope", String, default="none")
)

class User(Base):
    __table__ = Users

class Database:
    def __init__(self, engine):
        self.engine = create_engine(engine)
        Metadata.create_all(self.engine)
                
    
    def login(self, uuid):
        with self.engine.connect() as c:
            with c.begin():
                select_user = select(User.uuid).where(User.uuid == uuid)
                login = c.execute(select_user).first()
                if not login:
                    create_user = (
                        insert(User).values(uuid=uuid, activate=True)
                    )
                    c.execute(create_user)
                    login = c.execute(select_user).first()
                else:
                    activate = update(User).where(User.uuid == uuid).values(activate=True)
                    c.execute(activate)

    def deactivate(self, uuid):
        with self.engine.connect() as c:
            with c.begin():
                deactivate = update(User).where(User.uuid == uuid).values(activate=False)
                c.execute(deactivate)

    def get_users(self):
        with self.engine.connect() as c:
            with c.begin():
                users_exec = select(User).where(User.activate == True)
                users = c.execute(users_exec).all()
                return users
            
    def get_users_uuids(self):
        with self.engine.connect() as c:
            with c.begin():
                users_exec = select(User.uuid).where(User.activate == True)
                users = c.execute(users_exec).all()
                return users
            
    def get_user(self, uuid):
        with self.engine.connect() as c:
            with c.begin():
                user_exec = select(User).where(User.activate == True, User.uuid == uuid)
                user = c.execute(user_exec).one()
                return user
            
    def delete_user(self, uuid):
        with self.engine.connect() as c:
            with c.begin():
                delete_user_exec = delete(User).where(User.uuid == uuid)
                try:
                    c.execute(delete_user_exec)
                except Exception as err:
                    print(err)

    def user_update_horoscope(self, uuid, new_horoscope):
        with self.engine.connect() as c:
            with c.begin():
                update_user = update(User).where(User.uuid == uuid).values(horoscope=new_horoscope)
                try:
                    c.execute(update_user)
                except Exception as err:
                    print(err)