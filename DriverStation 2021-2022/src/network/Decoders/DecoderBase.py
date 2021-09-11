from abc import ABC, abstractstaticmethod

class DecoderBase(ABC):
    def decode(bytez:bytes) -> object:
        return ""