##
## Preproc high level
##


try:
    import davinsy_pre
except ModuleNotFoundError:
    Exception("Cannot import C libs")
from ctypes import *
from .operations import PPParam
from .operations import VECTOR1DF32_factory
from .operations import VECTOR2DF32_factory
from .operations import call_operation

from .logger import logger

class Preproc:

    def __init__(self,graph, local=True):
        self.graph = graph
        self.local = local

    def compute_signature(self, signal):

        logger.debug(" compute signature signal with size :"+ str(len(signal)))
        inputvect = VECTOR1DF32_factory(len(signal))(
            typeid=0xA0000011,
            size=sizeof(VECTOR1DF32_factory(len(signal))),
            len=len(signal),
            data=0,
            _=(c_float * len(signal))(*signal)
        )
        inputvect.data = cast(pointer(inputvect._), c_void_p)

        if self.local:
            res = davinsy_pre.run(self.graph, bytearray(inputvect))
        else:
            if (self.graph.nb != 1):                
                raise RuntimeError("In foreign mode, graph must have only one node")
                      
            #FIXME: do something better
            res = call_operation(self.graph.nodes[0].operation_id, 0, cast(pointer(self.graph.nodes[0].parameters),c_void_p).value, cast(pointer(inputvect), c_void_p).value )

        #DIRTY FIX: padd the result on 64 bits OS
        res = res + b"\0\0\0\0"

        res1 = VECTOR1DF32_factory(0).from_buffer(res)
        header_size = sizeof(res1)

        if PPParam(res1.typeid) == PPParam.OP_INOUT_VECT1D:
            dim_out = res1.len
            logger.debug("VECTOR1DF32 len "+ str(res1.len) + " size "+ str(res1.size))
                
            zeclass = VECTOR1DF32_factory(dim_out)

            res1 = zeclass.from_buffer(res)
            logger.debug("PD %08x"%res1.data)
            data = (c_float * int(dim_out)).from_buffer(res[header_size:])

            # import numpy as np
            # print("VECTOR1DF32 data "+ np.array(data, dtype='float32'))
            datalist = [f for f in data]
            logger.debug("VECTOR1DF32 data "+ str(datalist))
        elif PPParam(res1.typeid) == PPParam.OP_INOUT_VECT2D:
            res1 = VECTOR2DF32_factory(0).from_buffer(res)
            header_size = sizeof(res1)
            nb_it = res1.len[0]
            dim_out = res1.len[1]
            logger.debug("VECTOR2DF32 dim_out "+ str(dim_out) + " by nb_it "+str(nb_it))
            logger.debug("VECTOR1DF32 size "+ str(res1.size))

            zeclass = VECTOR2DF32_factory(dim_out*nb_it)
            res2 = zeclass.from_buffer(res) 
            # FIXME 
            # data = (c_float * int(dim_out*nb_it)).from_address(res2.data) # FIXME: right now we take only the first output vector
            data = (c_float * int(dim_out*nb_it)).from_buffer(res[header_size:])
            
            datalist = []
            for k in range(nb_it):
                datalisttmp = [f for f in data[k*dim_out:(k+1)*dim_out]]
                datalist.append(datalisttmp)
            # how to reshape ?
            logger.debug("VECTOR2DF32 data "+ str(datalist))
        else:
            raise(Exception("Unknown signature output type"))

        return data
