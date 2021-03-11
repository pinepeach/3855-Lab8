from sqlalchemy import Column, Integer, String, DateTime
from base import Base
import datetime

class Return(Base):
    """ Return """
    __tablename__ ="returns"

    id = Column(Integer, primary_key=True)
    title = Column(String(250),  nullable=False)
    store = Column(Integer, nullable=False)
    till_number = Column(Integer, nullable=False)
    transaction_number = Column(Integer, nullable=False)
    date = Column(String(10), nullable=False)
    sku = Column(Integer, nullable=False)
    name = Column(String(250), nullable=False)
    reason = Column(String(250), nullable=False)
    date_created = Column(DateTime, nullable=False)

    def __init__(self, title, store, till_number, transaction_number, date, sku, name, reason):
        self.title = title
        self.store = store
        self.till_number = till_number
        self.transaction_number = transaction_number
        self.date = date
        self.sku = sku
        self.name = name
        self.reason = reason
        self.date_created = datetime.datetime.now() # Sets the date/time record is created

    def to_dict(self):
        """ Dictionary Representation of a return transaction """
        dict = {}
        dict['id'] = self.id
        dict['title'] = self.title
        dict['gcid'] = {}
        dict['gcid']['store'] = self.store
        dict['gcid']['till_number'] = self.till_number
        dict['gcid']['transaction_number'] = self.transaction_number
        dict['gcid']['date'] = self.date
        dict['return_product'] = {}
        dict['return_product']['sku'] = self.sku
        dict['return_product']['name'] = self.name
        dict['return_product']['reason'] = self.reason
        dict['date_created'] = self.date_created

        return dict
