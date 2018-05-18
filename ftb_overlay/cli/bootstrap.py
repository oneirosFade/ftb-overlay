"""ftb-overlay bootstrapping."""

# All built-in application controllers should be imported, and registered
# in this file in the same way as ftboBaseController.

from ftb_overlay.cli.controllers.base import ftboBaseController


def load(app):
    app.handler.register(ftboBaseController)
