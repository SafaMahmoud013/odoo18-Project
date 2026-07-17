from odoo import models, fields


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
        ('0', 'Low'),
        ('1', 'Medium'),
        ('2', 'High'),
    ], string="Priority", default='1')

class TodoEmployee(models.Model):
    _name = "todo.employee"

    name = fields.Char(required=True)