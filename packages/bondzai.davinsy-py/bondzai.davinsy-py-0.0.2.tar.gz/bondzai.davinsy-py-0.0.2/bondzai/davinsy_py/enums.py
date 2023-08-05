'''
 THIS IS A GENERATED FILE, DO NOT EDIT
 BONDZAI
          /"*._         _
      .-*'`    `*-.._.-'/
    < * ))     ,       ( 
      `*-._`._(__.--*"`.\
'''


from enum import Enum


class EventOperationID(Enum):
    EVT_EXT_EXCEPTION = 0x00
    EVT_EXT_DATA_IN = 0x01
    EVT_EXT_CMD_STATUS = 0x100
    EVT_EXT_LOG = 0x101
    EVT_EXT_POSTPROC = 0x200
    EVT_EXT_CUSTOM_1 = 0xF00
    EVT_EXT_CUSTOM_2 = 0xF01
    EVT_EXT_CUSTOM_3 = 0xF02
    EVT_EXT_CUSTOM_4 = 0xF03
    EVT_INT_EXCEPTION = 0x1000
    EVT_INT_DATA_STORED = 0x1001
    EVT_INT_DISCOVERY = 0x1002
    EVT_INT_TRANSPORT = 0x1003
    EVT_INT_DATA_UPDATED = 0x1100
    EVT_INT_READY_TO_PREPROC_BATCH = 0x1101
    EVT_INT_PREPROC_BATCH_DONE = 0x1102
    EVT_INT_TRIGGER_NEXT = 0x1103
    EVT_INT_FINAL = 0x1104
    EVT_INT_READY_TO_PREPROC_SINGLE = 0x1105
    EVT_INT_PREPROC_SINGLE_DONE = 0x1106
    EVT_INT_READY_TO_TRAIN = 0x1107
    EVT_INT_READY_TO_INFER = 0x1108
    EVT_INT_CORRECTION_DONE = 0x1109
    EVT_INT_INFER_DONE = 0x1200
    EVT_INT_TRAIN_DONE = 0x1201
    EVT_INT_POSTPROC_DONE = 0x1202
    EVT_INT_ITERATE_DB = 0x1300
    EVT_INT_ITERATE_DONE = 0x1301
    EVT_INT_CUSTOM_1 = 0x1F00
    EVT_INT_CUSTOM_2 = 0x1F01
    EVT_INT_CUSTOM_3 = 0x1F02
    EVT_INT_CUSTOM_4 = 0x1F03
    EVT_INT_YIELD_1 = 0x2000
    EVT_INT_YIELD_2 = 0x2001
    EVT_INT_YIELD_3 = 0x2002
    EVT_INT_YIELD_4 = 0x2003
    EVT_INT_FORCE_TRAIN = 0x3001
    EVT_INT_FORCE_DATA_IN = 0x3002
    EVT_TRANSIENT_MMS_LOAD = 0xF001
    EVT_TRANSIENT_RAM_LOAD = 0xF002
    EVT_TRANSIENT_FLASH_LOAD = 0xF003
    EVT_MAX = 0xFFFF


class AgentAIMode(Enum):
    APP_AI_MODE_NOT_INIT = -1
    APP_AI_MODE_STANDBY = 0
    APP_AI_MODE_ENROLLEMENT = 1
    APP_AI_MODE_INFERENCE = 2


class PPOperationUID(Enum):
    OPS_ID_EXT = 0x80000000
    OPS_ID = 0x00000000
    OPS_MISC = 0x00000000
    OPS_MATH = 0x01000000
    OPS_DSP = 0x02000000
    OPS_IMG = 0x03000000
    OPS_STR = 0x04000000
    OPS_DBM = 0x05000000
    OPS_PST = 0x0E000000
    OPS_DIST = 0x0F000000
    OPS_UID_NOP = 0x00
    OPS_UID_NOPEND = 0x01
    OPS_UID_CP1D = 0x02
    OPS_UID_CP2D = 0x03
    OPS_UID_CP2X1D = 0x04
    OPS_UID_RMNFIRST1D_F32 = 0x05
    OPS_UID_LOGANF32 = 0x1000001
    OPS_UID_LOGA10F32 = 0x1000002
    OPS_UID_MEANF32 = 0x1000011
    OPS_UID_VARF32 = 0x1000012
    OPS_UID_RESHAPEF32 = 0x1000013
    OPS_UID_HISTOGRAMF32 = 0x1000014
    OPS_UID_SLICEF32 = 0x1000015
    OPS_UID_FFT2048F32 = 0x2000011
    OPS_UID_FFT1024F32 = 0x2000012
    OPS_UID_FFT16F32 = 0x2000018
    OPS_UID_MFCC2048F32 = 0x2000019
    OPS_UID_MFCC1024F32 = 0x200001A
    OPS_UID_MEL2048F32 = 0x2000021
    OPS_UID_MEL1024F32 = 0x2000022
    OPS_UID_MEL16F32 = 0x2000028
    OPS_UID_DCT2048F32 = 0x2000031
    OPS_UID_DCT1024F32 = 0x2000032
    OPS_UID_DCT512F32 = 0x2000033
    OPS_UID_DCT256F32 = 0x2000034
    OPS_UID_DCT128F32 = 0x2000035
    OPS_UID_NOISEMIXF32 = 0x2000061
    OPS_UID_PWSPANF32 = 0x2000062
    OPS_UID_PUSHSIG2DBM = 0x5000001
    OPS_UID_PST_BYPASS = 0xE000001
    OPS_UID_PST_EXT = 0x8E000001


class CommandOperationID(Enum):
    CMD_OPEN_SESSION = 0x00
    CMD_CLOSE_SESSION = 0x01
    CMD_SET = 0x100
    CMD_GET = 0x101
    CMD_DELETE = 0x102
    CMD_OPEN = 0x200
    CMD_CLOSE = 0x201
    CMD_WRITE = 0x202
    CMD_READ = 0x203
    CMD_START = 0x300
    CMD_STOP = 0x301
    CMD_SUBSCRIBE = 0x401
    CMD_UNSUBSCRIBE = 0x402


class LogCommandParameter(Enum):
    LOG_NB_KPIS = 6


class DBMCommandParameter(Enum):
    DBM_PARAM_INFO = 0x0000
    DBM_TABLE_ADDRESS_VM = 0x1000
    DBM_TABLE_ADDRESS_LBL = 0x1001
    DBM_TABLE_ADDRESS_DAT = 0x1002
    DBM_TABLE_ADDRESS_KEY = 0x1003
    DBM_TABLE_ADDRESS_CTX = 0x1004


class LogCommand(Enum):
    LOG_GET_KPI = 0x1100


class DBMCommand(Enum):
    DBM_EXPORT = 0x100
    DBM_EXPORT_ROW = 0x200
    DBM_IMPORT_ROW = 0x201
    DBM_DELETE_ROW = 0x202
    DBM_CHECK_POINT = 0x300
    DBM_RESTORE = 0x301
    DBM_DEL_CHECK_POINT = 0x302
    DBM_GET_CHECK_POINT = 0x303
    DBM_CREATE_TABLE = 0x400


class DBMTable(Enum):
    DBM_VM = 0x00
    DBM_LBL = 0x01
    DBM_DAT = 0x02
    DBM_KEY = 0x03
    DBM_CTX = 0x04
    DBM_SIG = 0x05
    DBM_GEN = 0x06
    DBM_TABLE_END = 0x07


class AgentTriggerType(Enum):
    TRIGGER_ON = 0
    TRIGGER_OFF = 1
    TRIGGER_KILL = 255


class MessageModule(Enum):
    BLD = 0x00
    COM = 0x01
    DBM = 0x02
    DLM = 0x03
    LOG = 0x04
    MAL = 0x05
    MMS = 0x06
    OTA = 0x07
    PRE = 0x08
    PST = 0x09
    RUN = 0x0A
    UTI = 0x0B
    UNK = 0x0C


class PPParam(Enum):
    OP_PARAM = 0x90000000
    OP_INOUT = 0xA0000000
    OP_INOUT_EMPTY = 0xA0000000
    OP_INOUT_MEMNEED = 0xA0000001
    OP_INOUT_VECT1DLEN = 0xA0000002
    OP_INOUT_VECT2DLEN = 0xA0000003
    OP_INOUT_VECT2X1DLEN = 0xA0000004
    OP_INOUT_VECT1D = 0xA0000011
    OP_INOUT_VECT2D = 0xA0000012
    OP_INOUT_VECT2X1D = 0xA0000013
    OP_PARAM_TYPE_PREPROC = 0x90001000
    OP_PARAM_TYPE_POSTPROC = 0x90002000
    OP_PARAM_TYPE_DIST = 0x90003000
    OP_PARAM_TYPE_RUN = 0x90004000
    OP_PARAM_TYPE_MISC = 0x90008000
    OP_PARAM_HPF = 0x90001001
    OP_PARAM_LPF = 0x90001002
    OP_PARAM_BPF = 0x90001003
    OP_PARAM_BSF = 0x90001004
    OP_PARAM_FFT = 0x90001101
    OP_PARAM_MFCC = 0x90001102
    OP_PARAM_MEL = 0x90001103
    OP_PARAM_DCT = 0x90001104
    OP_PARAM_DCT_2D = 0x90001105
    OP_PARAM_HIST = 0x90001106
    OP_PARAM_NOISEMIX = 0x90001301
    OP_PARAM_PWSPAN = 0x90001302
    OP_PARAM_COMPRESS = 0x90001402
    OP_PARAM_MATRIX = 0x90001403
    OP_PARAM_EMPTY = 0x90008000
    OP_PARAM_MODE = 0x90008001
    OP_PARAM_REMOVENFIRST = 0x90008003
    OP_PARAM_SHAPE = 0x90008005


