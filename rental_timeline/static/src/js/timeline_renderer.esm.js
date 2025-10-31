/** @odoo-module **/
import { TimelineRenderer } from "@web_timeline/views/timeline/timeline_renderer.esm";
import { renderToString } from "@web/core/utils/render";
import { useService } from "@web/core/utils/hooks";
import { _t } from "@web/core/l10n/translation";

const { DateTime } = luxon;
/**
 * RentalTimelineRenderer – v18 ready, no hacks, no py.eval, no DOM bombs
 */
export default class RentalTimelineRenderer extends TimelineRenderer {
    setup() {
        super.setup();
        this.orm = useService("orm"); // Für M2M-Gruppen
    }

    // -------------------------------------------------------------
    // 1. on_data_loaded – sauber, mit fallback
    // -------------------------------------------------------------
    async on_data_loaded(records, adjust_window = true) {
        const data = [];
        for (const record of records) {
            if (record[this.date_start]) {
                const transform = this.model._event_data_transform || this.event_data_transform.bind(this);
                data.push(transform(record));
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
    // 2. event_data_transform – ohne py.eval, mit JS-Logik
    // -------------------------------------------------------------
    event_data_transform(evt) {
        const [date_start, date_stop] = this._get_event_dates(evt);

        // Group ID
        let group = -1;
        if (this.model.last_group_bys?.[0]) {
            const val = evt[this.model.last_group_bys[0]];
            group = Array.isArray(val) ? val[0] : -1;
        }

        // Farben: JS-Check statt py.eval
        let bgColor = "";
        for (const color of this.colors || []) {
            const val = evt[color.field];
            const match = this._matchColorCondition(val, color.opt, color.value);
            if (match) {
                bgColor = color.color;
                break; // erste passende
            }
        }

        // Content + Tooltip (via renderToString + HTML)
        let content = evt.__name || evt.display_name || "";
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

    // Hilfsfunktion für Farben
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

        // Sammle alle Gruppen-IDs
        const groupIds = new Set();
        for (const r of records) {
            const val = r[field];
            if (Array.isArray(val)) {
                groupIds.add(val[0]);
            }
        }

        // M2M? Hole Namen via ORM
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
            // M2O oder einfache Felder
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

        // UNASSIGNED entfernen, wenn leer
        if (groups.length > 1 && groups[0].id === -1) {
            groups.shift();
        }

        return groups;
    }

    // -------------------------------------------------------------
    // 4. init_timeline – nur Optionen, KEINE DOM-Hacks, KEIN Popup
    // -------------------------------------------------------------
    init_timeline() {
        super.init_timeline();

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

        // Kein Popup-Patch, kein ItemSet-Hack → vis.js reicht
        // Tooltips via HTML in `content` + `title` Attribut

        // changed handler – nur Orientation fixen
        if (this.timeline) {
            const self = this;
            this.timeline.off("changed");
            this.timeline.on("changed", () => {
                this.timeline.setOptions({ orientation: { item: "top", axis: "top" } });

                this.draw_canvas();
                this.load_initial_data();
                // this.model?.reload?.();
            });
        }



        // // --- Tooltip-System ---
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

        // // --- Click-Handler (öffnet z. B. Formview) ---
        // this.timeline.on("select", (props) => {
        //     if (!props.items.length) return;
        //     const item = this.timeline.itemsData.get(props.items[0]);
        //     if (item && item.id && this.actionService) {
        //         this._onItemSelected(item);
        //     }
        // });

        // // --- Orientation Fix bei Resize/Change ---
        // this.timeline.on("changed", () => {
        //     this.timeline.setOptions({ orientation: { item: "top", axis: "top" } });
        //     this.draw_canvas();
        //     this.load_initial_data();
        // });

    }


    // // -------------------------------------------------------------
    // // Tooltip-Hilfsfunktionen
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
    //             maxWidth: "240px",
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

    // // -------------------------------------------------------------
    // // Optional: Klick öffnet das Formview
    // // -------------------------------------------------------------
    // _onItemSelected(item) {
    //     this.actionService.doAction({
    //         type: "ir.actions.act_window",
    //         res_model: this.model.resModel,
    //         res_id: item.id,
    //         views: [[false, "form"]],
    //         target: "new",
    //     });
    // }


    load_initial_data() {
        super.load_initial_data();
    }

}

RentalTimelineRenderer.template = "web_timeline.TimelineRenderer";
