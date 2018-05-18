"""ftb-overlay main application entry point."""

from cement.core.exc import FrameworkError, CaughtSignal
from cement.core.foundation import CementApp
from cement.utils.misc import init_defaults

from ftb_overlay.core import exc

# Application default.  Should update config/ftb_overlay.conf to reflect any
# changes, or additions here.
defaults = init_defaults('ftb_overlay')

# All internal/external plugin configurations are loaded from here
defaults['ftb_overlay']['plugin_config_dir'] = '/etc/ftb_overlay/plugins.d'

# External plugins (generally, do not ship with application code)
defaults['ftb_overlay']['plugin_dir'] = '/var/lib/ftb_overlay/plugins'

# External templates (generally, do not ship with application code)
defaults['ftb_overlay']['template_dir'] = '/var/lib/ftb_overlay/templates'


class ftboApp(CementApp):
    class Meta:
        label = 'ftb_overlay'
        config_defaults = defaults

        # All built-in application bootstrapping (always run)
        bootstrap = 'ftb_overlay.cli.bootstrap'

        # Internal plugins (ship with application code)
        plugin_bootstrap = 'ftb_overlay.cli.plugins'

        # Internal templates (ship with application code)
        template_module = 'ftb_overlay.cli.templates'

        # call sys.exit() when app.close() is called
        exit_on_close = True


class ftboTestApp(ftboApp):
    """A test app that is better suited for testing."""

    class Meta:
        # default argv to empty (don't use sys.argv)
        argv = []

        # don't look for config files (could break tests)
        config_files = []

        # don't call sys.exit() when app.close() is called in tests
        exit_on_close = False


# Define the applicaiton object outside of main, as some libraries might wish
# to import it as a global (rather than passing it into another class/func)
app = ftboApp()


def main():
    with app:
        try:
            app.run()

        except exc.ftboError as e:
            # Catch our application errors and exit 1 (error)
            print('ftboError > %s' % e)
            app.exit_code = 1

        except FrameworkError as e:
            # Catch framework errors and exit 1 (error)
            print('FrameworkError > %s' % e)
            app.exit_code = 1

        except CaughtSignal as e:
            # Default Cement signals are SIGINT and SIGTERM, exit 0 (non-error)
            print('CaughtSignal > %s' % e)
            app.exit_code = 0


if __name__ == '__main__':
    main()
