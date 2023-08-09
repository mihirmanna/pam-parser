# 📄 Description

## What is PAM?
[PAM][pam-url] (Pluggable Authentication Modules) is a suite of Linux libraries used to standardize the process of user 
authentication across different applications. The authentication process goes through one of many possible "stacks" 
of modules, depending on the rules laid out in a PAM configuration file. Since the configuration files are programmed 
in a "goto" style, it's hard to debug them when e.g. certain users get unintended permissions in a system. An example PAM config file is shown below.

```
% cat example_config

# sshd: auth account password session
auth       optional       pam_krb5.so use_kcminit
auth       optional       pam_ntlm.so try_first_pass
auth       optional       pam_mount.so try_first_pass
auth       required       pam_opendirectory.so try_first_pass
account    required       pam_nologin.so
account    required       pam_sacl.so sacl_service=ssh
account    required       pam_opendirectory.so
password   required       pam_opendirectory.so
session    required       pam_launchd.so
session    optional       pam_mount.so
```

## What does this tool do?
This command-line tool receives a PAM config file and recursively traverses all the possible routes (stacks) that a 
user could take through various modules during authentication. When parsing is complete, it can display various human-readable outputs, depending on the options specified by the user.

# ⭐️ Getting Started

## Prerequisites
This tool was developed using Python `3.10` and it is recommended to run it on that version or later to minimize the risk of errors. However, any Python version `3.x` should be able to run this tool without problems.

All requisite modules are part of the Python standard library.

## Installation
1. Navigate to this repository's [Releases][releases-url] page in order to find and download the latest release of this tool.
2. Unzip the file into a directory from which you'd like to access the tool.

Now you're ready to go! 🎉

# 🛠️ Usage
1. Open your computer's terminal application and navigate into the tool's directory (i.e. into the folder you unzipped).
2. Inside the directory, execute the following command (note the optional flags).
```
python pam_parser.py [-h] [-m] [-r] [-s] [-t MODULE_TYPE] config_file
```

## Arguments
This tool provides a number of optional flags available to the user, as well as the required `config_file` argument. It's generally recommended to use one flag at a time, although there are exceptions.

### `-h (--help)`
This flag shows the help message for the command-line tool. It does not require the `config_file` argument.

### `-r (--rules_list)`
This flag returns a formatted list of all the rules in the PAM config file. It also translates control flags such as `required`, `optional`, and `include`. An output for the above PAM config is shown below.
```
% python pam_parser.py -r example_config

Ln     Type        Module                    Success    Ignore     Default    Args
-----------------------------------------------------------------------------------
1      auth        pam_krb5.so               ok         None       ignore     use_kcminit
2      auth        pam_ntlm.so               ok         None       ignore     try_first_pass
3      auth        pam_mount.so              ok         None       ignore     try_first_pass
4      auth        pam_opendirectory.so      ok         ignore     bad        try_first_pass
5      account     pam_nologin.so            ok         ignore     bad        None
6      account     pam_sacl.so               ok         ignore     bad        sacl_service=ssh
7      account     pam_opendirectory.so      ok         ignore     bad        None
8      password    pam_opendirectory.so      ok         ignore     bad        None
9      session     pam_launchd.so            ok         ignore     bad        None
10     session     pam_mount.so              ok         None       ignore     None
```

### `-s (--text_stacks)`
This flag returns a list of all the possible stacks that the user could take through a set of modules. The list is filtered by module type, indicated by the `-t` flag. An output for the above PAM config file, filtered by `auth`, is shown below.
```
% python pam_parser.py -s -t auth example_config

1 pam_krb5.so SUCCESS=ok
2 pam_ntlm.so SUCCESS=ok
3 pam_mount.so SUCCESS=ok
4 pam_opendirectory.so SUCCESS=ok
[Exit stack]
---------------------
1 pam_krb5.so SUCCESS=ok
2 pam_ntlm.so SUCCESS=ok
3 pam_mount.so SUCCESS=ok
4 pam_opendirectory.so IGNORE=ignore
[Exit stack]
---------------------
1 pam_krb5.so SUCCESS=ok
2 pam_ntlm.so SUCCESS=ok
3 pam_mount.so SUCCESS=ok
4 pam_opendirectory.so DEFAULT=bad
[Exit stack]
---------------------
...
```

### `-m (--mermaid)`
This flag returns an auto-generated URL to a Mermaid flowchart illustrating the tree of possible routes through the PAM config file. Like the `-s` flag, this one is also filtered by module type, indicated by the `-t` flag. An output for the above PAM config file, filtered by `session`, is shown below.
```
% python pam_parser.py -m -t session example_config

https://mermaid.ink/img/...
```
This URL can be entered into any web browswer to get the following image.

<p align="center">
  <img src=https://mermaid.ink/img/LS0tCnRpdGxlOiBQQU0gQ29uZmlndXJhdGlvbiAtIHNlc3Npb24KLS0tCmdyYXBoCjlbcGFtX2xhdW5jaGQuc29dCjEwW3BhbV9tb3VudC5zb10KeHtkaWV9CmR7ZG9uZX0KCnN0eWxlIHggZmlsbDojZjE0MzQzCnN0eWxlIGQgZmlsbDojNDNmMTY4Cgo5LS0+fFNVQ0NFU1M9b2t8MTAKbGlua1N0eWxlIDAgc3Ryb2tlOiBncmVlbgo5LS0+fElHTk9SRT1pZ25vcmV8MTAKOS0uLT58REVGQVVMVD1iYWR8MTAKbGlua1N0eWxlIDIgc3Ryb2tlOiBncmF5CjEwLS0+fFNVQ0NFU1M9b2t8ZApsaW5rU3R5bGUgMyBzdHJva2U6IGdyZWVuCjEwLS0+fERFRkFVTFQ9aWdub3JlfGQK
 />
</p>

### `-t (--module_type) MODULE_TYPE`
This flag doesn't do anything on its own. It is used in conjunction with the `-s` or `-m` flags in order to filter them by module type. The provided `MODULE_TYPE` must be one of:
* auth
* account
* password
* session

See the above code for usage examples.

### `config_file`
This required argument specifies the path (relative or absolute) pointing to the PAM configuration file.

# 👨‍💻 Development
See the [Issues][issues-url] page for a full list of proposed features (and known issues).

## Contributions
Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are greatly appreciated!

If you have a suggestion that would make this tool better, please feel free to fork the repo and create a pull request. 😄

# ⚠️ License
Distributed under the MIT License. See `LICENSE.md` for more information.

<!--URLs-->
[pam-url]: https://www.redhat.com/sysadmin/pluggable-authentication-modules-pam
[releases-url]: https://github.com/mihirmanna/pam-parser/releases
[issues-url]: https://github.com/mihirmanna/pam-parser/issues
