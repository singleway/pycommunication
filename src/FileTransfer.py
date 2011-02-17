#coding=utf-8

import platform,thread,socket

def __transmit(file_name,remote_ip,remote_port,callback):
    if platform.system() == "Windows":
        from ctypes import WINFUNCTYPE, GetLastError, \
             windll, pythonapi, cast, WinError, create_string_buffer, \
             c_ushort, c_ubyte, c_char, WINFUNCTYPE, c_short, c_ubyte, \
             c_int, c_uint, c_long, c_ulong, c_void_p, byref, c_char_p, \
             Structure, Union, py_object, POINTER, pointer, sizeof, string_a
        
        _get_osfhandle = ctypes.CDLL("msvcrt.dll")._get_osfhandle
        #build socket
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        #open file
        f = open(file_name)
        
        #load library and get 'TransmitFile'
        TransmitFileType = WINFUNCTYPE(BOOL, SOCKET, HANDLE, DWORD, DWORD, POINTER(OVERLAPPED), POINTER(TRANSMIT_FILE_BUFFERS), DWORD)
        bogus_bytes = DWORD()
        TransmitFile = TransmitFileType(0)
        ret = windll.ws2_32.WSAIoctl(
            bogus_sock.fileno(), SIO_GET_EXTENSION_FUNCTION_POINTER, byref(WSAID_TRANSMITFILE), sizeof(WSAID_TRANSMITFILE),
            byref(TransmitFile), sizeof(TransmitFile), byref(bogus_bytes), None, None
        )
        
        sock.connect((remote_ip,remote_port))
        TransmitFile(_get_osfhandle(sock.fileno()),f.fileno(),0,0,None,None,0)
        callback()
    elif platform.system() == "Linux":
        pass

def transmit(file_name,remote_ip,remote_port,callback):
    thread.start_new_thread(__transmit,file_name,remote_ip,remote_port,callback)

