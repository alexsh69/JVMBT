from service.handlers.builds import SbtBuild, MavenBuild, GradleBuild
from service.static.config_manager import ConfigManager


class BuilderFactory(object):
    def __init__(self, input_argss):
        self.input_args = input_argss
        self.config = ConfigManager()

    def get_builder(self):
        builder = self._get_builder_type()
        cmd = self.config.get_builds[self.input_args.build_type]["cmd"]
        fail_string = self.config.get_builds[self.input_args.build_type]["fail_string"]
        return builder(
            cmd,
            self.input_args.sourcePath,
            self.input_args.fatJarLocation,
            fail_string
        )

    def _get_builder_type(self):
        builds = {
            "gradle": GradleBuild,
            "maven": MavenBuild,
            "sbt": SbtBuild
        }
        return builds[self.input_args.build_type]
