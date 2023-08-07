import re
from enum import IntEnum


class Flag(IntEnum):
    """Enumerates the different control flags"""

    SUCCESS = 0
    IGNORE = 1
    DEFAULT = 2


class Rule:
    """Outlines a PAM rule object with various attributes"""

    def __init__(self, line_num: int, module_type: str, control: str, module: str, args=None):
        """
        Constructs a new PAM rule with the given parameters
        :param line_num: The line number of the rule in the PAM file
        :param module_type: Can be one of four types: auth, account, password, or session
        :param control: Control flags for controlling success/failure behavior
        :param module: The name of the module (ex: pam_env.so)
        :param args: List of tokens for controlling module behavior
        """

        # Check module type and assign it
        if not (module_type in ['auth', 'account', 'password', 'session']):
            raise Exception('Invalid module type')
        else:
            self.type = module_type

        # Assign control flags [success, ignore, default]
        self.controls: list = [None, None, None]
        self.parse_control_list(control)

        self.line_num = line_num
        self.module = module
        self.args = args

    def parse_control_list(self, control: str):
        """
        Parses the control flag(s) into success, ignore, and default flags for this rule
        :param control: The control flag(s) provided in the rule definition
        :return: None
        """

        if control == 'required':
            self.controls[Flag.SUCCESS] = 'ok'
            self.controls[Flag.IGNORE] = 'ignore'
            self.controls[Flag.DEFAULT] = 'bad'
        elif control == 'requisite':
            self.controls[Flag.SUCCESS] = 'ok'
            self.controls[Flag.IGNORE] = 'ignore'
            self.controls[Flag.DEFAULT] = 'die'
        elif control == 'sufficient':
            self.controls[Flag.SUCCESS] = 'done'
            self.controls[Flag.IGNORE] = None
            self.controls[Flag.DEFAULT] = 'ignore'
        elif control == 'optional':
            self.controls[Flag.SUCCESS] = 'ok'
            self.controls[Flag.IGNORE] = None
            self.controls[Flag.DEFAULT] = 'ignore'
        elif control == 'include':
            self.controls[Flag.SUCCESS] = None
            self.controls[Flag.IGNORE] = None
            self.controls[Flag.DEFAULT] = None
        elif '[' in control:  # If the control flags are explicitly listed in the config
            if 'success=' in control:
                self.controls[Flag.SUCCESS] = re.findall('(?<=success=)([a-z]*\\d*)', control)[0]
            if 'ignore=' in control:
                self.controls[Flag.IGNORE] = re.findall('(?<=ignore=)([a-z]*\\d*)', control)[0]
            if 'default=' in control:
                self.controls[Flag.DEFAULT] = re.findall('(?<=default=)([a-z]*\\d*)', control)[0]
