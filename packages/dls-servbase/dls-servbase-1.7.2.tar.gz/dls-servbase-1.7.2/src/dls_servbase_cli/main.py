#!/usr/bin/env python

import argparse
import logging
import multiprocessing

# Base class with methods supporting MaxIV command-line programs.
from dls_mainiac_lib.mainiac import Mainiac

# The subcommands.
from dls_servbase_cli.subcommands.service import Service

# The package version.
from dls_servbase_cli.version import meta as version_meta
from dls_servbase_cli.version import version

logger = logging.getLogger(__name__)


# --------------------------------------------------------------
class Main(Mainiac):
    def __init__(self, app_name):
        super().__init__(app_name)

    # ----------------------------------------------------------
    def run(self):
        """"""

        if self._args.subcommand == "service":
            Service(self._args, self).run()

        else:
            raise RuntimeError("unhandled subcommand %s" % (self._args.subcommand))

    # ----------------------------------------------------------
    def build_parser(self, arglist=None):
        """
        Method called from mainiac command line parsing.
        Should return argparser for this program.
        """

        # Make a parser.
        parser = argparse.ArgumentParser(
            description="Command line interface to dls-servbase.",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        )

        # --------------------------------------------------------------------

        parser.add_argument(
            "--log_name",
            help="basis name for log",
            type=str,
            metavar="string",
            dest="log_name",
            default=None,
        )

        # --------------------------------------------------------------------
        subparsers = parser.add_subparsers(help="subcommands", dest="subcommand")
        subparsers.required = True

        # --------------------------------------------------------------------
        subparser = subparsers.add_parser(
            "service",
            help="Start single service and block until ^C or remotely requested shutdown.",
        )
        Service.add_arguments(subparser)

        return parser

    # --------------------------------------------------------------------------
    def configure_logging(self, settings=None):
        """
        Configure runtime logging, override base class.
        Presume that self._args is already set.
        """

        if self._args.log_name is None:
            self._args.log_name = self._args.subcommand

        # Name as it appears in logging.
        multiprocessing.current_process().name = self._args.log_name

        # Set mainaic's program name to include the subcommand.
        self.program_name("%s/%s" % (self.program_name(), self._args.log_name))

        # Enable the multiprocessing queue listener.
        settings = {
            "mpqueue": {"enabled": True},
        }

        # Let the base class do most of the work.
        Mainiac.configure_logging(self, settings)

        # Don't show specific asyncio debug.
        logging.getLogger("asyncio").addFilter(_asyncio_logging_filter())

    # ----------------------------------------------------------
    def version(self):
        """
        Method called from mainiac command line parsing.
        Should return string in form of N.N.N.
        """
        return version()

    # ----------------------------------------------------------
    def about(self):
        """
        Method called from mainiac command line parsing.
        Should return dict which can be serialized by json.
        """

        return {"versions": version_meta()}


# --------------------------------------------------------------------------------
class _asyncio_logging_filter:
    """
    Python logging filter to remove annoying asyncio messages.
    These are not super useful to see all the time at the DEBUG level.
    """

    def filter(self, record):

        if "Using selector" in record.msg:
            return 0

        return 1


# ---------------------------------------------------------------
def main():

    # Instantiate the app.
    main = Main("dls_servbase_cli")

    # Configure the app from command line arguments.
    main.parse_args_and_configure_logging()

    # Run the main wrapped in a try/catch.
    main.try_run_catch()


# ---------------------------------------------------------------
def get_parser():
    """
    Called from sphinx automodule.
    """

    # Instantiate the app.
    main = Main("dls_servbase_cli")

    # Configure the app from command line arguments.
    return main.build_parser()


# ---------------------------------------------------------------
# From command line, invoke the main method.
if __name__ == "__main__":
    main()
