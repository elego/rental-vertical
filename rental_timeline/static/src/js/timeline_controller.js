odoo.define('rental_timeline.TimelineController', function (require) {
    "use strict";


    var dialogs = require('web.view_dialogs');

    var TC = require('web_timeline.TimelineController');

    var TimelineController = TC.include({
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
                mode: 'readonly',
            }).open();
        },

    });

    return TimelineController;
});
