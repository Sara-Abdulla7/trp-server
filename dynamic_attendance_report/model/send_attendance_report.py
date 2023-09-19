import base64
from odoo import api, models, fields
import datetime
from odoo.exceptions import ValidationError
from datetime import timedelta


class HRAttendanceReport(models.Model):
    _inherit = 'hr.attendance'

    break_time = fields.Boolean(string="Break Time", compute='compute_break_time')
    net_worked_hours = fields.Float(string="Net Worked Hours", compute='compute_net_worked_hours')

    def compute_break_time(self):
        dt = datetime.datetime(2020, 7, 1)
        from_time = datetime.datetime.combine(dt.date(), datetime.time(9, 0, 0))
        to_time = datetime.datetime.combine(dt.date(), datetime.time(10, 0, 0))
        for rec in self:
            if rec.check_in and rec.check_out and (rec.check_in.date() == rec.check_out.date()):
                rec_check_in = datetime.datetime.combine(dt.date(), (rec.check_in).time())
                rec_check_out = datetime.datetime.combine(dt.date(), (rec.check_out).time())
                if self.check_datetime_in_range(from_time, to_time, rec_check_in) and self.check_datetime_in_range(
                        from_time, to_time,
                        rec_check_out):
                    rec.break_time = True
                else:
                    rec.break_time = False
            else:
                rec.break_time = False



    def compute_net_worked_hours(self):
        dt = datetime.datetime(2020, 7, 1)
        from_time1 = datetime.datetime.combine(dt.date(), datetime.time(5, 0, 0))
        to_time1 = datetime.datetime.combine(dt.date(), datetime.time(9, 0, 0))
        from_time2 = datetime.datetime.combine(dt.date(), datetime.time(10, 0, 0))
        to_time2 = datetime.datetime.combine(dt.date(), datetime.time(14, 0, 0))
        for rec in self:
            if rec.break_time:
                rec.net_worked_hours = rec.worked_hours
            else:
                if rec.check_in and rec.check_out and (rec.check_in.date() == rec.check_out.date()):
                    rec_check_in = datetime.datetime.combine(dt.date(), (rec.check_in).time())
                    rec_check_out = datetime.datetime.combine(dt.date(), (rec.check_out).time())
                    # Rules of Condition
                    # 1- if check in and check out in range (from_time1 ===> to_time1) or (from_time2 ===> to_time2)
                    if (self.check_datetime_in_range(from_time1, to_time1, rec_check_in) and self.check_datetime_in_range(
                            from_time1, to_time1,
                            rec_check_out)) or (self.check_datetime_in_range(from_time2, to_time2, rec_check_in) and self.check_datetime_in_range(
                            from_time2, to_time2,
                            rec_check_out)):
                        rec.net_worked_hours = rec.worked_hours

                    # 2- if check_in  in range (from_time1 ===> to_time1) and  check_out (from_time2 ===> to_time2)
                    elif (rec_check_in >= from_time1 and rec_check_in <= to_time1) and(rec_check_out >= from_time2 and rec_check_out <= to_time2):
                        rec.net_worked_hours = rec.worked_hours - 1
                    # 3- if check_in before from_time1 and check_out after from_time1
                    elif (rec_check_in < from_time1 and rec_check_out > from_time1):
                        # 3-1 if rec_check_out before to_time1
                        if rec_check_out <= to_time1:
                            rec.net_worked_hours = rec.worked_hours + (rec_check_in - from_time1).total_seconds() / 3600.0
                        # 3-2 if rec_check_out in range (to_time1 ==> from_time2)
                        elif rec_check_out >=to_time1 and rec_check_out <=from_time2 :
                            rec.net_worked_hours = (rec.worked_hours + (rec_check_in - from_time1).total_seconds() / 3600.0)+(to_time1 - rec_check_out).total_seconds() / 3600.0
                        # 3-3 if rec_check_out in range (from_time2 ==> to_time2)
                        elif rec_check_out >=from_time2 and rec_check_out <=to_time2 :
                            rec.net_worked_hours = (rec.worked_hours + (rec_check_in - from_time1).total_seconds() / 3600.0)-1
                        # 3-4 if rec_check_out after to_time2
                        elif rec_check_out >= to_time2:
                            rec.net_worked_hours = 8
                        else:
                            rec.net_worked_hours=0
                    # 4- if check_in after from_time1 and check_out after to_time2
                    elif (rec_check_in > from_time1 and rec_check_out > to_time2):
                        # 4-1 if check_in in range(from_time1 ==> to_time1)
                        if rec_check_in <= to_time1:
                            rec.net_worked_hours = (rec.worked_hours - (rec_check_out - to_time2).total_seconds() / 3600.0)-1
                        # 4-2 if check_in in range(to_time1 ==> from_time2)
                        elif rec_check_in >= to_time1 and rec_check_in <=from_time2 :
                            rec.net_worked_hours = (rec.worked_hours - (rec_check_out - to_time2).total_seconds() / 3600.0)- (from_time2 - rec_check_in).total_seconds() / 3600.0
                        # 4-3 if check_in in range(from_time2 ==> to_time2)
                        elif rec_check_in >=from_time2 and rec_check_in <=to_time2 :
                            rec.net_worked_hours = (rec.worked_hours - (rec_check_out - to_time2).total_seconds() / 3600.0)
                        # elif rec_check_out >= to_time2:
                        #     rec.net_worked_hours = 8
                        else:
                            rec.net_worked_hours=0

                    # 5- if check_in in range(from_time1 ==> to_time1) and check_out in range(to_time1 ==> from_time2)
                    elif (rec_check_in > from_time1 and rec_check_in < to_time1) and (rec_check_out >= to_time1 and rec_check_out <= from_time2):
                        rec.net_worked_hours = (rec.worked_hours - (rec_check_out - to_time1).total_seconds() / 3600.0)
                    # 6- if check_in in range(to_time1 ==> from_time2) and check_out in range(from_time2 ==> to_time2)
                    elif (rec_check_in > to_time1 and rec_check_in < from_time2) and (rec_check_out >= from_time2 and rec_check_out <= to_time2):
                        rec.net_worked_hours = (rec.worked_hours - (from_time2 - rec_check_in).total_seconds() / 3600.0)

                    elif (rec_check_in> to_time1 and rec_check_in< from_time2) and (rec_check_out>= from_time2 and rec_check_out< to_time2):
                        rec.net_worked_hours = (rec.worked_hours - (from_time2 - rec_check_in).total_seconds() / 3600.0)

                    elif (rec_check_in> to_time1 and rec_check_in< from_time2) and (rec_check_out >= to_time2):
                        rec.net_worked_hours = 4


                    elif (rec_check_in < from_time1 and rec_check_out > to_time2):
                        rec.net_worked_hours = 8

                    else:
                        rec.net_worked_hours = 0

                # check...............
                else:
                    rec.net_worked_hours =0


    def check_datetime_in_range(self, start_time, end_time, current_time):
        return start_time <= current_time <= end_time

    @api.model
    def attendance_cron_job_report(self):

        to = []
        cc = []

        send_to = self.env['attendance.email'].search([('email_type', '=', 'to')]).mapped('work_email')
        send_cc = self.env['attendance.email'].search([('email_type', '=', 'cc')]).mapped('work_email')

        for record in send_to:
            to.append(record)

        for record2 in send_cc:
            cc.append(record2)

        generated_report = self.env['ir.actions.report']._render_qweb_pdf(
            "dynamic_attendance_report.cron_attendance_employees", self.id)
        data_record = base64.b64encode(generated_report[0])
        ir_values = {
            'name': 'Report Notification',
            'type': 'binary',
            'datas': data_record,
            'store_fname': data_record,
            'mimetype': 'application/pdf',
            'res_model': 'hr.attendance',
        }
        report_attachment = self.env['ir.attachment'].sudo().create(ir_values)
        report_attachment.name = 'Attendance Report.pdf'
        email_template = self.env.ref('dynamic_attendance_report.email_template_attendance')
        if email_template:
            email_values = {
                'email_to': (','.join(to)),
                'email_cc': (','.join(cc)),
                'email_from': self.env.user.email,
            }
            email_template.attachment_ids = [(4, report_attachment.id)]
            email_template.send_mail(self.id, email_values=email_values, force_send=True)
            email_template.attachment_ids = [(5, 0, 0)]
        report_attachment.unlink()


class AttendanceReport(models.AbstractModel):
    _name = 'report.dynamic_attendance_report.attendance_report_manager'

    def get_dynamic_attendance_report_configuration(self):
        start_date = self.env['ir.config_parameter'].sudo().get_param('dynamic_attendance_report.start_date')
        end_date = self.env['ir.config_parameter'].sudo().get_param('dynamic_attendance_report.end_date')
        today_date = self.env['ir.config_parameter'].sudo().get_param('dynamic_attendance_report.today_date')

        if not start_date:
            raise ValidationError('Please Enter start date')
        if not end_date:
            raise ValidationError('Please Enter end date')
        return start_date, end_date, today_date

    @api.model
    def _get_report_values(self, docids, data=None):

        domain = []
        start_date, end_date, today_date = self.get_dynamic_attendance_report_configuration()

        am = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(hours=3)
        pm = datetime.datetime.now().replace(hour=23, minute=0, second=0, microsecond=0) - timedelta(hours=3)
        if today_date:
            domain += [('check_in', '>=', am), ('check_out', '<=', pm)]
        else:
            domain += [('check_in', '>=', start_date), ('check_out', '<=', end_date)]

        employee_attendance_by_group = self.env['hr.attendance']._read_group(domain=domain, fields=[],
                                                                             groupby=['employee_id'])
        new_list = []
        total_worked_hours = 0
        for emp in employee_attendance_by_group:
            if today_date:
                employee = self.env['hr.attendance'].search(
                    [('employee_id.id', '=', emp['employee_id'][0]), ('check_in', '>=', am - timedelta(hours=3)),
                     ('check_out', '<=', pm)])
            else:
                employee = self.env['hr.attendance'].search(
                    [('employee_id.id', '=', emp['employee_id'][0]), ('check_in', '>=', start_date),
                     ('check_out', '<=', end_date)])

            check_in = min([rec.check_in for rec in employee])
            check_out = max([rec.check_out for rec in employee])
            worked_hours = sum([rec.net_worked_hours for rec in employee if not rec.break_time])
            total_worked_hours += worked_hours

            vals = {
                'employee_id': employee.employee_id.name,
                'check_in': check_in + timedelta(hours=3),
                'check_out': check_out + timedelta(hours=3),
                'worked_hours': worked_hours,
                'employee_count': emp['employee_id_count'],
                'hours_per_day': employee.employee_id.resource_calendar_id.hours_per_day,
                'lost_time': (employee.employee_id.resource_calendar_id.hours_per_day - worked_hours) if (

                                                                                                                 employee.employee_id.resource_calendar_id.hours_per_day - worked_hours) > 0 else 0

            }
            new_list.append(vals)

        return {
            'docs': new_list,
            'start_date': datetime.datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S") + timedelta(hours=3),
            'end_date': datetime.datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S") + timedelta(hours=3),
            'worked_hours': total_worked_hours,
            'lst': total_worked_hours,
            'today_date': today_date,

        }