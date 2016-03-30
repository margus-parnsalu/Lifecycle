"""
Applications and lifecycle management package
__author__ = 'margusp'
"""

def include(config):

    #Apps package template location
    config.add_jinja2_search_path('arhea:app_apps/templates')

    #Applications
    config.add_route('application_view', '/apps')
    config.add_route('apps_csv_view', '/apps/csv')
    config.add_route('apps_domain_stat_view', '/apps/stat')
    config.add_route('tag_edit', '/apps/tag/{tag_id:\d+}/edit')
    config.add_route('app_tags_edit', '/apps/{app_id:\d+}/edit')


    # Link to models
    config.add_route('ea_models', 'http://ea.telekom.ee/Telekom/index.html')