"""
Custom Jinja filters, included in __init__.py
"""
def datetimeformat(value, format='%Y-%m-%d %H:%M'):
    if value == None or value == '':
        return ''
    return value.strftime(format)