odoo.define('rental.tour', function (require) {
    "use strict";
 
    var core = require('web.core');
    var tour = require('web_tour.tour');
    // var base = require("web_editor.base");
 
    var _t = core._t;
    var _wait = "1000";
 
    tour.register('rental_tour', {
        url: "/web",
        // wait_for: base.ready(),
        // test: true
    }, [tour.STEPS.SHOW_APPS_MENU_ITEM, {
        content: _t('Go to main menu of rental'),
        trigger: '.o_app[data-menu-xmlid="rental_base.menu_rental_root"]',
        position: 'bottom',
        width: 200
    }, {
        content: _t('Go to top menu of customer'),
        trigger: 'li a[data-menu-xmlid="rental_base.menu_top_customer"]',
        position: 'bottom'
    }, {
        content: _t('Go to menu rental quotation'),
        trigger: 'a[data-menu-xmlid="rental_base.menu_rental_quotations"]',
        position: 'bottom'
    }, {
        content: _t("Let's create new Rental Order."),
        trigger: '.o_list_button_add',
        position: 'bottom'
    }, {
        content: _t("Create or select Customer"),
        trigger: ".o_form_editable .o_field_many2one[name='partner_id'] .o_input_dropdown input",
        position: "bottom",
        run: 'click'
    }, {
        trigger: 'li a:contains("Azure Interior")',
        in_modal: false,
        extra_trigger: 'ul.ui-autocomplete',
        run: 'click'
    }, {
        content: _t('Set default_start_date to 05/01/2020'),
        trigger: '.o_form_editable .o_datepicker_input[name="default_start_date"]',
        run: 'text 03/01/2020',
        position: 'bottom',
    }, {
        content: _t('Set default_end_date to 07/01/2020'),
        trigger: '.o_form_editable .o_datepicker_input[name="default_end_date"]',
        run: 'text 05/01/2020',
        position: 'bottom',
    },{
        content: _t("Click here to create or add Product"),
        trigger: "a:contains('Add a product')",
        position: "bottom",
    }, {
        trigger: ".o_field_many2one[name='display_product_id'] .o_input_dropdown input",
        run: 'click'
    }, {
        trigger: 'li a:contains("Volvo L110H")',
        in_modal: false,
        extra_trigger: 'ul.ui-autocomplete',
        run: 'click'
    }, {
        content: _t('Click on Save & Close'),
        trigger: 'button span:contains(Save & Close)',
        extra_trigger: '.o_act_window',
        id: "rental_product_selected",
        run: 'click',
        position: 'bottom',
    }, {
        content: _t('Check total rental time'),
        trigger: 'td.o_data_cell:contains("62.00")',
        extra_trigger: 'div[name="order_line"]',
        in_modal: false,
        position: 'bottom',
        run: function (){} //check (must be diff between 05/01/2020 and 07/01/2020)
    }, {
        content: _t('Check Unit of measure'),
        trigger: 'td.o_data_cell:contains("Day(s)")',
        extra_trigger: 'div[name="order_line"]',
        in_modal: false,
        position: 'bottom',
        run: function (){} //check (must be Day(s))
    }, {
        content: _t('Check Unit Price'),
        trigger: 'td.o_data_cell:contains("200.00")',
        extra_trigger: 'div[name="order_line"]',
        in_modal: false,
        position: 'bottom',
        run: function (){} //check
    }, {
        content: _t('Save Rental Order'),
        trigger: '.o_form_button_save',
        position: 'bottom',
    }, {
        content: _t("Click Send by email"),
        trigger: 'button[name="action_quotation_send"]:visible:not(:disabled)',
    }, {
        content: _t("Click Send"),
        extra_trigger: '.o_act_window',
        trigger: '.btn[name="action_send_mail"]',
    }, {
        content: _t("Click Confirm"),
        extra_trigger: '.o_statusbar_status .btn-primary:contains("Quotation Sent")',
        trigger: 'button[name="action_confirm"]',
    }, {
        content: _t("Click on Delivery"),
        trigger: 'button[name="action_view_delivery"]',
    }, {
        content: _t('Check Outgoing Delivery'),
        trigger: 'td.o_data_cell:contains("Rental/Rental Out")',
        extra_trigger: '.o_list_view',
        in_modal: false,
        position: 'bottom',
        run: function (){} //check there must be OUT deleivery
    }, {
        content: _t('Check Incoming Delivery'),
        trigger: 'td.o_data_cell:contains("Rental/Rental In")',
        extra_trigger: '.o_list_view',
        in_modal: false,
        position: 'bottom',
        run: function (){} //check there must be IN deleivery
    }, {
        content: _t('Click on Outgoing Delivery'),
        trigger: 'td.o_data_cell:contains("Rental/Rental Out")',
        extra_trigger: '.o_list_view',
        position: 'bottom',
        run: 'click',
    }, {
        content: _t("Click on Validate"),
        trigger: 'button[name="button_validate"]',
    }, {
        content: _t('Click on Apply'),
        trigger: 'button span:contains("Apply")',
        extra_trigger: '.o_act_window',
        id: "rental_product_out",
        run: 'click',
        position: 'bottom',
    }, {
        content: _t('Check Done Quantity'),
        trigger: 'td.o_data_cell:contains("1.000")',
        extra_trigger: 'div[name="move_ids_without_package"]',
        in_modal: false,
        position: 'bottom',
        run: function (){} //check Done: 1.0 Unit(s)
    }, {
        content: _t("Use the breadcrumbs to <b>go back to your Transfer</b>."),
        trigger: ".breadcrumb-item:not(.active):nth-last-child(3)",
        extra_trigger: '.o_form_view',
        position: "bottom"
    }, {
        content: _t("Click on Create Invoice"),
        trigger: '.o_statusbar_buttons button span:contains("Create Invoice")',
    }, {
        content: _t('Click on Create and View Invoice'),
        trigger: 'button[name="create_invoices"]',
        extra_trigger: '.o_act_window',
        id: "rental_product_invoice",
        run: 'click',
        position: 'bottom',
    }, {
        content: _t('Check Sale Type on Invoice'),
        trigger: '.o_invoice_form a[name="sale_type_id"]:contains("Rental Order")',
        in_modal: false,
        position: 'bottom',
        run: function (){} //check Invoice: Sale Type = Rental Order
    }, {
        content: _t('Check Service Period from'),
        trigger: '.o_invoice_form span[name="date_start"]:contains("03/01/2020")',
        in_modal: false,
        position: 'bottom',
        run: function (){} //check Invoice: Service Period from 03/01/2020
    }, {
        content: _t('Check Service Period to'),
        trigger: '.o_invoice_form span[name="date_end"]:contains("05/01/2020")',
        in_modal: false,
        position: 'bottom',
        run: function (){} //check Invoice: Service Period to 05/01/2020
    }, {
        content: _t('Check total rental time on Invoice'),
        trigger: 'td.o_data_cell:contains("62.00")',
        extra_trigger: 'div[name="invoice_line_ids"]',
        in_modal: false,
        position: 'bottom',
        run: function (){} //check Invoice: (Rental Time : 62 days)
    }, {
        content: _t('Check Unit of measure on Invoice'),
        trigger: 'td.o_data_cell:contains("Day(s)")',
        extra_trigger: 'div[name="invoice_line_ids"]',
        in_modal: false,
        position: 'bottom',
        run: function (){} //check Invoice: (Uom : Day(s))
    }, {
        content: _t('Check Unit Price on Invoice'),
        trigger: 'td.o_data_cell:contains("200.00")',
        extra_trigger: 'div[name="invoice_line_ids"]',
        in_modal: false,
        position: 'bottom',
        run: function (){} //check Invoice: (Unit Price : 200.00)
    }, /*{
        content: _t('Click on Validate'),
        trigger: 'button[name="action_invoice_open"]',
        position: 'bottom',
    },*/
  ]);
});
