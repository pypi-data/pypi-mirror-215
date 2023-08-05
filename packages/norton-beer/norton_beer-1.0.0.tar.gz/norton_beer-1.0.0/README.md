[![CI pipeline](https://github.com/konstntokas/norton_beer/actions/workflows/python-package.yml/badge.svg)](https://github.com/konstntokas/norton_beer/actions/workflows/python-package.yml)
[![Coverage Status](https://coveralls.io/repos/github/konstntokas/norton_beer/badge.svg?branch=coverall_coverage)](https://coveralls.io/github/konstntokas/norton_beer?branch=coverall_coverage)

# norton_beer

The 'norton_beer' library is a python tool box for the Norton-Beer apodization functions.


## Main features

- Norton-Beer apodization window generation in spatial domain
- the analytical Fourier transform of the apodization window also known as instrument line shape (ILS)
- generation of new apodization window for a fixed spatial resolution of the ILS so that the sides lobes are minimized

## Installation

To use norton_beer, first install it using pip:

```pip install norton_beer```

## Testing

To test the `norton_beer` package, clone the repository and run:

```pytest```

Note that pytest needs to be installed on the local machine. 

## Documentation

- add paper when published
- add webpage of sphinx built documentation

