from sqlalchemy import create_engine, update, Column, BigInteger, CheckConstraint
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from default import Config

INITIAL_MONEY = 100

config = Config().database
Base = declarative_base()


class Database():
    def __init__(self):
        self.engine = create_engine(
            f"{config['dialect']}://{config['username']}:{config['password']}@{config['host']}:{config['port']}/{config['dbname']}")
        self.session = sessionmaker(bind=self.engine)()
        Base.metadata.create_all(self.engine)


class Economy_Table(Database):
    def __init__(self):
        super().__init__()

    class Economy(Base):
        __tablename__ = "economy"

        id = Column(BigInteger, primary_key=True)
        money = Column(BigInteger, CheckConstraint("money>=0"))

        def __repr__(self):
            return str(self.money)

    def query_user(self, user_id):
        user = self.session.query(self.Economy).filter_by(id=user_id).first()
        if user:
            return user
        else:
            return self.add_user(user_id)

    def add_user(self, user_id):
        new_user = self.Economy(id=user_id, money=INITIAL_MONEY)
        self.session.add(new_user)
        self.session.commit()
        return new_user

    def user_has_enough_money(self, user_id, desired_money: int):
        return self.query_user(user_id).money >= desired_money

    def update_users_money(self, user_id, new_money_value):
        statement = update(self.Economy).where(
            self.Economy.id == user_id).values(money=new_money_value)
        self.session.execute(statement)
        self.session.commit()
        return self.query_user(user_id)

    def add_money(self, user_id, value_to_be_added):
        if value_to_be_added < 1:
            return
        user_money = self.query_user(user_id).money
        return self.update_users_money(
            user_id, new_money_value=user_money + value_to_be_added)

    def subtract_money(self, user_id, value_to_be_subtracted):
        if value_to_be_subtracted < 1:
            return
        user_money = self.query_user(user_id).money
        value_to_be_subtracted = min(user_money, value_to_be_subtracted)
        return self.update_users_money(
            user_id, new_money_value=user_money - value_to_be_subtracted)
