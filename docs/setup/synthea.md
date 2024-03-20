# Synthea International

!!! warning

    Requires [OpenJDK](https://github.com/openjdk/jdk) to run. This particular setup was tested with [Homebrew openjdk@17](https://formulae.brew.sh/formula/openjdk) on an M1 MBP.

[Synthea](https://github.com/synthetichealth/synthea) is used for the structured generative component of Privacy Fingerprint with UK adaptation from [Synthea International](https://github.com/synthetichealth/synthea-international).

## Clone repositories

``` shell title="Open a terminal in a projects directory"
git clone https://github.com/nhsengland/privfp-experiments.git
git clone https://github.com/synthetichealth/synthea.git
git clone https://github.com/synthetichealth/synthea-international.git
```

## Modify Synthea

``` shell title="Checkout compatible versions"
cd synthea
git checkout fb43d3957762465211e70daeeb2bc00e0dbd1c1d

cd ../synthea-international
git checkout b4cd9a30f106957ae8f2682090d45b04a49a7c4b
```

``` shell title="Copy UK adaptation"
cp -R gb/* ../synthea
cd ../synthea
```

## Verify installation

``` shell title="Run Synthea"
./run_synthea "West Yorkshire"
```