from Network.Encoders.EncoderBase import EncoderBase
from json import dumps
import numpy as np

class ImageEncoder(EncoderBase):
    def encode(img: np.ndarray, camIdent=0) -> bytes:
        assert(img is not None), "Cannot encode NoneType"
        # return imgMetadata + EOM + imgAsBytes
        return dumps(dict(dtype=str(img.dtype), shape=img.shape, size=img.size, cam=camIdent)).encode() + EncoderBase.EOM + img.tobytes()

def test():
    ...