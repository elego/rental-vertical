# Part of rental-vertical See LICENSE file for full copyright and licensing details.

from odoo import models


class ProjectTask(models.Model):
    _inherit = "project.task"

    def name_get(self):
        result = []
        for record in self:
            if record.date_deadline:
                result.append(
                    (record.id, "%s [%s]" % (record.name, record.date_deadline))
                )
            else:
                result.append((record.id, record.name))
        return result
