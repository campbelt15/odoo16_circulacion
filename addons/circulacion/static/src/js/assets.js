odoo.define('circulacion.custom_button', function (require) {
    "use strict";

    var FormController = require('web.FormController');

    var CustomFormController = FormController.include({
        renderButtons: function () {
            this._super.apply(this, arguments);  // Call parent's method
            if (this.$buttons) {
                var button = $("<button/>", {
                    type: 'button',
                    text: 'Mi botón',
                    id: 'my-button',
                    class: 'btn btn-primary'
                });

                button.click(this.proxy('button_clicked'));
                this.$buttons.append(button);
            }
        },

        button_clicked: function () {
            // Your code for when the button is clicked
            console.log('Botón presionado!');
        },
    });

    return CustomFormController;
});
