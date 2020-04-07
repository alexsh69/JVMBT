from subprocess import Popen, PIPE
import logging

logger = logging.getLogger(__name__)

ERROR = "ERROR"
FAILED = "FAIL"


class Executor(object):
    def __init__(self):
        pass

    @staticmethod
    def execute(cmd: str) -> str:
        logger.info(f"Executing command: {cmd}")
        with Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True) as process:
            stdout = process.stdout.read().decode('utf-8')
            stderr = process.stderr.read().decode('utf-8')
        logger.info("Command completed!")
        logger.info(f"STDOUT: {stdout}")
        logger.info(f"STDERR: {stderr}")
        if len(stderr) > 0:
            if ERROR in stderr.upper() or FAILED in stderr.upper():
                raise RuntimeError(f"Process executor has exited with errors: {stderr}")
            else:
                logger.warning(f"Stderr was not empty (but does not contain error messages): {stderr}")
        return stdout
