+++
title = "Create a completion script"
type = "docs"
keywords = "command line,bash, zsh"
[menu.main]
    parent = "commandline"
    weight = 2
+++

Create a completion script
The completion script is code that uses the builtin bash command complete to define which completion suggestions can be displayed for a given executable. The nature of the completion options vary from simple static to highly sophisticated.

## Before you begin

*  [Install Dgraph]({{< relref "download" >}}#build-and-install).
*  Determine the shell you are running:
   ```bash
   echo $0
   ```
   An output similar to the following appears:
   ```bash
   user@workstation:~/dgraph$ echo $0
   bash
   ```

### Creating a completion script for Bash shell

1. To generate a `dgraph-completion.sh` configuration file for your `<SHELL>`, run the `completion` command:

    ```bash
    dgraph completion <SHELL> > ~/dgraph-completion.sh
    ```
    The contents of the file is similar to:
  
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
   The generated file has 2 lines at the beginning that need to be removed for the script to run properly.
  
1. You can comment out the 2 lines with a `#`, or remove them with the following command:

   ```bash
   sed -i.bak '1d;2d' ~/dgraph-completion.sh
   ```
1. Make the file executable by running the following command. You may require root user `sudo` privileges to run it:

   ```bash
   chmod +x ~/dgraph-completion.sh
   ```
1. Open the `.bashrc` file with any text editor. You might need `sudo` privileges to apply changes. For example:
   ```bash
   nano ~/.bashrc
   ```
1. Add the path to `dgraph-completion.sh` using the following syntax and save the file:
   ```bash
   . path/to/dgraph-completion.sh
   ```
1. Reload the `bashrc` settings with the following command:
   ```bash
   source ~/.bashrc
   ```
Now you can start typing `dgraph` and press <kbd>tab</kbd> to get auto-completion and suggestions:

```bash
user@workstation:~/dgraph$ dgraph 
acl            cert           debug          increment      migrate        tool           zero
alpha          completion     debuginfo      live           raftmigrate    upgrade        
bulk           conv           export_backup  lsbackup       restore        version   
```
