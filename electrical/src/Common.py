#meta root, find_dupe, round_up, repr_in_c, mk_dict, inverse_of, ljusts, Obj, Record, Table, OrdSet, log, ErrorLift :

import enum
from deps.pxd.utils            import root, find_dupe, round_up, repr_in_c, mk_dict, inverse_of, ljusts, Obj, Record, Table, OrdSet
from deps.pxd.log              import log
from deps.pxd.metapreprocessor import ErrorLift

################################################################################################################################
#
# CMSIS Functions.
#

class CMSIS_MODIFY:

    def __init__(self, macro):
        self.macro = macro

    def __call__(self, *args):

        # e.g. CMSIS_SET((a, b, c, d)) -> CMSIS_SET(a, b, c, d)
        if len(args) == 1:
            args, = args

        # e.g. CMSIS_SET(x for x in xs)
        args = tuple(args)

        # e.g. CMSIS_SET(())
        if len(args) == 0:
            return

        # e.g.
        # CMSIS_SET(  ->  CMSIS_SET(
        #     a, b,           (a, b, c, d),
        #     c, d,           (a, b, e, f),
        #     e, f,           (a, b, g, h),
        #     g, h,       )
        # )
        if not isinstance(args[0], tuple):
            args = tuple(
                (args[0], args[1], args[i], args[i + 1])
                for i in range(2, len(args), 2)
            )

        # e.g.
        # CMSIS_SET(         ->   CMSIS_SET(         &  CMSIS_SET(
        #     (a, b, c, d),           (a, b, c, d),         (x, y, z, w),
        #     (x, y, z, w),           (a, b, g, h),     )
        #     (a, b, g, h),       )
        # )
        args = inverse_of(
            ((section, register), (field, repr_in_c(value)))
            for section, register, field, value in args
        )

        for (section, register), field_values in args.items():

            if (field := find_dupe(field for field, value in field_values)) is not None:
                raise ValueError(ErrorLift(f'Modifying field "{field}" more than once.'))

            match field_values:

                # e.g. CMSIS_SET(a, b, c, d)
                case [(field, value)]:
                    Meta.line(f'''
                        {self.macro}({section}, {register}, {field}, {value});
                    ''')

                # e.g.
                # CMSIS_SET(
                #     a, b,
                #     c, d,
                #     e, f,
                #     g, h,
                # )
                case _:
                    with Meta.enter(self.macro, '(', ');'):
                        for columns in ljusts(((section, register), *field_values)):
                            Meta.line(f'{', '.join(columns)},')

    def __enter__(self):
        self.args = []
        return self.args

    def __exit__(self, *dont_care_about_exceptions):
        try:
            self(self.args)
        except Exception as err:
            # TODO This is an ugly way just so that the dumped stacktrace
            #      will be at the most useful place.
            if err.args and isinstance(err.args[0], ErrorLift):
                lifted_err = type(err).__new__(type(err))
                type(err).__init__(lifted_err, *err.args)
                raise lifted_err from err
            else:
                raise err from err

CMSIS_SET   = CMSIS_MODIFY('CMSIS_SET'  )
CMSIS_WRITE = CMSIS_MODIFY('CMSIS_WRITE')

def CMSIS_SPINLOCK(*args):

    match args:

        case spinlocks if all(isinstance(spinlock, tuple) for spinlock in spinlocks):
            pass

        case (sect, reg, field, value):
            spinlocks = [(sect, reg, field, value)]

        case ((sect, reg, field, value),):
            spinlocks = [(sect, reg, field, value)]

        case unknown:
            assert False, unknown

    for sect, reg, field, value in spinlocks:
        match value:
            case True  : Meta.line(f'while (!CMSIS_GET({sect}, {reg}, {field}));')
            case False : Meta.line(f'while (CMSIS_GET({sect}, {reg}, {field}));')
            case _     : Meta.line(f'while (CMSIS_GET({sect}, {reg}, {field}) != {value});')



################################################################################################################################
#
# Targets.
#

BUILD = root('./electrical/build')

TARGET  = lambda target_name: next(target for target in TARGETS if target.name == target_name)
TARGETS = (
    Record(
        name = 'SandboxNucleoH7S3L8',
        mcu  = 'STM32H7S3',
        srcs = root('''
            ./electrical/src/SandboxNucleoH7S3L8.c
            ./electrical/src/Prelude.S
        '''),
    ),
)

for target in TARGETS:

    arch_flags = ('''
        -mcpu=cortex-m7
        -mfloat-abi=hard
    ''')

    target.compiler_flags = (
        # Miscellaneous flags.
        f'''
            {arch_flags}
            -O0
            -ggdb3
            -std=gnu23
            -fmax-errors=1
            -fno-strict-aliasing
            -fno-eliminate-unused-debug-types
        '''

        # Defines.
        f'''
            -D _TARGET=_{target.name}
            {'\n'.join(
                f'-D {other_target.name}={int(other_target.name == target.name)}'
                for other_target in TARGETS
            )}
            {'\n'.join(
                f'-D {other_target.mcu}={int(other_target.mcu == target.mcu)}'
                for other_target in TARGETS
            )}
        '''

        # Warning configuration.
        f'''
            -Werror
            -Wall
            -Wextra
            -Wswitch-enum
            -Wundef
            -Wfatal-errors
            -Wstrict-prototypes
            -Wshadow
            -Wswitch-default

            -Wno-unused-function
            -Wno-main
            -Wno-double-promotion
            -Wno-conversion
            -Wno-unused-variable
            -Wno-unused-parameter
            -Wno-comment
            -Wno-unused-but-set-variable
            -Wno-format-zero-length
            -Wno-unused-label
        '''

        # Search path.
        f'''{'\n'.join(f'-I "{root(path)}"' for path in '''
            ./electrical/build/meta
            ./deps/CMSIS_6/CMSIS/Core/Include
            ./deps/cmsis_device_h7s3l8/Include
        '''.split())}'''
    )

    target.linker_flags = f'''
        {arch_flags}
        -nostdlib
        -lgcc
        -lc
    '''

TARGETS = tuple(Obj(target) for target in TARGETS)
