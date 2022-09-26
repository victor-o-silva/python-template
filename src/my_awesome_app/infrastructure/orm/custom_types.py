from decimal import Decimal

import sqlalchemy


class DecimalType(sqlalchemy.types.TypeDecorator):
    """
    Use `String` for sqlite, and `Numeric` for other dialects.
    """

    impl = sqlalchemy.Numeric(64, 32)
    cache_ok = True

    def load_dialect_impl(self, dialect):
        if dialect.name == 'sqlite':
            return dialect.type_descriptor(sqlalchemy.String(70))

        return dialect.type_descriptor(self.impl)

    def process_bind_param(self, value, dialect):
        if dialect.name == 'sqlite':
            return f'{value:.64f}'

        return value

    def process_result_value(self, value, dialect):
        if dialect.name == 'sqlite':
            return Decimal(value)

        return value
