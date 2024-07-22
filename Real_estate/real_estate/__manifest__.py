{
    'name': "Real Estate",
    'version': '1.0',
    'summary': 'Real Estate',
    'depends':  [ 'sale_subscription' , 'website' ,'web_studio'],
    'author':"komal",
    'description': """
    Description text
    """,

    "data": [
        "security/ir.model.access.csv",
        "data/product_sequence.xml",
        "views/estate_property_view.xml",
        "views/meter_view.xml",
        "views/product_view.xml",
        "views/properties_template.xml",
        "views/website_menu.xml",
        "views/realestate_menu.xml",
    ],
    "demo": [
        "data/product_demo.xml",
        "data/plan_demo.xml",
    ],

    'installable': True,
    'application': True,

    'category': 'Real Estate/Real Estate',
}