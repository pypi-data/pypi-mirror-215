import asyncio
import logging
import multiprocessing
import os

import pytest

# Multiconf.
from dls_multiconf_lib.constants import ThingTypes as MulticonfThingTypes
from dls_multiconf_lib.multiconfs import Multiconfs, multiconfs_set_default

logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------------------------
class BaseContextTester:
    """
    This is a base class for tests which use Context.
    """

    def __init__(self):
        self.tasks_execution_outputs = {}
        self.residuals = ["stdout.txt", "stderr.txt", "main.log"]

        # Temporary directory (created later) for the live of this main program.
        self.__temporary_directory = None

    def main(self, constants, configuration_file, output_directory):
        """
        This is the main program which calls the test using asyncio.
        """

        # Save these for when the configuration is loaded.
        self.__configuration_file = configuration_file
        self.__output_directory = output_directory

        multiprocessing.current_process().name = "main"

        # self.__blocked_event = asyncio.Event()

        failure_message = None
        try:
            # Run main test in asyncio event loop.
            asyncio.run(self._main_coroutine(constants, output_directory))

        except Exception as exception:
            logger.exception(
                "unexpected exception in the test method", exc_info=exception
            )
            failure_message = str(exception)

        if failure_message is not None:
            pytest.fail(failure_message)

    # ----------------------------------------------------------------------------------------
    def get_multiconf(self):

        dls_servbase_multiconf = Multiconfs().build_object(
            {
                "type": MulticonfThingTypes.YAML,
                "type_specific_tbd": {"filename": self.__configuration_file},
            }
        )

        # For convenience, always do these replacement.
        dls_servbase_multiconf.substitute({"output_directory": self.__output_directory})

        # Add various things from the environment into the multiconf.
        dls_servbase_multiconf.substitute(
            {
                "CWD": os.getcwd(),
                "PYTHONPATH": os.environ.get("PYTHONPATH", "PYTHONPATH"),
            }
        )

        # Set the global value of our multiconf which might be used in other modules.
        multiconfs_set_default(dls_servbase_multiconf)

        return dls_servbase_multiconf
