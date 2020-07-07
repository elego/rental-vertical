odoo.define('rental.contract', function (require) {
    "use strict";

    var core = require('web.core');
    var tour = require('web_tour.tour');

    var _t = core._t;
    var _wait = "1000";

    tour.register('rental_contract_tour', {
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
        trigger: 'li a:contains("Deco Addict")',
        in_modal: false,
        extra_trigger: 'ul.ui-autocomplete',
        run: 'click'
    }, {
        content: _t('Set default_start_date to 04/01/2020'),
        trigger: '.o_form_editable .o_datepicker_input[name="default_start_date"]',
        run: 'text 04/01/2020',
        position: 'bottom',
    }, {
        content: _t('Set default_end_date to 08/01/2020'),
        trigger: '.o_form_editable .o_datepicker_input[name="default_end_date"]',
        run: 'text 08/01/2020',
        position: 'bottom',
    }, {
        content: _t("Click here to create or add Product"),
        trigger: "a:contains('Add a product')",
        position: "bottom",
    }, {
        trigger: ".o_field_many2one[name='display_product_id'] .o_input_dropdown input",
        run: 'click'
    }, {
        trigger: 'li a:contains("Cat 930M")',
        in_modal: false,
        extra_trigger: 'ul.ui-autocomplete',
        run: 'click'
    }, {
        trigger: ".o_field_many2one[name='product_uom'] .o_input_dropdown input",
        extra_trigger: ".o_field_many2one[name='display_product_id'] .o_external_button",
        run: 'click'
    }, {
        trigger: 'li a:contains("Month(s)")',
        in_modal: false,
        extra_trigger: 'ul.ui-autocomplete',
        run: 'click'
    }, {
        content: _t('Click on Save & Close'),
        trigger: 'button span:contains(Save & Close)',
        extra_trigger: '.o_act_window',
        run: 'click',
        position: 'bottom',
    }, {
        content: _t('Check total rental time'),
        trigger: 'td.o_data_cell:contains("4.00")',
        extra_trigger: 'div[name="order_line"]',
        in_modal: false,
        position: 'bottom',
        run: function (){} //check (must be diff between 04/01/2020 and 08/01/2020)
    }, {
        content: _t('Check Unit of measure'),
        trigger: 'td.o_data_cell:contains("Month(s)")',
        extra_trigger: 'div[name="order_line"]',
        in_modal: false,
        position: 'bottom',
        run: function (){} //check (must be Month(s))
    }, {
        content: _t('Check Unit Price'),
        trigger: 'td.o_data_cell:contains("4,500.00")',
        extra_trigger: 'div[name="order_line"]',
        in_modal: false,
        position: 'bottom',
        run: function (){} //check
    }, {
        content: _t('Save Rental Order'),
        trigger: '.o_form_button_save',
        position: 'bottom',
    }, {
        content: _t("Click on line to"),
        trigger: "tr.o_data_row",
        extra_trigger: 'div.o_form_readonly',
        run: 'click',
        position: "bottom",
    }, {
        content: _t('Check End Date'),
        trigger: 'span[name="end_date"]:contains("08/01/2020")',
        in_modal: false,
        position: 'bottom',
        run: function (){
            if ($('span[name="date_end"]:contains("08/01/2020")').length) {
                console.log('Check date_end successfully.');
            } else {
                console.error('Check date_end unsuccessfully');
            }
        } //check End Date = Date End 08/01/2020 (#3748)
    }, {
        content: _t('Click Button Close'),
        trigger: 'i.fa-close',
        in_modal: false,
    }, {
        content: _t("Click Print"),
        trigger: 'button[name="print_quotation"]:visible:not(:disabled)',
    }, {
        content: _t("Click Confirm"),
        extra_trigger: '.o_statusbar_status .btn-primary:contains("Quotation Sent")',
        trigger: 'button[name="action_confirm"]:visible:not(:disabled)',
    }, {
        content: _t("Click on Contracts"),
        trigger: 'button[name="action_show_contracts"]',
        extra_trigger: '.o_statusbar_status .btn-primary:contains("Sales Order")'
    }, {
        content: _t('Check Contract Type'),
        trigger: '.o_form_view span[name="contract_type"]:contains("Customer")',
        in_modal: false,
        position: 'bottom',
        run: function (){} //check Contract: Contract Type = Customer
    }, {
        content: _t('Check Contract Subtype'),
        trigger: '.o_form_view a[name="type_id"]:contains("Rental Contract")',
        extra_trigger: 'div[name="contract_line_ids"]',
        in_modal: false,
        position: 'bottom',
        run: function (){} //check Contract: Contract Subtype = Rental Contract
    }, {
        content: _t("Click on contract line"),
        trigger: "tr.o_data_row",
        run: 'click',
        position: "bottom",
    }, {
        content: _t('Check Analytic Account'),
        trigger: 'a[name="analytic_account_id"]:contains("[01532] Cat 930M")',
        in_modal: false,
        position: 'bottom',
        run: function (){}
    }, {
        content: _t('Click Button Close'),
        trigger: 'i.fa-close',
        in_modal: false,
    }, /*{
        content: _t('Check Analytic Account on Invoice'),
        trigger: '.o_form_view span[name="analytic_account_id"]:contains("[01532] Cat 930M")',
        extra_trigger: 'div[name="contract_line_ids"]',
        in_modal: false,
        position: 'bottom',
        run: function (){} //check Contract: (Analytic Account : [01532] Cat 930M)
    }, */{
        content: _t('Check Date of Next Invoice'),
        trigger: '.o_form_view span[name="recurring_next_date"]:contains("04/01/2020")',
        extra_trigger: 'div[name="contract_line_ids"]',
        in_modal: false,
        position: 'bottom',
        run: function (){} //check Contract: Date of Next Invoice = 04/01/2020
    }, {
        content: _t('Check Date Start on contract line'),
        trigger: 'td.o_data_cell:contains("04/01/2020")',
        extra_trigger: 'div[name="contract_line_ids"]',
        in_modal: false,
        position: 'bottom',
        run: function (){} //check Contract Line: Date Start = 04/01/2020
    }, {
        content: _t('Check Date End on contract line'),
        trigger: 'td.o_data_cell:contains("08/01/2020")',
        extra_trigger: 'div[name="contract_line_ids"]',
        in_modal: false,
        position: 'bottom',
        run: function (){} //check Contract Line: Date End = 07/31/2020 (1 day before)
    },
    // TODO checks on analytic account of product in contract line
    {
        content: _t("Use the breadcrumbs to <b>go back to your Rental Order</b>."),
        trigger: ".breadcrumb-item:not(.active):last",
        extra_trigger: '.o_form_view',
        position: "bottom"
    }, {
        content: _t("Click on Delivery"),
        trigger: 'button[name="action_view_delivery"]',
        extra_trigger: '.o_form_view',
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
        content: _t("Use the breadcrumbs to <b>go back to Rental Order</b>."),
        trigger: ".breadcrumb-item:not(.active):nth-last-child(3)",
        extra_trigger: '.o_form_view',
        position: "bottom"
    }, {
        content: _t("Click on Contracts"),
        trigger: 'button[name="action_show_contracts"]',
        extra_trigger: '.o_statusbar_status .btn-primary:contains("Sales Order")',
    }, {
        content: _t('Go to menu of Settings'),
        trigger: 'li a[data-menu-xmlid="base.menu_administration"]',
        position: 'bottom',
    }, {
        content: _t('Click on Activate the developer mode'),
        trigger: 'div.form-row a:contains("Activate the developer mode")',
        position: 'bottom',
    }, {
        content: _t('Go to main menu of Rental'),
        trigger: '.mk_apps_sidebar li a[data-menu-xmlid="rental_base.menu_rental_root"]',
        extra_trigger: 'a.o_menu_brand:contains("Discuss")',
        position: 'bottom',
    }, {
        content: _t('Go to top menu of Customer'),
        trigger: 'li a[data-menu-xmlid="rental_base.menu_top_customer"]',
        extra_trigger: 'a.o_menu_brand:contains("Rentals")',
        position: 'bottom'
    }, {
        content: _t('Go to menu Rental Orders'),
        trigger: 'a[data-menu-xmlid="rental_base.menu_rental_orders"]',
        position: 'bottom'
    },
    // Here click on first record of rental order which is our record of this tour
    {
        content: _t('Click on Rental Order who has 04/01/2020'),
        trigger: 'table.o_list_view tbody tr:first-child',
        extra_trigger: '.o_list_view',
        position: 'bottom',
        run: 'click',
    }, {
        content: _t("Click on Contracts"),
        trigger: 'button[name="action_show_contracts"]',
        extra_trigger: '.o_statusbar_status .btn-primary:contains("Sales Order")',
    },{
        content: _t("Click on Create Invoice"),
        trigger: 'button[name="recurring_create_invoice"]',
        extra_trigger: '.o_form_view',
    }, {
        content: _t('Click on Invoices'),
        trigger: 'button[name="action_show_invoices"]',
        extra_trigger: 'div[name="invoice_count"] span.o_stat_value:contains("1")',
        run: 'click',
        position: 'bottom',
    }, {
        content: _t('Check status of Invoice which is created on 04/01/2020'),
        trigger: 'td.o_data_cell:contains("Draft")',
        extra_trigger: '.o_list_view',
        in_modal: false,
        position: 'bottom',
        run: function (){} //check Invoice: Status = Draft
    }, {
        content: _t('Click on Invoice from list which is created on 04/01/2020'),
        trigger: 'td.o_data_cell:contains("04/01/2020")',
        extra_trigger: '.o_list_view',
        position: 'bottom',
        run: 'click',
    }, {
        content: _t('Check Sale Type on Invoice'),
        trigger: '.o_invoice_form a[name="sale_type_id"]:contains("Rental Order")',
        in_modal: false,
        position: 'bottom',
        run: function (){} //check Invoice: Sale Type = Rental Order
    }, {
        content: _t('Check Contract Type on Invoice'),
        trigger: '.o_invoice_form a[name="contract_type_id"]:contains("Rental Contract")',
        in_modal: false,
        position: 'bottom',
        run: function (){} //check Invoice: Contract Type = Rental Contract
    }, {
        content: _t('Check Invoice Date on Invoice'),
        trigger: 'td span[name="date_invoice"]:contains("04/01/2020")',
        extra_trigger: '.o_invoice_form',
        in_modal: false,
        position: 'bottom',
        run: function (){} //check Invoice: Invoice Date = 04/01/2020
    }, {
        content: _t('Check total rental time on Invoice'),
        trigger: 'td.o_data_cell:contains("1.000")',
        extra_trigger: 'div[name="invoice_line_ids"]',
        in_modal: false,
        position: 'bottom',
        run: function (){} //check Invoice: (Rental Time : 1 month)
    }, {
        content: _t('Check Unit of measure on Invoice'),
        trigger: 'td.o_data_cell:contains("Month(s)")',
        extra_trigger: 'div[name="invoice_line_ids"]',
        in_modal: false,
        position: 'bottom',
        run: function (){} //check Invoice: (Uom : Month(s))
    }, {
        content: _t('Check Unit Price on Invoice'),
        trigger: 'td.o_data_cell:contains("4,500.00")',
        extra_trigger: 'div[name="invoice_line_ids"]',
        in_modal: false,
        position: 'bottom',
        run: function (){} //check Invoice: (Unit Price : 4,500.00)
    }, {
        content: _t('Check Analytic Account on Invoice'),
        trigger: 'td.o_data_cell span[name="account_analytic_id"]:contains("[01532] Cat 930M")',
        extra_trigger: 'div[name="invoice_line_ids"]',
        in_modal: false,
        position: 'bottom',
        run: function (){} //check Invoice: (Analytic Account : [01532] Cat 930M)
    },
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
