"""CLI tests for ftb_overlay."""

from ftb_overlay.utils import test


class CliTestCase(test.ftboTestCase):
    def test_ftb_overlay_cli(self):
        argv = ['--foo=bar']
        with self.make_app(argv=argv) as app:
            app.run()
            self.eq(app.pargs.foo, 'bar')
