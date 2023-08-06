from enum import Enum

class MSG_TYPE(Enum):
    MSG_TYPE_CHUNK=0
    MSG_TYPE_FULL=1
    MSG_TYPE_EXCEPTION=2
    MSG_TYPE_STEP=3
    MSG_TYPE_META=4
    MSG_TYPE_REF=5
    MSG_TYPE_CODE=6
    MSG_TYPE_UI=7
