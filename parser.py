import base64
import copy
from IPython.display import Image, display
from rule import *


def read_config(file: str):
    """
    Reads a PAM config file and saves it to a 2D list
    :param file: The absolute path of the file
    :return: A 2D list formatting of the file
    """

    # Save file contents to a string
    with open(file, 'r') as f:
        lines = f.read()

    # Parse contents into a 2D list
    lines = lines.splitlines()
    lines_2d = []
    for line in lines:
        if len(line.strip()) == 0 or line[0] == '#':  # Ignore blank lines and comments in config file
            continue
        else:
            lines_2d.append(re.split(' +(?![^[]+])', line, 3))  # Regex ignores whitespace between []

    return lines_2d


def filter_2d(list_2d: list[list[str]], key: str, positive_search=True):
    """
    Filters a 2D list based on the provided key
    :param list_2d: The list to filter
    :param key: The key to filter by
    :param positive_search: True if accepting only lists with the key, False if accepting only lists without the key
    :return: The filtered 2D list
    """

    filtered_list = []
    for list_ in list_2d:
        if positive_search is True:
            if key in list_:
                filtered_list.append(list_)
        else:
            if key not in list_:
                filtered_list.append(list_)

    return filtered_list


def parse_rules(rule_list: list[list[str]]):
    """
    Parses the list of config rules into a list of Rule objects with the corresponding attributes
    :param rule_list: The list of config rules
    :return: A list of Rule objects
    """

    # Parse each rule into a Rule object
    rule_objects = []
    for i in range(len(rule_list)):
        line_num = i+1
        line = rule_list[i]
        if len(line) == 3:  # Rule definition has no args
            rule_objects.append(Rule(line_num, line[0], line[1], line[2]))
        elif len(line) > 3:  # Rule definition has args
            rule_objects.append(Rule(line_num, line[0], line[1], line[2], line[3]))

    return rule_objects


def traverse_all(rules_list: list[Rule], module_type: str, text_stacks: list[list[str]], exit_branch=False, curr_line=1):
    """
    Recursively traverses all paths through the PAM file and makes a list of them
    :param rules_list: The list of rules in the PAM file
    :param module_type: The type of the module in the PAM file
    :param exit_branch: True if done or die is raised, the ctrl flag is None, or we're at the end of the PAM file
    :param curr_line: The current line in the PAM file
    :param text_stacks The stack list, to be returned eventually
    :return: A list containing every possible stack
    """

    curr_rule = rules_list[curr_line - 1]

    # Base cases
    if (exit_branch is True) or (curr_line > len(rules_list)) or (curr_rule.type != module_type):
        text_stacks[-1].append('[Exit stack]')  # Append exit string to current last stack
        return text_stacks

    # Recursive case
    for i in range(3):

        ctrl_action = curr_rule.controls[i]

        if '[Exit stack]' in text_stacks[-1]:  # If the last stack is already complete...
            text_stacks.append(copy.deepcopy(text_stacks[-1]))  # Duplicate it so that the entire path is saved...

            # And remove the end of it, to replace with the current stack's modules
            while (str(curr_line) + ' ' + curr_rule.module) not in text_stacks[-1][-1]:
                del text_stacks[-1][-1]
            del text_stacks[-1][-1]

        # Add this module to the current stack
        text_stacks[-1].append(str(curr_line) + ' ' + curr_rule.module + ' ' + Flag(i).name + '=' + (ctrl_action or 'None'))

        # Go to the next module
        if ctrl_action is None:
            text_stacks = traverse_all(rules_list, module_type, text_stacks, True, curr_line)
        elif ctrl_action == 'done':
            text_stacks = traverse_all(rules_list, module_type, text_stacks, True, curr_line)
        elif ctrl_action == 'die':
            text_stacks = traverse_all(rules_list, module_type, text_stacks, True, curr_line)
        elif ctrl_action == 'ok':
            text_stacks = traverse_all(rules_list, module_type, text_stacks, False, curr_line + 1)
        elif ctrl_action == 'ignore':
            text_stacks = traverse_all(rules_list, module_type, text_stacks, False, curr_line + 1)
        elif ctrl_action == 'bad':
            text_stacks = traverse_all(rules_list, module_type, text_stacks, False, curr_line + 1)
        else:  # Skipping lines
            next_line = curr_line + 1 + int(ctrl_action)
            text_stacks = traverse_all(rules_list, module_type, text_stacks, False, next_line)

    return text_stacks


def generate_mermaid_script(rules_list: list[Rule], title: str, module_type: str):
    """
    Generates a Mermaid script to make a flowchart with the list of rules
    :param rules_list: The list of rules in the PAM file
    :param title: The title of the flowchart
    :param module_type: The type of the modules in this stack
    :return: The Mermaid flowchart script as a string
    """

    # Header
    script = ('---\n'
              f'title: {title}\n'
              '---\n')
    script += 'graph\n'

    # Nodes
    for rule in rules_list:
        if rule.type == module_type:
            script += f'{rule.line_num}[{rule.module}]\n'
    script += ('x{die}\n'
               'd{done}\n\n')

    # Node fill colors
    script += ('style x fill:#f14343\n'  # Die = red
               'style d fill:#43f168\n\n')  # Done = green

    # Arrows
    num_arrows = 0
    for rule in rules_list:
        for i in range(3):
            ctrl_action = rule.controls[i]

            # No arrow drawn
            if ctrl_action is None:
                continue

            script += f'{rule.line_num}'  # Initial node

            # Arrow styling
            if ctrl_action == 'bad':
                script += '-.->'  # Dotted arrow
            else:
                script += '-->'  # Solid arrow
            script += f'|{Flag(i).name}={ctrl_action}|'  # Arrow label (ex: SUCCESS=ok)

            # Final node
            if ctrl_action == 'done':
                script += 'd\n'
            elif ctrl_action == 'die':
                script += 'x\n'
            elif ctrl_action == 'ok':
                if rules_list[rule.line_num].type == module_type:
                    script += f'{rule.line_num + 1}\n'
                else:
                    script += 'd\n'
            elif ctrl_action == 'ignore':
                if rules_list[rule.line_num].type == module_type:
                    script += f'{rule.line_num + 1}\n'
                else:
                    script += 'd\n'
            elif ctrl_action == 'bad':
                if rules_list[rule.line_num].type == module_type:
                    script += f'{rule.line_num + 1}\n'
                else:
                    script += 'd\n'
            else:  # Skipping lines in PAM file
                next_line = rule.line_num + 1 + int(ctrl_action)
                if rules_list[next_line - 1].type == module_type:
                    script += f'{next_line}\n'
                else:
                    script += 'd\n'

            # Arrow color
            if i == 0:  # Current ctrl value is SUCCESS
                script += f'linkStyle {num_arrows} stroke: green\n'
            if ctrl_action == 'die':  # Arrow points to die
                script += f'linkStyle {num_arrows} stroke: red\n'
            if ctrl_action == 'bad':  # Arrow indicates bad stack
                script += f'linkStyle {num_arrows} stroke: gray\n'

            num_arrows += 1

    return script


def print_formatted_config(rules_list: list[Rule]):
    """Prints a formatted version of the PAM config file"""

    # Header
    print('Ln' + ' ' * 5 + 'Type' + ' ' * 8 + 'Module' + ' ' * 20 + 'Success' + ' ' * 4 + 'Ignore' + ' ' * 5 + 'Default' + ' ' * 4 + 'Args')
    print('-----------------------------------------------------------------------------------')

    # Rule properties
    for rule in rules_list:
        print(str(rule.line_num) + ' ' * (7 - len(str(rule.line_num))), end='')  # Line number
        print(rule.type + ' ' * (12 - len(rule.type)), end='')  # Rule type
        print(rule.module + ' ' * (26 - len(rule.module)), end='')  # Module name
        print(str(rule.controls[Flag.SUCCESS]) + (' ' * (11 - len(str(rule.controls[Flag.SUCCESS]))))  # Control flags
              + str(rule.controls[Flag.IGNORE]) + (' ' * (11 - len(str(rule.controls[Flag.IGNORE]))))
              + str(rule.controls[Flag.DEFAULT]) + (' ' * (11 - len(str(rule.controls[Flag.DEFAULT])))), end='')
        print(rule.args)  # Args


def print_formatted_stacks(stacks_list: list[list[str]]):
    """Prints a formatted version of the stack list"""

    for stack in stacks_list:
        for module in stack:
            print(module)
        print('---------------------')


if __name__ == '__main__':
    config_list = read_config('samplePAM.txt')
    rules = parse_rules(config_list)
    stacks = traverse_all(rules, 'auth', [[]])

    # Print rules and stack list to the console
    # print_formatted_config(rules)
    # print_formatted_stacks(stacks)
    print(generate_mermaid_script(rules, 'PAM Config', 'auth'))