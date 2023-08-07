from parser import *


if __name__ == '__main__':
    config_list = read_config('samplePAM.txt')
    rules = parse_rules(config_list)
    stacks = generate_stacks(rules, 'auth', [[]])

    # Print rules and stack list to the console
    # print_formatted_config(rules)
    # print_formatted_stacks(stacks)
    # print(generate_mermaid(rules, 'PAM Config', 'auth'))
