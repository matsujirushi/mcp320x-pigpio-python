#!/usr/bin/env python3

import pigpio


class Mcp3208:

    def __init__(self, pi: pigpio.pi, spi_handle: int):
        self.__pigpio = pi
        self.__h = spi_handle

    def read(self, channel: int, single_ended: bool = True) -> int:
        configuration_bits = (0b1000 if single_ended else 0b0000) | channel

        write_data = bytearray(3)
        write_data[0] = 0b0000_0100 | configuration_bits >> 2
        write_data[1] = configuration_bits << 6 & 0b1100_0000

        _, read_data = self.__pigpio.spi_xfer(self.__h, write_data)

        return (read_data[1] & 0b0000_1111) << 8 | read_data[2]


if __name__ == "__main__":
    import time

    pi = pigpio.pi()
    adc = Mcp3208(pi, pi.spi_open(0, 1000000, 0))

    while True:
        for channel in range(8):
            print(f"{adc.read(channel)}\t", end="")
        print()

        time.sleep(1)
