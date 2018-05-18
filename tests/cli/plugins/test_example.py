"""Tests for Example Plugin."""

from ftb_overlay.utils import test


class ExamplePluginTestCase(test.ftboTestCase):
    def test_load_example_plugin(self):
        self.app.setup()
        self.app.plugin.load_plugin('example')
