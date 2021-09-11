from enum import Enum
import numpy as np

class MessageHeader(Enum):
    image=np.ndarray,
    controllerEvent=...