{
    "name": "Custom CRM",
    "version": "16.0.1.0.0",
    'author': "Ridhin",
    "depends": ["base", "crm","sale_crm"],
    "data": [
        'security/ir.model.access.csv',
        'data/acess.xml',
        'views/crm_lead_view.xml',
        'views/crm_priority_view.xml',
        'views/crm_stages_view.xml'
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
