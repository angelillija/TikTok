from utils.signer.lib.pkcs7_padding import pkcs7_padding_data_length
import ctypes

class ByteBuf:
    def __init__(self, data, size=None):
        if data:
            self.mem = data
        
        if size is not None:
            self.data_size = size
        elif data is not None:
            self.data_size = len(data)
        else:
            raise ValueError("Either size or data must be provided")

        self.pos = 0

    def data(self):
        return self.mem

    def size(self):
        return self.data_size

    def remove_padding(self):
        padding_size = pkcs7_padding_data_length(self.mem, self.data_size, 16)
        if padding_size == 0:
            return self.data_size
        self.data_size = padding_size
        dst = (ctypes.c_uint8 * self.data_size)()
        dst = self.mem[:self.data_size]
        self.mem = dst
        return self.mem