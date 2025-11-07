/** @odoo-module **/

/* Odoo rental_timeline
 * Part of rental-vertical See LICENSE file for full copyright and licensing details.
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl). */

import { _t } from "@web/core/l10n/translation";
import { registry } from "@web/core/registry";
import {RentalTimelineArchParser} from "./rental_timeline_arch_parser.esm";
// import {TimelineModel} from "@web_timeline/views/timeline/timeline_model.esm";
import RentalTimelineModel from "./timeline_model.esm";
import RentalTimelineController from "./timeline_controller.esm";
import RentalTimelineRenderer  from "./timeline_renderer.esm";

const viewRegistry = registry.category("views");

export const RentalTimelineView = {
    type: "rental_timeline",
    searchMenuTypes: ["filter", "groupBy", "comparison", "favorite"],
    display_name: _t("Rental Timeline"),
    icon: "fa fa-calendar",
    multiRecord: true,
    ArchParser: RentalTimelineArchParser,
    Controller: RentalTimelineController,
    Renderer: RentalTimelineRenderer,
    Model: RentalTimelineModel,
    jsLibs: ["/rental_timeline/static/lib/vis/vis-timeline-graph2d.js"],
    cssLibs: ["/rental_timeline/static/lib/vis/vis-timeline-graph2d.css"],

    props: (genericProps, view) => {
        const { arch, fields, resModel } = genericProps;
        const parser = new view.ArchParser();
        const archInfo = parser.parse(arch, fields);
        const modelParams = {
            ...archInfo,
            resModel,
            fields,
        };

        return {
            ...genericProps,
            modelParams,
            Model: view.Model,
            Renderer: view.Renderer,
        };
    },

}

viewRegistry.add("rental_timeline", RentalTimelineView);
