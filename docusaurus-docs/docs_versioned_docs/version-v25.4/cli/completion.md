---
title: dgraph completion
---

The `dgraph completion` command generates shell completion scripts for `bash` and `zsh`, making it easier to work with the Dgraph CLI by enabling tab completion for commands, subcommands, and flags.

## Installation

### Bash

To enable bash completion for the current session:

```bash
source <(dgraph completion bash)
```

To install bash completion permanently:

#### Linux

```bash
# Generate and save the completion script
dgraph completion bash > /etc/bash_completion.d/dgraph

# Reload your shell
source ~/.bashrc
```

#### macOS

```bash
# Install bash-completion if not already installed
brew install bash-completion

# Generate and save the completion script
dgraph completion bash > $(brew --prefix)/etc/bash_completion.d/dgraph

# Reload your shell
source ~/.bash_profile
```

### Zsh

To enable zsh completion for the current session:

```bash
source <(dgraph completion zsh)
```

To install zsh completion permanently:

```bash
# Add completion script to fpath
dgraph completion zsh > "${fpath[1]}/_dgraph"

# Reload your shell
exec $SHELL
```

Or add to your `~/.zshrc`:

```bash
autoload -U compinit
compinit
source <(dgraph completion zsh)
```

## Command Reference

```shell
Generates shell completion scripts for bash or zsh
Usage:
 dgraph completion [command]

Available Commands:
 bash        bash shell completion
 zsh         zsh shell completion

Flags:
 -h, --help   help for completion

Use "dgraph completion [command] --help" for more information about a command.
```

## Usage

Once installed, you can use tab completion to:

- Complete command names: `dgraph al<TAB>` → `dgraph alpha`
- Complete subcommands: `dgraph acl <TAB>` → shows `add`, `del`, `info`, `mod`
- Complete flag names: `dgraph alpha --re<TAB>` → `dgraph alpha --replicas`

## Troubleshooting

If completion isn't working:

1. **Verify installation**: Make sure the completion script is in the correct directory
2. **Check permissions**: Ensure the completion script is readable
3. **Reload shell**: Try opening a new terminal or running `exec $SHELL`
4. **Check version**: Ensure you're using a compatible shell version

For bash, you can verify completion is loaded:

```bash
complete -p dgraph
```

This should show output indicating the completion function is registered.

