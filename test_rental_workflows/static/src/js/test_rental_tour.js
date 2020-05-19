odoo.define('rental.tour', function (require) {
    "use strict";
 
    var core = require('web.core');
    var tour = require('web_tour.tour');
 
    var _t = core._t;
    var _wait = "1000";

    tour.register('rental_tour', {
        url: "/web",
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
        content: _t('Set default_start_date to 03/01/2020'),
        trigger: '.o_form_editable .o_datepicker_input[name="default_start_date"]',
        run: 'text 03/01/2020',
        position: 'bottom',
    }, {
        content: _t('Set default_end_date to 05/01/2020'),
        trigger: '.o_form_editable .o_datepicker_input[name="default_end_date"]',
        run: 'text 05/01/2020',
        position: 'bottom',
    }, {
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
    },
    // check validation with Off-Days (Off-Day Type : Weekend)
    {
        content: _t('Check Off-Time'),
        trigger: '.o_form_editable td span[name="offday_number"]:contains("0.00")',
        extra_trigger: '.o_form_editable',
        in_modal: false,
        position: 'bottom',
        run: function (){} // check Off-Time : 0.00 Day(s)
    }, {
        content: _t("Click on Off Days"),
        trigger: "div.o_notebook ul li a:contains('Off-Days')",
        position: "bottom",
    }, {
        content: _t("Change Off-Day Type to Weekend"),
        trigger: '.o_notebook select[name="fixed_offday_type"]',
        extra_trigger: '.o_notebook',
        run: function (){
            var inputValue = $('.o_notebook select[name="fixed_offday_type"] option:last-child').val();
            $('.o_notebook select[name="fixed_offday_type"]').val(inputValue);
            $('.o_notebook select[name="fixed_offday_type"]').trigger('change');
        }
    }, {
        content: _t('Check Off-Time'),
        trigger: '.o_form_editable td span[name="offday_number"]:contains("17.00")',
        extra_trigger: '.o_notebook',
        in_modal: false,
        position: 'bottom',
        run: function (){} // check Off-Time : 17 Day(s)(total number of weekend days from 03/01/2020 to 05/01/2020)
    }, {
        content: _t("Click to add line of additional days off"),
        trigger: "div[name='add_offday_ids'] a:contains('Add a line')",
        extra_trigger: 'div[name="add_offday_ids"]',
        run: 'click',
        position: "bottom",
    }, {
        content: _t('Add additional off-days to 03/13/2020'),
        trigger: 'div[name="add_offday_ids"] .o_datepicker_input[name="date"]',
        run: 'text 03/13/2020',
        position: 'bottom',
    }, {
        content: _t('Add additional off-days Description'),
        trigger: 'div[name="add_offday_ids"] input[name="name"]',
        run: 'text Public Holiday',
        position: 'bottom',
    }, {
        content: _t('Check Off-Time'),
        trigger: '.o_form_editable td span[name="offday_number"]:contains("18.00")',
        extra_trigger: '.o_notebook',
        in_modal: false,
        position: 'bottom',
        run: function (){} //check Off-Time : 17 + 1 = 18 Day(s)
    },{
        content: _t('Click on Save & Close'),
        trigger: 'button span:contains(Save & Close)',
        extra_trigger: '.o_act_window',
        id: "rental_product_selected",
        run: 'click',
        position: 'bottom',
    }, {
        content: _t('Check Ordered Qty'),
        trigger: 'td.o_data_cell:contains("44.00")',
        extra_trigger: 'div[name="order_line"]',
        in_modal: false,
        position: 'bottom',
        run: function (){} //check Ordered Qty: 44 = [62 - (17 + 1)], where 62=diff(05/01/2020 - 03/01/2020)
    }, {
        content: _t('Check Unit of measure'),
        trigger: 'td.o_data_cell:contains("Day(s)")',
        extra_trigger: 'div[name="order_line"]',
        in_modal: false,
        position: 'bottom',
        run: function (){} //check Unit of measure : Day(s)
    }, {
        content: _t('Check Unit Price'),
        trigger: 'td.o_data_cell:contains("200.00")',
        extra_trigger: 'div[name="order_line"]',
        in_modal: false,
        position: 'bottom',
        run: function (){} //check Unit Price : 200.00
    },
    // check validation without Off-Days (Off-Day Type : None)
    {
        content: _t("Click on line to edit"),
        trigger: "div[name='order_line'] tr.o_data_row span[name='product_id']",
        extra_trigger: 'div[name="order_line"]',
        run: 'click',
        position: "bottom",
    }, {
        content: _t("Change Off-Day Type to None"),
        trigger: '.o_notebook select[name="fixed_offday_type"]',
        extra_trigger: '.o_notebook',
        run: function (){
            var inputValue = $('.o_notebook select[name="fixed_offday_type"] option:nth-last-child(2)').val();
            $('.o_notebook select[name="fixed_offday_type"]').val(inputValue);
            $('.o_notebook select[name="fixed_offday_type"]').trigger('change');
        }
    }, {
        content: _t('Remove Additional Off Days line'),
        trigger: 'div[name="add_offday_ids"] td.o_list_record_remove button[name="delete"]',
        extra_trigger: 'div[name="add_offday_ids"]',
        run: 'click',
        position: 'bottom',
    }, {
        content: _t('Check Off-Time'),
        trigger: '.o_form_editable td span[name="offday_number"]:contains("0.00")',
        extra_trigger: '.o_form_editable',
        in_modal: false,
        position: 'bottom',
        run: function (){} // check Off-Time : 0.00 Day(s)
    }, {
        content: _t('Click on Save & Close'),
        trigger: 'button span:contains(Save & Close)',
        extra_trigger: '.o_act_window',
        id: "rental_product_selected",
        run: 'click',
        position: 'bottom',
    }, {
        content: _t('Check Ordered Qty'),
        trigger: 'td.o_data_cell:contains("62.00")',
        extra_trigger: 'div[name="order_line"]',
        in_modal: false,
        position: 'bottom',
        run: function (){} //check Ordered Qty: 62 = diff(05/01/2020 - 03/01/2020)
    }, {
        content: _t('Check Unit of measure'),
        trigger: 'td.o_data_cell:contains("Day(s)")',
        extra_trigger: 'div[name="order_line"]',
        in_modal: false,
        position: 'bottom',
        run: function (){} //check Unit of measure : Day(s)
    }, {
        content: _t('Check Unit Price'),
        trigger: 'td.o_data_cell:contains("200.00")',
        extra_trigger: 'div[name="order_line"]',
        in_modal: false,
        position: 'bottom',
        run: function (){} //check Unit Price : 200.00
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
        trigger: 'button[name="action_confirm"]:visible:not(:disabled)',
    }, {
        content: _t("Click on Delivery"),
        trigger: 'button[name="action_view_delivery"]',
    }, {
        content: _t('Check Outgoing Delivery'),
        trigger: 'td.o_data_cell:contains("WH/OUT/")',
        extra_trigger: '.o_list_view',
        in_modal: false,
        position: 'bottom',
        run: function (){} //check there must be OUT deleivery
    }, {
        content: _t('Check Incoming Delivery'),
        trigger: 'td.o_data_cell:contains("WH/IN/")',
        extra_trigger: '.o_list_view',
        in_modal: false,
        position: 'bottom',
        run: function (){} //check there must be IN deleivery
    }, {
        content: _t('Click on Outgoing Delivery'),
        trigger: 'td.o_data_cell:contains("WH/OUT/")',
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
    },
    // TODO checks on analytic account of product in invoice line
    /*{
        content: _t('Click on Validate'),
        trigger: 'button[name="action_invoice_open"]',
        position: 'bottom',
    },*/
    {
        content: _t('Go to Overview'),
        trigger: 'li a[data-menu-xmlid="rental_timeline.menu_overview"]',
        position: 'bottom'
    },
  ]);
});
