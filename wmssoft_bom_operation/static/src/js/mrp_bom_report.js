odoo.define('wmssoft_bom_operation.mrp_bom_report', function (require) {
    "use strict";
    
    var core = require('web.core');
    var _t = core._t;
    
    var MrpBomReport = require('@mrp/js/mrp_bom_report')[Symbol.for("default")];
    
    MrpBomReport.include({
        get_custom_operations: function(event) {
            var self = this;
            var $parent = $(event.currentTarget).closest('tr');
            var activeID = $parent.data('bom-id');
            var qty = $parent.data('qty');
            var productId = $parent.data('product_id');
            var level = $parent.data('level') || 0;
            return this._rpc({
                    model: 'report.mrp.report_bom_structure',
                    method: 'get_custom_operations',
                    args: [
                        productId,
                        activeID,
                        parseFloat(qty),
                        level + 1
                    ]
                })
                .then(function (result) {
                    self.render_html(event, $parent, result);
                });
        },
    });
});
