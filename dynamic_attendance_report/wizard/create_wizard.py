from datetime import datetime, timedelta
from odoo import models, fields, api, exceptions, _
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta 


class CreateWizard(models.TransientModel):
  _name = 'create.wizard'
  _description = "Wizard Create"

  start_date = fields.Datetime(required=True, string="Start Date")
  end_date = fields.Datetime(required=True, string="End Date")
  employee_id = fields.Many2one('hr.employee',string="Employee")

  # def send_email_template(self):
  #       self.env.ref("dynamic_attendance_report.email_template_attendance").send_mail(self.id, force_send=True)



  # func for print excel 
  def action_print_excel_report(self):
    partner = self.env['hr.attendance'].search_read([('check_in', '>=', self.start_date),
                                                         ('check_out', '<=', self.end_date)])
    rec = self.env['hr.attendance'].search_read([('check_in', '>=', self.start_date),
                                                    ('check_out', '<=', self.end_date),
                                                    ('employee_id.id', '=', self.employee_id.id)])
    data = {
            'form': self.read()[0],
            'partner': partner,
            'rec': rec
        }
    return self.env.ref('dynamic_attendance_report.report_details_xlsx').report_action(self, data=data)

     

  #func for print pdf
  def action_print_pdf(self):



      data = {
       'ids': self.ids,
       'model': self._name,
       #'total_hours': self.calculate_total_hours(),
       'form': {
       'start_date':self.start_date,
       'end_date': self.end_date,
       'employee_id': self.employee_id.id
    },
    }
      return self.env.ref('dynamic_attendance_report.report_pdf_details').report_action(self, data=data)
    
class createreportpdf(models.AbstractModel):
  _name = 'report.dynamic_attendance_report.report_details_pdf'


  @api.model
  def _get_report_values(self, docids, data=None):

    domain=[]
    if data['form']['employee_id']:
        domain +=[('employee_id.id', '=', data['form']['employee_id'])]
    if data['form']['start_date']:
        domain +=[('check_in', '>=', data['form']['start_date'])]
    if data['form']['end_date']:
        domain +=[('check_out', '<=', data['form']['end_date'])]
        
    print('domain',domain)    
    atte = self.env['hr.attendance']._read_group(domain=domain, fields=[], groupby=['employee_id'])
    print('test',atte) 
    print('kkkkk',len(atte))
    new_list=[]
    total_worked_hours=0
    for emp in atte:
        ff=self.env['hr.attendance'].search([('employee_id.id','=',emp['employee_id'][0]),('check_in', '>=', data['form']['start_date']),('check_out', '<=', data['form']['end_date'])])
        print('ppppp',ff)
        check_in=min([rec.check_in for rec in ff])
        print(check_in)
        check_out=max([rec.check_out for rec in ff])
        print(check_out)
        worked_hours=sum([rec.worked_hours for rec in ff])

        print(worked_hours)
        total_worked_hours +=worked_hours


        vals={
                'employee_id': ff.employee_id.name,
                'check_in': check_in + timedelta(hours=3),
                'check_out': check_out + timedelta(hours=3),
                'worked_hours': worked_hours,
                'employee_count':emp['employee_id_count'],
                'hours_per_day':ff.employee_id.resource_calendar_id.hours_per_day,
                'test_col':(ff.employee_id.resource_calendar_id.hours_per_day - worked_hours) if (ff.employee_id.resource_calendar_id.hours_per_day - worked_hours) >0 else 0
        }
        print(vals)
        new_list.append(vals)
    



    
    # if data['form']['start_date'] and data['form']['end_date'] and not data['form']['employee_id']:
    #     docs = self.env['hr.attendance'].search([('check_in', '>=', data['form']['start_date']),('check_out', '<=', data['form']['end_date'])])
            

    # if data['form']['start_date'] and data['form']['end_date'] and data['form']['employee_id']:
    #     docs = self.env['hr.attendance'].search([('check_in', '>=', data['form']['start_date']),
    #                                                 ('check_out', '<=', data['form']['end_date']),
    #                                                 ('employee_id.id', '=', data['form']['employee_id'])])
        
            
       
        
    # lst = []
    # for t in docs:
    #     vals = {
                
    #             'worked_hours': t.worked_hours
              
        
    #         }
    #     lst.append(vals['worked_hours'])

    # docs_list = []
    # for x in docs:
    #     vals = {
    #             'employee_id': x.employee_id.name,
    #             'check_in': x.check_in + timedelta(hours=3),
    #             'check_out': x.check_out + timedelta(hours=3),
    #             'worked_hours': x.worked_hours,
               
            
    #     }
    #     docs_list.append(vals)

    start = data['form']['start_date']
    end = data['form']['end_date']
        

    start_date = datetime.strptime(start, "%Y-%m-%d %H:%M:%S") + timedelta(hours=3)
    end_date = datetime.strptime(end, "%Y-%m-%d %H:%M:%S") + timedelta(hours=3)
       


    



    return {
            'doc_model': 'create.wizard',
            'docs': new_list,
            'start_date':start_date,
            'end_date': end_date,
            # 'worked_hours':[(rec.worked_hours for rec in docs)],
            'worked_hours':total_worked_hours,
            # 'lst':sum(lst),
            'lst':total_worked_hours,

            
            
        }

    @api.constrains('start_date','end_date')
    def _date_check(self):
        for r in self:
            if r.start_date > r.end_date:
                raise ValidationError("The Start date must be less than End date")

   

                                                                                