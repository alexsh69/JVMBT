import logging
import os
import os.path
from os import path

from service.exceptions import JvmbtBuildException, FatJarNotExistsException

from ..build import Build

logger = logging.getLogger(__name__)


class SbtBuild(Build):
    def __init__(self, gradle_build_cmd, repository_root, final_jar_location, fail_string: str):
        super().__init__()
        self.sbt_build_cmd = gradle_build_cmd
        self.repository_root = repository_root
        self.final_jar_location = final_jar_location
        self.fail_string = fail_string
        self.complete_cmd = self.__build_command()
        logger.debug(f"Build command: {self.complete_cmd}")

    def build(self) -> str:
        work_dir  = os.getcwd()
        try:
            os.chdir(self.repository_root)
            out = self.process_executor.execute(cmd=self.complete_cmd)
        except Exception as e:
            raise e
        finally:
            os.chdir(work_dir)
        self.__check_build_status(out=out, fail_string=self.fail_string)
        return self.process_fat_jar_path()

    def __build_command(self):
        logger.debug("Building run command...")
        return self.sbt_build_cmd.format(repository_root=self.repository_root)

    @staticmethod
    def __check_build_status(out, fail_string):
        if fail_string in out.upper():
            logger.error(f"Maven build failed: {out}")
            raise JvmbtBuildException(f"Build failed! Stacktrace: {out}")

    def process_fat_jar_path(self):
        finalName = "internal.jar"
        finalFullPath = os.path.join(self.repository_root, "out", finalName)
        if not path.exists(finalFullPath):
            raise FatJarNotExistsException(f"FatJar file does not exists in a file system: {finalFullPath}")
        return finalFullPath

    def cleanup(self):
        target_directory = os.path.join(self.repository_root, "target")
        super().cleanup(build_base_path=target_directory)

        out_directory = os.path.join(self.repository_root, "out")
        super().cleanup(build_base_path=out_directory)
