import logging
# import shutil
# import stat
import os

# Internal packages:
from ..process import Executor

logger = logging.getLogger(__name__)
LINUX = 'posix'
WINDOWS = 'nt'


class Build(object):
    def __init__(self):
        self.process_executor = Executor()

    def build(self):
        pass

    def cleanup(self, build_base_path):
        try:
            # os.chmod(build_base_path, stat.S_IWRITE)
            # shutil.rmtree(path=build_base_path)
            if os.name == WINDOWS:
                os.system(f'rmdir /S /Q "{build_base_path}"')
            elif os.name == LINUX:
                os.system(f'rm -rf "{build_base_path}"')
            else:
                raise OSError(f"Unrecognized OS: {os.name}")
            logger.info("Cleanup complete!")
        except OSError as e:
            logger.warning(f"Error thrown while running cleanup: {e}")
