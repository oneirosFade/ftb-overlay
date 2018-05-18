"""Testing utilities for ftb-overlay."""

from cement.utils.test import *

from ftb_overlay.cli.main import ftboTestApp


class ftboTestCase(CementTestCase):
    app_class = ftboTestApp

    def setUp(self):
        """Override setup actions (for every test)."""
        super(ftboTestCase, self).setUp()

    def tearDown(self):
        """Override teardown actions (for every test)."""
        super(ftboTestCase, self).tearDown()
