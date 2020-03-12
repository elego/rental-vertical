odoo.define('rental_timeline.TimelineRenderer', function(require){
    "use strict";

    var TR = require('web_timeline.TimelineRenderer');

    var TimelineRenderer = TR.include({
        split_groups: function(events, group_bys){
            if(group_bys.length === 0){
                return events;
            }
            var groups = [];
            var self = this;
            //groups.push({id: -1, content: _t('-')});
            _.each(events, function(event){
                var group_name = event[_.first(group_bys)];
                if(group_name){
                    if(group_name instanceof Array){
                        var group = _.find(groups, function(existing_group){
                            return _.isEqual(existing_group.id, group_name[0]);
                        });

                        if(_.isUndefined(group)){
                            var tooltip = null;
                            if(self.qweb.has_template('tooltip-item-group')){
                                tooltip = self.qweb.render('tooltip-item-group', {
                                    'record': event
                                });
                            }
                            group = {
                                id: group_name[0],
                                content: group_name[1],
                                tooltip: tooltip
                            };
                            groups.push(group);
                        }
                    }
                }
            });
            return groups;
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

    return TimelineRenderer;
});
