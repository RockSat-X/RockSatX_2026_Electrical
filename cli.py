#! /usr/bin/env python3

################################################################ Dependencies ################################################################



import types, sys, shlex, pathlib, shutil, subprocess, time

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



def import_pyserial():

    try:
        import serial
        import serial.tools.list_ports
    except ModuleNotFoundError as error:
        with log(ansi = 'fg_red'):
            log(f'[ERROR] Python got {type(error).__name__} ({error}); try doing:')
            log(f'        > pip install pyserial', ansi = 'bold')
        sys.exit(1)

    return serial, serial.tools.list_ports



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

    # Make.
    elif missing_program in (roster := [
        'make'
    ]):
        with log(ansi = 'fg_red'):
            log(f'[ERROR] Python couldn\'t find "{missing_program}" in your PATH; have you installed it yet?')
            log(f'        If you\'re on a Windows system, run the following command and restart your shell:')
            log(f'        > winget install ezwinports.make', ansi = 'bold')

    # Not implemented.
    else:
        raise RuntimeError(
            f'Unknown required program "{missing_program}"; '
            f'please raise an issue or patch the script yourself.'
        )

    sys.exit(1)



################################################################ Helpers ################################################################



def log_stlinks(stlinks):

    header, rows = ljusts(({
        'Probe Index'   : stlink.probe_index,
        'Board Name'    : stlink.board_name,
        'Device'        : stlink.comport.device,
        'Description'   : stlink.comport.description,
        'Serial Number' : stlink.serial_number,
    } for stlink in stlinks), include_keys = True)

    log(f'| {' | '.join(header)} |')
    for row in rows:
        log(f'| {' | '.join(row.values())} |')



def request_stlinks(
    *,
    specific_one              = False,
    specific_probe_index      = None,
    flag_to_use_when_multiple = None,
):

    #
    # Parse output of STM32_Programmer_CLI's findings.
    #

    require('STM32_Programmer_CLI')

    listing_lines = subprocess.check_output(['STM32_Programmer_CLI', '-l', 'st-link']).decode('utf-8').splitlines()
    stlinks       = [
        types.SimpleNamespace(
            probe_index        = int(listing_lines[i + 0].removeprefix(prefix).removesuffix(':')),
            serial_number      =     listing_lines[i + 1].split(':')[1].strip(),
            firmware           =     listing_lines[i + 2].split(':')[1].strip(),
            access_port_number = int(listing_lines[i + 3].split(':')[1].strip()),
            board_name         =     listing_lines[i + 4].split(':')[1].strip(),
        )
        for i in range(len(listing_lines))
        if listing_lines[i].startswith(prefix := 'ST-Link Probe ')
    ]

    #
    # Find each ST-Link's corresponding serial port.
    #

    serial, list_ports = import_pyserial()

    comports = list_ports.comports()

    for stlink in stlinks:
        stlink.comport, = [comport for comport in comports if comport.serial_number == stlink.serial_number]

    #
    # If a specific probe index was given, give back that specific ST-Link.
    #

    if specific_probe_index is not None:

        if not stlinks:
            log(f'[ERROR] No ST-Links found.', ansi = 'fg_red')
            sys.exit(1)

        if not (matches := [stlink for stlink in stlinks if stlink.probe_index == specific_probe_index]):
            log_stlinks(stlinks)
            log()
            log(f'[ERROR] No ST-Links found with probe index of "{specific_probe_index}".', ansi = 'fg_red')
            sys.exit(1)

        stlink, = matches

        return stlink

    #
    # If the caller is assuming there's only one ST-Link, then give back the only one.
    #

    if specific_one:

        if not stlinks:
            log(f'[ERROR] No ST-Links found.', ansi = 'fg_red')
            sys.exit(1)

        if len(stlinks) >= 2:
            log_stlinks(stlinks)
            log()
            if flag_to_use_when_multiple is None:
                log(f'[ERROR] Multiple ST-Links found; I don\'t know which one to use.', ansi = 'fg_red')
            else:
                log(f'[ERROR] Multiple ST-Links found; specify which one to use with "{flag_to_use_when_multiple}".', ansi = 'fg_red')
            sys.exit(1)

        stlink, = stlinks

        return stlink

    #
    # Otherwise, give back the list of the ST-Links we found (if any).
    #

    return stlinks



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



@ui(f'Delete all build artifacts.')
def clean():

    # @/on 2025-july-21/by:`Phuc Doan`.
    # We could also call "make clean" to do some of the cleaning,
    # but I've encountered a bug in ST's Makefile where it doesn't actually do it properly. :/

    directories = root('''
        ./electrical/nucleo_h7s3l8_cubemx_test/Makefile/Boot/build
    ''')

    for directory in directories:
        execute(
            bash = f'''
                rm -rf {directory}
            ''',
            cmd = f'''
                if exist {directory} rmdir /S /Q {directory}
            ''',
        )



@ui('Compile and generate the binary for flashing.')
def build():

    require('make')

    require(
        'arm-none-eabi-gcc',
        'arm-none-eabi-cpp',
        'arm-none-eabi-objcopy',
    )

    execute(f'''
        make -C {root('./electrical/nucleo_h7s3l8_cubemx_test/Makefile')}
    ''')



@ui('Flash the binary to the MCU.')
def flash():

    require('STM32_Programmer_CLI')

    stlink = request_stlinks(specific_one = True)

    attempts = 0

    while True:

        # Maxed out attempts?
        if attempts == 3:
            log()
            log('[ERROR] Failed to flash (maybe due to ST-Link not being connected or that it\'s busy).', ansi = 'fg_red')
            sys.exit(1)

        # Not the first try?
        elif attempts:
            log()
            log('[WARNING] Failed to flash (maybe due to verification error); trying again...', ansi = 'fg_yellow')
            log()

        # Try flashing.
        exit_code = execute(f'''
            STM32_Programmer_CLI
                --connect port=SWD index={stlink.probe_index}
                --download {root('./electrical/nucleo_h7s3l8_cubemx_test/Makefile/Boot/build/nucleo_h7s3l8_cubemx_test_Boot.bin')} 0x08000000
                --verify
                --start
        ''', nonzero_exit_code_ok = True)

        # Try again if needed.
        if exit_code:
            attempts += 1
        else:
            break



@ui('Set up a debugging session.')
def debug(
    just_gdbserver : (bool, 'Just set up the GDB-server and nothing else.') = False
):

    require(
        'ST-LINK_gdbserver',
        'STM32_Programmer_CLI',
    )

    if just_gdbserver: # This is mainly used for Visual Studio Code debugging.
        execute(f'''
            ST-LINK_gdbserver
                --stm32cubeprogrammer-path {pathlib.Path(shutil.which('STM32_Programmer_CLI')).parent}
                --swd
                --apid 1
                --verify
                --attach
        ''', keyboard_interrupt_ok = True)



@ui('Search and list for any ST-Links connected to the computer.', name = 'stlinks')
def _():
    if stlinks := request_stlinks():
        log_stlinks(stlinks)
    else:
        log('No ST-Link detected by STM32_Programmer_CLI.')



exit(ui.invoke(sys.argv[1:]))
