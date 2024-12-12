#!/usr/bin/env python3

import sys, pathlib, argparse
import yaml

this_script_dir = pathlib.Path(__file__).parent

###############################################################################
def parse_command_line(args, description):
###############################################################################
    parser = argparse.ArgumentParser(
        usage="""\n{0} <ARGS> [--verbose]
OR
{0} --help

\033[1mEXAMPLES:\033[0m
    \033[1;32m# Generate the Fortran90 module 'constants.F90' with all constants.\033[0m
    > {0} --lang f90 -o constants.F90
    \033[1;32m# Generate the C++ header 'constants.h' with only 'mathematics' and 'geophysics' constants\033[0m
    > {0} --lang cxx --groups mathematics geophysics -o constants.h
""".format(pathlib.Path(args[0]).name),
        description=description
    )

    langs = ['cxx','f90']
    parser.add_argument('-l','--lang',help=f'Language for which to enerate. Valid options={langs}',
                        type=str, choices=langs, required=True)
    parser.add_argument('-g' ,'--groups', help='Groups to include in the generated file (optional). If not provided, include all groups', nargs='+')
    parser.add_argument('-f' ,'--filename', help='Name of the generated output file', type=str, required=True)

    return parser.parse_args(args[1:])

###############################################################################
def generate_file(lang,groups,filename):
###############################################################################

    constants_file = this_script_dir.parent / 'pcd.yaml'
    with open(constants_file, 'r') as fd:
        constants_dict = yaml.safe_load(fd)['physical_constants_dictionary']

    groups_in_file = {}
    for g in constants_dict['set']:
        if len(g.keys())>1:
            raise ValueError('Invalid formatting of pcd database. Each entry of the "set" sequence should contain ONE dictionary')
        for k,v in g.items():
            groups_in_file[k] = v
    valid_groups = list(groups_in_file.keys())
    if groups is not None and any(item not in valid_groups for item in groups):
        raise ValueError(f"Invalid value for groups: {','.join(groups)}. Valid choices are {','.join(valid_groups)}")

    with open(filename,'w') as ofile:
        # Header
        if lang=='cxx':
            ofile.write('#ifndef E3SM_CONSTANTS_HPP\n')
            ofile.write('#define E3SM_CONSTANTS_HPP\n\n')
            ofile.write('namespace e3sm {\n')
        elif lang=='f90':
            ofile.write('module e3sm_constants\n')
            ofile.write('    implicit none\n\n')
            ofile.write('    !define double precision kind\n')
            ofile.write('    integer, parameter :: dp = selected_real_kind(15, 307)  ! Double precision\n')
        else:
            raise RuntimeError(f'Missing implementation of file header for language {lang}')

        # Content, by group
        for gname,group in groups_in_file.items():
            if groups is None or gname in groups:
                if lang=='cxx':
                    ofile.write(f'\n// {gname} constants\n')
                elif lang=='f90':
                    ofile.write(f'\n    !{gname} constants\n')
                else:
                    raise RuntimeError(f'Missing implementation of section name for language {lang}')

                for c in group['entries']:
                    n = c['symbol']
                    v = c['value']
                    if lang=='cxx':
                        ofile.write (f'constexpr double {n} = {v};\n')
                    elif lang=='f90':
                        ofile.write (f'    real(dp), parameter :: {n} = {v}_dp\n')
                    else:
                        raise RuntimeError(f'Missing implementation of constant entry for language {lang}')

        # Footer
        if lang=='cxx':
            ofile.write('\n} // namespace e3sm \n')
            ofile.write('#endif // E3SM_CONSTANTS_HPP')
        elif lang=='f90':
            ofile.write('\nend module e3sm_constants')
        else:
            raise RuntimeError(f'Missing implementation of file footer for language {lang}')


###############################################################################
def _main_func(description):
###############################################################################
    generate_file(**vars(parse_command_line(sys.argv, description)))
    sys.exit(0)

###############################################################################

if (__name__ == "__main__"):
    _main_func(__doc__)
