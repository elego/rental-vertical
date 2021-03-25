import base64

from odoo import api, fields, models
from odoo.tools import pycompat


class MailTemplate(models.Model):
    _inherit = "mail.template"

    @api.multi
    def generate_email(self, res_ids, fields=None):
        res = super(MailTemplate, self).generate_email(res_ids, fields)
        multi_mode = True
        if isinstance(res_ids, pycompat.integer_types):
            res_ids = [res_ids]
            multi_mode = False

        res_ids_to_templates = self.get_email_template(res_ids)
        for res_id in res_ids:
            related_model = self.env[self.model_id.model].browse(res_id)

            if related_model._name == "account.invoice":
                template = res_ids_to_templates[res_id]
                inv_print_name = self._render_template(
                    template.report_name, template.model, res_id
                )
                new_attachments = []
                # check Customer Invoice and has Toll Charge Lines
                if related_model.type == "out_invoice" and related_model.toll_line_ids:
                    # We add an attachment for Toll Collect
                    toll_report_name = "TOLL-" + inv_print_name + ".pdf"
                    toll_pdf = self.env.ref(
                        "rental_toll_collect.toll_charge_lines"
                    ).render_qweb_pdf([res_id])[0]
                    toll_pdf = base64.b64encode(toll_pdf)
                    new_attachments.append((toll_report_name, toll_pdf))

                attachments_list = (
                    multi_mode
                    and res[res_id].get("attachments", False)
                    or res.get("attachments", False)
                )
                if attachments_list:
                    attachments_list.extend(new_attachments)
                else:
                    res[res_id]["attachments"] = new_attachments
        return res
