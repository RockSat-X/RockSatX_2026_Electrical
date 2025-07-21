#! /usr/bin/env python3

################################################################ Dependencies ################################################################



import sys, shlex, pathlib, shutil, subprocess, time

try:
    import deps.pxd.ui
    import deps.pxd.metapreprocessor
    import deps.pxd.cite
    from deps.pxd.log   import log
    from deps.pxd.utils import *
except ModuleNotFoundError as err:
    print(f'[ERROR] Could not import "{err.name}"; maybe the Git submodules need to be initialized/updated? Try doing:')
    print(f'        > git submodule update --init --recursive')
    print(f'        If this still doesn\'t work, please raise an issue or patch the script yourself.')
    sys.exit(1)



################################################################ Helpers ################################################################



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



################################################################ CLI Commands ################################################################



def ui_hook(subcmd_name):

    start = time.time()
    yield
    end = time.time()

    if (elapsed := end - start) >= 0.5:
        log()
        log(f'> "{subcmd_name}" took: {elapsed :.3f}s')



ui = deps.pxd.ui.UI(
    f'{root(pathlib.Path(__file__).name)}',
    f'Clippy the command line program.',
    ui_hook,
)



@ui('Set up a debugging session.')
def debug(
    just_gdbserver : (bool, 'Just set up the GDB-server and nothing else.') = False
):

    if just_gdbserver: # This is mainly used for Visual Studio Code debugging.
        execute(f'''
            ST-LINK_gdbserver
                --stm32cubeprogrammer-path {pathlib.Path(shutil.which('STM32_Programmer_CLI')).parent}
                --swd
                --apid 1
                --verify
                --attach
        ''', keyboard_interrupt_ok = True)



exit(ui.invoke(sys.argv[1:]))
