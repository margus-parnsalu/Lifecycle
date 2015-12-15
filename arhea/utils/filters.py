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
            query_object = (query_object.filter(coalesce(getattr(validation_class, attr), '').
                                                ilike(value)))
        except:
            pass#When model object does not have dictionary value do nothing
    return query_object


def req_get_todict(request_get):
    """Handling search Form get parameter passing to template sorting"""
    if len(request_get) == 0:#No GET parameters
        return {}
    else:
        #Need to pass GET parameters in dict for route_url
        return {k:v for k, v in request_get.items()}


def req_paging_dict(request, sort, items):
    route_name = request.matched_route.name
    if route_name[-5:] !=':page':
        route_name = request.matched_route.name+':page'
    return {'current_page': int(request.matchdict.get('page', '1')),
            'url_for_page': lambda p: request.route_url(route_name,
                                                        page=p,
                                                        _query=(('sort', sort), )),
            'items_per_page': items}