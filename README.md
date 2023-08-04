# 📄 Context
PAM (Pluggable Authentication Modules) is a suite of Linux libraries used to standardize the process of user 
authentication across different applications. The authentication process goes through one of many possible "stacks" 
of modules, depending on the rules laid out in a PAM configuration file. Since PAM configuration files are programmed 
in a "goto" style, it's hard to debug them when e.g. certain users get unintended permissions in a system.

# 🛠️ Uses
This tool receives a PAM file and recursively traverses all the possible routes (stacks) that a user could 
take through various modules during authentication. When parsing is complete, it can generate a formatted text 
output outlining each possible stack and the corresponding module success codes.

# 👨‍💻 Feature Development

## 🏗️ Under Construction
* Mermaid diagram (flowchart) generation
* CLI integration

## 🔮 Future Plans
* Filter text stack output by success codes, modules, etc.
