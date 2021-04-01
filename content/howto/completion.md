+++
date = "2017-03-20T22:25:17+11:00"
description = "Dgraph supports command-line completion, a common feature provided by shells like bash or zsh that helps you to type commands in a fast and easy way."
title = "Shell Completion"
weight = 1
[menu.main]
    parent = "howto"
+++

Command-line completion is a common feature provided by shells like `bash` or `zsh` that lets you type commands in a fast and easy way.
This functionality automatically fills in partially typed commands when the user press the <kbd>tab</kbd> key.

## Completion script

The command-line interpreter requires a completion script to define which completion suggestions can be displayed for a given executable. 

Using the `dgraph completion` command you can generate a file that can be added to your shell configuration. Once added, you will be able to auto-complete any `dgraph` command.

{{% notice "note" %}}
Dgraph command completion currently supports `bash` and `zsh` shells.
{{% /notice %}}

First, you need to know which shell you are running. If you don't know, you can execute the following command:
```sh
echo $0
```

and the output should look like:

```sh
user@workstation:~/dgraph$ echo $0
bash
```

## Bash shell

To generate a `dgraph-completion.sh` configuration file for your `bash` shell, run the `completion` command as follows:

```sh
dgraph completion bash > ~/dgraph-completion.sh
```

The file content should look like:

```bash
[Decoder]: Using assembly version of decoder
Page Size: 4096
# bash completion for dgraph                               -*- shell-script -*-

__dgraph_debug()
{
    if [[ -n ${BASH_COMP_DEBUG_FILE} ]]; then
        echo "$*" >> "${BASH_COMP_DEBUG_FILE}"
    fi
}
...
..
.
```

Currently, the generated file has 2 lines at the beginning that need to be removed, or else the script won't run properly.
You can comment them out with a `#`, or you can easily remove them with the following command:

```sh
sed -i.bak '1d;2d' ~/dgraph-completion.sh
```

Next, you have to make that file executable by running the following command (your system might require `sudo` to run it):

```sh
chmod +x ~/dgraph-completion.sh
```

Now open the `.bashrc` file with any text editor (you might need `sudo` to apply changes). For example:

```sh
nano ~/.bashrc
```

Once opened, add the path to `dgraph-completion.sh` using the following syntax and save:

```sh
. path/to/dgraph-completion.sh
```

Finally, reload the `bashrc` settings with the following command:

```sh
source ~/.bashrc
```

Now you can start typing `dgraph` and press <kbd>tab</kbd> to get auto-completion and suggestions:

```txt
user@workstation:~/dgraph$ dgraph 
acl            cert           debug          increment      migrate        tool           zero
alpha          completion     debuginfo      live           raftmigrate    upgrade        
bulk           conv           export_backup  lsbackup       restore        version   
```
