/*
 * Copyright (c) 2015-2019, Texas Instruments Incorporated
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 *
 * *  Redistributions of source code must retain the above copyright
 *    notice, this list of conditions and the following disclaimer.
 *
 * *  Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in the
 *    documentation and/or other materials provided with the distribution.
 *
 * *  Neither the name of Texas Instruments Incorporated nor the names of
 *    its contributors may be used to endorse or promote products derived
 *    from this software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
 * THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
 * PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
 * CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
 * EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
 * PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
 * OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
 * WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
 * OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
 * EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */

/*
 *  ======== uartecho.c ========
 */
#include <stdint.h>
#include <stddef.h>
#include <math.h>

/* Driver Header files */
#include <ti/drivers/GPIO.h>
#include <ti/drivers/UART.h>

/* Driver configuration */
#include "ti_drivers_config.h"

/*
 *  ======== mainThread ========
 */
void *mainThread(void *arg0)
{
    char        input;
    char        buffer[40] = {0};
    const char  resetMsg[] = "Custom SAS simulator:\r\n";
    const char  detectMsg[] = "Detected!\r\n";
    const char  echoPrompt[] = "Echoing characters:\r\n";
    UART_Handle uart;
    UART_Params uartParams;

    /* Call driver init functions */
    GPIO_init();
    UART_init();

    /* Configure the LED pin */
    GPIO_setConfig(CONFIG_GPIO_LED_0, GPIO_CFG_OUT_STD | GPIO_CFG_OUT_LOW);

    /* Turn on user LED */
    GPIO_write(CONFIG_GPIO_LED_0, CONFIG_GPIO_LED_ON);

    /* Create a UART with data processing off. */
    UART_Params_init(&uartParams);
    uartParams.writeDataMode = UART_DATA_BINARY;
    uartParams.readDataMode = UART_DATA_BINARY;
    uartParams.readReturnMode = UART_RETURN_FULL;
    uartParams.readEcho = UART_ECHO_OFF;
    uartParams.baudRate = 115200;

    uart = UART_open(CONFIG_UART_0, &uartParams);

    if (uart == NULL) {
        /* UART_open() failed */
        while (1);
    }

    UART_write(uart, resetMsg, sizeof(resetMsg));
    uint16_t voc = 0;
    uint16_t vmp = 0;
    uint16_t imp = 0;
    uint16_t isc = 0;
    uint32_t n = 0;
    uint16_t index = 0;
    float Voc;
    float Vmp;
    float Imp;
    float Isc;
    float N;
    float Rs = 0;
    float log2  = 0.69314718;
    float table[1024] = {0};
    uint16_t j = 0;
    float vout = 0;
    uint8_t SOO = 0xFE;
    uint8_t EOO = 0xFD;
    float i;
    float x;
    float series;
    float v;
    /* Loop forever echoing */
    while (1) {
        UART_read(uart, &input, sizeof(input));
        if (input == 0xFD)
        {
            UART_read(uart, &voc, sizeof(voc));
            UART_read(uart, &vmp, sizeof(vmp));
            UART_read(uart, &imp, sizeof(imp));
            UART_read(uart, &isc, sizeof(isc));
            UART_read(uart, &n, sizeof(n));
            UART_read(uart, &input, sizeof(input));
            if (input == 0xFE)
            {
                UART_write(uart, &voc, sizeof(voc));
                UART_write(uart, &vmp, sizeof(vmp));
                UART_write(uart, &imp, sizeof(imp));
                UART_write(uart, &isc, sizeof(isc));
                UART_write(uart, &n, sizeof(n));
                Voc = (float) voc / 10.0;
                Vmp = (float) vmp / 10.0;
                Imp = (float) imp / 10.0;
                Isc = (float) isc / 10.0;
                N = ((float) n) / 1000.0;
                Rs  = (Voc - Vmp) / Imp;
                for (j = 0; j < 1024; j++)
                {
                    i = ((float)j * Isc) / 1023.0;
                    x = pow((i/Isc),N);
                    series = log2;
                    series -= (x / 2);
                    series -= (pow(x,2)/8);
                    series -= (pow(x,3)/24);
                    series -= (pow(x,4)/64);
                    v = (Voc * series) / log2;
                    v -= Rs * ( i - Isc );
                    v /= (1 + ( ( Rs * Isc ) / Voc ) );
                    table[j]  = v;
                }
            }
            UART_write(uart, &EOO, sizeof(EOO));
        }
        if (input == 0xFB)
        {
//            UART_read(uart, &index, sizeof(index));
//            UART_write(uart, &index, sizeof(index));
//            vout = table[index];
            UART_read(uart, &input, sizeof(input));
            if (input == 0xFC)
            {
                UART_write(uart, &SOO, sizeof(SOO));
                for (j = 0; j < 1024; j++)
                {
                    vout = table[j];
                    UART_write(uart, &vout, sizeof(vout));
                }
                //UART_write(uart, &vout, sizeof(vout));
                //UART_write(uart, &EOO, sizeof(EOO));
            }
            UART_write(uart, &EOO, sizeof(EOO));
        }

    }
}
