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

```bash title="Add CorrectMatch package to Julia"
julia -e 'using Pkg; Pkg.add("CorrectMatch")'
```