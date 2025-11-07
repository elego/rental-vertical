/** @odoo-module alias=rental_timeline.RentalTimelineModel **/

import { TimelineModel } from "@web_timeline/views/timeline/timeline_model.esm";
import { KeepLast } from "@web/core/utils/concurrency";
import { renderToString } from "@web/core/utils/render";
import { registry } from "@web/core/registry";
import { KanbanCompiler } from "@web/views/kanban/kanban_compiler";
import { useViewCompiler } from "@web/views/view_compiler";
import { evaluate } from "@web/core/py_js/py";
import { onWillStart } from "@odoo/owl";

const { DateTime } = luxon;

export default class RentalTimelineModel extends TimelineModel {

    setup(params) {
        this.params = params;
        this.model_name = params.resModel;
        this.fields = this.params.fields;
        this.date_start = this.params.date_start;
        this.date_stop = this.params.date_stop;
        this.date_delay = this.params.date_delay;
        this.colors = this.params.colors;
        this.last_group_bys = this.params.default_group_by.split(",");

        const templates = useViewCompiler(KanbanCompiler, this.params.templateDocs);
        this.recordTemplate = templates["timeline-item"];

        this.keepLast = new KeepLast();

        // --- important ---
        onWillStart(async () => {
            this.write_right = await this.orm.call(
                this.model_name,
                "check_access_rights",
                ["write", false]
            );
            this.unlink_right = await this.orm.call(
                this.model_name,
                "check_access_rights",
                ["unlink", false]
            );
            this.create_right = await this.orm.call(
                this.model_name,
                "check_access_rights",
                ["create", false]
            );
        });

    }


    /**
     * Override _event_data_transform to include JS color logic and tooltip HTML
     * @param {Object} evt - Record from Odoo
     * @returns {Object} timeline item
     */
    _event_data_transform(record) {
        // // Base call to super (fallback)
        // const baseItem = super._event_data_transform ? super._event_data_transform(evt) : {};

        // // Get event dates
        // const [date_start, date_stop] = this._get_event_dates(evt);

        // // Group ID
        // let group = -1;
        // if (this.last_group_bys?.[0]) {
        //     const val = evt[this.last_group_bys[0]];
        //     group = Array.isArray(val) ? val[0] : -1;
        // }

        // // Colors: JS check instead of py.eval
        // let bgColor = "";
        // for (const color of this.colors || []) {
        //     const val = evt[color.field];
        //     const match = this._matchColorCondition(val, color.opt, color.value);
        //     if (match) {
        //         bgColor = color.color;
        //         break;
        //     }
        // }

        // // Content + Tooltip
        // let content = evt.display_name || "";
        // let tooltipHtml = content;

        // try {
        //     content = renderToString("rental_timeline.timeline_item", { record: evt });
        //     const temp = document.createElement("div");
        //     temp.innerHTML = content;
        //     const tooltipEl = temp.querySelector(".tooltip_content");
        //     if (tooltipEl) {
        //         tooltipHtml = tooltipEl.innerHTML; // keep HTML for custom tooltip
        //     }
        // } catch (e) {
        //     // fallback to display_name
        // }

        // const item = {
        //     ...baseItem,
        //     id: evt.id,
        //     start: date_start.toJSDate ? date_start.toJSDate() : date_start,
        //     end: date_stop && DateTime.fromISO(date_start) < DateTime.fromISO(date_stop)
        //         ? date_stop.toJSDate ? date_stop.toJSDate() : date_stop
        //         : undefined,
        //     group,
        //     content,
        //     evt,
        //     title: tooltipHtml.replace(/<\/?[^>]+(>|$)/g, ""), // native tooltip fallback
        //     style: bgColor ? `background-color: ${bgColor};` : "",
        //     tooltip: tooltipHtml, // custom tooltip for Renderer
        // };

        // return item;



        const [date_start, date_stop] = this._get_event_dates(record);
        let group = [];
        if(
            this.last_group_bys[0] !== "product_categ_id" &&
            this.last_group_bys[0] !== "order_name" &&
            this.last_group_bys[0] !== "partner_id"
        ) {
            group = record[this.last_group_bys[0]];
        } else {
            group = record.product_id;
        }

        if (group && Array.isArray(group) && group.length > 0) {
            group = group[0];
        } else {
            group = -1;
        }
        let colorToApply = false;
        for (const color of this.colors) {
            if (evaluate(color.ast, record)) {
                colorToApply = color.color;
            }
        }

        let content = record.display_name;
        if (this.recordTemplate) {
            content = this._render_timeline_item(record);
        }

        const timeline_item = {
            start: date_start.toJSDate(),
            content: content,
            id: record.id,
            order: record.order,
            group: group,
            evt: record,
            style: `background-color: ${colorToApply};`,
        };
        // Only specify range end when there actually is one.
        if (date_stop && DateTime.fromISO(date_start) < DateTime.fromISO(date_stop)) {
            timeline_item.end = date_stop.toJSDate();
        }
        return timeline_item;


    }

    /**
     * Simple JS implementation of color matching
     */
    _matchColorCondition(value, operator, target) {
        if (value === undefined || value === false) return false;
        switch (operator) {
            case "==":
            case "=":
                return String(value) === target;
            case "!=":
                return String(value) !== target;
            case "in":
                return target.split(",").map(t => t.trim()).includes(String(value));
            case "not in":
                return !this._matchColorCondition(value, "in", target);
            default:
                return false;
        }
    }

}
