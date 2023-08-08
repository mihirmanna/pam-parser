from parse_functions import *
import argparse

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='This tool parses PAM files into human-readable formats, enabling '
                                                 'systems admins to more easily debug them.')

    # Positional arguments
    parser.add_argument(
        'config_file',
        type=str,
        help='The path to the PAM config file')

    # Options
    parser.add_argument(
        '-m', '--mermaid',
        default=False,
        action='store_true',
        help='Return a URL to the Mermaid flowchart'
    )
    parser.add_argument(
        '-r', '--rules_list',
        default=False,
        action='store_true',
        help='Return a formatted list of all rules in the PAM config file'
    )
    parser.add_argument(
        '-s', '--text_stacks',
        default=False,
        action='store_true',
        help='Return a list of all possible stacks'
    )
    parser.add_argument(
        '-t', '--module_type',
        type=str,
        help='Only modules of this type are included in the stack outputs. '
             'Must be one of: auth, account, password, session'
    )

    args = parser.parse_args()
    config_list = read_config(args.config_file)
    rules = parse_rules(config_list)

    if args.mermaid is True:
        if args.module_type is None:
            parser.error('The --mermaid (-m) argument requires --module_type (-t) MODULE_TYPE')
        else:
            print(generate_mermaid(rules, 'PAM Configuration', args.module_type))
    if args.text_stacks is True:
        if args.module_type is None:
            parser.error('The --mermaid (-m) argument requires --module_type (-t) MODULE_TYPE')
        else:
            stacks = generate_stacks(rules, args.module_type, [[]])
            print_formatted_stacks(stacks)
    if args.rules_list is True:
        print_formatted_config(rules)