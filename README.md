## Installing Bun

### macOS and Linux

```bash#macOS/Linux_(curl)
$ curl -fsSL https://bun.sh/install | bash # for macOS, Linux, and WSL
# to install a specific version
$ curl -fsSL https://bun.sh/install | bash -s "bun-v$BUN_LATEST_VERSION"
```


## Checking installation

To check that Bun was installed successfully, open a new terminal window and run `bun --version`.

```sh
$ bun --version
1.x.y
```
If you've installed Bun but are seeing a `command not found` error, you may have to manually add the installation directory (`~/.bun/bin`) to your `PATH`.

### How to add your `PATH`

{% details summary="Linux / Mac" %}
First, determine what shell you're using:

```sh
$ echo $SHELL
/bin/zsh # or /bin/bash or /bin/fish
```

Then add these lines below to bottom of your shell's configuration file.

```bash#~/.zshrc
# add to ~/.zshrc
export BUN_INSTALL="$HOME/.bun"
export PATH="$BUN_INSTALL/bin:$PATH"
```

```bash#~/.bashrc
# add to ~/.bashrc
export BUN_INSTALL="$HOME/.bun"
export PATH="$BUN_INSTALL/bin:$PATH"
```

```sh#~/.config/fish/config.fish
# add to ~/.config/fish/config.fish
export BUN_INSTALL="$HOME/.bun"
export PATH="$BUN_INSTALL/bin:$PATH"
```

