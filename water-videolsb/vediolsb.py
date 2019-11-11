#!/bin/python
# -*- coding=utf-8 -*-

import struct
#其实有一个wave的库

wav_file = open('jay.wav', 'rb')
#打开一个文件

# 'RIFF'+4字节size+'WAVE'
wav_RIFF_chunk = wav_file.read(12)

# 用struct的结构解析方法得到一个元祖，<代表小端表示数据，4s表示长度为4的字符串，i表示一个整形，再4s表示有一个长度为4的字符串
RIFF, size, WAVE = struct.unpack('<4sI4s', wav_RIFF_chunk)
#第二个参数是要读取的数据，第一个参数像printf,<小关存储，是高位减一还是低位减一的问题，4s说明长度为4的字符串，I无符号的整数
#因为struct.unpack返回的是一个元组，因此此处其实是RIFF,size,WAVE=(a,b,c)

print(RIFF, size, WAVE)
# 'fmt '+4字节size
wav_fmt_chunk_header = wav_file.read(8)
# fmt数据块的头部包括4字符字符串'fmt '以及一个4字节整形的大小，可能为16或者18
FMT, size = struct.unpack('<4sI', wav_fmt_chunk_header)
print(FMT, size)
# 根据大小来读取相印的数据
wav_fmt_chunk_data = wav_file.read(size)
# 当大小为16时，不包含一个short型的extra信息
if size == 16:
    codec, nChannels, samplerate, byterate, blockalign, bits = struct.unpack('<HHIIHH', wav_fmt_chunk_data)
# 当大小为18时，包含一个short型的extra信息
else:
    codec, nChannels, samplerate, byterate, blockalign, bits, extra = struct.unpack('<HHIIHHH', wav_fmt_chunk_data)