odoo.define("rental_timeline.RentalTimelineController", function (require) {
    "use strict";

    var dialogs = require("web.view_dialogs");

    var _TimelineController = require("web_timeline.TimelineController");

    var RentalTimelineController = _TimelineController.extend({
        // /**
        //  * @override
        //  */
        // update: function (params, options) {
        //     const res = this._super.apply(this, arguments);
        //     if (_.isEmpty(params)) {
        //         return res;
        //     }
        //     const defaults = _.defaults({}, options, {
        //         adjust_window: true,
        //     });
        //     const domains = params.domain;
        //     const contexts = params.context;
        //     const group_bys = params.groupBy;
        //     this.last_domains = domains;
        //     this.last_contexts = contexts;
        //     // Select the group by
        //     let n_group_bys = group_bys;
        //     if (this.renderer.arch.attrs.default_group_by) {
        //         n_group_bys = this.renderer.arch.attrs.default_group_by.split(",");
        //     }
        //     this.renderer.last_group_bys = n_group_bys;
        //     this.renderer.last_domains = domains;

        //     let fields = this.renderer.fieldNames;
        //     fields = _.uniq(fields.concat(n_group_bys));
        //     return $.when(
        //         this._rpc({
        //             model: this.model.modelName,
        //             method: "search_read",
        //             kwargs: {
        //                 fields: fields,
        //                 domain: domains,
        //             },
        //             context: this.getSession().user_context,
        //         }).then((data) =>
        //             this.renderer.on_data_loaded(
        //                 data,
        //                 n_group_bys,
        //                 defaults.adjust_window
        //             )
        //         )
        //     );
        // },
        /**
         * @override
         */
        update: function (params, options) {
            const res = this._super.apply(this, arguments);
            if (_.isEmpty(params)) {
                return res;
            }
            const defaults = _.defaults({}, options, {
                adjust_window: true,
            });
            const domains = params.domain || this.renderer.last_domains || [];
            const contexts = params.context || [];
            const group_bys = params.groupBy || this.renderer.last_group_bys || [];
            this.last_domains = domains;
            this.last_contexts = contexts;
            // Select the group by
            let n_group_bys = group_bys;
            if (!n_group_bys.length && this.renderer.arch.attrs.default_group_by) {
                n_group_bys = this.renderer.arch.attrs.default_group_by.split(",");
            }
            this.renderer.last_group_bys = n_group_bys;
            this.renderer.last_domains = domains;

            let fields = this.renderer.fieldNames;
            fields = _.uniq(fields.concat(n_group_bys));
            $.when(
                res,
                this._rpc({
                    model: this.model.modelName,
                    method: "search_read",
                    kwargs: {
                        fields: fields,
                        domain: domains,
                        order: [{name: this.renderer.arch.attrs.default_group_by}],
                    },
                    context: this.getSession().user_context,
                }).then((data) =>
                    this.renderer.on_data_loaded(
                        data,
                        n_group_bys,
                        defaults.adjust_window
                    )
                )
            );

            return res;
        },

        _onGroupClick: function (event) {
            var groupField = this.renderer.last_group_bys[0];
            return this.do_action({
                type: "ir.actions.act_window",
                res_model: this.renderer.fields[groupField].relation,
                res_id: event.data.item.group,
                target: "new",
                flags: {
                    mode: "readonly",
                },
                views: [[false, "form"]],
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
                res_id:
                    parseInt(res_id, 10).toString() === res_id
                        ? parseInt(res_id, 10)
                        : res_id,
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
