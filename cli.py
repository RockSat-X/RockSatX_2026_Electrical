#! /usr/bin/env python3

import re, os, sys, types, shlex, shutil, pathlib, subprocess, collections, inspect, io, builtins, itertools, math, time, string, zlib

def execute(
    dflt                  = None, *,
    bash                  = None,
    cmd                   = None,
    pwsh                  = None,
    keyboard_interrupt_ok = False,
    nonzero_exit_code_ok  = False
):

    if cmd is not None and pwsh is not None:
        raise RuntimeError(
            f'CMD and PowerShell commands cannot be both provided; '
            f'please raise an issue or patch the script yourself.'
        )

    match sys.platform:

        case 'win32':
            if pwsh is None:
                insts    = cmd
                use_pwsh = False
            else:
                insts    = pwsh
                use_pwsh = True

        case _:
            insts    = bash
            use_pwsh = False

    if insts is None:
        insts = dflt

    if insts is None:
        raise RuntimeError(
            f'Missing shell instructions for platform "{sys.platform}"; '
            f'please raise an issue or patch the script yourself.'
        )

    if use_pwsh:
        require('pwsh')

    if isinstance(insts, str):
        insts = [insts]

    for inst in insts:

        inst = inst.strip()

        if not inst:
            continue

        lex                  = shlex.shlex(inst)
        lex.quotes           = '"'
        lex.whitespace_split = True
        lex.commenters       = ''
        lex_parts            = list(lex)
        inst                 = ' '.join(lex_parts)

        print(f'$ {lex_parts[0]}'    , end = '')
        print(' '                    , end = '')
        print(' '.join(lex_parts[1:]),         )

        if use_pwsh:
            # Invoke PowerShell; note that it's slow to do just this,
            # so we'd use CMD when we don't need PowerShell features.
            inst = ['pwsh', '-Command', inst]

        try:
            exit_code = subprocess.call(inst, shell = True)
        except KeyboardInterrupt as err:
            exit_code = None
            if not keyboard_interrupt_ok:
                raise err

        if exit_code and not nonzero_exit_code_ok:
            print()
            print(f'[ERROR] Shell command exited with a non-zero code of {exit_code}.')
            sys.exit(exit_code)

        return exit_code

execute( # @/`Useless "ap" flag`.
    f'''
        STM32_Programmer_CLI
            --connect port=SWD
            --download ./electrical/nucleo_h7s3l8_cubemx_test/Makefile/Boot/build/nucleo_h7s3l8_cubemx_test_Boot.bin 0x08000000
            --verify
            --start
    ''',
    nonzero_exit_code_ok = True
)
