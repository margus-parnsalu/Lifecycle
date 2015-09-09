"""
Applications and lifecycle management package
__author__ = 'margusp'
"""

def include(config):

    #Apps package template location
    config.add_jinja2_search_path('arhea:app_apps/templates')

    #Applications
    config.add_route('application_view', '/apps')
    config.add_route('tag_edit', '/apps/tag/{tag_id:\d+}/edit')
    config.add_route('app_tags_edit', '/apps/{app_id:\d+}/edit')
