#! /usr/bin/env python3

################################################################ Dependencies ################################################################



import sys, shlex, pathlib, shutil, subprocess, time

try:
    import deps.pxd.ui
    import deps.pxd.metapreprocessor
    import deps.pxd.cite
    from deps.pxd.log   import log
    from deps.pxd.utils import *
except ModuleNotFoundError as error:
    print(f'[ERROR] Could not import "{error.name}"; maybe the Git submodules need to be initialized/updated? Try doing:')
    print(f'        > git submodule update --init --recursive')
    print(f'        If this still doesn\'t work, please raise an issue or patch the script yourself.')
    sys.exit(1)



def require(*needed_programs):

    missing_program = next((program for program in needed_programs if shutil.which(program) is None), None)

    if not missing_program:
        return # The required programs were found on the machine.

    # PowerShell.
    if missing_program in (roster := [
        'pwsh',
    ]):
        with log(ansi = 'fg_red'):
            log(f'[ERROR] Python couldn\'t find "pwsh" in your PATH; have you installed PowerShell yet?')
            log(f'        > https://apps.microsoft.com/detail/9MZ1SNWT0N5D', ansi = 'bold')
            log(f'        Installing PowerShell via Windows Store is the most convenient way.')

    # STM32CubeCLT.
    elif missing_program in (roster := [
        'STM32_Programmer_CLI',
        'ST-LINK_gdbserver'
    ]):
        with log(ansi = 'fg_red'):
            log(f'[ERROR] Python couldn\'t find "{missing_program}" in your PATH; have you installed STM32CubeCLT yet?')
            log(f'        > https://www.st.com/en/development-tools/stm32cubeclt.html', ansi = 'bold')
            log(f'        Install and then make sure all of these commands are available in your PATH:')
            for program in roster:
                if shutil.which(program) is not None:
                    log(f'            - [located] {program}', ansi = 'fg_green')
                else:
                    log(f'            - [missing_program] {program}')

    # Arm GNU Toolchain.
    elif missing_program in (roster := [
        'arm-none-eabi-gcc',
        'arm-none-eabi-cpp',
        'arm-none-eabi-objcopy',
        'arm-none-eabi-gdb',
    ]):
        with log(ansi = 'fg_red'):
            log(f'[ERROR] Python couldn\'t find "{missing_program}" in your PATH; have you installed the Arm GNU toolchain (version 14.2.Rel1, December 10, 2024) yet?')
            log(f'        > website : https://developer.arm.com/downloads/-/arm-gnu-toolchain-downloads', ansi = 'fg_bright_red')
            for platform, url in (
                ('win32', 'https://armkeil.blob.core.windows.net/developer/Files/downloads/gnu/14.2.rel1/binrel/arm-gnu-toolchain-14.2.rel1-mingw-w64-x86_64-arm-none-eabi.exe'),
                ('linux', 'https://armkeil.blob.core.windows.net/developer/Files/downloads/gnu/14.2.rel1/binrel/arm-gnu-toolchain-14.2.rel1-x86_64-arm-none-eabi.tar.xz'       ),
            ):
                log(f'        > {platform.ljust(len('website'))} : {url}', ansi = ('bold', 'fg_bright_red') if sys.platform == platform else 'fg_bright_red')
            log(f'        Install/unzip and then make sure all of these commands are available in your PATH:')
            for program in roster:
                if shutil.which(program) is not None:
                    log(f'            - [located] {program}', ansi = 'fg_green')
                else:
                    log(f'            - [missing_program] {program}')

    # Picocom.
    elif missing_program in (roster := [
        'picocom'
    ]):
        with log(ansi = 'fg_red'):
            log(f'[ERROR] Python couldn\'t find "{missing_program}" in your PATH; have you installed it yet?')
            log(f'        If you\'re on a Debian-based distro, this is just simply:')
            log(f'        > sudo apt install picocom', ansi = 'bold')
            log(f'        Otherwise, you should only be getting this message on some other Linux distribution, ')
            log(f'        to which I have faith in you to figure this out on your own.')

    # Not implemented.
    else:
        raise RuntimeError(
            f'Unknown required program "{missing_program}"; '
            f'please raise an issue or patch the script yourself.'
        )

    sys.exit(1)



################################################################ Helpers ################################################################



def execute(
    default               = None, *,
    bash                  = None,
    cmd                   = None,
    powershell            = None,
    keyboard_interrupt_ok = False,
    nonzero_exit_code_ok  = False
):

    #
    # Determine the shell instructions we'll be executing based on the operating system.
    #

    if cmd is not None and powershell is not None:
        raise RuntimeError(
            f'CMD and PowerShell commands cannot be both provided; '
            f'please raise an issue or patch the script yourself.'
        )

    match sys.platform:

        case 'win32':
            use_powershell = cmd is None
            instructions   = pwsh if use_powershell else cmd

        case _:
            instructions   = bash
            use_powershell = False

    if instructions is None:
        instructions = default # Because sometimes the shell instructions are universal (e.g. "echo hello!").

    if instructions is None:
        raise RuntimeError(
            f'Missing shell instructions for platform "{sys.platform}"; '
            f'please raise an issue or patch the script yourself.'
        )

    if use_powershell:
        require('pwsh')

    if isinstance(instructions, str):
        instructions = [instructions]

    #
    # Carry out every shell instruction.
    #

    for instruction in instructions:

        instruction = instruction.strip()

        if not instruction:
            continue

        lexer                  = shlex.shlex(instruction)
        lexer.quotes           = '"'
        lexer.whitespace_split = True
        lexer.commenters       = ''
        lexer_parts            = list(lexer)
        instruction            = ' '.join(lexer_parts)

        log(f'$ {lexer_parts[0]}'    , end = '', ansi = 'fg_bright_green')
        log(' '                      , end = ''                          )
        log(' '.join(lexer_parts[1:]),                                   )

        if use_powershell: # Note that it's slow to invoke PowerShell, so we'd use cmd.exe when we don't need PowerShell features.
            instruction = ['pwsh', '-Command', instruction]

        try:
            exit_code = subprocess.call(instruction, shell = True)
        except KeyboardInterrupt:
            if keyboard_interrupt_ok:
                exit_code = None
            else:
                raise

        if exit_code and not nonzero_exit_code_ok:
            log()
            log(f'[ERROR] Shell command exited with a non-zero code of {exit_code}.', ansi = 'fg_red')
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
    f'The command line program (pronounced "clippy").',
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
