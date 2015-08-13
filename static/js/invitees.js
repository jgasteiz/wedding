(function () {
    'use_strict';

    /**
     *  Invitees controller constructor.
     */
    var InviteesController = function () {
        this.selectedInvitees = [];

        var that = this;
        $('.invitee-selector').change(function () {
            that.selectInvitees(this);
        });

        $('.send-email').click(function () {
            that.sendEmails(this);
        });

        this.disableEmailButtons(true);
    }

    /**
     *  Given a boolean, enables or disables the buttons for sending emails.
     */
    InviteesController.prototype.disableEmailButtons = function (disabled) {
        $('.send-email').prop('disabled', disabled);
    };

    /**
     *  Given an element (checkbox), adds or removes an invitee id to/from the
     *  controller's selectedInvitees list.
     */
    InviteesController.prototype.selectInvitees = function (el) {
        var inviteeId = $(el).data('id'),
            isChecked = $(el).prop('checked');

        $('.invitee-row[data-row="' + inviteeId + '"]').toggleClass('bg-warning', isChecked);
        if (isChecked) {
            this.selectedInvitees.push(inviteeId);
        } else {
            var idIndex = this.selectedInvitees.indexOf(inviteeId);
            if (idIndex > -1) {
                this.selectedInvitees.splice(idIndex, 1);
            }
        }

        if (this.selectedInvitees.length > 0) {
            // Enable email buttons
            this.disableEmailButtons(false);
        } else {
            // Disable email buttons
            this.disableEmailButtons(true);
        }
    };

    /**
     *  Given an element (button), posts a payload with the selected invitees
     *  and the email id from the button.
     */
    InviteesController.prototype.sendEmails = function (el) {
        // Disable email buttons
        this.disableEmailButtons(true);

        var url = $(el).data('url'),
            emailId = $(el).data('email-id'),
            csrftoken = $(el).parent().data('csrftoken'),
            payload = {
                email: emailId,
                invitees: this.selectedInvitees,
                csrftoken: csrftoken
            },
            that = this;

        // Send payload to server.
        $.ajax({
            method: "POST",
            url: url,
            data: payload,
            headers: {'X-CSRFToken': csrftoken}
        })
        .done(function(response) {
            window.location.reload();
        })
        .fail(function(response) {
            that.disableEmailButtons(false);
            console.log(response);
        });
    };

    // Initialise the controller.
    var inviteesController = new InviteesController();
})();
