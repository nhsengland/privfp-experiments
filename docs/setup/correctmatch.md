# CorrectMatch

!!! warning

    Requires [Julia](https://github.com/JuliaLang/julia) to run. This particular setup was tested with [Julia version 1.8.5](https://julialang.org/downloads/) on an M1 MBP.

[CorrectMatch](https://github.com/computationalprivacy/pycorrectmatch) is used via a thin Python wrapper for the Julia module CorrectMatch.jl to estimate uniqueness from small population samples.

## Install CorrectMatch in Julia

``` shell title="Change working directory to privfp-experiments"
cd privfp-experiments
julia
```

``` julia title="Add CorrectMatch package"
using Pkg
Pkg.add("CorrectMatch")
```

## Install PyCorrectMatch dependencies

``` shell title="Create Python virtual environment"
python3.11 -m venv .venv
source .venv/bin/activate
```

``` shell title="Install correctmatch package"
pip install correctmatch
python
```

``` python title="Install Julia dependencies through virtual environment"
import julia
julia.install()
```

## Verify installlation

``` python title="Run correctmatch"
import numpy as np
import correctmatch

arr = np.random.randint(1, 5, size=(1000, 5))
correctmatch.precompile()  # precompile the Julia module
correctmatch.uniqueness(arr)  # true uniqueness for 1,000 records
```