from glitchtech_ai.tools import OpenAi, ManageSettings


class Main:
    def __init__(self):
        self.ms = ManageSettings(project_name="GlitchTech-AI")
        self.oa = OpenAi(prompt="You are a tired butler.")

        self.prompt = "[ OA ]-> "

    def toggle_persistent_messages(self) -> bool:
        toggled = str(not self.ms.config.getboolean("main", "persistent_messages"))

        self.ms.store_setting(key="persistent_messages", value=toggled)
        self.oa.persistent_messages = self.ms.config.getboolean("main", "persistent_messages")

        return self.oa.persistent_messages

    def populate_defaults(self, token):
        self.ms.store_setting(key="persistent_messages", value="True")
        self.ms.store_setting(key="open_ai_token", value=token)
        return "[!] Settings file has been created."

    def validate_token(self):
        token = "open_ai_token"

        if self.ms.settings_file_exists() and self.oa.token:
            return True

        if self.ms.setting_exists(key=token) and not self.oa.token:
            print('No API token detected. Attempting to import from settings.')
            self.oa.update_token(token=self.ms.retrieve_setting(key=token))
            return True

        if not self.ms.setting_exists(key=token) and not self.oa.token:
            command = input('No API token detected. Please enter valid OpenAI token: ')
            self.populate_defaults(token=command)
            self.oa.update_token(token=self.ms.retrieve_setting(key=token))
            return True

        return False

    def prompt_command(self):
        command = input(self.prompt)
        if command.lower() in ['quit', 'q', 'exit', 'e']:
            print(self.oa.session_usage)
            return False
        elif command.lower() in ['persistent_messages', 'pm']:
            print(f"Persistent Messages: {self.toggle_persistent_messages()}")
            return True
        elif command:
            print(self.oa.chat_completions(user_input=command))
            return True


def cli():
    main = Main()

    while True:
        main.validate_token()

        if not main.prompt_command():
            break


if __name__ == '__main__':
    cli()
