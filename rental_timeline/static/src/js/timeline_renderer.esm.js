/** @odoo-module **/
import { TimelineRenderer } from "@web_timeline/views/timeline/timeline_renderer.esm";
import { renderToString } from "@web/core/utils/render";
import { useService } from "@web/core/utils/hooks";
import { _t } from "@web/core/l10n/translation";
import Popup from "./Popup";

const { DateTime } = luxon;
/**
 * RentalTimelineRenderer – v18 ready, no hacks, no py.eval, no DOM bombs
 */
export default class RentalTimelineRenderer extends TimelineRenderer {
    setup() {
        super.setup();
        this.orm = useService("orm"); // For M2M groups
        this.tooltipPopup = new Popup(document.body);
    }

    // -------------------------------------------------------------
    // 1. on_data_loaded – clean, with fallback
    // -------------------------------------------------------------
    async on_data_loaded(records, adjust_window = true) {
        const data = [];
        for (const record of records) {
            if (record[this.date_start]) {
                const transform = this.model._event_data_transform(record) || this.event_data_transform.bind(this);
                data.push(transform);
            }
        }

        const groups = await this.split_groups(records);
        this.timeline.setGroups(groups);
        this.timeline.setItems(data);

        if ((this.mode.data === "fit" || !this.mode.data) && adjust_window) {
            this.timeline.fit();
        }
    }

    // -------------------------------------------------------------
    // 2. event_data_transform – one py.eval, with JS logic
    // -------------------------------------------------------------
    _event_data_transform(evt) {
        super._event_data_transform(evt);
        // Content + Tooltip (via renderToString + HTML)
        let content = evt.__name || evt.display_name || "";

        const [date_start, date_stop] = this._get_event_dates(evt);

        // Group ID
        let group = -1;
        if (this.model.last_group_bys?.[0]) {
            const val = evt[this.model.last_group_bys[0]];
            group = Array.isArray(val) ? val[0] : -1;
        }

        // Colors: JS check instead of py.eval
        let bgColor = "";
        for (const color of this.colors || []) {
            const val = evt[color.field];
            const match = this._matchColorCondition(val, color.opt, color.value);
            if (match) {
                bgColor = color.color;
                break; // first match
            }
        }

        let title = content;

        if (this.arch?.children?.length) {
            try {
                content = renderToString("rental_timeline.timeline_item", { record: evt });
                const temp = document.createElement("div");
                temp.innerHTML = content;
                const tooltipEl = temp.querySelector(".tooltip_content");
                title = tooltipEl?.innerText || content;
            } catch (e) {
                // fallback
            }
        }

        const item = {
            id: evt.id,
            start: date_start,
            content,
            title: title.replace(/<\/?[^>]+(>|$)/g, ""), // strip HTML for native tooltip
            group,
            evt,
            style: bgColor ? `background-color: ${bgColor};` : "",
        };

        if (date_stop && !DateTime.fromISO(date_start).equals(DateTime.fromISO(date_stop))) {
            item.end = date_stop;
        }

        return item;
    }

    // Helper function for colors
    _matchColorCondition(value, operator, target) {
        if (value === undefined || value === false) return false;
        switch (operator) {
            case "==": case "=": return String(value) === target;
            case "!=": return String(value) !== target;
            case "in": return target.split(",").map(t => t.trim()).includes(String(value));
            case "not in": return !this._matchColorCondition(value, "in", target);
            default: return false;
        }
    }

    // -------------------------------------------------------------
    // 3. split_groups
    // -------------------------------------------------------------
    async split_groups(records) {

        const groups = [];
        const grouped_field = this.model.last_group_bys[0];
        if (!grouped_field) {
            return records;
        }
        let seq = 1;

        // Keep track of group IDs
        const groupMap = new Map();

        // basic version: only for product_id grouping
        for (const event of records) {
            const productGroup = event.product_id;
            if (Array.isArray(productGroup)) {
                let group = groups.find(g => g.id === productGroup[0]);
                if (!group && !productGroup[1].startsWith("All")) {
                    const tooltip = this.renderTooltip(event);
                    groups.push({
                        id: productGroup[0],
                        content: productGroup[1],
                        tooltip,
                        partner_id: event.partner_id,
                        order_name: event.order_name,
                        product_id: event.product_id,
                        order: seq++,
                    });
                }
            }
        }

        // grouping by product_categ_id
        if (grouped_field === "product_categ_id") {
            const groupCategs = [];
            for (const event of records) {
                const categ = event.product_categ_id;
                if (Array.isArray(categ)) {
                    let group = groupCategs.find(g => g.content === categ[1]);
                    if (!group) {
                        const tooltip = this.renderTooltip(event);
                        const nestedGroups = [];
                        for (const e2 of records) {
                            if (e2.product_categ_name === event.product_categ_name) {
                                if (!nestedGroups.includes(e2.product_id?.[0])) {
                                    nestedGroups.push(e2.product_id?.[0]);
                                }
                            }
                        }
                        group = {
                            id: categ[0] + 1000000,
                            content: categ[1],
                            nestedGroups,
                            tooltip,
                            order: seq++,
                        };
                        groupCategs.push(group);
                    }
                }
            }
            groups.push(...groupCategs);
        }

        // grouping by order_name
        else if (grouped_field === "order_name") {
            const groupOrders = [];
            for (const event of records) {
                const orderName = event.order_name;
                if (orderName && !groupOrders.find(g => g.content === orderName)) {
                    const tooltip = this.renderTooltip(event);
                    const nestedGroups = [];
                    for (const e2 of records) {
                        if (e2.order_name === orderName && e2.product_id) {
                            if (!nestedGroups.includes(e2.product_id[0])) {
                                nestedGroups.push(e2.product_id[0]);
                            }
                        }
                    }
                    groupOrders.push({
                        id: event.id + 1000000,
                        content: orderName,
                        nestedGroups,
                        tooltip,
                        order_name: orderName,
                        order: seq++,
                    });
                }
            }
            groups.push(...groupOrders);
        }

        // grouping by partner_id
        else if (grouped_field === "partner_id") {
            const groupPartners = [];
            for (const event of records) {
                const partner = event.partner_id;
                if (Array.isArray(partner)) {
                    let group = groupPartners.find(g => g.content === partner[1]);
                    if (!group) {
                        const tooltip = this.renderTooltip(event);
                        const nestedGroups = [];
                        for (const e2 of records) {
                            if (e2.partner_id?.[1] === partner[1]) {
                                if (!nestedGroups.includes(e2.product_id?.[0])) {
                                    nestedGroups.push(e2.product_id[0]);
                                }
                            }
                        }
                        groupPartners.push({
                            id: partner[0] + 1000000,
                            content: partner[1],
                            nestedGroups,
                            tooltip,
                            partner_id: partner,
                            order: seq++,
                        });
                    }
                }
            }
            groups.push(...groupPartners);
        }

        // Fallback if no groups
        if (!groups.length) {
            groups.push({ id: -1, content: _t("<b>UNASSIGNED</b>"), order: 0 });
        }

        return groups;
    }

    /**
     * Render tooltip content for a group
     * Instead of QWeb, use OWL component or just HTML string
     */
    renderTooltip(record) {
        if (!record) return "";
        return `
            <table border="1" style="border-collapse: collapse;">
                <tr><td>Product: </td><td>${record.product_id?.[1] || "-"}</td></tr>
                <tr><td>Partner: </td><td>${record.partner_id?.[1] || "-"}</td></tr>
                <tr><td>Type: </td><td>${record.type_formated || "-"}</td></tr>
                <tr><td>Warehouse: </td><td>${record.warehouse_name || "-"}</td></tr>
                <tr><td>Category: </td><td>${record.product_categ_name || "-"}</td></tr>
            </table>
        `;
    }

    // -------------------------------------------------------------
    // 4. init_timeline – just options, no DOM hacks, no popup
    // -------------------------------------------------------------
    init_timeline() {
        super.init_timeline();

        // Event forwarding to Controller-Props
        this.timeline.on("doubleClick", (props) => {
            const item = this.timeline.itemsData.get(props.item);
            if (!item) return;
            this.props.onItemDoubleClick?.(item);
        });

        this.timeline.on("groupclick", (props) => {
            const group = props.group;
            this.props.onGroupClick?.(group);
        });

        // Custom Options
        this.options.editable = this.options.editable || {};
        Object.assign(this.options.editable, {
            add: false,
            updateTime: false,
            updateGroup: false,
            remove: false,
        });

        this.options.orientation = { item: "top", axis: "top" };
        this.options.verticalScroll = true;

        if (this.timeline) {
            this.timeline.setOptions(this.options);
        }

        // --- Tooltip-System ---
        // this.timeline.on("itemover", (props) => {
        //     const item = this.timeline.itemsData.get(props.item);
        //     if (!item) return;

        //     // Tooltip HTML aus Item oder Group
        //     const tooltipHtml =
        //         item.evt?.tooltip ||
        //         item.title ||
        //         (this.timeline.groupsData.get(item.group)?.tooltip ?? null);

        //     if (tooltipHtml) this._showTooltip(props.event, tooltipHtml);
        // });

        // this.timeline.on("itemout", () => this._hideTooltip());
        // this.timeline.on("mouseMove", (props) => this._moveTooltip(props.event));

        // --- Tooltip-System (nur bei Items) ---
        this.timeline.off("itemover");
        this.timeline.off("itemout");

        // this.timeline.on("itemover", (props) => {
        //     const item = this.timeline.itemsData.get(props.item);
        //     if (!item) return;

        //     // Tooltip HTML aus Template oder Fallback
        //     const tooltipHtml =
        //         item.evt?.tooltip ||
        //         item.title ||
        //         (this.timeline.groupsData.get(item.group)?.tooltip ?? null);

        //     if (tooltipHtml) {
        //         this._showTooltip(props.event, tooltipHtml);
        //     }
        // });

        this.timeline.on("itemover", (props) => {
            const item = this.timeline.itemsData.get(props.item);
            if (!item || !item.evt) return;

            const evt = item.evt;
            // Tooltip from fields:
            const tooltipHtml = `
                <div class="tooltip_content" style="display: block;">
                    <table border="1">
                        <tr>
                            <td>Order: </td>
                            <td>${evt.order_name}</td>
                        </tr>
                        <tr>
                            <td>Start date</td>
                            <td>${evt.date_start_formated}</td>
                        </tr>
                        <tr>
                            <td>End date</td>
                            <td>${evt.date_end_formated}</td>
                        </tr>
                        <tr>
                            <td>Total days</td>
                            <td>${evt.number_of_days ?? ""}</td>
                        </tr>
                        <tr>
                            <td>Rental period</td>
                            <td>${evt.rental_period ?? ""}</td>
                        </tr>
                        <tr>
                            <td>Customer</td>
                            <td>${evt.display_name ?? ""}</td>
                        </tr>
                        <tr>
                            <td>Shipping address</td>
                            <td>${evt.partner_shipping_address ?? ""}</td>
                        </tr>
                        <tr>
                            <td>Warehouse</td>
                            <td>${evt.warehouse_name ?? ""}</td>
                        </tr>
                        <tr>
                            <td>Type</td>
                            <td>${evt.type_formated ?? ""}</td>
                        </tr>
                        <tr>
                            <td>Price</td>
                            <td>${evt.amount ?? ""}</td>
                        </tr>
                    </table>
                </div>
            `;

            this._showTooltip(props.event, tooltipHtml);
        });

        // --- Group Tooltip System (Sidebar-Groups) ---
        const groupContainer = this.timeline.dom?.left; // Sidebar DOM
        if (groupContainer) {
            // wait, until the dom is rendered
            setTimeout(() => {
                groupContainer.querySelectorAll(".vis-label").forEach((labelEl) => {
                    const groupName = labelEl.textContent.trim();
                    const group = Array.from(this.timeline.groupsData.getIds())
                        .map((id) => this.timeline.groupsData.get(id))
                        .find((g) => g.content?.includes(groupName));

                    if (!group) return;

                    labelEl.addEventListener("mouseenter", (event) => {
                        const tooltipHtml =
                            group.tooltip ||
                            group.title ||
                            `<div class="tooltip_content"><b>${groupName}</b></div>`;
                        this._showTooltip(event, tooltipHtml);
                    });

                    labelEl.addEventListener("mousemove", (event) => {
                        this._moveTooltip(event);
                    });

                    labelEl.addEventListener("mouseleave", () => {
                        this._hideTooltip();
                    });
                });
            }, 100);
        }

        this.timeline.on("itemout", () => this._hideTooltip());

        this.timeline.on("itemout", () => this._hideTooltip());

        // --- Click-Handler ---
        this.timeline.on("select", (props) => {
            if (!props.items.length) return;
            const item = this.timeline.itemsData.get(props.items[0]);
            if (item && item.id && this.actionService) {
                this._onItemSelected(item);
            }
        });

    }


    // -------------------------------------------------------------
    // Tooltip-Helpers – old version with DOM element
    // -------------------------------------------------------------

    _showTooltip(evt, html) {
        if (!this.tooltipPopup) {
            this.tooltipPopup = new Popup(document.body);
        }
        this.tooltipPopup.setText(html);
        this.tooltipPopup.setPosition(evt.clientX + 10, evt.clientY + 10);
        this.tooltipPopup.show(true);
    }

    _hideTooltip() {
        if (this.tooltipPopup) {
            this.tooltipPopup.hide();
        }
    }

    _moveTooltip(evt) {
        if (!this.tooltipPopup) return;
        this.tooltipPopup.setPosition(evt.clientX + 10, evt.clientY + 10);
        this.tooltipPopup.show(true);
    }

    // -------------------------------------------------------------
    // Option: click on item – open form view
    // -------------------------------------------------------------
    _onItemSelected(item) {
        this.actionService.doAction({
            type: "ir.actions.act_window",
            res_model: this.model.resModel,
            res_id: item.id,
            views: [[false, "form"]],
            target: "new",
        });
    }

    /**
     * Clears and draws the canvas items.
     *
     * @private
     */
    draw_canvas() {
        super.draw_canvas();
    }


    load_initial_data() {
        super.load_initial_data();
    }

    async create_completed(id) {
        const records = await this.orm.call(this.model_name, "read", [
            [id],
            this.params.fieldNames,
        ]);
        return this._event_data_transform(records[0]);
    }

}

RentalTimelineRenderer.template = "web_timeline.TimelineRenderer";
