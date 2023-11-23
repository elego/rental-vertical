odoo.define("activate_toll_charge_invoicing.tour", function (require) {
    "use strict";

    var core = require("web.core");
    var tour = require("web_tour.tour");

    var _t = core._t;
    var _wait = "1000";

    tour.register(
        "activate_toll_charge_invoicing_tour",
        {
            test: true,
            url: "/web",
        },
        [
            tour.stepUtils.showAppsMenuItem(),
            {
                content: _t("Go to main menu Rental"),
                trigger: '.o_app[data-menu-xmlid="rental_base.menu_rental_root"]',
                position: "bottom",
                width: 200,
            },
            {
                content: _t("Go to menu of rental > configuration"),
                trigger: 'li a[data-menu-xmlid="rental_base.menu_config"]',
                position: "bottom",
            },
            {
                content: _t("Go to menu of rental > configuration > settings"),
                trigger: 'li a[data-menu-xmlid="rental_base.menu_settings"]',
                position: "bottom",
                timeout: 30000,
            },
            {
                content: _t("Set automatic invoicing of toll charges to True"),
                trigger:
                    'div.o_field_boolean[name="automatic_toll_charge_invoicing"] input[type="checkbox"]',
                extra_trigger: '.o_control_panel:contains("Settings")',
                run: function () {
                    $(
                        'div.o_field_boolean[name="automatic_toll_charge_invoicing"] input[type="checkbox"]'
                    ).prop("checked", true);
                    $(
                        'div.o_field_boolean[name="automatic_toll_charge_invoicing"] input[type="checkbox"]'
                    ).trigger("change");
                    $('.o_statusbar_buttons button[name="execute"]').click();
                },
            },
        ]
    );
});
