from datetime import datetime, timedelta
from odoo import models, fields, api, exceptions, _
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta 

class AttendanceEmail(models.Model):
    _name = 'attendance.email'

    employee_name = fields.Many2one('hr.employee',string=' Employee Name')
    work_email= fields.Char(string='Work Email')
    email_type = fields.Selection([('to', 'To'),('cc', 'Cc')],string="Send Type")

    @api.onchange('employee_name')
    def onchange_employee_name(self):
      if self.employee_name:
         if self.employee_name.work_email:
            self.work_email = self.employee_name.work_email

  