from abc import ABC, abstractstaticmethod

class EncoderBase(ABC):
    @abstractstaticmethod
    def encode(obj:object) -> bytes:
        return b""