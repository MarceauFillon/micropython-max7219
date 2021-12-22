class MockPin:
    IN = 0
    OUT = 1
    OPEN_DRAIN = 2
    ALT = 3
    PULL_UP = 0
    AF1_TIM1 = 0
    IRQ_RISING = 0
    IRQ_FALLING = 1

    pins = {}

    def __init__(self, name, debug=False, *args, **kwargs):
        self.name = name
        self._value = 0
        self.debug = debug
        MockPin.pins[name] = self

    def init(self, *args, **kwargs):
        pass

    def __call__(self, value=None):
        if self.debug:
            print(f"{self.name} = {value}")
        return self.value(value) if value is not None else 0

    def off(self):
        pass

    def on(self):
        pass

    def value(self, value=None):
        if value is not None:
            self._value = value
            return None
        return self._value


class MockSPI:
    ''
    LSB = 1
    MSB = 0
    def deinit():
        pass

    def init():
        pass

    def read():
        pass

    def readinto():
        pass

    def write():
        pass

    def write_readinto():
        pass

class FakeMax7219(MockSPI):
    def __init__(self, num, debug=False, on_char=' ', off_char='\u2588'):
        self.num = num
        self.brightness = 0
        self.buffer = bytearray(8 * self.num)
        self.unit_counter = 0
        self.debug = debug
        self.on_char = on_char
        self.off_char = off_char 

    def write(self, buf):
        if len(buf) >= 2:
            if self.debug:
                print(buf)
            if 1 <= buf[0] <= 8:
                if self.debug:
                    print(buf[0], buf[1], (buf[0] - 1) * self.num + self.unit_counter, self.unit_counter)
                self.buffer[(buf[0] - 1) * self.num + self.unit_counter] = buf[1]
                self.unit_counter += 1
                if self.unit_counter >= self.num:
                    self.unit_counter = 0
                    if buf[0] == 8:
                        self.displayLeds()
    
    def _print_unit_row(b):
        print('{:08b}'.format(b).replace('0', self.on_char).replace('1', self.off_char), end='')

    def displayLeds(self):
        for row in range(8):
            for unit in range(self.num):
                FakeMax7219._print_unit_row(self.buffer[row * self.num + unit])
            print()