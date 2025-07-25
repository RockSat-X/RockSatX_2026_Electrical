.syntax unified

//
// Default Handler Indirect, due to limitations of weak symbols.
//

.section .text
.thumb_func
HANDLER_Default_indirect:
    b HANDLER_Default

//
// Reset Interrupt.
//

.section .text
.thumb_func
.global HANDLER_Reset
HANDLER_Reset:

    //
    // Move bytes from LMA to VMA for the data section.
    //

    ldr r0, =LINK_data_load_addr_start
    ldr r1, =LINK_data_virt_addr_start
    ldr r2, =LINK_data_virt_addr_end

    b is_copying_data_done
    copy_data:
        ldr r3, [r0]
        str r3, [r1]
        add r0, 4
        add r1, 4
    is_copying_data_done:
        cmp r1, r2
        bne copy_data

    //
    // Zero-initialize BSS section.
    //

    mov r0, 0
    ldr r1, =LINK_bss_addr_start
    ldr r2, =LINK_bss_addr_end

    b is_zeroing_bss_done
    zero_bss:
        str r0, [r1]
        add r1, 4
    is_zeroing_bss_done:
        cmp r1, r2
        bne zero_bss

    //
    // Enable the floating point coprocessor.
    // Must be done here since GCC can emit vector push/pop instructions on entering main
    // that'd otherwise emit an illegal instruction fault.
    //

    ldr r0, =0xE000ED88                     // CPACR register address. @/pg 597/tbl B3-4/`ARMv7-M`.
    ldr r1, [r0]
    orr r1, r1, (0b11 << 22) | (0b11 << 20) // Full access to coprocessor 10 and 11. @/pg 614/sec B3.2.20/`ARMv7-M`.
    str r1, [r0]

    //
    // Finished initializing, we begin main!
    //

    b main

//
// Vector Table.
//

.section .vector_table, "a"

    .word LINK_stack_addr
    .word HANDLER_Reset

    #include "INTERRUPT_TABLE.meta"
    /* #meta INTERRUPT_TABLE
        INTERRUPT_TABLE = Obj(
            STM32H7S3 = ( # @/pg 860/tbl 142/`H7S3rm`.
                'NMI',
                'HardFault',
                'MemManage',
                'BusFault',
                'UsageFault',
                None,
                None,
                None,
                None,
                'SVCall',
                'DebugMonitor',
                None,
                'PendSV',
                'SysTick',
                'PVD_PVM',
                None,
                'DTS',
                'IWDG',
                'WWDG',
                'RCC',
                None,
                None,
                'FLASH',
                'RAMECC',
                'FPU',
                None,
                None,
                'TAMP',
                None,
                None,
                'EXTI0',
                'EXTI1',
                'EXTI2',
                'EXTI3',
                'EXTI4',
                'EXTI5',
                'EXTI6',
                'EXTI7',
                'EXTI8',
                'EXTI9',
                'EXTI10',
                'EXTI11',
                'EXTI12',
                'EXTI13',
                'EXTI14',
                'EXTI15',
                'RTC',
                'SAES',
                'CRYP',
                'PKA',
                'HASH',
                'RNG',
                'ADC1_2',
                'GPDMA1_Channel0',
                'GPDMA1_Channel1',
                'GPDMA1_Channel2',
                'GPDMA1_Channel3',
                'GPDMA1_Channel4',
                'GPDMA1_Channel5',
                'GPDMA1_Channel6',
                'GPDMA1_Channel7',
                'TIM1_BRK',
                'TIM1_UP',
                'TIM1_TRG_COM',
                'TIM1_CC',
                'TIM2',
                'TIM3',
                'TIM4',
                'TIM5',
                'TIM6',
                'TIM7',
                'TIM9',
                'SPI1',
                'SPI2',
                'SPI3',
                'SPI4',
                'SPI5',
                'SPI6',
                'HPDMA1_Channel0',
                'HPDMA1_Channel1',
                'HPDMA1_Channel2',
                'HPDMA1_Channel3',
                'HPDMA1_Channel4',
                'HPDMA1_Channel5',
                'HPDMA1_Channel6',
                'HPDMA1_Channel7',
                'SAI1_A',
                'SAI1_B',
                'SAI2_A',
                'SAI2_B',
                'I2C1_EV',
                'I2C1_ER',
                'I2C2_EV',
                'I2C2_ER',
                'I2C3_EV',
                'I2C3_ER',
                'USART1',
                'USART2',
                'USART3',
                'UART4',
                'UART5',
                'UART7',
                'UART8',
                'I3C1_EV',
                'I3C1_ER',
                'OTG_HS',
                'ETH',
                'CORDIC',
                'GFXTIM',
                'DCMIPP',
                None,
                None,
                'DMA2D',
                'JPEG',
                'GFXMMU',
                'I3C1_WKUP',
                'MCE1',
                'MCE2',
                'MCE3',
                'XSPI1',
                'XSPI2',
                'FMC',
                'SDMMC1',
                'SDMMC2',
                None,
                None,
                'OTG_FS',
                'TIM12',
                'TIM13',
                'TIM14',
                'TIM15',
                'TIM16',
                'TIM17',
                'LPTIM1',
                'LPTIM2',
                'LPTIM3',
                'LPTIM4',
                'LPTIM5',
                'SPDIF_RX',
                'MDIOS',
                'ADF1_FLT0',
                'CRS',
                'UCPD1',
                'CEC',
                'PSSI',
                'LPUART1',
                'WAKEUP_PIN',
                'GPDMA1_Channel8',
                'GPDMA1_Channel9',
                'GPDMA1_Channel10',
                'GPDMA1_Channel11',
                'GPDMA1_Channel12',
                'GPDMA1_Channel13',
                'GPDMA1_Channel14',
                'GPDMA1_Channel15',
                'HPDMA1_Channel8',
                'HPDMA1_Channel9',
                'HPDMA1_Channel10',
                'HPDMA1_Channel11',
                'HPDMA1_Channel12',
                'HPDMA1_Channel13',
                'HPDMA1_Channel14',
                'HPDMA1_Channel15',
                None,
                None,
                None,
                'FDCAN1_IT0',
                'FDCAN1_IT1',
                'FDCAN2_IT0',
                'FDCAN2_IT1',
            ),
        )

        @Meta.ifs(INTERRUPT_TABLE, style='#if')
        def _(__):

            target_mcu, entries = __

            yield f'TARGET_MCU_IS_{target_mcu}'

            for entryi, entry in enumerate(entries):

                Meta.line(f'''

                    // [{entryi - 14}] {'Reserved' if entry is None else entry}.

                ''')

                if entry is None:

                    # No interrupt handler here.
                    Meta.line('.word 0')

                else:

                    Meta.line([ # TODO Meta.line needs to be able to handle multiple args.
                        f'.word HANDLER_{entry}'                           , # Insert the address of the handler routine.
                        f'.weak HANDLER_{entry}'                           , # If there exists an implementation of the handler, use it.
                        f'.set  HANDLER_{entry}, HANDLER_Default_indirect' , # Otherwise, use the default handler.
                    ])
    */
