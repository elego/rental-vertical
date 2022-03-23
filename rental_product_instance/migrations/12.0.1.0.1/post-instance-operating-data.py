from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    instances = env["product.product"].search(
        [
            ("product_instance", "=", True),
            ("show_instance_condition_type", "in", ("km", "hour")),
            "|",
            ("instance_condition_km", "!=", ""),
            ("instance_condition_hour", "!=", ""),
        ]
    )
    operating_data_obj = env["instance.operating.data"]
    for instance in instances:
        vals = {
            "instance_id": instance.id,
            "date": instance.instance_condition_date,
        }
        if instance.show_instance_condition_type == "km":
            vals["operating_data"] = instance.instance_condition_km
        elif instance.show_instance_condition_type == "hour":
            vals["operating_data"] = instance.instance_condition_hour
        operating_data_obj.create(vals)
