from abc import ABC, abstractstaticmethod

class DecoderBase(ABC):
    EOM = b"<<"
    @abstractstaticmethod
    def decode(bytez:bytes, *args, **kwargs) -> object: ...