# Installing Julia

!!! warning

    Requires [Julia](https://github.com/JuliaLang/julia) to run. This particular setup was tested with [Julia version 1.8.5](https://julialang.org/downloads/) on an M1 MBP.

[CorrectMatch](https://github.com/computationalprivacy/pycorrectmatch) is used via a thin Python wrapper for the Julia module CorrectMatch.jl to estimate uniqueness from small population samples.

## Install Julia

Open a new terminal and install the recommended [julia installer](https://julialang.org/downloads/)
``` bash title="Install Julia"
curl -fsSL https://install.julialang.org | sh
```

``` bash title="Download Julia version 1.8.5 and set default to 1.8.5"
juliaup add 1.8.5
juliaup default 1.8.5
```

## Adding Julia to Path

You will want to use a text editor such as nano to edit your shell configuration file.

```bash title="Opening shell configuration file for Mac"
nano ~/.bash_profile
```

```bash title="Opening shell configuration file for WSL"
nano ~/.bashrc
```

Then on this file you will need to add this line to the bottom of this file
```txt title="Adding Julia to path"
export PATH="$HOME/.julia/juliaup/bin:$PATH"
```

You will need to reload the terminal OR you can run the following commands:

```bash title="Re-initialising the Shell for Mac"
source ~/.bash_profile
```

```bash title="Re-initialising the Shell for WSL"
source ~/.bashrc
```

## Adding CorrectMatch

```bash title="Add CorrectMatch package to Julia"
julia -e 'using Pkg; Pkg.add("CorrectMatch")'
```