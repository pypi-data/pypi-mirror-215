# ---- All C structures needed for operations ----
import sys
import traceback
import numpy as np
from ctypes import c_long, c_longlong, c_uint, c_ubyte, c_void_p, c_float, c_char, c_int, c_int32
from ctypes import sizeof, Union, Structure
from enum import Enum

from .enums import PPOperationUID, PPParam
from .logger import logger
from . import utils


OP_PARAM_MAX_SIZE = 512  # NOTE: ALIGN WITH DAVINSY.


C_LONG_TYPE = c_longlong if sys.maxsize > 2 ** 32 else c_long



class CPARAM(Structure):
    """
    Generic CPARAM (as union)
    """
    _fields_ = [
        ("typeid", c_uint),
        ("size", c_uint),
        ("data", OP_PARAM_MAX_SIZE * c_ubyte)
    ]

    def get_out_len(self, previous):
        raise RuntimeError("Not implemented")

    def get_temp_len(self, previous):
        raise RuntimeError("Not implemented")

    def check_node(self):
        raise RuntimeError("Not implemented")


def VECTOR1DF32_factory(length):
    class VECTOR1DF32(Structure):
        _fields_ = [
            ("typeid", c_uint),
            ("size", c_uint),
            ("len", c_uint),
            ("data", c_void_p),
            ("_", c_float * int(length))
        ]

    return VECTOR1DF32


def VECTOR1DF32_to_pyList(inp):

    structheader = VECTOR1DF32_factory(0).from_address(inp)
    lenvect = structheader.len
    inputvect = VECTOR1DF32_factory(lenvect).from_address(inp)
    datain = (c_float * int(inputvect.len)).from_address(inputvect.data)

    dataintList = [datain[k] for k in range(inputvect.len)]

    # logger.info("CP1D: header: typeid %08x len %d" % (structheader.typeid,lenvect))
    # logger.info("CP1D: invector: typeid %08x len %d" % (inputvect.typeid,inputvect.len))
    # logger.info("CP1D: invector: typeid %08x len %d" % (inputvect.typeid,inputvect.len))
    # logger.info("CP1D: invector: typeid %08x len %d" % (inputvect.typeid,inputvect.len))
    # logger.info("CP1D: type(datain)"+str(type(datain)))
    # logger.info("CP1D: type(dataintList)"+str(type(dataintList)))

    return dataintList


def VECTOR1DF32_from_pyList(dataoutList):
    lenvect = len(dataoutList)
    outvect = VECTOR1DF32_factory(lenvect)(
        typeid=0xA0000011,
        size=sizeof(VECTOR1DF32_factory(lenvect)),
        len=lenvect,
        data=0,
        _=(c_float * lenvect)(*dataoutList)
    )
    return outvect


def VECTOR2DF32_factory(length):
    class VECTOR2DF32(Structure):
        _fields_ = [
            ("typeid", c_uint),
            ("size", c_uint),
            ("len", 2 * c_uint),
            ("data", c_void_p),
            ("_", c_float * int(length))
        ]

    return VECTOR2DF32


def VECTOR2DF32_to_pyArray(inp):

    structheader = VECTOR2DF32_factory(0).from_address(inp)
    dim = (2 * c_uint).from_address(structheader.len)
    dim = [dim[k] for k in range(2)]
    length = np.prod(dim)
    inputvect = VECTOR2DF32_factory(length).from_address(inp)
    datain = (c_float * int(length)).from_address(inputvect.data)

    dataintList = [datain[k] for k in range(inputvect.len)]
    dataintArray = np.array(dataintList)
    
    return dataintArray


def VECTOR2DF32_from_pyArray(dataoutArray):
    dim = dataoutArray.shape
    lenvect = np.prod(dim)
    outvect = VECTOR2DF32_factory(lenvect)(
        typeid=0xA0000012,
        size=sizeof(VECTOR2DF32_factory(lenvect)),
        len=(2 * c_uint)(*list(dim)),
         data=0,
        _=(c_float * lenvect)(*dataoutArray.flatten())
    )
    return outvect


def VECTOR2X1DF32_factory(length):
    class VECTOR2X1DF32(Structure):
        _fields_ = [
            ("typeid", c_uint),
            ("size", c_uint),
            ("len1", c_uint),
            ("data1", c_void_p),
            ("len2", c_uint),
            ("data2", c_void_p),
            ("_", c_float * int(length))
        ]

    return VECTOR2X1DF32


# MAX_PARAM_DATA_SIZE_VECTOR2DF32 = int(  (sizeof(CPARAM) - sizeof(VECTOR2DF32_factory(0))  -3*sizeof(c_uint)) /sizeof(c_float) )

MAX_PARAM_DATA_SIZE_VECTOR2DF32 = int(70)  # max value


class CPARAMMODE(Structure):
    _fields_ = [
        ("typeid", c_uint),
        ("size", c_uint),
        ("mode", c_uint)
    ]

    def get_out_len(self, previous, op_uid):
        if op_uid == PPOperationUID.OPS_UID_CP1D.value:
            if (self.mode == 0):
                return sizeof(VECTOR1DF32_factory(0))

        return 0  # defined by the operation

    def get_temp_len(self, previous, op_uid):
        return 0

    def check_node(self):
        return True

class CPARAMDCT2D(Structure):
    _fields_ = [
        ("typeid", c_uint),
        ("size", c_uint),
        ("dct_length", c_uint),
        ("width", c_uint),
        ("skipfirst", c_uint),
    ]

    def get_out_len(self, previous, op_uid):
        if op_uid == PPOperationUID.OPS_UID_CP1D.value:
            if (self.mode == 0):
                return sizeof(VECTOR1DF32_factory(0))

        return 0  # defined by the operation

    def get_temp_len(self, previous, op_uid):
        return 0

    def check_node(self):
        return True

# PARAM_COMPRESS

class CPARAM_COMPRESS(Structure):
    _fields_ = [
        ("typeid", c_uint),
        ("size", c_uint),
        ("dimIn", c_uint),
        ("dimOut", c_uint),
    ]
    def check_node(self):
        return True
    
def CPARAM_COMPRESS_factory():

    return CPARAM_COMPRESS

def CPARAM_COMPRESS_to_pyDict(param):

    structheader = CPARAM_COMPRESS_factory().from_address(param)
    return structheader

# CPARAM_SHAPE
class CPARAM_SHAPE(Structure):
    _fields_ = [
        ("typeid", c_uint),
        ("size", c_uint),
        ("nbrows", c_uint),
        ("nbcols", c_uint),
    ]
    def check_node(self):
        return True
    
def CPARAM_SHAPE_factory():

    return CPARAM_SHAPE

def CPARAM_SHAPE_to_pyDict(param):

    structheader = CPARAM_SHAPE_factory().from_address(param)
    return structheader

# CPARAMSPECTRUM
class CPARAMSPECTRUM(Structure):
    _fields_ = [
        ("typeid", c_uint),
        ("size", c_uint),
        ("mode", c_uint),
        ("wintype", c_uint),
        ("normtype", c_uint),
        ("nbvectout", c_uint)
    ]

    def get_out_len(self, previous, op_uid):
        raise RuntimeError("Not implemented")

    def get_temp_len(self, previous, op_uid):
        raise RuntimeError("Not implemented")

    def check_node(self):
        raise RuntimeError("Not implemented")


class CPARAMMFCC(Structure):
    _fields_ = [
        ("typeid", c_uint),
        ("size", c_uint),
        ("mode", c_uint),
        ("wintype", c_uint),
        ("normtype", c_uint),
        ("melref", c_float),
        ("melLogFormula", c_uint),
        ("melLogTop_dB", c_float),
        ("nmfcc", c_uint),
        ("nbvectout", c_uint)
    ]

    def get_out_len(self, previous, op_uid):
        return sizeof(VECTOR2DF32_factory(0)) + self.nmfcc * self.nbvectout * sizeof(c_float)

    def get_temp_len(self, previous, op_uid):
        return 2048 * 6 * 4 + 128 * 4

    def check_node(self):
        return True


class CPARAMMEL(Structure):
    _fields_ = [
        ("typeid", c_uint),
        ("size", c_uint),
        ("mode", c_uint),
        ("wintype", c_uint),
        ("normtype", c_uint),
        ("melref", c_float),
        ("melLogFormula", c_uint),
        ("melLogTop_dB", c_float),
        ("nbvectout", c_uint)
    ]

    def get_out_len(self, previous, op_uid):
        raise RuntimeError("Not implemented")

    def get_temp_len(self, previous, op_uid):
        raise RuntimeError("Not implemented")

    def check_node(self):
        raise RuntimeError("Not implemented")


class CPARAMDCT(Structure):
    _fields_ = [
        ("typeid", c_uint),
        ("size", c_uint),
        ("mode", c_uint),
        ("logFormula", c_uint),
        ("logTop_dB", c_float),
        ("nmfcc", c_uint),
        ("nbvectout", c_uint)
    ]

    def get_out_len(self, previous, op_uid):
        raise RuntimeError("Not implemented")

    def get_temp_len(self, previous, op_uid):
        raise RuntimeError("Not implemented")

    def check_node(self):
        raise RuntimeError("Not implemented")


class CPARAMNOISEMIX(Structure):
    _fields_ = [
        ("typeid", c_uint),
        ("size", c_uint),
        ("mode", c_uint),
        ("snr", c_float),
        ("option", c_uint)
    ]

    def get_out_len(self, previous, op_uid):
        # WARN INPLACE
        return sizeof(VECTOR1DF32_factory(0))

    def get_temp_len(self, previous, op_uid):
        return 0

    def check_node(self):
        return True


paramspan_vector2df32 = VECTOR2DF32_factory(MAX_PARAM_DATA_SIZE_VECTOR2DF32)  # max value


class CPARAMSPAN(Structure):
    _fields_ = [
        ("typeid", c_uint),
        ("size", c_uint),
        ("mode", c_uint),
#        ("span", paramspan_vector2df32) # legacy
        ("span_lenx",c_uint),
        ("span_leny",c_uint),
        ("span_data",c_void_p),
        ("_",c_float * int(MAX_PARAM_DATA_SIZE_VECTOR2DF32)) # max(span_lenx/2)*span_leny))
    ]

    def get_out_len(self, previous, op_uid):

        size = 0

        if previous is not None:
            if isinstance(previous,CPARAMMFCC):
                logger.debug("header size %f" % sizeof(VECTOR2DF32_factory(0)))
                logger.debug("nmfcc %d" % previous.nmfcc)
                logger.debug("sizeof(float) %f" % sizeof(c_float))

                logger.debug("nbparts %d %d %f" % (self.span_lenx, self.span_leny, self.span_lenx/ 2))
                size = sizeof(VECTOR2DF32_factory(0)) + previous.nmfcc * self.span_leny* self.span_lenx / 2 * sizeof(
                    c_float)

        return size

    def get_temp_len(self, previous, op_uid):
        return 0

    def check_node(self):
        return True


class CALLPARAMS(Union):
    _fields_ = [
        ("param", CPARAM),
        ("param_mel", CPARAMMEL),
        ("param_dct", CPARAMDCT),
        ("param_mfcc", CPARAMMFCC),
        ("param_noisemix", CPARAMNOISEMIX),
        ("param_pwspan", CPARAMSPAN),
        ("param_mode", CPARAMMODE),
        ("param_dct2d", CPARAMDCT2D),
        ("param_compress", CPARAM_COMPRESS),
        ("param_shape", CPARAM_SHAPE)
    ]


def fill_params(defaultData, parameters):
    if parameters["typeid"] == PPParam.OP_PARAM_MFCC.value:
        logger.info("Setting MFCC params", parameters)

        if parameters["nmfcc"] > 127:
            raise RuntimeError(f"WARNING n MFCC too high {parameters['nmfcc']}, max value is 127")

        res = CALLPARAMS(
            param_mfcc=CPARAMMFCC(
                typeid=parameters["typeid"],
                size=parameters["size"],
                mode=parameters["mode"],
                wintype=parameters["wintype"],
                normtype=parameters["normtype"],
                melref=parameters["melref"],
                melLogFormula=parameters["melLogFormula"],
                melLogTop_dB=parameters["melLogTop_dB"],
                nmfcc=parameters["nmfcc"],
                nbvectout=parameters["nbvectout"]
            )
        )
        if not res.param_mfcc.check_node():
            logger.warn("Node : Parameters inconsistency in mfcc")

    elif parameters["typeid"] == PPParam.OP_PARAM_PWSPAN.value:
        logger.info("Setting PWSPAN params", parameters)

        # TODO
        # cast_paramspan
        # update size
        sizeBytes = parameters["size"]
        span_lenx = int(parameters["span_lenx"] )
        span_leny = int(parameters["span_leny"])
        sizeData = span_lenx*span_leny* 4

        if sizeBytes <= 32 : # 64bits pointer
            logger.warn(f"Overwrite PWSPAN Size with {span_lenx} by {span_leny} = {sizeData} bytes")
            sizeBytes += sizeData

        res = CALLPARAMS(
            param_pwspan=CPARAMSPAN(
                typeid=parameters["typeid"],  # 4 Bytes
                size=sizeBytes,               # 4 Bytes
                mode=parameters["mode"],      # 4 Bytes
                span_lenx=span_lenx,  # 4 Bytes
                span_leny=span_leny,  # 4 Bytes
                span_data= 0,                       # 8 Bytes
                _=(c_float * MAX_PARAM_DATA_SIZE_VECTOR2DF32)(*parameters["span_data"])
            )
        )
        # res.param_pwspan.span.data = cast(pointer(res.param_pwspan.span._), c_void_p)
        if not res.param_pwspan.check_node():
            logger.warn("Node : Parameters inconsistency in pwspan")
    elif parameters["typeid"] == PPParam.OP_PARAM_NOISEMIX.value:
        logger.info("Setting NoiseMix params", parameters)
        res = CALLPARAMS(
            param_noisemix=CPARAMNOISEMIX(
                typeid=parameters["typeid"],
                size=parameters["size"],
                mode=parameters["mode"],
                snr=parameters["snr"],
                option=parameters["option"]
            )
        )
        if not res.param_noisemix.check_node():
            logger.warn("Node : Parameters inconsistency in NoiseMix")
    elif parameters["typeid"] == PPParam.OP_PARAM_MODE.value:
        logger.info("Setting param_mode params", parameters)
        res = CALLPARAMS(
            param_mode=CPARAMMODE(
                typeid=parameters["typeid"],
                size=parameters["size"],
                mode=parameters["mode"]
            )
        )
        if not res.param_mode.check_node():
            logger.warn("Node : Parameters inconsistency in param_mode")
    elif parameters["typeid"] == PPParam.OP_PARAM_DCT_2D.value:
        logger.info(f"Setting param_dct2d params  {parameters}")
        res = CALLPARAMS(
            param_dct2d=CPARAMDCT2D(
                typeid=parameters["typeid"],
                size=parameters["size"],
                dct_length=parameters["dct_length"],
                width=parameters["width"],
                skipfirst=parameters["skipfirst"]
            )
        )
        if not res.param_mode.check_node():
            logger.warn("Node : Parameters inconsistency in param_dct2d")
    elif parameters["typeid"] == PPParam.OP_PARAM_COMPRESS.value:
        logger.info("Setting OP_PARAM_COMPRESS params", parameters)
        res = CALLPARAMS(
            param_compress=CPARAM_COMPRESS(
                typeid=parameters["typeid"],
                size=parameters["size"],
                dimIn=parameters["dimIn"],
                dimOut=parameters["dimOut"],
            )
        )
        if not res.param_compress.check_node():
            logger.warn("Node : Parameters inconsistency in param_compress")

    elif parameters["typeid"] == PPParam.OP_PARAM_SHAPE.value:
        logger.info("Setting CPARAM_SHAPE params", parameters)
        res = CALLPARAMS(
            param_shape=CPARAM_SHAPE(
                typeid=parameters["typeid"],
                size=parameters["size"],
                nbrows=parameters["nbrows"],
                nbcols=parameters["nbcols"],
            )
        )
        if not res.param_shape.check_node():
            logger.warn("Node : Parameters inconsistency in param_compress")
    else:
        raise RuntimeError("Unknown param type: %08x" % parameters["typeid"])

    return res


class CUST_OP(Enum):
    OP_INIT_FILE_DLM = 0x80000000
    OP_INIT_FILE_PST = 0x80000001
    OP_PUSH_FILE = 0x80000002
    OP_SEND_EVT_ID = 0x80000003  # define OP_SEND_EVT_ID      OP_CUST_MIN | 0x0000003

    OP_TRAIN_INFO = 0x80000004
    OP_INFER_INFO = 0x80000005

    OP_CUST_FIRST = 0x80000100


class CUST_TYPE_ID(Enum):

    # load(operations.define)
    OP_TYPE_ID_NAME = 0x80000000
    OP_TYPE_ID_DIM = 0x80000001
    OP_TYPE_ID_DLM = 0x80000002
    OP_TYPE_ID_PST = 0x80000003

    #    OP_TYPE_ID_TRAIN_INFO     = 0x80000004
    OP_TYPE_ID_INFERINFO = 0x80000005


class CINIT_GEN_PARAM(Structure):
    _fields_ = [
        ("typeid", c_uint),
        ("size", c_uint),
        ("data", c_char * 128),
    ]


class CINIT_FILE_PARAM(Structure):
    _fields_ = [
        ("typeid", c_uint),
        ("size", c_uint),
        ("name", c_char * 128),
    ]


class CPUSH_FILE_PARAM(Structure):
    _fields_ = [
        ("typeid", c_uint),
        ("size", c_uint),
        ("dim", c_uint),
    ]


class CPUSH_PARAM(Structure):
    _fields_ = [
        ("typeid", c_uint),
        ("size", c_uint),
        ("dim", c_uint),
    ]


class CPUSH_INFERINFO(Structure):
    _fields_ = [
        ("typeid", c_uint),
        ("size", c_uint),
        ("dim", c_uint),
        ("proba", C_LONG_TYPE),
        ("lutlables", C_LONG_TYPE),
        # pst info
        ("p_info", C_LONG_TYPE),
    ]

    def todict(self):
        newres = dict()
        newres['dim'] = self.dim

        if self.dim < 0:
            logger.error("[OPERATION_PY] ERROR: Corrupted Infer Info")
            newres['proba'] = []
            newres['lutlables'] = []
            newres['pst_label_dlm'] = 0
            newres['pst_label_out'] = 0
            newres['pst_confidenceLevel'] = 0.0
        elif self.dim == 0:
            logger.warn("[OPERATION_PY] WARN: Empty Infer Info")
            newres['proba'] = []
            newres['lutlables'] = []
            newres['pst_label_dlm'] = 0
            newres['pst_label_out'] = 0
            newres['pst_confidenceLevel'] = 0.0
        else:
            tmp = (c_float * self.dim).from_address(self.proba)
            newres['proba'] = [float(a) for a in tmp]
            tmp = (c_int32 * self.dim).from_address(self.lutlables)
            newres['lutlables'] = [int(a) for a in tmp]
            pstinfo = CPSTINFO.from_address(self.p_info)
            newres['pst_label_dlm'] = pstinfo.label_dlm
            newres['pst_label_out'] = pstinfo.label_out
            newres['pst_confidenceLevel'] = pstinfo.confidenceLevel

        return newres


class CPUSH_FILE_DLM(Structure):
    _fields_ = [
        ("typeid", c_uint),
        ("size", c_uint),
        ("proba", C_LONG_TYPE),
        ("lutlables", C_LONG_TYPE),
    ]


class CPUSH_FILE_DLM(Structure):
    _fields_ = [
        ("typeid", c_uint),
        ("size", c_uint),
        ("proba", C_LONG_TYPE),
        ("lutlables", C_LONG_TYPE),
    ]


class CPSTINFO(Structure):
    _fields_ = [
        ("outvect", C_LONG_TYPE),
        ("dim", c_int),
        ("confidenceLevel", c_float),
        ("label_dlm", c_uint),
        ("label_out", c_uint)
    ]


class CPUSH_FILE_PST(Structure):
    _fields_ = [
        ("typeid", c_uint),
        ("size", c_uint),
        ("p_info", C_LONG_TYPE),
    ]


class CMODE_PARAM(Structure):
    _fields_ = [
        ("typeid", c_uint),
        ("size", c_uint),
        ("mode", c_int),
    ]


class CEVENT_ID(Structure):
    _fields_ = [
        ("typeid", c_uint),
        ("size", c_uint),
        ("evtid", c_uint),
    ]


class OperationRegistry():
    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls._instance = cls()
        return cls._instance

    def __init__(self, registry: dict = {}):
        self.registry = registry
        self.dlm_file_name = ""
        self.pst_file_name = ""
        self.event_listeners = []

    def _init_file(self, op, param):
        logger.info("== Init file", op)
        logger.info("== Init file", param.name)

        name = bytearray(param.name).decode("utf8")
        if op == CUST_OP.OP_INIT_FILE_PST.value:
            self.pst_file_name = name
        else:
            self.dlm_file_name = name

        if param.typeid != CUST_TYPE_ID.OP_TYPE_ID_NAME.value:
            raise RuntimeError("Bad typeid fo init file")

        f = open(name, "w")
        f.close()

    def _push_file(self, param, inp):
        typeid = c_uint.from_address(inp)
        logger.debug("typeid %08x" % typeid.value)
        if typeid.value == CUST_TYPE_ID.OP_TYPE_ID_DLM.value:
            struct = CPUSH_FILE_DLM.from_address(inp)
            proba = (c_float * param.dim).from_address(struct.proba)
            line = ""
            logger.debug("dim", param.dim)
            logger.debug("size %d" % struct.size)
            logger.debug("proba %x" % struct.proba, proba[0])

            try :
                with open(self.dlm_file_name, "a+") as f:
                    logger.debug("opened %s" % self.dlm_file_name)
                    csvline = ""
                    for k in range(param.dim):
                        csvline += "%0.3f" % proba[k]
                        line += "%0.1f" % (100 * proba[k])
                        if k < param.dim - 1:
                            csvline += " "
                            line += " "
                    logger.debug(line)
                    print(csvline, file=f)
            except Exception as e :
                logger.debug("No file %s" % self.dlm_file_name)

        elif typeid.value == CUST_TYPE_ID.OP_TYPE_ID_PST.value:
            struct = CPUSH_FILE_PST.from_address(inp)
            pstinfo = CPSTINFO.from_address(struct.p_info)
            logger.debug("dim", pstinfo.dim)
            with open(self.pst_file_name, "a+") as f:
                print("%d %d %0.1f\n" % (pstinfo.label_dlm, pstinfo.label_out, pstinfo.confidenceLevel), file=f)
            logger.debug(
                "POST: %d => %d , %0.1f" % (pstinfo.label_dlm, pstinfo.label_out, 100.0 * pstinfo.confidenceLevel))
        else:
            logger.error("Unknown typeid")

    def add_event_listener(self, listener):
        self.event_listeners.append(listener)

    def add_custom_operation(self, opId: str, operation: callable):
        """
        Add a custom operation
        Args:
            opId: operation ID number
            operation: operation function, needs to have (op_id, event, param, inp) arguments
        """
        if opId in self.registry.keys():
            logger.warning(f"Operation already existing at ID {opId}")
        else:
            self.registry.update({opId: operation})

# operation called by DavinSy
    def call_operation(self, op_id, event, param, inp):
        logger.debug("==============================")
        logger.debug("=== INSIDE PYTHON OPERATION")
        logger.debug("op_id %08x" % op_id)
        logger.debug("event %016x" % event)
        logger.debug("param %016x" % param)
        logger.debug("input %016x" % inp)

        if op_id == CUST_OP.OP_TRAIN_INFO.value or \
            op_id == CUST_OP.OP_INFER_INFO.value or \
            op_id == CUST_OP.OP_SEND_EVT_ID.value :
            for listener in self.event_listeners:
                listener(op_id, event, param, inp)

        # LEGACY
        try:
            if op_id == CUST_OP.OP_INIT_FILE_DLM.value or op_id == CUST_OP.OP_INIT_FILE_PST.value:
                logger.info("== Case 1")
                s = CINIT_FILE_PARAM.from_address(param)
                logger.info("== Struct", s)
                self._init_file(op_id, s)
            elif op_id == CUST_OP.OP_PUSH_FILE.value:
                logger.info("== Case 2")
                s = CPUSH_FILE_PARAM.from_address(param)
                self._push_file(s, inp)

            elif op_id >= CUST_OP.OP_CUST_FIRST.value:
                try:
                    if op_id in self.registry:
                        return self.registry[op_id](op_id, event, param, inp)
                    else:
                        logger.warn(" OP %08x not in registery" % op_id)
                except:
                    traceback.print_exc()

        except Exception:
            traceback.print_exc()


def call_operation(op_id, event, param, inp):
    return OperationRegistry().call_operation(op_id, event, param, inp)


# ------ CUSTOM OPERATIONS ------
def cp1D(op_id, event, param, inp):
    dataintList = VECTOR1DF32_to_pyList(inp)
    dataoutList = [(dataintList[k]) for k in range(len(dataintList))]
    out = VECTOR1DF32_from_pyList(dataoutList)

    return bytearray(out)
