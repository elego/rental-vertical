/* Odoo web_timeline
 * Copyright 2015 ACSONE SA/NV
 * Copyright 2016 Pedro M. Baeza <pedro.baeza@tecnativa.com>
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl). */

_.str.toBoolElse = function (str, elseValues, trueValues, falseValues) {
    var ret = _.str.toBool(str, trueValues, falseValues);
    if (_.isUndefined(ret)) {
        return elseValues;
    }
    return ret;
};


odoo.define('rental_timeline.RentalTimelineView', function (require) {
    "use strict";

    var core = require('web.core');
    var view_registry = require('web.view_registry');
    var AbstractView = require('web.AbstractView');
    var TimelineModel = require('web_timeline.TimelineModel');
    var _TimelineView = require('web_timeline.TimelineView');
    var RentalTimelineRenderer = require('rental_timeline.RentalTimelineRenderer');
    var RentalTimelineController = require('rental_timeline.RentalTimelineController');

    var _lt = core._lt;

    function isNullOrUndef(value) {
        return _.isUndefined(value) || _.isNull(value);
    }

    var RentalTimelineView = _TimelineView.extend({
        display_name: _lt('Rental Timeline'),
        config: {
            Model: TimelineModel,
            Controller: RentalTimelineController,
            Renderer: RentalTimelineRenderer,
        },
    });

    view_registry.add('rental_timeline', RentalTimelineView);
    return RentalTimelineView;
});
