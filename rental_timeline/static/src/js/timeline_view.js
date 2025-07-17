/* Odoo rental_timeline
 * Part of rental-vertical See LICENSE file for full copyright and licensing details.
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl). */

_.str.toBoolElse = function (str, elseValues, trueValues, falseValues) {
    var ret = _.str.toBool(str, trueValues, falseValues);
    if (_.isUndefined(ret)) {
        return elseValues;
    }
    return ret;
};

odoo.define("rental_timeline.RentalTimelineView", function (require) {
    "use strict";

    var core = require("web.core");
    var view_registry = require("web.view_registry");
    var TimelineModel = require("web_timeline.TimelineModel");
    var _TimelineView = require("web_timeline.TimelineView");
    var RentalTimelineRenderer = require("rental_timeline.RentalTimelineRenderer");
    var RentalTimelineController = require("rental_timeline.RentalTimelineController");
    var _lt = core._lt;

    var RentalTimelineView = _TimelineView.extend({
        display_name: _lt("Rental Timeline"),
        jsLibs: ["/rental_timeline/static/lib/vis/vis-timeline-graph2d.js"],
        cssLibs: ["/rental_timeline/static/lib/vis/vis-timeline-graph2d.css"],
        config: _.extend({}, _TimelineView.prototype.config, {
            Model: TimelineModel,
            Controller: RentalTimelineController,
            Renderer: RentalTimelineRenderer,
        }),
        viewType: "rental_timeline"
    });

    view_registry.add("rental_timeline", RentalTimelineView);
    
    return RentalTimelineView;
});
