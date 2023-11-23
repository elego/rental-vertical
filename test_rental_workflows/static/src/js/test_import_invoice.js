odoo.define("rental.invoice", function (require) {
    "use strict";

    var core = require("web.core");
    var tour = require("web_tour.tour");

    var _t = core._t;
    var _wait = "1000";

    tour.register(
        "rental_import_invoice",
        {
            url: "/web",
        },
        [
            tour.stepUtils.showAppsMenuItem(),
            {
                trigger: '.o_app[data-menu-xmlid="muk_dms.main_menu_muk_dms"]',
                content: _t("Go to main menu of Document"),
                position: "right",
            },
            {
                // Li[data-attribute_id]:nth-child(4)
                // div.o_kanban_view.mk_file_kanban_view.o_kanban_small_column.align-content-start.o_kanban_ungrouped > div:nth-child(1) > div.o_dropdown_kanban.dropdown > a > span
                trigger:
                    ".mk_file_kanban_view > div:nth-child(1) > div.o_dropdown_kanban.dropdown > a > span",
                // Extra_trigger: ".mk_file_kanban_view",
                content: _t(
                    "Click here to add some products or services to your quotation."
                ),
                position: "bottom",
                run: "click",
            } /* {
        trigger: ".ui-menu-item > a",
        auto: true,
        in_modal: false,
    },*/ /* {
        trigger: '.o_dropdown_kanban .dropdown-toggle .o-no-caret .btn',
        run: 'click'
    },*/ /* {
        trigger: '.o_dropdown_kanban .dropdown > a',
        content: _t("Let's create new Rental Order."),
        extra_trigger: ".o_dropdown_kanban",
        position: 'bottom',
        run: 'click'
    }, */ /* {
        trigger: ".mk_file_kanban_operations a[data-name='action_import_invoice')",
        // extra_trigger: ".o_dropdown_kanban"
        content: _t("Click here to add some products or services to your quotation."),
        position: "click",
    },*/,
        ]
    );
});
