odoo.define('rental.quality', function (require) {
    "use strict";

    var core = require('web.core');
    var tour = require('web_tour.tour');

    var _t = core._t;
    var _wait = "1000";

    tour.register('rental_return_product_qc', {
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
        extra_trigger: 'ul.ui-autocomplete',
        in_modal: false,
        run: 'click'
    }, {
        content: _t('Set default_start_date to 04/01/2020'),
        trigger: '.o_form_editable .o_datepicker_input[name="default_start_date"]',
        run: 'text 04/01/2020',
        position: 'bottom',
    }, {
        content: _t('Set default_end_date to 04/15/2020'),
        trigger: '.o_form_editable .o_datepicker_input[name="default_end_date"]',
        run: 'text 04/15/2020',
        position: 'bottom',
    },{
        content: _t("Click here to create or add Product"),
        trigger: "a:contains('Add a product')",
        position: "bottom",
    }, {
        trigger: ".o_field_many2one[name='display_product_id'] .o_input_dropdown input",
        run: 'click'
    }, {
        trigger: 'li a:contains("Cat 933M")',
        extra_trigger: 'ul.ui-autocomplete',
        in_modal: false,
        run: 'click'
    }, {
        content: _t('Click on Save & Close'),
        trigger: 'button span:contains(Save & Close)',
        extra_trigger: '.o_act_window',
        run: 'click',
        position: 'bottom',
    }, {
        content: _t('Check total rental time'),
        trigger: 'td.o_data_cell:contains("15.00")',
        extra_trigger: 'div[name="order_line"]',
        in_modal: false,
        position: 'bottom',
        run: function (){} //check (must be diff between 04/01/2020 and 04/15/2020)
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
        trigger: '.btn[name="action_send_mail"]',
        extra_trigger: '.o_act_window',
    }, {
        content: _t("Click Confirm"),
        trigger: 'button[name="action_confirm"]:visible:not(:disabled)',
        extra_trigger: '.o_statusbar_status .btn-primary:contains("Quotation Sent")',
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
    }, 
    // Quality test when WH/OUT/, status : Quality success
    {
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
        content: _t("Click on Inspections"),
        trigger: 'div[name="created_inspections"]',
    }, {
        content: _t('Click on Created Inspection'),
        trigger: 'td.o_data_cell:contains("Rental Generic Test")',
        extra_trigger: '.o_list_view',
        position: 'bottom',
        run: 'click',
    }, {
        content: _t('Check Test Name'),
        trigger: 'tr td a:contains("Rental Generic Test")',
        extra_trigger: '.o_form_readonly',
        in_modal: false,
        position: 'bottom',
        run: function (){} //check (Test: Rental Generic Test)
    }, {
        content: _t('Check Product'),
        trigger: 'a[name="product_id"]:contains("[01533] Cat 933M")',
        extra_trigger: '.o_form_readonly',
        in_modal: false,
        position: 'bottom',
        run: function (){} //check (Product: Cat 933M)
    }, {
        content: _t("Let's write answers for quality test questions."),
        trigger: '.o_form_button_edit',
        position: 'bottom'
    }, {
        trigger: "td.o_data_cell:contains('tire condition')",
        extra_trigger:"div[name='inspection_lines']",
        run: 'click'
    }, {
        trigger: "tr.o_selected_row td div.o_field_many2one[name='qualitative_value'] .o_input_dropdown input",
        extra_trigger:"tr.o_selected_row",
        run: 'click'
    }, {
        trigger: 'ul.ui-autocomplete li a:contains("Good")',
        extra_trigger: 'ul.ui-autocomplete:visible',
        in_modal: false,
        run: 'click'
    }, {
        trigger: "table.o_editable_list tr:nth-child(2) td.o_data_cell:contains('Paint / lettering')",
        extra_trigger:"div[name='inspection_lines']",
        run: 'click'
    }, {
        trigger: "table.o_editable_list tr:nth-child(2) td div.o_field_many2one[name='qualitative_value'] .o_input_dropdown input",
        extra_trigger:"div[name='inspection_lines']",
        run: 'click'
    }, {
        trigger: 'ul.ui-autocomplete li a:contains("Good")',
        extra_trigger: 'ul.ui-autocomplete:visible',
        in_modal: false,
        run: 'click'
    }, {
        trigger: "table.o_editable_list tr:nth-child(3) td.o_data_cell:contains('Scratches / dents')",
        extra_trigger:"div[name='inspection_lines']",
        run: 'click'
    }, {
        trigger: "table.o_editable_list tr:nth-child(3) td div.o_field_many2one[name='qualitative_value'] .o_input_dropdown input",
        extra_trigger:"div[name='inspection_lines']",
        run: 'click'
    }, {
        trigger: 'ul.ui-autocomplete li.ui-menu-item a:contains("No")',
        extra_trigger: 'ul.ui-autocomplete:visible',
        in_modal: false,
        run: 'click'
    }, {
        trigger: "table.o_editable_list tr:nth-child(4) td.o_data_cell:contains('Damage')",
        extra_trigger:"div[name='inspection_lines']",
        run: 'click'
    }, {
        trigger: "table.o_editable_list tr:nth-child(4) td div.o_field_many2one[name='qualitative_value'] .o_input_dropdown input",
        extra_trigger:"div[name='inspection_lines']",
        run: 'click'
    }, {
        trigger: 'ul.ui-autocomplete li.ui-menu-item a:contains("No")',
        extra_trigger: 'ul.ui-autocomplete:visible',
        in_modal: false,
        run: 'click'
    }, {
        content: _t("Confirm quality test questions and answers"),
        trigger: 'button[name="action_confirm"]',
    }, {
        content: _t("Save the quality control test."),
        trigger: '.o_form_button_save',
        extra_trigger: '.o_statusbar_status .btn-primary:contains("Quality success")',
        position: 'bottom',
    }, {
        content: _t("Use the breadcrumbs to <b>go back to your Transfers</b>."),
        trigger: ".breadcrumb-item:not(.active):nth-last-child(4)",
        extra_trigger: '.o_form_view',
        position: "bottom"
    }, 
    // Quality test when WH/IN/, status : Quality success
    {
        content: _t('Click on Incoming Delivery'),
        trigger: 'td.o_data_cell:contains("WH/IN/")',
        extra_trigger: '.o_list_view',
        position: 'bottom',
        run: 'click',
    }, {
        content: _t("Click on Check Availability"),
        trigger: 'button[name="action_assign"]',
        extra_trigger: '.o_statusbar_status .btn-primary:contains("Waiting")',
    },{
        content: _t("Click on Validate"),
        trigger: 'button[name="button_validate"]',
        extra_trigger: '.o_statusbar_status .btn-primary:contains("Ready")',
    }, {
        content: _t('Click on Apply'),
        trigger: 'button span:contains("Apply")',
        extra_trigger: '.o_act_window',
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
        content: _t("Click on Inspections"),
        trigger: 'div[name="created_inspections"]',
    }, {
        content: _t('Click on Created Inspection'),
        trigger: 'td.o_data_cell:contains("Rental Generic Test")',
        extra_trigger: '.o_list_view',
        position: 'bottom',
        run: 'click',
    }, {
        content: _t('Check Test Name'),
        trigger: 'tr td a:contains("Rental Generic Test")',
        extra_trigger: '.o_form_readonly',
        in_modal: false,
        position: 'bottom',
        run: function (){} //check (Test: Rental Generic Test)
    }, {
        content: _t('Check Product'),
        trigger: 'a[name="product_id"]:contains("[01533] Cat 933M")',
        extra_trigger: '.o_form_readonly',
        in_modal: false,
        position: 'bottom',
        run: function (){} //check (Product: Cat 933M)
    },{
        content: _t("Let's write answers for quality test questions."),
        trigger: '.o_form_button_edit',
        position: 'bottom'
    }, {
        trigger: "td.o_data_cell:contains('tire condition')",
        extra_trigger:"div[name='inspection_lines']",
        run: 'click'
    }, {
        trigger: "tr.o_selected_row td div.o_field_many2one[name='qualitative_value'] .o_input_dropdown input",
        extra_trigger:"tr.o_selected_row",
        run: 'click'
    }, {
        trigger: 'ul.ui-autocomplete li a:contains("Good")',
        extra_trigger: 'ul.ui-autocomplete:visible',
        in_modal: false,
        run: 'click'
    }, {
        trigger: "table.o_editable_list tr:nth-child(2) td.o_data_cell:contains('Paint / lettering')",
        extra_trigger:"div[name='inspection_lines']",
        run: 'click'
    }, {
        trigger: "table.o_editable_list tr:nth-child(2) td div.o_field_many2one[name='qualitative_value'] .o_input_dropdown input",
        extra_trigger:"div[name='inspection_lines']",
        run: 'click'
    }, {
        trigger: 'ul.ui-autocomplete li a:contains("Good")',
        extra_trigger: 'ul.ui-autocomplete:visible',
        in_modal: false,
        run: 'click'
    }, {
        trigger: "table.o_editable_list tr:nth-child(3) td.o_data_cell:contains('Scratches / dents')",
        extra_trigger:"div[name='inspection_lines']",
        run: 'click'
    }, {
        trigger: "table.o_editable_list tr:nth-child(3) td div.o_field_many2one[name='qualitative_value'] .o_input_dropdown input",
        extra_trigger:"div[name='inspection_lines']",
        run: 'click'
    }, {
        trigger: 'ul.ui-autocomplete li.ui-menu-item a:contains("No")',
        extra_trigger: 'ul.ui-autocomplete:visible',
        in_modal: false,
        run: 'click'
    }, {
        trigger: "table.o_editable_list tr:nth-child(4) td.o_data_cell:contains('Damage')",
        extra_trigger:"div[name='inspection_lines']",
        run: 'click'
    }, {
        trigger: "table.o_editable_list tr:nth-child(4) td div.o_field_many2one[name='qualitative_value'] .o_input_dropdown input",
        extra_trigger:"div[name='inspection_lines']",
        run: 'click'
    }, {
        trigger: 'ul.ui-autocomplete li.ui-menu-item a:contains("No")',
        extra_trigger: 'ul.ui-autocomplete:visible',
        in_modal: false,
        run: 'click'
    }, {
        content: _t("Confirm quality test questions and answers"),
        trigger: 'button[name="action_confirm"]',
    }, {
        content: _t("Save the quality control test."),
        extra_trigger: '.o_statusbar_status .btn-primary:contains("Quality success")',
        trigger: '.o_form_button_save',
        position: 'bottom',
    }, {
        content: _t('Go to Overview'),
        trigger: 'li a[data-menu-xmlid="rental_timeline.menu_overview"]',
        position: 'bottom'
    },
  ]);
});
