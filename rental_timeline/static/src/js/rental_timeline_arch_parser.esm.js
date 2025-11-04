/** @odoo-module */

/**
 * @typedef {Object} ArchInfo
 * @property {string} arch
 * @property {string} countField
 */

import {TimelineArchParser} from "@web_timeline/views/timeline/timeline_arch_parser.esm";

export class RentalTimelineArchParser extends TimelineArchParser {

    parse(arch, fields) {
        if (arch.tag === "rental_timeline") {
            const timelineNode = arch.children?.find((child) => child.tag === "timeline");
            if (!timelineNode) {
                throw new Error("rental_timeline view must contain a <timeline> node");
            }

            arch.attrs = { ...arch.attrs, ...timelineNode.attrs };

            arch.children = timelineNode.children;
        }

        return super.parse(arch, fields);
    }

}
