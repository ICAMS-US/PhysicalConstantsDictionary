# Dictionary Syntax

The Physical Constants Dictionary (PCD) is codified in [YAML 1.2](http://yaml.org/spec/1.2/spec.html).

The content of such YAML file must comply with the current syntax rules:

## Main Structure

A PCD is a YAML node of kind [mappings](http://yaml.org/spec/1.2/spec.html), i.e. an unordered set of key: value node pairs, with the unique key name `physical_constants_dictionary`.

```yaml
physical_constants_dictionary:
  # Dictionary content goes here
```

## Top-Level Fields

The value associated to the `physical_constants_dictionary` key consists of the following YAML mapping nodes:

### version_number (optional)
The dictionary version, as in the standard GNU scheme: major.minor.revision

### institution (optional)
The name of the institution responsible for the dictionary

### description (optional)
A short description of the dictionary file

### contact (optional)
The email address of the designed POC for this file

### set (mandatory)
Internally consistent physical constants sets are included as YAML [block sequences](http://yaml.org/spec/1.2/spec.html) of mappings. A physical constant set is codified as a YAML mapping node, with the set name as the main key. Each set must begin with a hyphen (-), separated by space from the set name (key).

## Physical Constants Sets

The value associated to a set key includes the following mapping nodes:

### description (mandatory)
A brief description of the constants set

### citation (mandatory)
Literature references associated with the set

### entries
This node includes the actual dictionary entries for each physical constant included in the set. Entries are also organized as block sequences of mapping nodes, and must begin with a hyphen (-).

## Physical Constant Entry Format

A physical constant entry can be defined as shown in the example below:

```yaml
- name: standard_acceleration_of_gravity
  value: 9.80665
  units: m s-2
  prec: double
  type: strict
  uncertainty: exact
  description: |
    Nominal acceleration of an object in a vacuum at sea level at a
    geodetic latitude of 45 degrees.
```

## Entry Field Definitions

The name of each key and its associated value are listed below:

### name
Physical constant's standard name

### value
Physical constant's numerical value

### units
Physical constant's units

### prec
`single` (4 bytes) or `double` (8 bytes) indicate the parameter's kind in Fortran

### uncertainty (optional)
The constant's absolute uncertainty (a number, or `exact`)

### relative_uncertainty (optional)
The constant's relative uncertainty (a number, or `exact`)

### description
A detailed description of the physical constant, with additional references if necessary.
