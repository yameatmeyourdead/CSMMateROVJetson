from typing import Callable, Dict
from src.network.Decoders.DecoderBase import DecoderBase
from src.network.Encoders.EncoderBase import EncoderBase

__encoders:Dict[EncoderBase, Callable] = {}
__decoders:Dict[DecoderBase, Callable] = {}

def registerEncoder(encoder:EncoderBase):
    __encoders[encoder.__class__] = encoder.encode

def registerDecoder(decoder:DecoderBase):
    __decoders[decoder.__class__] = decoder.decode

def hasEncoder(encoder) -> bool:
    return encoder.__class__ in __encoders

def hasDecoder(decoder) -> bool:
    return decoder.__class__ in __decoders

def canSerialize(obj:object) -> bool:
    return obj.__class__ in __encoders and obj.__class__ in __decoders

def encode(obj:object) -> bytes:
    return __encoders[obj.__class__](obj)

def decode(bytez:bytes, cls) -> object:
    return __decoders[cls](bytez)