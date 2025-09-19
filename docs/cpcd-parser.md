# The CPCD Parser

The Community Physical Constant Dictionary (CPCD) parser is a command-line tool that allow users to generate a Fortran source file containing all or a selection of the contstants in the YAML
Physical Constants Dictionary.

## Requirements

The CPCD parser requires:
- The yaml-cpp library (version 0.6.2 or later), an open-source YAML parser and emitter written in C++ that supports [YAML version 1.2](https://yaml.org/spec/1.2/spec.html)
- A C++ compiler supporting the C++11 standard

## Installation

At this time, the CPCD parser is distributed within the same repository as the Community Physical Constant Dictionary in the `tools/` directory, under a GNU General Public License ([GPL](https://www.gnu.org/licenses/gpl-3.0.en.html)).

### Getting the Source Code

The source code can be downloaded as follows:

```bash
git clone https://github.com/ESCOMP/PhysicalConstantsDictionary.git
```

### Installing yaml-cpp

The yaml-cpp library uses CMake to support cross-platform building. A custom distribution for the yaml-cpp library (version 0.6.2) using the standard GNU build system is available [here](https://github.com/NESII/yaml-cpp/tree/gnu_autotools).

To download and build yaml-cpp, follow these steps:

```bash
git clone -b gnu_autotools https://github.com/NESII/yaml-cpp.git
cd yaml-cpp
./configure --prefix=<your_yamlcpp_installation_path>
make
make install
```

### Building the CPCD parser

The CPCD parser uses a standard GNU build system. To build this package on a given platform, the configure script needs to be run first:

```bash
./configure
```

This script will look for a suitable compiler (supporting C++11), then attempt to find the yaml-cpp library. The library's installation path can be provided to configure via:

1. The `YAML_CPP` environment variable, set after loading the corresponding yaml-cpp module in common installations
2. The `--with-yamlcpp` configure option, e.g.:

```bash
./configure --with-yamlcpp=/usr/local/yaml-cpp/0.6.2
```

The configure script also allows to set the installation path for the CPCP parser:

```bash
./configure --prefix=/usr/local/cpcd
```

A complete list of configure options can be obtained by typing:

```bash
./configure --help
```

Once configure completes successfully, the CPCD parser can be built by typing:

```bash
make
```

and installed as:

```bash
make install
```

The last step will install the `cpcd` executable under the `bin/` subdirectory of your installation path, e.g.: `/usr/local/cpcd/bin/cpcd`.

## Running the CPCD parser

The CPCD parser provides a command-line interface and can be driven through multiple options. A full list of options can be obtained by running `cpcd` with no options, or as `cpcd --help`:

```bash
$ ./src/cpcd --help
Usage: cpcd [options] ...
Main tool to validate, parse, and extract physical constant sets from the Community Physical Constant Dictionary

Mandatory arguments to long options are mandatory for short options too.
  -d, --dictionary YAML_FILE    Use YAML_FILE as dictionary
  -r, --request YAML_FILE       Extract constants listed in YAML_FILE (optional)
                                If not specified, extracts all constants
  -o, --output FILE             Save Fortran output to FILE
  -x, --validate                Validate dictionary file before proceeding
  -v, --verbose                 Use verbose output
  -V, --version                 Print version information
  -h, --help                    Display available options

Exit status: 0 if successful, 1 if an error occurs.
For bugs reporting, please visit: <https://github.com/ICAMS-US/PhysicalConstantsDictionary>
```

### Request File Format

A collection of physical constants to be extracted from the dictionary can be provided to the CPCD parser also in a YAML file. A sample file (`req.yaml`) is distributed with this package in the `cpcd/test/` directory. Its content is included below:

```yaml
# This is an example of a user-requested list of physical constants
# to be looked up in the dictionary by the CPCD parser and included
# in the generated source code.

mathematical: [pi, em_gamma, square_root_of_2]
universal_physical:
    - standard_acceleration_of_gravity
    - speed_of_light_in_vacuum
    - stefan_boltzmann_constant
earth_physical: mean_radius
water: [ liquid_water_triple_point_density, vapor_water_triple_point_density ]
```

### Example Usage

The CPCD parser will output a source file that can be added to a model source code. Fortran is the only output language currently supported by the CPCD parser.

The following command:

```bash
$ cpcd -d pcd.yaml -r req.yaml
```

will generate the Fortran module file `cpcd_mod.F90` in the current directory. This file will contain the extracted physical constants as Fortran parameters, declared by default as double precision:

```fortran
module cpcd

  integer, parameter :: cpcd_kind = kind(1.d0)

  character(len=*), parameter :: cpcd_version = '0.0.1'
  character(len=*), parameter :: cpcd_institution = 'ICAMS'

! - from set mathematical
  real(cpcd_kind), parameter :: mathematical_pi = 3.141592653589793238462643_cpcd_kind
  real(cpcd_kind), parameter :: mathematical_em_gamma = 0.577215664901532860606512_cpcd_kind
  real(cpcd_kind), parameter :: mathematical_square_root_of_2 = 1.4142135623730950488_cpcd_kind
! - from set universal_physical
  real(cpcd_kind), parameter :: universal_physical_speed_of_light_in_vacuum = 299792458_cpcd_kind
  real(cpcd_kind), parameter :: universal_physical_standard_acceleration_of_gravity = 9.80665_cpcd_kind
  real(cpcd_kind), parameter :: universal_physical_stefan_boltzmann_constant = 5.67036713E-08_cpcd_kind
! - from set earth_physical
  real(cpcd_kind), parameter :: earth_physical_mean_radius = 6371008.7714_cpcd_kind
! - from set water
  real(cpcd_kind), parameter :: water_liquid_water_triple_point_density = 999.793_cpcd_kind
  real(cpcd_kind), parameter :: water_vapor_water_triple_point_density = 0.00485458_cpcd_kind

end module cpcd
```
