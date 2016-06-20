def include(config):

    #Apps package template location
    config.add_jinja2_search_path('arhea:app_sd/templates')

    #Applications
    config.add_route('ci_admin_view', '/ci/admin')
    config.add_route('ci_load_view', '/ci/load')
    config.add_route('ci_clean_view', '/ci/purge')
    config.add_route('ci_codes_view', '/cis')