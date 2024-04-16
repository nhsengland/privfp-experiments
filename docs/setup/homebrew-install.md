# HomeBrew Installation

[![Platform](https://img.shields.io/badge/Platform-UNIX%20%28Apple%20users%29%20%7C%20WSL%20%28Windows%20users%29-blue)](https://shields.io/)

This codebase supports both UNIX (Apple users) and Windows users who have installed Windows Subsystem for Linux (WSL).

HomeBrew is the recommended installer used in this repository and will need to be installed. For the official installation guidance [click here](https://docs.brew.sh/Installation).

If you are using a Windows machine you will need to install Windows Subsystem for Linux (WSL) to use HomeBrew. This is a more complicated process and would require you to:

1. Install WSL. For guidance [click here](https://learn.microsoft.com/en-us/windows/wsl/install).
2. Set-up a Sudo User Account.
3. Grant Sudo Permissions to the User Account.
4. Sign-in to your new Sudo User Account to install HomeBrew. (This is because HomeBrew **cannot** be installed on the root sudo user.)

For more detailed guidance, we have provided more detail below.

<details>
<summary>Recommended Homebrew Set-up for WSL users</summary>
<h2>WSL Users</h2>

<h3>Install Windows Subsystem for Linux (WSL)</h3>

<p>If you haven't already done so, install WSL by following the official documentation provided by Microsoft: <a href="https://learn.microsoft.com/en-us/windows/wsl/install">Windows Subsystem for Linux Installation Guide.</a></p>

<pre><code class="language-shell">wsl --install</code></pre>

<h3>Set up a Sudo User Account</h3>

<ul>
<li>Launch your WSL distribution and open a terminal window.</li>
<li>Run the following command and replace <strong>username</strong> with your desired username, to create a user.</li>
</ul>

<pre><code class="language-bash">sudo adduser &lt;username&gt;</code></pre>

<p>Follow the prompts to set a password and fill in any additional information as required.</p>

<h3>Grant Sudo Permissions to the User Account</h3>

<ul>
<li>Run the following command and replace <strong>username</strong> with your desired username, to add your user account to the sudo group.</li>
</ul>

<pre><code class="language-bash">sudo usermod -aG sudo &lt;username&gt;</code></pre>

<h3>Switch to Your New User Account</h3>

<ul>
<li>Log out of the current session by typing logout and press Enter.</li>
</ul>

<pre><code class="language-bash">logout</code></pre>

<ul>
<li>Log back in using the newly created user account credentials.</li>
</ul>

<pre><code class="language-bash">su &lt;username&gt;</code></pre>

<h3>Install Homebrew</h3>

<ul>
<li>With your WSL terminal open and logged in as your newly created user, run the following command to install Homebrew:</li>
</ul>

<pre><code class="language-bash">/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"</code></pre>

<p>Then follow the Next Steps given to you when you install HomeBrew to add Homebrew to your PATH.</p>

<h3>Verify HomeBrew Installation</h3>

<ul>
<li>Close and reopen your WSL terminal to apply any changes to the shell configuration.</li>
<li>Run the following command to verify that Homebrew is installed and configured correctly:</li>
</ul>

<pre><code class="language-bash">brew --version
brew update</code></pre>
</details>

<details>
<summary>Recommend HomeBrew set-up for Apple Users</summary>

<h3>1. Install Homebrew</h3>

<ul>
  <li>With your WSL terminal open and logged in as your newly created user, run the following command to install Homebrew:</li>
</ul>

<pre><code class="language-bash">/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
</code></pre>

<ul>
  <li>Then follow the Next Steps given to you when you install HomeBrew to add Homebrew to your PATH.</li>
</ul>

<h3>2. Verify HomeBrew Installation:</h3>

<ul>
  <li>Close and reopen your WSL terminal to apply any changes to the shell configuration.</li>
  <li>Run the following command to verify that Homebrew is installed and configured correctly:</li>
</ul>

<pre><code class="language-bash">brew --version
brew update
</code></pre>

</details>
