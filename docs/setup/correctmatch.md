# CorrectMatch

!!! warning

    Requires [Julia](https://github.com/JuliaLang/julia) to run. This particular setup was tested with [Julia version 1.8.5](https://julialang.org/downloads/) on an M1 MBP.

[CorrectMatch](https://github.com/computationalprivacy/pycorrectmatch) is used via a thin Python wrapper for the Julia module CorrectMatch.jl to estimate uniqueness from small population samples.

## Install Julia

Open a new terminal and install the recommended [julia installer](https://julialang.org/downloads/)
``` shell title="Install Julia"
curl -fsSL https://install.julialang.org | sh
```

``` shell title="Download Julia version 1.8.5 and set default to 1.8.5"
juliaup add 1.8.5
juliaup default 1.8.5
```

``` julia title="Add CorrectMatch package to Julia"
julia -e 'using Pkg; Pkg.add("CorrectMatch")'
```

## Verify installlation

``` python title="Run correctmatch"
import numpy as np
import correctmatch
import julia
from julia.api import Julia
import os

path_julia = os.popen("which julia").read().strip()
julia.install(julia=path_julia)
Julia(compiled_modules=False, runtime=path_julia)

arr = np.random.randint(1, 5, size=(1000, 5))
correctmatch.precompile()  # precompile the Julia module
correctmatch.uniqueness(arr)  # true uniqueness for 1,000 records
```