
from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    start_datee= fields.Datetime(string= "Start Date", config_parameter='dynamic_attendance_report.start_datee')
    end_datee= fields.Datetime(string= "End Date", config_parameter='dynamic_attendance_report.end_datee')

    today_datee= fields.Boolean(string= "Date Of Today", config_parameter='dynamic_attendance_report.today_datee')

    