Just the scripts to generate data for [eleanor](https://github.com/afeinstein20/eleanor).

## Notes to self

To setup the environment:

```bash
conda env create --prefix ./env -f environment.yml
conda activate ./env
```

To update the environment:

```bash
conda env update --prefix ./env -f environment.yml --prune
```

To download FFIs (with the [tess-ffi-dl](https://github.com/dfm/tess-ffi-dl) package):

```bash
./tess-ffi-dl $FFI_PATH $SECTOR_NUMBER --threads=10
```

To generate postcards:

```bash
scripts/eleanor-postcards $SECTOR_NUMBER $FFI_PATH $FFI_PATH/tess/postcards
```

To generate backgrounds:

```bash
scripts/eleanor-backgrounds $SECTOR_NUMBER $FFI_PATH/tess/postcards
```
