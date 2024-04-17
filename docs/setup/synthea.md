# Setting up Synthea International

[Synthea](https://github.com/synthetichealth/synthea) is used for the structured generative component of Privacy Fingerprint with UK adaptation from [Synthea International](https://github.com/synthetichealth/synthea-international).

## Install openjdk via HomeBrew

!!! warning

    This particular setup was tested with [Homebrew openjdk@17](https://formulae.brew.sh/formula/openjdk).

You will need to ensure [HomeBrew](homebrew-install.md) is set-up correctly, then you can run:
``` shell title="Install openjdk@17"
sudo apt-get update
brew install openjdk@17
```

You can then verify OpenJDK 17 is installed by checking the version
```bash
java -version
```

## Clone repositories

!!! warning

    If you are using WSL, ensure you git clone Synthea using WSL. If you want to work in your local C: drive you can access this drive via the /mnt/c folder in your wsl terminal. For more information click [here](https://learn.microsoft.com/en-us/windows/wsl/faq).

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

## Modify Synthea Properties

You will need to replace the file inside the synthea repository (synthea/src/main/resources/synthea.properties) with the file located locally in this repository (privfp-experiments/src/generate/synthea_properties/synthea.properties).

