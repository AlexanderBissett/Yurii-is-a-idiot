from ctypes import * 

def myFmtCallback(command, modifier, arg):
    print(command)
    return 1    # TRUE

def format_drive(Drive, Format, Title):
    fm = windll.LoadLibrary('fmifs.dll')
    FMT_CB_FUNC = WINFUNCTYPE(c_int, c_int, c_int, c_void_p)
    FMIFS_UNKNOWN = 0
    fm.FormatEx(c_wchar_p(Drive), FMIFS_UNKNOWN, c_wchar_p(Format),
                c_wchar_p(Title), True, c_int(0), FMT_CB_FUNC(myFmtCallback))
    
format_drive('F:\\', 'NTFS', 'USBDrive')