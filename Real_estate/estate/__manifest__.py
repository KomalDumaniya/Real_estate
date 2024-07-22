{
    'name': "Estate Commision",
    'version': '1.0',
    'summary': 'Estate',
    'depends': ['purchase','real_estate', 'crm'],
    'author':"nidhipatel",
    'description': """
    Description text
    """,

    "data": [
        "security/ir.model.access.csv",
        "views/estate_lead_views.xml",
        "views/estate_contact_views.xml",
        "views/estate_commision_line_views.xml",
        "views/estate_commision_bill_views.xml",
        "views/estate_employees_views.xml",
        "views/estate_rental_contract_views.xml",
        "views/estate_account_move_views.xml",
        "views/estate_rental_contract_gantt_views.xml",
        "views/template_contactus.xml",
        "views/estate_menu.xml",
    ],

    # 'category': 'estate/estate',
    'category': 'Real Estate/Estate Commision',
}