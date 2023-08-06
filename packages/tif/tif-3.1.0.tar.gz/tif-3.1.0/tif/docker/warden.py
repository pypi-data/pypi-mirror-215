from tif.fabric.logger import Logger
from tif.fabric import cli


class Warden:
    def __init__(self, environment_dir : str, services : dict) -> None:
        self.environment_dir = environment_dir
        self.logger = Logger()
        self.services = services

    def start(self, context):
        command = "warden svc start"
        self._log_command(command)
        context.run(command, pty=True)


    def stop(self, context):
        command = "warden svc stop"
        self._log_command(command)
        context.run(command, pty=True)

    def sign_certificate(self, context):
        site = cli.prompt(">>> Enter the site for the certificate: ").strip()
        if not site:
            self.logger.error('Site is required to sign a certificate')
            exit()
        with context.cd(self.environment_dir):
            command = "warden sign-certificate {}".format(site)
            self._log_command(command)
            context.run(command, pty=True)

    def shell(self, context):
        command = "warden shell"
        with context.cd(self.environment_dir):
            self._log_command(command)
            context.run(command, pty=True)

    def up(self, context):
        command = "warden env up"
        with context.cd(self.environment_dir):
            self._log_command(command)
            context.run(command, pty=True)

    def env_start(self, context):
        command = "warden env start"
        with context.cd(self.environment_dir):
            self._log_command(command)
            context.run(command, pty=True)

    def env_stop(self, context):
        command = "warden env stop"
        with context.cd(self.environment_dir):
            self._log_command(command)
            context.run(command, pty=True)

    def varnish_hist(self, context):
        command = "warden env exec {} varnishhist".format(self.services['varnish'])
        with context.cd(self.environment_dir):
            self._log_command(command)
            context.run(command, pty=True)

    def varnish_log(self, context):
        command = 'warden env exec -T {} varnishlog'.format(self.services['varnish'])
        with context.cd(self.environment_dir):
            self._log_command(command)
            context.run(command, pty=True)

    def varnish_reload(self, context):
        command = "warden env exec {} varnishreload".format(self.services['varnish'])
        with context.cd(self.environment_dir):
            self._log_command(command)
            context.run(command, pty=True)
    
    def varnish_purge(self, context):
        command = "warden env exec {} varnishadm 'ban req.url ~ .'".format(self.services['varnish'])
        with context.cd(self.environment_dir):
            self._log_command(command)
            context.run(command, pty=True)
            self.logger.success("Successfully purged data from varnish service")

    def debug(self, context):
        command = "warden debug"
        with context.cd(self.environment_dir):
            self._log_command(command)
            context.run(command, pty=True)
    
    def db_query(self, context, db_user, db_password, db, query):
        query = "mysql -u{} -p{}  {} -e \"{}\"".format(db_user, db_password, db, query)
        command = "warden env exec {} {}".format(self.services['db'], query)
        with context.cd(self.environment_dir):
            self._log_command(command)
            context.run(command, pty=True)

    def db_import(self, context):
        dump_file = cli.prompt(">>> Enter dump file to import. Must be a .sql file: ").strip()
        if dump_file:
            command = "cat {} | warden {} import".format(dump_file, self.services['db'])
            with context.cd(self.environment_dir):
                self._log_command(command)
                context.run(command, pty=True)
                self.logger.success("Dump file successfully imported!")
        else:
            self.logger.error("Aborted!")

    def bin_magento_exec(self, context, command):
        command = "warden env exec {} bin/magento {}".format(self.services['php'], command)
        with context.cd(self.environment_dir):
            self._log_command(command)
            context.run(command, pty=True)

    def artisan_exec(self, context, command):
        command = "warden env exec {} php artisan {}".format(self.services['php'], command)
        with context.cd(self.environment_dir):
            self._log_command(command)
            context.run(command, pty=True)

    def composer_install(self, context, flags = ''):
        command = "warden env exec {} composer install {}".format(self.services['php'], flags)
        with context.cd(self.environment_dir):
            self._log_command(command)
            context.run(command, pty=True)

    def composer_update(self, context, flags = ''):
        command = "warden env exec {} composer update {}".format(self.services['php'], flags)
        with context.cd(self.environment_dir):
            self._log_command(command)
            context.run(command, pty=True)
    
    def composer_run_setup_local_packages(self, context):
        command = "warden env exec {} composer run setup-local-packages".format(self.services['php'])
        with context.cd(self.environment_dir):
            self._log_command(command)
            context.run(command, pty=True)

    def composer_run_setup_vcs_packages(self, context):
        command = "warden env exec {} composer run setup-vcs-packages".format(self.services['php'])
        with context.cd(self.environment_dir):
            self._log_command(command)
            context.run(command, pty=True)
    
    def composer_require(self, context, flags = ''):
        package = cli.prompt(">>> Enter composer package to require: ").strip()
        if package:
            command = "warden env exec {} composer require {} {}".format(self.services['php'], package, flags)
            with context.cd(self.environment_dir):
                self._log_command(command)
                context.run(command, pty=True)

    def composer_require_dev(self, context, flags = ''):
        package = cli.prompt(">>> Enter dev composer package to require: ").strip()
        if package:
            command = "warden env exec {} composer require --dev {} {}".format(self.services['php'], package, flags)
            with context.cd(self.environment_dir):
                self._log_command(command)
                context.run(command, pty=True)

    def _log_command(self, command):
        self.logger.log("Running command '{}'".format(command))