import os
import platform

from configparser import ConfigParser


class ManageSettings:
    def __init__(self, project_name: str):
        self.project_name = project_name

        self.project_path = self._determine_project_path()
        self.settings_file_name = "settings.conf"

        self.settings_file_path = os.path.join(self.project_path, self.settings_file_name)

        self.config: ConfigParser
        self._setup_config()

    def _determine_project_path(self):
        if platform.system() == "Linux":
            return f"{os.environ['HOME']}/.cache/{self.project_name}"

        if platform.system() == "Windows":
            return f"{os.environ['LOCALAPPDATA']}\\{self.project_name}"

    def _setup_config(self):
        self.config = ConfigParser(allow_no_value=True)

        if not os.path.exists(self.project_path):
            os.makedirs(self.project_path)

        self.config.read(self.settings_file_path)

        if not self.config.has_section('main'):
            self.config.add_section('main')

    def settings_file_exists(self) -> bool:
        return os.path.exists(self.settings_file_path)

    def setting_exists(self, key) -> bool:
        return self.config.has_option('main', key)

    def store_setting(self, key: str, value: str):
        self.config.set('main', key, value)

        with open(self.settings_file_path, 'w') as f:
            self.config.write(f)

    def retrieve_setting(self, key):
        self.config.read(self.settings_file_path)
        return self.config.get('main', key)


if __name__ == '__main__':
    ls = ManageSettings(project_name="PersonalProject")
    ls.store_setting(key="persistent_messages_test_1", value="test")
    print(ls.setting_exists(key="persistent_messages_test_1"))
