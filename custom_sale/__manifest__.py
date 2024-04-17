{
    "name": "Custom Sale",
    "version": "16.0.1.0.0",
    'author': "Ridhin",
    "depends": ["base", "sale","mrp","purchase","purchase_requisition"],
    "data": [
        'security/ir.model.access.csv',
        'views/sale_order_view.xml',
        'views/work_order_design_view.xml',
        'views/mrp_bom_view.xml',
        'views/purchase_order_view.xml'
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
