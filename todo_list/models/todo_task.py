from odoo import models, fields, api
from datetime import date


class TodoTask(models.Model):
    _name = "todo.task"
    _description = "To Do Task"

    name = fields.Char(string='Task Name')
    assigned_to = fields.Many2one('todo.employee', string='Assigned To')
    description = fields.Text()
    due_date = fields.Date()
    status = fields.Selection([
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ],
        default='new'
    )
    priority = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ], string="Priority", default="medium")
    is_overdue = fields.Boolean(
        string="Overdue",
        compute="_compute_is_overdue"
    )

    @api.depends("due_date", "status")
    def _compute_is_overdue(self):
        today = fields.date.today()

        for record in self:
            record.is_overdue = (
                    record.due_date
                    and record.due_date < today
                    and record.status != "completed"
            )


class TodoEmployee(models.Model):
    _name = "todo.employee"

    name = fields.Char(required=True)
