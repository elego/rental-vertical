odoo.define('rental_timeline.RentalTimelineController', function (require) {
    "use strict";


    var dialogs = require('web.view_dialogs');

    var _TimelineController = require('web_timeline.TimelineController');

    var RentalTimelineController = _TimelineController.extend({

        // custom_events: _.extend({}, _TimelineController.prototype.custom_events, {
        //     onParentGroupClick: '_onParentGroupClick'
        // }),

        
        // _onParentGroupClick: function (event) {
        //     if($("div").getClass === "vis-label vis-nesting-group collapsed" || $("div").getClass === "vis-label vis-nesting-group expanded"){
        //         var groupField = "product_categ_id"
        //     }
        // },

        _onGroupClick: function (event) {
            if(this.renderer.last_group_bys[0] !== "product_categ_id") {
                var groupField = this.renderer.last_group_bys[0];
            } else {
                var groupField = this.renderer.grouped_by;
            }

            $("div").click(function () {
                var getClass = this.className;
            });

            // if(getClass === "vis-label vis-nesting-group collapsed" || getClass === "vis-label vis-nesting-group expanded"){
            //     return this.do_action({
            //         type: 'ir.actions.act_window',
            //         res_model: this.renderer.view.fields["product_categ_id"].relation,
            //         res_id: event.data.item.group,
            //         target: 'new',
            //         flags: {
            //             mode: 'readonly',
            //         },
            //         views: [[false, 'form']],
            //     });
            // } else {
            //     return this.do_action({
            //         type: 'ir.actions.act_window',
            //         res_model: this.renderer.view.fields[groupField].relation,
            //         res_id: event.data.item.group,
            //         target: 'new',
            //         flags: {
            //             mode: 'readonly',
            //         },
            //         views: [[false, 'form']],
            //     });
            // }

            return this.do_action({
                        type: 'ir.actions.act_window',
                        res_model: this.renderer.view.fields[groupField].relation,
                        res_id: event.data.item.group,
                        target: 'new',
                        flags: {
                            mode: 'readonly',
                        },
                        views: [[false, 'form']],
                    });
        },

        _onUpdate: function (event) {
            var self = this;
            this.renderer = event.data.renderer;
            var item = event.data.item;
            var title = item.evt.__name;
            var res_model = item.evt.click_res_model;
            var res_id = item.evt.click_res_id;
            new dialogs.FormViewDialog(this, {
                res_model: res_model,
                res_id: parseInt(res_id, 10).toString() === res_id ? parseInt(res_id, 10) : res_id,
                context: this.getSession().user_context,
                title: title,
                view_id: Number(this.open_popup_action),
                on_saved: function () {
                    self.write_completed();
                },
                readonly: true,
            }).open();
        },

    });

    return RentalTimelineController;
});
