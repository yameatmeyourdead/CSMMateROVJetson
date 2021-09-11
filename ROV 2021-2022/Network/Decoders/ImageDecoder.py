from Network.Decoders.DecoderBase import DecoderBase
from json import loads
import numpy as np

class ImageDecoder(DecoderBase):
    def decode(bytez: bytes, ) -> object:
        