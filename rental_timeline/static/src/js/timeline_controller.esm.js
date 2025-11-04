/** @odoo-module alias=rental_timeline.RentalTimelineController **/

import { TimelineController } from "@web_timeline/views/timeline/timeline_controller.esm";
import { FormViewDialog } from "@web/views/view_dialogs/form_view_dialog";
import { useService } from "@web/core/utils/hooks";
import { _t } from "@web/core/l10n/translation";
import {Layout} from "@web/search/layout";
import {standardViewProps} from "@web/views/standard_view_props";

const { DateTime } = luxon;

export default class RentalTimelineController extends TimelineController {
    setup() {
        super.setup();
        this.orm = useService("orm");
        this.dialogService = useService("dialog");
        this.actionService = useService("action");
    }

    get rendererProps() {
        return {
            ...super.rendererProps,
            onGroupClick: this._onGroupClick.bind(this),
            onItemDoubleClick: this._onItemDoubleClick.bind(this),
            onUpdate: this._onUpdate.bind(this),
        };
    }

    /**
     * Triggered when a group in the timeline is clicked. (sidebar group)
     */
    _onGroupClick(item) {
        const groupField = this.model.last_group_bys?.[0];
        if (!groupField) return;

        const fieldInfo = this.model.fields[groupField];
        const resModel = fieldInfo?.relation;
        const resId = item.group;
        if (!resModel || !resId) return;

        this.actionService.doAction({
            type: "ir.actions.act_window",
            res_model: resModel,
            res_id: resId,
            views: [[false, "form"]],
            target: "new",
            flags: { mode: "readonly" },
        });
    }

    /**
     * Triggered when a timeline item is clicked (to open form view / popup).
     */
    _onUpdate(item) {
        if (!item) return;
        const evt = item.evt || {};
        const resId = Number(evt.click_res_id);
        const title = evt.__name || "Details";
        const viewId = Number(this.props.archInfo?.attrs?.popup_view_id || 0);

        if(this.open_popup_action) {
            const options = {
                resModel: this.model.model_name,
                resId,
                title,
                readonly: true,
                viewId
            }

            this.Dialog = this.dialogService.add(FormViewDialog, options, {});
        } else {
            this.env.services.action.switchView("form", {
                resId: item_id,
                mode:  "edit",
            });
        }

        // if (viewId) {
        //     this.dialogService.add(FormViewDialog, {
        //         resModel: this.model.model_name,
        //         resId,
        //         title,
        //         viewId,
        //         readonly: true,
        //     });
        // } else {
        //     this.actionService.switchView("form", {
        //         resId,
        //         mode: "readonly",
        //     });
        // }
    }

    _onItemDoubleClick(event) {
        // return this.openItem(event.id, false);

        const groupField = this.model.last_group_bys?.[0];
        if (!groupField) return;

        const fieldInfo = this.model.fields[groupField];
        const resModel = fieldInfo?.relation;
        const resId = event.group;
        if (!resModel || !resId) return;

        this.actionService.doAction({
            type: "ir.actions.act_window",
            res_model: resModel,
            res_id: resId,
            views: [[false, "form"]],
            target: "new",
            flags: { mode: "readonly" },
        });

    }

    openItem(item_id, is_editable) {
        super.openItem(item_id, is_editable);
    }

}

RentalTimelineController.components = {
    ...RentalTimelineController.components,
    Layout,
};
// RentalTimelineController.templateName = "rental_timeline.TimelineView";

RentalTimelineController.props = {
    ...standardViewProps,
    Model: Function,
    modelParams: Object,
    Renderer: Function,
};
