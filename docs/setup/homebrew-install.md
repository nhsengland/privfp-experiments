# HomeBrew Installation

This codebase suuports both Apple users and those who have installed WSL on a windows machine.

## WSL Users

### Install Windows Subsystem for Linux (WSL)

If you haven't already done so, install WSL by following the official documentation provided by Microsoft: [Windows Subsystem for Linux Installation Guide.](https://learn.microsoft.com/en-us/windows/wsl/install)

```shell
wsl --install
```

### Set up a Sudo User Account

* Launch your WSL distribution and open a terminal window.
* Run the following command and replace **username** with your desired username, to create a user.

```bash
sudo adduser <username>
```

* Follow the prompts to set a password and fill in any additional information as required.

### Grant Sudo Permissions to the User Account

* Run the following command and replace **username** with your desired username, to add your user account to the sudo group.

```bash
sudo usermod -aG sudo <username>
```

### Switch to Your New User Account

* Log out of the current session by typing logout and press Enter.

```bash
logout
```

* Log back in using the newly created user account credentials.

```bash
su <username>
```

### Install Homebrew

* With your WSL terminal open and logged in as your newly created user, run the following command to install Homebrew:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

* Then follow the Next Steps given to you when you install HomeBrew to add Homebrew to your PATH.

### Verify HomeBrew Installation

* Close and reopen your WSL terminal to apply any changes to the shell configuration.
* Run the following command to verify that Homebrew is installed and configured correctly:

```bash
brew --version
brew update
```


## Apple Users

### 1. Install Homebrew

* With your WSL terminal open and logged in as your newly created user, run the following command to install Homebrew:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

* Then follow the Next Steps given to you when you install HomeBrew to add Homebrew to your PATH.

### 2. Verify HomeBrew Installation:

* Close and reopen your WSL terminal to apply any changes to the shell configuration.
* Run the following command to verify that Homebrew is installed and configured correctly:

```bash
brew --version
brew update
```