---
title: Command-line completion
---

Command-line completion is a feature in shells such as `bash` or `zsh` that saves you extra typing and helps out when you cannot remember a command’s syntax.
This functionality automatically fills in partially typed commands when you press the <kbd>tab</kbd> key.

Some of the advantages of command-line completion are:

* saves you from typing text when it can be auto-completed
* helps you know what are the available continuations for the commands
* prevents errors and improve the experience by hiding or showing options based on what you have already typed

## Completion script

The command-line interpreter requires a completion script to define which completion suggestions can be displayed for a given executable. 

Using the `dgraph completion` command you can generate a file that can be added to your shell configuration. After you add the file you can auto-complete any `dgraph` command.

:::note
Dgraph command completion currently supports `bash` and `zsh` shells.
:::
