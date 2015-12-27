
NTIER = {'technologies': [{'domain': 'Persistance', 'subdomain': 'Database',
                           'technology': 'RDBMS', 'note': 'Relational Database',
                           'components': [{'component': 'Postgres', 'status': 'Preferred'},
                                          {'component': 'Oracle', 'status': 'Preferred'},
                                          {'component': 'MS Sql', 'status': 'Acceptable'},
                                          ]
                           },
                          {'domain': 'Persistance', 'subdomain': 'Database',
                           'technology': 'NoSql', 'note': 'Non Relational Database',
                           'components': [{'component': 'Redis', 'status': 'Preferred'},
                                          {'component': 'Hazelcast', 'status': 'Preferred'},
                                          ]
                           },
                          {'domain': 'Persistance', 'subdomain': 'Database',
                           'technology': 'DW', 'note': 'Data Warehouse',
                           'components': [{'component': 'Vertica', 'status': 'Preferred'},
                                          {'component': 'Teradata', 'status': 'Acceptable'},
                                          {'component': 'Oracle', 'status': 'Do not select'},
                                          ]
                           },
                          {'domain': 'Integration', 'subdomain': 'Data Integration',
                           'technology': 'ETL', 'note': '',
                           'components': [{'component': 'MS SSIS', 'status': 'Preferred'},
                                          {'component': 'ODI', 'status': 'Preferred'},
                                          ]
                           },
                          {'domain': 'Integration', 'subdomain': 'Data Integration',
                           'technology': 'Event Queue', 'note': '',
                           'components': [{'component': 'RabbitMQ', 'description': 'AMQP', 'note': '', 'status': 'Preferred'},
                                          {'component': 'Oracle SOA suite', 'description': 'AQ, JMS', 'note': '', 'status': 'Acceptable'},
                                          ]
                           },
                          {'domain': 'Integration', 'subdomain': 'Application Integration',
                           'technology': 'Synchronous', 'note': '',
                           'components': [{'component': 'REST API Frameworks', 'description': 'REST', 'note': 'Distributed endpoints', 'status': 'Preferred'},
                                          {'component': 'Oracle SOA suite', 'description': 'SOAP', 'note': 'Central platform', 'status': 'Preferred'},
                                          ]
                           },

                         ]
         }