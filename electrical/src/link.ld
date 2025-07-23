/* #include "link.meta"
/* #meta LINK_DEFINES
    LINK_DEFINES = Table(
        ('name'           , 'type'),
        ('LINK_guard_addr', 'u32' ),
        ('LINK_guard_size', 'u32' ),
        ('LINK_stack_addr', 'u32' ),
        ('LINK_stack_size', 'u32' ),
    )

    for define in LINK_DEFINES:
        Meta.line(f'''
            extern nullptr_t {define.name}[];
            #define          {define.name} (({define.type}) &{define.name})
        ''')
*/

#define CONCAT_(X, Y) X##Y
#define CONCAT(X, Y)  CONCAT_(X, Y)
#define PICK(X)       CONCAT(X, _TARGET)

#if NucleoH7S3L8
    LINK_guard_size = 1024; /* Must be a power of two and at least 32 bytes. @/pg 632/sec B3.5/`ARMv7-M`. */
    LINK_stack_size = 8192;
#endif

ENTRY(HANDLER_Reset) /* Just to indicate where program execution would begin for debugging purposes; doesn't actually affect anything. */

MEMORY
{
    #if NucleoH7S3L8 /* @/pg 151/fig 3/`H7S3rm`. */
        AXI_SRAM (rw) : ORIGIN = 0x24000000, LENGTH = 456K
        DTCM     (rw) : ORIGIN = 0x20000000, LENGTH = 64K /* TODO There's actually 192K worth of memory available to use, but we might have to program the option bytes? */
        FLASH    (rx) : ORIGIN = 0x08000000, LENGTH = 64K
    #endif
}

SECTIONS
{
    /**************************************************************** FLASH ****************************************************************/

    .vector_table_output_section :
    {
        KEEP(*(.vector_table))
    } > FLASH

    .text_output_section : ALIGN(4)
    {
        *(.text*)
    } > FLASH

    .rodata_output_section : ALIGN(4)
    {
        *(.rodata*)
    } > FLASH

    .eh_frame_output_section  : { *(.eh_frame*)  } > FLASH
    .ARM_exidx_output_section : { *(.ARM.exidx*) } > FLASH

    /**************************************************************** RAM ****************************************************************/

    .stack_output_section : ALIGN(32) /* For MPU region alignment. */
    {
        LINK_guard_addr  = .;
        .               += LINK_guard_size;
        .               += LINK_stack_size;
        LINK_stack_addr  = .;

        #define STACK_LOCATION_NucleoH7S3L8 DTCM
    } > PICK(STACK_LOCATION)

    .data_output_section : ALIGN(4)
    {
        LINK_data_load_addr_start = LOADADDR(.data_output_section);
        LINK_data_virt_addr_start = .;
        *(.data)
        .                       = ALIGN(4);
        LINK_data_virt_addr_end = .;

        #define DATA_LOCATION_NucleoH7S3L8 AXI_SRAM
    } > PICK(DATA_LOCATION) AT > FLASH

    .bss_output_section : ALIGN(4)
    {
        LINK_bss_addr_start = .;
        *(.bss)
        .                 = ALIGN(4);
        LINK_bss_addr_end = .;

        #define BSS_LOCATION_NucleoH7S3L8 AXI_SRAM
    } > PICK(BSS_LOCATION)
}
