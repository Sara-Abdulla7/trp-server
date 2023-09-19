# -*- coding: utf-8 -*-
{
    'name': "Dynamic Attendance Report",

    'summary': """It is a report that displays the attendance and departure details of the employees by specifying the time period""",

    'description': """
        Long description of module's purpose
    """,

    'author': "TRP",
    'website': "https://www.trp.sa",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'HR Resources',
    'version': '0.16',

    # any module necessary for this one to work correctly
    'depends': ['base','hr_attendance','report_xlsx'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'wizard/create_wizard_view.xml',
        'reports/report_pdf.xml',
        'reports/attendance_report.xml',
        'reports/report.xml',
        'data/cron.xml',
        'data/email_template.xml',
        'views/attendance_send_email_report.xml',
        'views/res_config_settings.xml',
        'views/hr_attendance.xml',
    ],
        'images': ['static/description/icon.png'],
}
