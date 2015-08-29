"""
Helper function to modify SqlAlchemy query object
"""
from sqlalchemy.sql.functions import coalesce

def sqla_dyn_filters(filter_dict, query_object, validation_class):
    """SqlAlchemy query object modification with dynamic filters"""
    for attr, value in filter_dict:
        if value == '':
            value = '%'
        try:
            query_object = query_object.filter(coalesce(getattr(validation_class, attr), '').like(value))
        except:
            pass#When model object does not have dictionary value do nothing
    return query_object