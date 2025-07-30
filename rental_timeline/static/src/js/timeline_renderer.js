/* Odoo rental_timeline
 * Part of rental-vertical See LICENSE file for full copyright and licensing details.
 * License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl). */

odoo.define("rental_timeline.RentalTimelineRenderer", function (require) {
    "use strict";

    var _TimelineRenderer = require("web_timeline.TimelineRenderer");
    const core = require("web.core");
    const _t = core._t;

    var RentalTimelineRenderer = _TimelineRenderer.extend({

        load_initial_data: function () {
            this._super();
        },

        on_data_loaded_2: function (events, group_bys, adjust_window) {
            const data = [];
            this.grouped_by = group_bys;
            for (const evt of events) {
                if (evt[this.date_start]) {
                    data.push(this.event_data_transform(evt));
                }
            }
            this.split_groups(events, group_bys).then((groups) => {
                this.timeline.setGroups(groups);
                this.timeline.setItems(data);
                const mode = !this.mode || this.mode === "fit";
                const adjust = _.isUndefined(adjust_window) || adjust_window;
                if (mode && adjust) {
                    this.timeline.fit();
                }
            });
        },

        /**
         * Get the groups.
         *
         * @param {Object[]} events
         * @param {String[]} group_bys
         * @private
         * @returns {Array}
         */
        split_groups: async function (events, group_bys) {
            const superGroups = await this._super.apply(this, arguments);
            if (group_bys.length === 0) {
                return events;
            }
            const groups = [];
            groups.push({id: -1, content: _t("<b>UNASSIGNED</b>"), order: -1});
            var seq = 1;
            const self = this;

            for (const evt of events) {
                const grouped_field = _.first(group_bys);
                const group_name = evt[grouped_field];
                if (group_name) {
                    if (group_name instanceof Array) {
                        let group = _.find(
                            groups,
                            (existing_group) => existing_group.id === group_name[0]
                        );
                        if (_.isUndefined(group)) {
                            // Check if group is m2m in this case add id -> value of all
                            // found entries.
                            await this._rpc({
                                model: this.modelName,
                                method: "fields_get",
                                args: [grouped_field],
                                context: this.getSession().user_context,
                            }).then(async (fields) => {
                                if (fields[grouped_field].type === "many2many") {
                                    const list_values =
                                        await this.get_m2m_grouping_datas(
                                            fields[grouped_field].relation,
                                            group_name
                                        );
                                    for (const vals of list_values) {
                                        let is_inside = false;
                                        for (const gr of groups) {
                                            if (vals.id === gr.id) {
                                                is_inside = true;
                                                break;
                                            }
                                        }
                                        if (!is_inside) {
                                            vals.order = seq;
                                            seq += 1;
                                            groups.push(vals);
                                        }
                                    }
                                } else {
                                    var tooltip = null;

                                    if (self.qweb.has_template("tooltip-item-group")) {
                                        tooltip = self.qweb.render(
                                            "tooltip-item-group",
                                            {
                                                record: evt,
                                            }
                                        );
                                    }

                                    group = {
                                        id: group_name[0],
                                        content: group_name[1],
                                        tooltip: tooltip,
                                        order: seq,
                                    };

                                    groups.push(group);
                                    seq += 1;
                                }
                            });
                        }
                    }
                }
            }

            if (groups[0].id === -1) {
                groups.shift();
            }
            return groups;
        },

        /**
         * Initializes the timeline
         * (https://visjs.github.io/vis-timeline/docs/timeline).
         *
         * @private
         */
        init_timeline: function () {
            let res = this._super();
            var self = this;
            var util = vis.util;
            this.options.editable = {
                add: false,
                updateTime: false,
                updateGroup: false,
                remove: false,
            };
            this.options.orientation = {
                item: "top",
                axis: "top",
            };
            this.options.verticalScroll = true;
            this.timeline.setOptions(this.options);

            this.timeline.off("changed").on("changed", function () {
                this.options.orientation = {
                    item: "top",
                    axis: "top",
                };
                self.draw_canvas();
                self.canvas.$el.attr(
                    "style",
                    self.$el.find(".vis-content").attr("style") +
                        self.$el.find(".vis-itemset").attr("style")
                );
                self.load_initial_data();
            });

            (function (_create, setData) {
                vis.timeline.components.Group.prototype.setData = function (data) {
                    setData.apply(this, [data]);
                    this.copy_data = data;
                };
                vis.timeline.components.Group.prototype._create = function () {
                    _create.apply(this);
                    this.popup = null;
                    this.dom.label.addEventListener(
                        "mouseover",
                        this._onMouseOver.bind(this)
                    );
                    this.dom.label.addEventListener(
                        "mouseout",
                        this._onMouseOut.bind(this)
                    );
                    this.dom.label.addEventListener(
                        "mousemove",
                        this._onMouseMove.bind(this)
                    );
                };
                vis.timeline.components.Group.prototype._onMouseOver = function (
                    event
                ) {
                    if (this.copy_data.tooltip == null) return;
                    if (this.popup == null)
                        this.popup = new Popup(this.itemSet.body.dom.root, "flip");
                    this.popup.setText(this.copy_data.tooltip);
                    var container = this.itemSet.body.dom.centerContainer;
                    this.popup.setPosition(
                        event.clientX -
                            util.getAbsoluteLeft(container) +
                            container.offsetLeft,
                        event.clientY -
                            util.getAbsoluteTop(container) +
                            container.offsetTop
                    );
                    this.popup.show();
                };
                vis.timeline.components.Group.prototype._onMouseOut = function (event) {
                    if (this.popup != null) {
                        this.popup.hide();
                    }
                };
                vis.timeline.components.Group.prototype._onMouseMove = function (
                    event
                ) {
                    if (this.popup) {
                        if (!this.popup.hidden) {
                            var container = this.itemSet.body.dom.centerContainer;
                            this.popup.setPosition(
                                event.clientX -
                                    util.getAbsoluteLeft(container) +
                                    container.offsetLeft,
                                event.clientY -
                                    util.getAbsoluteTop(container) +
                                    container.offsetTop
                            );
                            this.popup.show(); // Redraw
                        }
                    }
                };
            })(
                vis.timeline.components.Group.prototype._create,
                vis.timeline.components.Group.prototype.setData
            );

            (function (_onUpdateItem) {
                // We set the option add=false, so we must overwrite the function _onUpdateItem
                // because in the function _onUpdateItem is a check if add is true
                // now we set add to true, call the function and set add back to false
                vis.timeline.components.ItemSet.prototype._onUpdateItem = function (
                    item
                ) {
                    var add = this.options.editable.add;
                    this.options.editable.add = true;
                    _onUpdateItem.apply(this, [item]);
                    this.options.editable.add = add;
                };
            })(vis.timeline.components.ItemSet.prototype._onUpdateItem);

            (function (_repaintDragCenter) {
                // We set the option updateTime=false, so we must overwrite the function _onUpdateItem
                // because in the function _onUpdateItem is a check if updateTime is true
                // now we set updateTime to true, call the function and set updateTime back to false
                vis.timeline.components.items.Item.prototype._repaintDragCenter =
                    function () {
                        var updateTime = this.options.editable.updateTime;
                        this.options.editable.updateTime = true;
                        _repaintDragCenter.apply(this);
                        this.options.editable.updateTime = updateTime;

                        //                     If(this.selected && !this.dom.dragCenter && false){
                        //                         hammer.off('tap');
                        //                         hammer.off('doubletap');
                        //                         hammer.on('tap', function(event){
                        //                             //event.stopPropagation();
                        //                             me.parent.itemSet._onUpdateItem(me);
                        //                             me.parent.itemSet.body.emitter.emit('click', {
                        //                                 event: event,
                        //                                 item: me.id
                        //                             });
                        //                         });
                        //                     }
                    };
            })(vis.timeline.components.items.Item.prototype._repaintDragCenter);

            return res;
        },

        /**
         * Transform Odoo event object to timeline event object.
         *
         * @param {TransformEvent} evt
         * @private
         * @returns {Object}
         */
        event_data_transform: function (evt) {
            const [date_start, date_stop] = this._get_event_dates(evt);

            let group = evt[this.last_group_bys[0]];
            if (group && group instanceof Array) {
                group = _.first(group);
            } else {
                group = -1;
            }

            for (const color of this.colors) {
                if (py.eval(`'${evt[color.field]}' ${color.opt} '${color.value}'`)) {
                    this.color = color.color;
                }
            }

            let content = evt.__name || evt.display_name;
            if (this.arch.children.length) {
                content = this.render_timeline_item(evt);
            }

            let title = "";
            if (content) {
                const doc = document.createElement("html");
                doc.innerHTML = "<html><body>" + content + "</body></html>";
                const tt_content = doc.getElementsByClassName("tooltip_content");
                if (tt_content && tt_content.length) {
                    title = tt_content[0].innerHTML;
                }
            }

            const r = {
                title: title,
                start: date_start,
                content: content,
                id: evt.id,
                group: group,
                evt: evt,
                style: `background-color: ${this.color};`,
            };
            // Check if the event is instantaneous,
            // if so, display it with a point on the timeline (no 'end')
            if (date_stop && !moment(date_start).isSame(date_stop)) {
                r.end = date_stop;
            }

            this.color = null;

            return r;
        },

        /**
         * Set the rental_timeline window to today (day).
         *
         * @private
         */
        _onTodayClicked: function () {
            this._scaleCurrentWindow(1, "days", "day");
        },

        /**
         * Scale the rental_timeline window to a day.
         *
         * @private
         */
        _onScaleDayClicked: function () {
            this._scaleCurrentWindow(1, "days", "now");
        },

        /**
         * Scale the rental_timeline window to a week.
         *
         * @private
         */
        _onScaleWeekClicked: function () {
            this._scaleCurrentWindow(7, "days", "now");
        },

        /**
         * Scale the rental_timeline window to a month.
         *
         * @private
         */
        _onScaleMonthClicked: function () {
            this._scaleCurrentWindow(1, "months", "now");
        },

        /**
         * Scale the rental_timeline window to a year.
         *
         * @private
         */
        _onScaleYearClicked: function () {
            this._scaleCurrentWindow(1, "years", "now");
        },

        /**
         * Scales the rental_timeline window based on the current window.
         *
         * @param {Integer} factor The timespan (in hours) the window must be scaled to.
         * @private
         */
        _scaleCurrentWindow: function (
            factor,
            time_unit = "hours",
            startOf = "current_window"
        ) {
            if (this.timeline) {
                var start = null;
                if (startOf == "current_window") {
                    start = this.timeline.getWindow().start;
                } else {
                    var moment_now = new moment();
                    start = startOf == "now" ? moment_now : moment_now.startOf(startOf);
                }
                this.current_window = {
                    start: start,
                    end: moment(start).add(factor, time_unit),
                };
                this.timeline.setWindow(this.current_window);
            }
        },
    });

    return RentalTimelineRenderer;
});
