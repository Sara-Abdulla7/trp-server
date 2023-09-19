from datetime import datetime, timedelta
from odoo import models, fields, api
import base64
import io

class createreportxlsx(models.AbstractModel):
    _name = 'report.dynamic_attendance_report.report_xlsx_details'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, sales):
        bold = workbook.add_format({'bold': True})
        format_1 = workbook.add_format({'bold': True, 'align': 'center', 'bg_color': 'yellow'})
        sheet = workbook.add_worksheet("report")
        row = 0
        col = 0
        sheet.set_column('A:G', 20)
        sheet.write(row, col, 'Employee', format_1)
        sheet.write(row, col + 1, 'Check In', format_1)
        sheet.write(row, col + 2, 'Check Out', format_1)
        sheet.write(row, col + 3, 'Work Hours', format_1)        
        

        if data['form']['start_date'] and data['form']['end_date']  and not data['form']['employee_id']:
            partner_list = []
            for t in data['partner']:
                vals = {'worked_hours': t['worked_hours']
                }
                # hours = round(sum(partner_list), 2)
                # minutes = int(hours * 60)
                # time_string = "{:02d}:{:02d}".format(*divmod(minutes, 60))
                partner_list.append(vals['worked_hours'])
            for obj in data['partner']:
                def Check_in():
                    check_in = obj['check_in']
                    convert_check_in = datetime.strptime(check_in, "%Y-%m-%d %H:%M:%S")
                    add_on_check_in = str(convert_check_in + timedelta(hours=3))
                    return add_on_check_in

                def Check_out():
                    check_out = obj['check_out']
                    convert_check_out = datetime.strptime(check_out, "%Y-%m-%d %H:%M:%S")
                    add_on_check_out = str(convert_check_out + timedelta(hours=3))
                    return add_on_check_out

                hours, minutes = divmod(int(obj['worked_hours'] * 60), 60)
                time_obj = (datetime.min + timedelta(hours=hours, minutes=minutes)).time()
                

                sheet.write(row + 1, col, obj['employee_id'][1])
                sheet.write(row + 1, col + 1, Check_in())
                sheet.write(row + 1, col + 2, Check_out())
                sheet.write(row + 1, col + 3, str(time_obj))
                sheet.write(row + 2, col, 'Total Worked Hours', format_1)
                sheet.write(row + 2, col + 3, round(sum(partner_list),2))

                # sheet.write(row + 1, col + 3,round(obj['worked_hours'],2))
                # sheet.write(row + 2, col, 'Total Worked Hours', format_1)
                # sheet.write(row + 2, col + 3,round(sum(partner_list),2))
                row += 1
            
                
        if data['form']['start_date'] and data['form']['end_date'] and data['form']['employee_id']:
            rec_list = []
            for t in data['rec']:
                vals = {
                    'worked_hours': t['worked_hours']

                }
                # time_in_hours = t['worked_hours'] * 24  
                # time_in_hours_rounded = round(time_in_hours, 2)
                rec_list.append(vals['worked_hours'])
            for x in data['rec']:
                def Check_in():
                    check_in = x['check_in']
                    convert_check_in = datetime.strptime(check_in, "%Y-%m-%d %H:%M:%S")
                    add_on_check_in = str(convert_check_in + timedelta(hours=3))
                    return add_on_check_in

                def Check_out():
                    check_out = x['check_out']
                    convert_check_out = datetime.strptime(check_out, "%Y-%m-%d %H:%M:%S")
                    add_on_check_out = str(convert_check_out + timedelta(hours=3))
                    return add_on_check_out
                hours, minutes = divmod(int(x['worked_hours'] * 60), 60)
                time = (datetime.min + timedelta(hours=hours, minutes=minutes)).time()
                

                sheet.write(row + 1, col, x['employee_id'][1])
                sheet.write(row + 1, col + 1, Check_in())
                sheet.write(row + 1, col + 2, Check_out())
                sheet.write(row + 1, col + 3, str(time))

                #sheet.write(row + 1, col + 3,round(x['worked_hours'],2))
                # sheet.write(row + 1, col + 3, time_in_hours_rounded)
                # sheet.write(row + 1, col + 3,round(x['worked_hours'],2))
                sheet.write(row + 2, col, 'Total Worked Hours', format_1)
                sheet.write(row + 2, col + 3,round(sum(rec_list),2))
                row += 1
                





