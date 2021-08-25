from abc import ABC, abstractmethod
from enum import Enum
from typing import Any
import numpy as np
import json
try:
    import evdev
except ImportError:
    print("REQUIRES EVDEV AND LINUX MACHINE")
    exit()


EOM = b"<<"

class messageType(Enum):
    command = "0001"
    controller = "0000"
    data = "1001"
    camera = "0110"
    message = "1010"

class encoder(ABC):
    @staticmethod
    @abstractmethod
    def encode(data:Any) -> bytes:
        return b""

class commandEncoder(encoder):
    def encode(data:Any) -> bytes:
        return b""

class controllerEncoder(encoder):
    def encode(data:Any) -> bytes:
        return b""

class dataEncoder(encoder):
    def encode(data:Any) -> bytes:
        return b""

class cameraEncoder(encoder):
    @staticmethod
    def encode(camIdent:int, img:np.ndarray) -> bytes:
        assert (camIdent is not None and img is not None)
        return messageType.camera.value.encode() + (json.dumps(dict(dtype=str(img.dtype), shape=img.shape, size=img.size, cam=camIdent)).encode("utf-8") + EOM + img.tobytes() + EOM)

class messageEncoder(encoder):
    @staticmethod
    def encode(message:str) -> bytes:
        return message.encode(encoding="utf-8") + EOM

encoders = {
    "command":commandEncoder,
    "controller":controllerEncoder,
    "data":dataEncoder,
    "camera":cameraEncoder,
    "message":messageEncoder
}

class decoder(ABC):
    @staticmethod
    @abstractmethod
    def decode(data):
        return ""

class commandDecoder(decoder):
    @staticmethod
    def decode(data):
        return ""

class controllerDecoder(decoder):
    @staticmethod
    def decode(data):
        return ""

class dataDecoder(decoder):
    @staticmethod
    def decode(name:str, data:bytes):
        return ""

class cameraDecoder(decoder):
    @staticmethod
    def decode(metaData:str, array:bytes) -> np.ndarray:
        metaData = json.loads(metaData)
        return np.ndarray(metaData["shape"], dtype=metaData["dtype"], buffer=array)

class messageDecoder(decoder):
    @staticmethod
    def decode(data:bytes):
        return data.decode()

decoders = {
    "command":commandDecoder,
    "controller":controllerDecoder,
    "data":dataDecoder,
    "camera":cameraDecoder,
    "message":messageDecoder
}