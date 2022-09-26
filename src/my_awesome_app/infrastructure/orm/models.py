from sqlalchemy import Column, String, BigInteger, Integer

from my_awesome_app.infrastructure.orm.base_model import BaseOrmModel
from my_awesome_app.infrastructure.orm.custom_types import DecimalType


class OperationModel(BaseOrmModel):
    id = Column(BigInteger().with_variant(Integer, 'sqlite'), primary_key=True)
    a = Column(DecimalType(), nullable=False)
    operation = Column(String(10), nullable=False)
    b = Column(DecimalType(), nullable=False)
    result = Column(DecimalType(), nullable=False)

    __tablename__ = 'operation'
