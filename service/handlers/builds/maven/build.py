import logging
import os
import os.path
from os import path

from service.exceptions import JvmbtBuildException, FatJarNotExistsException

from ..build import Build
from service.handlers.factory.XmlFactory import XmlFactory

logger = logging.getLogger(__name__)


class MavenBuild(Build):
    def __init__(self, maven_build_cmd, repository_root, final_jar_location, fail_string: str):
        super().__init__()
        self.maven_build_cmd = maven_build_cmd
        self.repository_root = repository_root
        self.final_jar_location = final_jar_location
        self.fail_string = fail_string
        self.complete_cmd = self.__build_command()
        logger.debug(f"Build command: {self.complete_cmd}")

    def build(self) -> str:
        out = self.process_executor.execute(cmd=self.complete_cmd)
        self.__check_build_status(out=out, fail_string=self.fail_string)
        return self.process_fat_jar_path()

    def __build_command(self):
        logger.debug("Building run command...")
        return self.maven_build_cmd.format(repository_root=self.repository_root)

    @staticmethod
    def __check_build_status(out, fail_string):
        if fail_string in out.upper():
            logger.error(f"Maven build failed: {out}")
            raise JvmbtBuildException(f"Build failed! Stacktrace: {out}")

    def process_fat_jar_path(self):
        pom_file = os.path.join(self.repository_root, "pom.xml")
        customFileName = XmlFactory.process_xpath(pom_file, "/*[1]/*[local-name() = 'build']"
                                                            "/*[local-name() = 'finalName']/text()")
        artifactId = XmlFactory.process_xpath(pom_file, "/*[1]/*[local-name() = 'artifactId']/text()")
        version = XmlFactory.process_xpath(pom_file, "/*[1]/*[local-name() = 'version']/text()")

        finalName = f"{customFileName}.jar" if customFileName is not None else f"{artifactId}-{version}.jar"
        finalFullPath = os.path.join(self.repository_root, "target", finalName)
        if not path.exists(finalFullPath):
            raise FatJarNotExistsException(f"FatJar file does not exists in a file system: {finalFullPath}")
        return finalFullPath

    def cleanup(self):
        build_directory = os.path.join(self.repository_root, "target")
        super().cleanup(build_base_path=build_directory)

