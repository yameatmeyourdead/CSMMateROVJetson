from abc import ABC, abstractstaticmethod

class EncoderBase(ABC):
    EOM = b"<<"
    @abstractstaticmethod
    def encode(obj:object, *args, **kwargs) -> bytes: ...