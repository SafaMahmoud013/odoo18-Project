from odoo import fields, models, api
from odoo.exceptions import ValidationError


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    employee_code = fields.Char(
        string="Employee Code",
        required=True,
        copy=False,
        readonly=True,
        default="New"
    )

    _sql_constraints = [
        (
            'employee_code_unique',
            'unique(employee_code)',
            'Employee Code must be unique.'
        )
    ]

    national_id = fields.Char(
        string="National ID",
        required=True
    )

    passport_number = fields.Char(
        string="Passport Number"
    )

    employment_date = fields.Date(
        string="Joining Date"
    )

    birth_date = fields.Date(
        string="Birth Date"
    )


    insurance_number = fields.Char(
        string="Insurance Number"
    )

    emergency_contact = fields.Char(
        string="Emergency Contact"
    )

    emergency_phone = fields.Char(
        string="Emergency Phone"
    )

    blood_type = fields.Selection([
        ('a+', 'A+'),
        ('a-', 'A-'),
        ('b+', 'B+'),
        ('b-', 'B-'),
        ('ab+', 'AB+'),
        ('ab-', 'AB-'),
        ('o+', 'O+'),
        ('o-', 'O-'),
    ], string="Blood Type")

    marital_status = fields.Selection([
        ('single', 'Single'),
        ('married', 'Married'),
        ('divorced', 'Divorced'),
        ('widowed', 'Widowed'),
    ], string="Marital Status")

    employee_status = fields.Selection(
        [
            ('active', 'Active'),
            ('inactive', 'Inactive'),
        ],
        string="Employee Status",
        compute="_compute_employee_status",
        store=True,
    )

    @api.constrains('national_id')
    def _check_national_id(self):
        for employee in self:
            if employee.national_id:
                duplicate = self.search([
                    ('national_id', '=', employee.national_id),
                    ('id', '!=', employee.id)
                ], limit=1)

                if duplicate:
                    raise ValidationError(
                        ("National ID already exists.")
                    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("employee_code", "New") == "New":
                vals["employee_code"] = self.env["ir.sequence"].next_by_code(
                    "hr.employee.sequence"
                ) or "New"

        return super().create(vals_list)

    @api.depends('active')
    def _compute_employee_status(self):
        for employee in self:
            employee.employee_status = 'active' if employee.active else 'inactive'

    @api.onchange('marital_status')
    def _onchange_marital_status(self):
        if self.marital_status == 'married':
            return {
                'warning': {
                    'title': 'Marital Status',
                    'message': 'Please make sure the employee emergency contact information is completed.'
                }
            }