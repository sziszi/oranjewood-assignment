/** @odoo-module **/
// Copyright 2026 Oranjewood
// License OPL-1 (Odoo Proprietary License v1.0), see the LICENSE file.

import {_t} from "@web/core/l10n/translation";
import {formatFloat} from "@web/core/utils/numbers";
import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.SaleMarginInfo = publicWidget.Widget.extend({
    selector: ".o_sale_margin_info",
    events: {
        "show.bs.collapse": "_onShowMarginInfo",
    },

    init() {
        this._super(...arguments);
        this.rpc = this.bindService("rpc");
    },

    async _onShowMarginInfo() {
        const {orderId, token} = this.el.dataset;
        this._showState("loading");
        try {
            const result = await this.rpc(`/my/orders/${orderId}/margin_info`, {
                access_token: token,
            });
            const percentage = formatFloat(result.margin_percentage, {digits: [16, 2]});
            this.el.querySelector(".o_sale_margin_percentage").textContent =
                `${percentage}%`;
            this.el.querySelector(".o_sale_margin_required").textContent =
                result.requires_manager_approval ? _t("Yes") : _t("No");
            this._showState("values");
        } catch {
            this._showState("error");
        }
    },

    _showState(state) {
        for (const name of ["loading", "values", "error"]) {
            this.el
                .querySelector(`.o_sale_margin_${name}`)
                .classList.toggle("d-none", name !== state);
        }
    },
});
