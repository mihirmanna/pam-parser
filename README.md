# 📄 Context
PAM (Pluggable Authentication Modules) is a suite of Linux libraries used to standardize the process of user 
authentication across different applications. The authentication process goes through one of many possible "stacks" 
of modules, depending on the rules laid out in a PAM configuration file. Since the configuration files are programmed 
in a "goto" style, it's hard to debug them when e.g. certain users get unintended permissions in a system.

# 🛠️ Tool Features
This tool receives a PAM config file and recursively traverses all the possible routes (stacks) that a user could 
take through various modules during authentication. When parsing is complete, it can:
* Generate a formatted text output outlining each possible stack and the corresponding modules' success codes
* Generate a URL to a Mermaid flowchart that illustrates the tree of possible routes through the modules

# 👨‍💻 Feature Development

## 🏗️ Under Construction
* CLI integration

## 🛫 Future Plans
* Filter text stack output by success codes, modules, etc.
