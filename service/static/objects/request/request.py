import os

from service.static.config_manager import ConfigManager

class Request(object):
    def __init__(self, input_args):
        self.build_type = input_args.build_type
        self.transaction_id = input_args.transactionId
        self.local_base = self.__get_local_path()
        self.run_script_path = self.__get_run_script_path(input_args.run_script_path)
        self.config = ConfigManager()

    def __get_run_script_path(self, run_script_relative_path: str) -> str:
        # Todo: There is a bug here. For some reason, this line returns C:\\{input_json['run_script_path']}
        # return os.path.join(self.local_base, run_script_relative_path)
        return self.local_base + run_script_relative_path

    def __get_local_path(self) -> str:
        return os.path.join(os.getcwd(), 'tmp', self.transaction_id)

    def get_tmp_out_folder(self):
        return os.path.join(self.local_base, "out", self.transaction_id)
