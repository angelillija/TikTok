def pkcs7_padding_data_length(buffer, buffer_size, modulus):
    if buffer_size % modulus != 0 or buffer_size < modulus:
        return 0
    padding_value = buffer[buffer_size-1]
    if padding_value < 1 or padding_value > modulus:
        return 0
    if buffer_size < padding_value + 1:
        return 0
    count = 1
    buffer_size -= 1
    for i in range(count, padding_value):
        buffer_size -= 1
        if buffer[buffer_size] != padding_value:
            return 0
    return buffer_size

def pkcs7_padding_pad_buffer(buffer: bytearray, data_length: int, buffer_size: int, modulus: int) -> int:
    pad_byte = modulus - (data_length % modulus)
    if data_length + pad_byte > buffer_size:
        return -pad_byte
    for i in range(pad_byte):
        buffer[data_length+i] = pad_byte
    return pad_byte

def padding_size(size: int) -> int:
    mod = size % 16
    if mod > 0:
        return size + (16 - mod)
    return size