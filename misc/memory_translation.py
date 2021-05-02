# R3000 Virtual Memory To Physical Memory Translation


from typing import Dict, Union
from enum import Enum


PAGE_FRAME    = 0b11111111111111111111000000000000
OFFSET        = 0b00000000000000000000111111111111
ASID          = 0b00000000000000000000111111000000

CACHE_CONTROL = 0b00000000000000000000100000000000
WRITE_CONTROL = 0b00000000000000000000010000000000
VALID         = 0b00000000000000000000001000000000
GLOBAL        = 0b00000000000000000000000100000000


class Address: pass
class Error: pass


class R3000:
    def __init__(self, tlb: Dict[int, int], entry_high: int) -> None:
        self._tlb = tlb
        self._entry_high = entry_high

    def translate(self, virtual_address: int) -> Union[Address, Error]:
        vpn, offset = virtual_address & PAGE_FRAME, virtual_address & OFFSET
        key = vpn | self._entry_high

        if key in self._tlb:
            address = Address(self._tlb[key])
            if address.is_valid():
                return address.set_offset(offset)
            else:
                return Error.INVALID_ENTRY
     
        if any(vpn == entry & PAGE_FRAME for entry in self._tlb):
            return Error.MISMATCHED_ASID

        return Error.NO_MAPPING


class Address:
    def __init__(self, physical_address: int) -> None:
        self._physical_address = physical_address

    def set_offset(self, offset: int) -> Address:
        return Address(self._physical_address & PAGE_FRAME | offset)

    def is_valid(self) -> bool:
        return self._physical_address & VALID

    def is_writeable(self) -> bool:
        return self._physical_address & WRITE_CONTROL

    def is_global(self) -> bool:
        return self._physical_address & GLOBAL

    def __str__(self) -> str:
        hex_string = lambda n: "0x" + f"{n:08x}".upper()

        s = f"Address: {hex_string(self._physical_address)}\n"
        s += f"Writeable: {'Y' if self.is_writeable() else 'N'}\n"
        s += f"Global: {'Y' if self.is_global() else 'N'}"

        return s


class Error(Enum):
    NO_MAPPING = 0
    INVALID_ENTRY = 1
    MISMATCHED_ASID = 2


if __name__ == "__main__":
    computer = R3000(
        {
            0x00028200: 0x0063f400,
            0x00034200: 0x001fc600,
            0x0005b200: 0x002af200,
            0x0008a100: 0x00145600,
            0x0005c100: 0x006a8700,
            0x0001c200: 0x00a97600,
        },
        0x00000200
    )

    test_cases = [0x00028123, 0x0008a7eb, 0x0005cfff, 
                  0x0001c642, 0x0005b888, 0x00034000, 0x0]

    for i, test_case in enumerate(test_cases):
        res = computer.translate(test_case)

        print(f"Test Case: 0x{f'{test_case:08x}'.upper()}")
        if res is Error.NO_MAPPING:
            print("No mapping currently exists in the TLB")
        elif res is Error.MISMATCHED_ASID:
            print("ASID is mismatched")
        elif res is Error.INVALID_ENTRY:
            print("Entry is not valid")
        else:
            print(res)

        if i != len(test_cases) - 1:
            print()