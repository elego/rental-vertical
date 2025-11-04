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
        if (!this.model.last_group_bys?.length) {
            return records;
        }

        const groups = [{ id: -1, content: _t("<b>UNASSIGNED</b>"), order: -1 }];
        let seq = 1;
        const field = this.model.last_group_bys[0];

        // Collect all group IDs
        const groupIds = new Set();
        for (const r of records) {
            const val = r[field];
            if (Array.isArray(val)) {
                groupIds.add(val[0]);
            }
        }

        // M2M? get names via ORM
        if (this.fields[field]?.type === "many2many" && groupIds.size) {
            const relation = this.fields[field].relation;
            const res = await this.orm.searchRead(
                relation,
                [["id", "in", [...groupIds]]],
                ["id", "display_name"]
            );
            for (const rec of res) {
                groups.push({
                    id: rec.id,
                    content: rec.display_name,
                    order: seq++,
                });
            }
        } else {
            // M2O or simple fields
            for (const r of records) {
                const val = r[field];
                if (Array.isArray(val) && val[0]) {
                    if (!groups.some(g => g.id === val[0])) {
                        groups.push({
                            id: val[0],
                            content: val[1],
                            order: seq++,
                        });
                    }
                }
            }
        }

        // UNASSIGNED remove, if empty
        if (groups.length > 1 && groups[0].id === -1) {
            groups.shift();
        }

        return groups;
    }

    // -------------------------------------------------------------
    // 4. init_timeline – just options, no DOM hacks, no popup
    // -------------------------------------------------------------
    init_timeline() {
        super.init_timeline();

        // Event forwarding to Controller-Props
        // this.timeline.on("select", (props) => {
        //     const item = this.timeline.itemsData.get(props.items[0]);
        //     if (!item) return;
        //     this.props.onGroupClick?.(item);
        // });

        this.timeline.on("doubleClick", (props) => {
            const item = this.timeline.itemsData.get(props.item);
            if (!item) return;
            this.props.onItemDoubleClick?.(item);
        });

        this.timeline.on("groupclick", (props) => {
            const group = props.group;
            this.props.onGroupClick?.(group);
        });

         // --- Custom Group Template for sidebar clicks ---
        // this.options.groupTemplate = (group) => {
        //     const div = document.createElement("div");
        //     div.textContent = group.content;
        //     div.style.cursor = "pointer";
        //     div.onclick = () => {
        //         this.props.onGroupClick?.(group);
        //     };
        //     return div;
        // };

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


    // // -------------------------------------------------------------
    // // Tooltip-Helpers – old version with DOM element
    // // -------------------------------------------------------------
    // _showTooltip(evt, html) {
    //     if (!this.tooltipEl) {
    //         this.tooltipEl = document.createElement("div");
    //         this.tooltipEl.className = "vis-custom-tooltip";
    //         Object.assign(this.tooltipEl.style, {
    //             position: "fixed",
    //             zIndex: 9999,
    //             background: "rgba(30,30,30,0.9)",
    //             color: "#fff",
    //             padding: "6px 8px",
    //             borderRadius: "6px",
    //             fontSize: "12px",
    //             maxWidth: "1000px",
    //             pointerEvents: "none",
    //         });
    //         document.body.appendChild(this.tooltipEl);
    //     }
    //     this.tooltipEl.innerHTML = html;
    //     this.tooltipEl.style.display = "block";
    //     this._moveTooltip(evt);
    // }

    // _hideTooltip() {
    //     if (this.tooltipEl) this.tooltipEl.style.display = "none";
    // }

    // _moveTooltip(evt) {
    //     if (!this.tooltipEl) return;
    //     const offset = 12;
    //     this.tooltipEl.style.left = evt.clientX + offset + "px";
    //     this.tooltipEl.style.top = evt.clientY + offset + "px";
    // }

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
