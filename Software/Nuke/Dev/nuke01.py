import ctypes as ct

def FmtCallback(command, modifier, arg):
    print(command)
    return 1

def format_drive(Drive, Format, Title):
    fm = ct.windll.LoadLibrary('fmifs.dll')
    FMT_CB_FUNC = ct.WINFUNCTYPE(
        ct.c_int,
        ct.c_int,
        ct.c_int,
        ct.c_void_p,
    )
    FMIFS_UNKNOWN = 0
    fm.FormatEx(
        ct.c_wchar_p(Drive),
        FMIFS_UNKNOWN,
        ct.c_wchar_p(Format),
        ct.c_wchar_p(Title),
        True,
        ct.c_int(0),
        FMT_CB_FUNC(FmtCallback),
    )

format_drive('E:\\', 'NTFS', 'Wiped')
