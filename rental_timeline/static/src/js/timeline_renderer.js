odoo.define('rental_timeline.RentalTimelineRenderer', function(require){
    "use strict";

    var _TimelineRenderer = require('web_timeline.TimelineRenderer');

    var time = require('web.time');

    var RentalTimelineRenderer = _TimelineRenderer.extend({
        
        /**
         * Get the groups.
         *
         * @private
         * @returns {Array}
         */
        split_groups: function(events, group_bys){
            if(group_bys.length === 0){
                return events;
            }

            var groups = [];
            var self = this;
            //groups.push({id: -1, content: _t('-')});

            var count = 1
            _.each(events, function(event){
                var product_group_name = event[_.first(["product_id"])];
                if(product_group_name) {
                    if(product_group_name instanceof Array) {
                        let group = _.find(groups, function(existing_group){
                            return _.isEqual(existing_group.id , product_group_name[0]);
                        });

                        if(_.isUndefined(group)) {
                            var tooltip = null; 
                            if(self.qweb.has_template('tooltip-item-group')){
                                tooltip = self.qweb.render('tooltip-item-group', {
                                    'record': event
                                });
                            }
                            if(product_group_name[1].slice(0,3) !== "All") {

                                group = {
                                    id: product_group_name[0],
                                    content: product_group_name[1],
                                    tooltip: tooltip
                                };
                                groups.push(group);
                            }

                        }
                    }
                }
            })

            if(group_bys[0] === "product_categ_id"){

                var group_categs = []
    
                console.log("groups by product_id: ", groups)
    
                _.each(events, function(event){
                    var group_name = event[_.first(group_bys)];
                    if(group_name){
                        if(group_name instanceof Array){
                            let group = _.find(group_categs, function(existing_group){
                                return _.isEqual(existing_group.id, group_name[0] * 100);
                                // return _.isEqual(existing_group, group_name);
                            });
    
                            // if(!groups.includes(group)){
                            if(_.isUndefined(group)){
                                
                                var tooltip = null;
                                if(self.qweb.has_template('tooltip-item-group')){
                                    tooltip = self.qweb.render('tooltip-item-group', {
                                        'record': event
                                    });
                                }
    
                                let nested_groups = []
                                _.each(events, function(event_p){
                                    if(event_p.product_categ_name === event.product_categ_name) { 
                                        if(!nested_groups.includes(event_p.product_id[0])){
                                            nested_groups.push(event_p.product_id[0]) 
                                        }
                                        console.log(`event_p.product_categ_name ${event_p.product_categ_name}`)                                   
                                    }
                                })
    
                                group = {
                                    id: group_name[0] * 100,
                                    content: group_name[1], 
                                    nestedGroups: nested_groups,
                                    tooltip: tooltip,
                                };
        
                                group_categs.push(group);
                            } 
    
                        }
                    }
                });

                groups = groups.concat(group_categs)
            }

            console.log("groups by group_bys: ", groups)

            return groups;
        },

        /**
         * Transform Odoo event object to timeline event object.
         *
         * @private
         * @returns {Object}
         */
         event_data_transform: function (evt) {
            var self = this;
            var date_start = new moment();
            var date_stop = null;

            var date_delay = evt[this.date_delay] || false,
                all_day = this.all_day ? evt[this.all_day] : false;

            if (all_day) {
                date_start = time.auto_str_to_date(evt[this.date_start].split(' ')[0], 'start');
                if (this.no_period) {
                    date_stop = date_start;
                } else {
                    date_stop = this.date_stop ? time.auto_str_to_date(evt[this.date_stop].split(' ')[0], 'stop') : null;
                }
            } else {
                date_start = time.auto_str_to_date(evt[this.date_start]);
                date_stop = this.date_stop ? time.auto_str_to_date(evt[this.date_stop]) : null;
            }

            if (!date_stop && date_delay) {
                date_stop = moment(date_start).add(date_delay, 'hours').toDate();
            }
            
            if(self.last_group_bys[0] !== "product_categ_id") {
                var group = evt[self.last_group_bys[0]];
            } else {
                var group = evt.product_id
            }
            if (group) {
                if (group instanceof Array) {
                    group = _.first(group);
                }
            } else {
                group = -1;
            }
            var color = null;
            if (self.arch.attrs.color_field !== undefined) {
                color = evt[self.arch.attrs.color_field];
            } else {
                _.each(self.colors, function (col) {
                    if (eval("'" + evt[col.field] + "' " + col.opt + " '" + col.value + "'")) {
                        color = col.color;
                    }
                });
            }

            var content = _.isUndefined(evt.__name) ? evt.display_name : evt.__name;
            if (this.arch.children.length) {
                content = this.render_timeline_item(evt);
            }

            var title = "";
            if (content) {
                var doc = document.createElement('html');
                doc.innerHTML = "<html><body>" + content + "</body></html>"
                var tt_content = doc.getElementsByClassName('tooltip_content')
                if (tt_content && tt_content.length) {
                    title = tt_content[0].innerHTML
                }
            }

            var r = {
                'title': title,
                'start': date_start,
                'content': content,
                'id': evt.id,
                'group': group,
                'evt': evt,
                'style': 'background-color: ' + color + ';'
            };
            // Check if the event is instantaneous, if so, display it with a point on the timeline (no 'end')
            if (date_stop && !moment(date_start).isSame(date_stop)) {
                r.end = date_stop;
            }
            return r;
        },


        init_timeline: function(){
            var self = this;
            var util = vis.util;
            this._super();
            this.options.editable = {
                add: false,
                updateTime: false,
                updateGroup: false,
                remove: false
            };
            this.options.orientation = {
                item: 'top',
                axis: 'top'
            };
            this.options.verticalScroll = true;
            this.timeline.setOptions(this.options);

            // this.timeline.on('click', self.on_parent_group_click)

            this.timeline.on('doubleClick', self.on_group_double_click);
            // this.timeline.on('click', self.on_group_click);
            this.timeline.on('click', function(props){
                props.event.preventDefault()
            });

            // turn off the internal hammer tap event listener
            this.timeline.off('changed').on('changed', function() {
                this.options.orientation = {
                    item: 'top',
                    axis: 'top'
                };
                self.draw_canvas();
                self.canvas.$el.attr(
                    'style',
                    self.$el.find('.vis-content').attr('style') + self.$el.find('.vis-itemset').attr('style')
                );
            });

            

            (function(_create, setData){
                vis.timeline.components.Group.prototype.setData = function(data){
                    setData.apply(this, [data]);
                    this.copy_data = data;
                }
                vis.timeline.components.Group.prototype._create = function(){
                    _create.apply(this);
                    this.popup = null;
                    this.dom.label.addEventListener('mouseover', this._onMouseOver.bind(this));
                    this.dom.label.addEventListener('mouseout', this._onMouseOut.bind(this));
                    this.dom.label.addEventListener('mousemove', this._onMouseMove.bind(this));
                };
                vis.timeline.components.Group.prototype._onMouseOver = function(event){
                    if(this.copy_data.tooltip == null) return;
                    if(this.popup == null) this.popup = new Popup(this.itemSet.body.dom.root, 'flip');
                    this.popup.setText(this.copy_data.tooltip);
                    var container = this.itemSet.body.dom.centerContainer;
                    this.popup.setPosition(
                        event.clientX - util.getAbsoluteLeft(container) + container.offsetLeft,
                        event.clientY - util.getAbsoluteTop(container) + container.offsetTop
                    );
                    this.popup.show();
                };
                vis.timeline.components.Group.prototype._onMouseOut = function(event){
                    if(this.popup != null){
                        this.popup.hide();
                    }
                };
                vis.timeline.components.Group.prototype._onMouseMove = function(event){
                    if(this.popup){
                        if(!this.popup.hidden){
                            var container = this.itemSet.body.dom.centerContainer;
                            this.popup.setPosition(
                                event.clientX - util.getAbsoluteLeft(container) + container.offsetLeft,
                                event.clientY - util.getAbsoluteTop(container) + container.offsetTop
                            );
                            this.popup.show(); // Redraw
                        }
                    }
                };
            })(
                vis.timeline.components.Group.prototype._create,
                vis.timeline.components.Group.prototype.setData
            );

            (function(_onUpdateItem){
                // we set the option add=false, so we must overwrite the function _onUpdateItem
                // because in the function _onUpdateItem is a check if add is true
                // now we set add to true, call the function and set add back to false
                vis.timeline.components.ItemSet.prototype._onUpdateItem = function(item){
                    var add = this.options.editable.add;
                    this.options.editable.add = true;
                    _onUpdateItem.apply(this, [item]);
                    this.options.editable.add = add;
                };
            })(
                vis.timeline.components.ItemSet.prototype._onUpdateItem
            );

            (function(_repaintDragCenter){
                // we set the option updateTime=false, so we must overwrite the function _onUpdateItem
                // because in the function _onUpdateItem is a check if updateTime is true
                // now we set updateTime to true, call the function and set updateTime back to false
                vis.timeline.components.items.Item.prototype._repaintDragCenter = function(){
                    var updateTime = this.options.editable.updateTime;
                    this.options.editable.updateTime = true;
                    _repaintDragCenter.apply(this);
                    this.options.editable.updateTime = updateTime;

//                     if(this.selected && !this.dom.dragCenter && false){
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
            })(
                vis.timeline.components.items.Item.prototype._repaintDragCenter
            );
        },

         
        /**
         * Handle double click on a group header.
         *
         * @private
         */
         on_group_double_click: function (e) {
            if (e.what === 'group-label' && e.group !== -1) {
                this._trigger(e, function() {
                    // Do nothing
                }, 'onGroupDoubleClick');
            }
        },

        /**
         * Set groups and events.
         *
         * @private
         */
         on_data_loaded_2: function (events, group_bys, x2x, adjust_window) {
            var self = this;
            var data = [];
            var groups = [];

            if(group_bys[0] !== "product_categ_id") {
                this.grouped_by = group_bys;

                _.each(events, function (event) {
                    if (event[self.date_start]) {
                        if (x2x) {
                            _.each(event[group_bys], function (gr) {
                                var x2x_object = jQuery.extend({}, event);
                                x2x_object[group_bys] = [gr];
                                // Creating a UNIQUE id with [id]_[gr].
                                // This id is unique due the unique relationship
                                // between two records in O2M or M2M
                                x2x_object.id = event.id + "_" + gr;
                                data.push(self.event_data_transform(x2x_object));
                            })
                        } else {
                            data.push(self.event_data_transform(event));
                        }
                    }
                });
            } else {
                this.grouped_by = "product_id"
                _.each(events, function (event) {
                    if (event[self.date_start]) {
                        if (x2x) {
                            _.each(event["product_id"], function (gr) {
                                var x2x_object = jQuery.extend({}, event);
                                x2x_object["product_id"] = [gr];
                                // Creating a UNIQUE id with [id]_[gr].
                                // This id is unique due the unique relationship
                                // between two records in O2M or M2M
                                x2x_object.id = event.id + "_" + gr;
                                data.push(self.event_data_transform(x2x_object));
                            })
                        } else {
                            data.push(self.event_data_transform(event));
                        }
                    }
                });
            }

            if (x2x) {
                groups = this.groups;
                this.selected_groups = this.groups;
                this.createSelectGroups();
            } else {
                if (typeof this.$select_groups !== 'undefined') {
                    this.$('.selected-groups').html('');
                    this.$select_groups.remove();
                }
                groups = this.split_groups(events, group_bys);
                groups = new vis.DataSet(groups)
            }
            this.timeline.setGroups(groups);
            this.timeline.setItems(data);
            var mode = !this.mode || this.mode === 'fit';
            var adjust = _.isUndefined(adjust_window) || adjust_window;
            if (mode && adjust) {
                this.timeline.fit();
            }
        },

        _do_nothing:function(){
            console.log("click event is fired")
        },

        _onTodayClicked: function(){
            this._scaleCurrentWindow(1, 'days', 'day');
        },

        _onScaleDayClicked: function(){
            this._scaleCurrentWindow(1, 'days', 'now');
        },

        _onScaleWeekClicked: function(){
            this._scaleCurrentWindow(7, 'days', 'now');
        },

        _onScaleMonthClicked: function(){
            this._scaleCurrentWindow(1, 'months', 'now');
        },

        _onScaleYearClicked: function(){
            this._scaleCurrentWindow(1, 'years', 'now');
        },

        _scaleCurrentWindow: function(factor, time_unit='hours', startOf='current_window'){
            if(this.timeline){
                var start = null;
                if(startOf == 'current_window'){
                    start = this.timeline.getWindow().start;
                }
                else{
                    var moment_now = new moment();
                    start = startOf == 'now' ? moment_now : moment_now.startOf(startOf);
                }
                this.current_window = {
                    start: start,
                    end: moment(start).add(factor, time_unit)
                };
                this.timeline.setWindow(this.current_window);
            }
        },
    });

    return RentalTimelineRenderer;
});
