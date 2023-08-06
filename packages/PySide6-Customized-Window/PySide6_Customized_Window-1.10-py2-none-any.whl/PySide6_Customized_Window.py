import sys
if sys.platform != 'win32': raise Exception('Windows, ReactOS or Wine is required.')
try:
    from PySide6.QtWidgets import *
    from PySide6.QtGui import *
    from PySide6.QtCore import *
    ISPYSIDE1 = False
except: raise ImportError('Cannot load PySide6.')
import ctypes
try: import winreg
except: import _winreg as winreg
from ctypes.wintypes import MSG, POINT, RECT


__all__ = ['CustomizedWindow', 'BlurWindow']


user32 = ctypes.windll.user32


class LOGFONT(ctypes.Structure):
    _fields_ = [
    ('lfHeight', ctypes.c_long),
    ('lfWidth', ctypes.c_long),
    ('lfEscapement', ctypes.c_long),
    ('lfOrientation', ctypes.c_long),
    ('lfWeight', ctypes.c_long),
    ('lfItalic', ctypes.c_byte),
    ('lfUnderline', ctypes.c_byte),
    ('lfStrikeOut', ctypes.c_byte),
    ('lfCharSet', ctypes.c_byte),
    ('lfOutPrecision', ctypes.c_byte),
    ('lfClipPrecision', ctypes.c_byte),
    ('lfQuality', ctypes.c_byte),
    ('lfPitchAndFamily', ctypes.c_byte),
    ('lfFaceName', ctypes.c_wchar * 32)]


class NONCLIENTMETRICS(ctypes.Structure):
    _fields_ = [
    ('cbSize', ctypes.c_ulong),
    ('iBorderWidth', ctypes.c_long),
    ('iScrollWidth', ctypes.c_long),
    ('iScrollHeight', ctypes.c_long),
    ('iCaptionWidth', ctypes.c_long),
    ('iCaptionHeight', ctypes.c_long),
    ('lfCaptionFont', LOGFONT),
    ('iSmCaptionWidth', ctypes.c_long),
    ('iSmCaptionHeight', ctypes.c_long),
    ('lfSmCaptionFont', LOGFONT),
    ('iMenuWidth', ctypes.c_long),
    ('iMenuHeight', ctypes.c_long),
    ('lfMenuFont', LOGFONT),
    ('lfStatusFont', LOGFONT),
    ('lfMessageFont', LOGFONT),
    ('iPaddedBorderWidth', ctypes.c_long),]


class NCCALCSIZE_PARAMS(ctypes.Structure):
    _fields_ = [('rgrc', RECT * 3), ('lppos', ctypes.POINTER(ctypes.c_void_p))]


class WindowCompositionAttribute(ctypes.Structure):
    _fields_ = [('Attribute', ctypes.c_long), ('Data', ctypes.POINTER(ctypes.c_long)), ('SizeOfData', ctypes.c_ulong)]


class ACCENT_POLICY(ctypes.Structure):
    _fields_ = [('AccentState', ctypes.c_ulong), ('AccentFlags', ctypes.c_ulong), ('GradientColor', ctypes.c_ulong),
        ('AnimationId', ctypes.c_ulong)]


class DWM_BLURBEHIND(ctypes.Structure):
    _fields_ = [('dwFlags', ctypes.c_ulong), ('fEnable', ctypes.c_long), ('hRgnBlur', ctypes.c_void_p), ('fTransitionOnMaximized', ctypes.c_long)]


class MARGINS(ctypes.Structure):
    _fields_ = [('cxLeftWidth', ctypes.c_long), ('cxRightWidth', ctypes.c_long), ('cyTopHeight', ctypes.c_long), ('cyBottomHeight', ctypes.c_long)]


class WINDOWCOMPOSITIONATTRIBDATA(ctypes.Structure):
    _fields_ = [('Attribute', ctypes.c_ulong), ('Data', ctypes.POINTER(ACCENT_POLICY)), ('SizeOfData', ctypes.c_ulong)]


class Win10BlurEffect:
    def __init__(self):
        self.WCA_ACCENT_POLICY, self.ACCENT_ENABLE_BLURBEHIND, self.ACCENT_ENABLE_ACRYLICBLURBEHIND = 19, 3, 4
        self.accentPolicy = ACCENT_POLICY()
        self.winCompAttrData = WINDOWCOMPOSITIONATTRIBDATA()
        self.winCompAttrData.Attribute = self.WCA_ACCENT_POLICY
        self.winCompAttrData.SizeOfData = ctypes.sizeof(self.accentPolicy)
        self.winCompAttrData.Data = ctypes.pointer(self.accentPolicy)
    def __initAP(self, a, b, c, d):
        b = ctypes.c_ulong(int(b, base=16))
        d = ctypes.c_ulong(d)
        accentFlags = ctypes.c_ulong(0x20 | 0x40 | 0x80 | 0x100 | 0x200 if c else 0)
        self.accentPolicy.AccentState = a
        self.accentPolicy.GradientColor = b
        self.accentPolicy.AccentFlags = accentFlags
        self.accentPolicy.AnimationId = d
    def setAeroEffect(self, hWnd, gradientColor='01000000', isEnableShadow=True, animationId=0):
        self.__initAP(self.ACCENT_ENABLE_BLURBEHIND, gradientColor, isEnableShadow, animationId)
        return user32.SetWindowCompositionAttribute(hWnd, ctypes.byref(self.winCompAttrData))
    def setAcrylicEffect(self, hWnd, gradientColor='01000000', isEnableShadow=True, animationId=0):
        self.__initAP(self.ACCENT_ENABLE_ACRYLICBLURBEHIND, gradientColor, isEnableShadow, animationId)
        return user32.SetWindowCompositionAttribute(hWnd, ctypes.byref(self.winCompAttrData))


class MenuBtn(QAbstractButton):
    def __init__(self, parent):
        super(MenuBtn, self).__init__(parent)
        self.parent = parent
        self.parentattr = lambda arg: getattr(parent, '_CustomizedWindow__' + arg)
        self.isminbtn, self.ismaxbtn, self.isclosebtn = map(isinstance, [self] * 3, [MinBtn, MaxBtn, CloseBtn])
        self.updateSize = lambda: self.setFixedSize(*list(map(self.parentattr, ['menubtn_w', 'title_h'])))
        self.updateSize()
        self.setFocusPolicy(Qt.NoFocus)
        self.bgclr = Qt.transparent
    def paintEvent(self, *a):
        self.updateSize()
        w, h = self.width(), self.height()
        parent = self.parent
        dpi, realdpi = parent.dpi(), parent.realdpi()
        isdarktheme = parent.isDarkTheme()
        isactivewindow = parent.hwnd() == user32.GetForegroundWindow()
        ISMAXIMIZED = user32.IsZoomed(parent.hwnd())
        resizable_h, resizable_v = map(self.parentattr, ['resizable_h', 'resizable_v'])
        resizable_hv = resizable_h and resizable_v
        painter, path = QPainter(self), QPainterPath()
        painter.setBrush(self.bgclr)
        painter.setPen(Qt.NoPen)
        painter.drawRect(self.rect())
        painter.setBrush(Qt.NoBrush)
        isdisabledmaxbtn = self.ismaxbtn and not (resizable_h or resizable_v)
        pen = QPen(self.parentattr('menubtnclr_%s_%s' % ('d' if isdarktheme else 'l', 'ac' if isactivewindow and not isdisabledmaxbtn else 'in')))
        penwidth = int(1.35 * dpi / 96.0)
        pen.setWidth(penwidth)
        painter.setPen(pen)
        f1, f2 = lambda n: int(n * w), lambda n: int(n * h)
        if realdpi >= 143: painter.setRenderHint(QPainter.Antialiasing)
        if self.isminbtn:
            path.moveTo(f1(0.391), f2(0.500))
            path.lineTo(f1(0.609), f2(0.500))
        elif self.ismaxbtn:
            if ISMAXIMIZED:
                path.moveTo(f1(0.402), f2(0.406))
                path.lineTo(f1(0.559), f2(0.406))
                path.lineTo(f1(0.559), f2(0.656))
                path.lineTo(f1(0.402), f2(0.656))
                path.lineTo(f1(0.402), f2(0.406))
                path.moveTo(f1(0.441), f2(0.344))
                path.lineTo(f1(0.598), f2(0.344))
                path.lineTo(f1(0.598), f2(0.594))
            else:
                path.moveTo(f1(0.402), f2(0.344))
                path.lineTo(f1(0.598), f2(0.344))
                path.lineTo(f1(0.598), f2(0.656))
                path.lineTo(f1(0.402), f2(0.656))
                path.lineTo(f1(0.402), f2(0.344))
        elif self.isclosebtn:
            path.moveTo(f1(0.402), f2(0.344))
            path.lineTo(f1(0.598), f2(0.656))
            path.moveTo(f1(0.598), f2(0.344))
            path.lineTo(f1(0.402), f2(0.656))
        painter.drawPath(path)


class MinBtn(MenuBtn): pass
class MaxBtn(MenuBtn): pass
class CloseBtn(MenuBtn): pass


class SystemVBoxLayout(QVBoxLayout):
    def __init__(self, parent):
        super(SystemVBoxLayout, self).__init__()
        self.setContentsMargins(*[0] * 4)
        self.setSpacing(0)


class SystemHBoxLayout(QHBoxLayout):
    def __init__(self, parent):
        super(SystemHBoxLayout, self).__init__()
        self.parent = parent
        self.istitlebarlayout, self.istitleiconlayout = map(isinstance, [self] * 2, [TitleBarLayout, TitleIconLayout])
        self.updateMargin = lambda: self.setContentsMargins(*[parent._CustomizedWindow__titleicon_mgn if self.istitleiconlayout else 0] * 4)
        self.updateMargin()
        self.setSpacing(0)


class TitleBarLayout(SystemHBoxLayout): pass
class TitleIconLayout(SystemHBoxLayout): pass


class SystemLbl(QAbstractButton):
    def __init__(self, parent):
        super(SystemLbl, self).__init__(parent)
        self.parent = parent
        self.parentattr = lambda arg: getattr(parent, '_CustomizedWindow__' + arg)
        self.isbglbl, self.istitlebar, self.isclientarealbl, self.istitletextlbl, self.istitleiconcontainerlbl, self.istitleiconlbl = map(isinstance, [self] * 6, [BgLbl, TitleBar, ClientAreaLbl, TitleTextLbl, TitleIconContainerLbl, TitleIconLbl])
        if self.istitlebar: self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed), self.setFixedHeight(self.parentattr('title_h'))
        elif self.isbglbl or self.isclientarealbl or self.istitletextlbl or self.istitleiconlbl: self.setSizePolicy(*[QSizePolicy.Expanding] * 2)
        elif self.istitleiconcontainerlbl: self.setFixedSize(*[self.parentattr('title_h')] * 2)
        self.setFocusPolicy(Qt.NoFocus)
        self.bgclr = Qt.transparent
        self.draw = True
    def paintEvent(self, *a):
        parent = self.parent
        isdarktheme = parent.isDarkTheme()
        isblurwindow = self.parentattr('isblurwindow')
        isaeroenabled = isAeroEnabled()
        isactivewindow = parent.hwnd() == user32.GetForegroundWindow()
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        bgclr = Qt.transparent
        title_h = self.parentattr('title_h')
        f1 = lambda pen: (painter.setBrush(Qt.NoBrush), painter.setPen(pen))
        if self.isbglbl: bgclr = Qt.transparent if (isblurwindow and isaeroenabled) else QColor(*[58 if isdarktheme else 197] * 3)
        elif self.istitlebar:
            self.setFixedHeight(title_h)
            if isblurwindow:
                if self.draw:
                    bgclr = QLinearGradient(*[0] * 3 + [self.height()])
                    list(map(bgclr.setColorAt, [0, 1], [QColor(*[0 if isdarktheme else 255] * 3 + [107]), QColor(*[0 if isdarktheme else 255] * 3 + [197])]))
                else: bgclr = QColor(*[0 if isdarktheme else 255] * 3 + [127])
            else: bgclr = QColor(*[0 if isdarktheme else 255] * 3)
        elif self.isclientarealbl:
            self.placeClientArea()
            if isblurwindow: bgclr = QColor(*[0 if isdarktheme else 255] * 3 + [127])
            else: bgclr = QColor(*[0 if isdarktheme else 255] * 3)
        elif self.istitletextlbl:
            pen = QPen(self.parentattr('titletextclr_%s_%s' % ('d' if isdarktheme else 'l', 'ac' if isactivewindow else 'in')))
            f1(pen)
            font = QFont(self.parentattr('captionfont'))
            font.setPixelSize(self.parentattr('title_fontsize'))
            painter.setFont(font)
            if self.draw: painter.drawText(self.rect(), Qt.AlignVCenter, parent.windowTitle())
        elif self.istitleiconcontainerlbl:
            self.setFixedSize(*[title_h] * 2)
        elif self.istitleiconlbl:
            pixmap = parent.windowIcon().pixmap(self.width(), self.height())
            if self.draw: painter.drawPixmap(0, 0, pixmap)
        painter.setBrush(bgclr)
        painter.setPen(Qt.NoPen)
        painter.drawRect(self.rect())
        if self.istitlebar or self.isclientarealbl:
            pen = QPen(QColor(*[96 if isdarktheme else 159] * 3))
            grey_bd_w = int(3 * parent.dpi() / 96.0)
            pen.setWidth(grey_bd_w)
            f1(pen)
            painter.drawRect(0, -grey_bd_w if self.isclientarealbl else 0, self.width(), self.height() + grey_bd_w * (2 if self.istitlebar else 1))
    def placeClientArea(self):
        parent = self.parent
        border_w = self.parentattr('border_w')
        title_h = self.parentattr('title_h')
        ISMAXIMIZED = user32.IsZoomed(parent.hwnd())
        parent.clientArea.setGeometry(QRect(*[0, 0, parent.width(), parent.height() - title_h] if ISMAXIMIZED else [border_w, 0, parent.width() - border_w * 2, parent.height() - border_w - title_h]))


class BgLbl(SystemLbl): pass
class TitleBar(SystemLbl): pass
class ClientAreaLbl(SystemLbl): pass
class TitleTextLbl(SystemLbl): pass
class TitleIconContainerLbl(SystemLbl): pass
class TitleIconLbl(SystemLbl): pass


def isAeroEnabled():
    try:
        pfEnabled = ctypes.c_ulong()
        ctypes.windll.dwmapi.DwmIsCompositionEnabled(ctypes.byref(pfEnabled))
        return pfEnabled.value
    except: return 0


def isdarktheme():
    try: value = winreg.QueryValueEx(winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'Software\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize'), 'AppsUseLightTheme')[0]
    except: return False
    return False if value else True


def gethwnd(window):
    hwnd = window.winId()
    if type(hwnd) != int:
        try:
            f = ctypes.pythonapi.PyCapsule_GetPointer
            f.restype, f.argtypes = ctypes.c_void_p, [ctypes.py_object, ctypes.c_char_p]
            hwnd = f(hwnd, None)
        except ValueError:
            f = ctypes.pythonapi.PyCObject_AsVoidPtr
            f.restype, f.argtypes = ctypes.c_void_p, [ctypes.py_object]
            hwnd = f(hwnd)
    return hwnd


def getdpiforwindow(hwnd):
    dpi = 96
    try:
        dpi_x, dpi_y = [ctypes.c_ulong()] * 2
        monitor_h = user32.MonitorFromWindow(hwnd, 2)
        ctypes.windll.shcore.GetDpiForMonitor(monitor_h, 0, ctypes.byref(dpi_x), ctypes.byref(dpi_y))
        dpi = dpi_x.value
    except:
        dpiaware = user32.IsProcessDPIAware() if hasattr(user32, 'IsProcessDPIAware') else True
        if dpiaware:
            hDC = user32.GetDC(None)
            dpi = ctypes.windll.gdi32.GetDeviceCaps(hDC, 88)
            user32.ReleaseDC(None, hDC)
    return dpi


def getautohidetbpos():
    SPI_GETWORKAREA = 0x30
    priscrc = RECT()
    prisc_w, prisc_h = map(user32.GetSystemMetrics, [0, 1])
    priscrc.left, priscrc.top, priscrc.right, priscrc.bottom = 0, 0, prisc_w, prisc_h
    tb_hwnd = user32.FindWindowA(b'Shell_TrayWnd', None)
    if not tb_hwnd: return 4
    tb_rc = RECT()
    user32.GetWindowRect(tb_hwnd, ctypes.byref(tb_rc))
    tb_l, tb_t, tb_r, tb_b, sc_l, sc_t, sc_r, sc_b = [getattr(tb_rc, i[0]) for i in tb_rc._fields_] + [getattr(priscrc, i[0]) for i in priscrc._fields_]
    if tb_l < sc_l and tb_t == sc_t and tb_r != sc_r and tb_b == sc_b: return 0
    elif tb_l == sc_l and tb_t < sc_t and tb_r == sc_r and tb_b != sc_b: return 1
    elif tb_l != sc_l and tb_t == sc_t and tb_r > sc_r and tb_b == sc_b: return 2
    elif tb_l == sc_l and tb_t != sc_t and tb_r == sc_r and tb_b > sc_b: return 3
    else: return 4


def setwin11blur(hWnd):
    ENTRY_21H2, ENTRY_22H2, VALUE_21H2, VALUE_22H2 = 1029, 38, 1, 3
    return list(map(ctypes.windll.dwmapi.DwmSetWindowAttribute, [hWnd] * 2, [ENTRY_21H2, ENTRY_22H2], [ctypes.byref(ctypes.c_long(VALUE_21H2)), ctypes.byref(ctypes.c_long(VALUE_22H2))], [ctypes.sizeof(ctypes.c_long)] * 2))


def getcaptionfont():
    res = NONCLIENTMETRICS()
    res.cbSize = ctypes.sizeof(NONCLIENTMETRICS)
    user32.SystemParametersInfoW(0x29, ctypes.sizeof(NONCLIENTMETRICS), ctypes.byref(res), 0)
    return res.lfCaptionFont.lfFaceName


class SplashScreen(QSplashScreen):
    def __init__(self, parent):
        super(SplashScreen, self).__init__()
        self.__hwnd = gethwnd(self)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        dpi = parent.dpi()
        sc = QApplication.screens()[0].size() if hasattr(QApplication, 'screens') else QDesktopWidget().screenGeometry(0)
        f1 = lambda n: int(n * dpi / 96.0)
        f2 = lambda obj1, obj2: [(obj1.width() - obj2.width()) // 2, (obj1.height() - obj2.height()) // 2]
        self.resize(*[f1(500)] * 2)
        self.move(*f2(sc, self))
        self.mainlbl = QLabel(self)
        bgclr = 'rgba(0, 0, 0, 179)' if parent.isDarkTheme() else 'rgba(255, 255, 255, 179)'
        shadowcolour, bordercolour = '#7F7F7F', 'rgba(127, 127, 127, 79)'
        self.mainlbl.setStyleSheet('background: %s; border-radius: %dpx; border: %dpx solid %s' % (bgclr, f1(20), f1(2), bordercolour))
        self.mainlbl.resize(self.width() - f1(50), self.height() - f1(50))
        self.mainlbl.move(*f2(self, self.mainlbl))
        self.iconlbl = QLabel(self)
        iconsize = [f1(150)] * 2
        pixmap = QPixmap.fromImage(parent.windowIcon().pixmap(*iconsize).toImage()).scaled(*iconsize)
        self.iconlbl.setPixmap(pixmap)
        self.iconlbl.resize(*iconsize)
        self.iconlbl.move(*f2(self, self.iconlbl))
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(f1(50))
        shadow.setColor(shadowcolour)
        shadow.setOffset(0, 0)
        self.mainlbl.setGraphicsEffect(shadow)


class CustomizedWindow(QWidget):
    '''A customized window based on PySideX.'''
    def __init__(self):
        super(CustomizedWindow, self).__init__()
        self.__hwnd = gethwnd(self)
        hwnd = self.hwnd()
        self.__isblurwindow = isinstance(self, BlurWindow)
        self.setAttribute(Qt.WA_TranslucentBackground, True) if ISPYSIDE1 else self.setStyleSheet('CustomizedWindow{background: rgba(0, 0, 0, 0)}')
        self.__resizable_h, self.__resizable_v = [True] * 2
        SWP_NOSIZE, SWP_NOMOVE, SWP_NOZORDER, SWP_FRAMECHANGED, SWP_NOSENDCHANGING = 0x1, 0x2, 0x4, 0x20, 0x400
        self.__updatencarea = lambda: user32.SetWindowPos(hwnd, None, 0, 0, 0, 0, SWP_NOSIZE | SWP_NOMOVE | SWP_NOZORDER | SWP_FRAMECHANGED | SWP_NOSENDCHANGING)
        self.__SWL = getattr(user32, 'SetWindowLongPtrW' if hasattr(user32, 'SetWindowLongPtrW') else 'SetWindowLongW')
        self.__defaultSWL = lambda: self.__SWL(hwnd, -16, 0xc00000 | 0x40000 | 0x20000 | (0x10000 if (self.__resizable_h or self.__resizable_v) else 0))
        self.__WNDPROC = ctypes.WINFUNCTYPE(ctypes.c_long, ctypes.c_long, ctypes.c_ulong, ctypes.c_long, ctypes.c_long)
        self.__BasicMHAddr = ctypes.cast(self.__WNDPROC(self.__BasicMH), ctypes.c_void_p)
        if hasattr(user32, 'GetWindowLongPtrW'): self.__orig_BasicMH = user32.GetWindowLongPtrW(hwnd, -4)
        else: self.__orig_BasicMH = user32.GetWindowLongW(hwnd, -4)
        self.__handle_setWindowFlags()
        if isAeroEnabled(): self.__setDWMEffect(self.__isblurwindow)
        self.__realdpi = getdpiforwindow(hwnd)
        self.__hdpisfroundingpolicy = 3
        self.__hdpiscalingenabled = hasattr(Qt, 'AA_EnableHighDpiScaling') and QApplication.testAttribute(Qt.AA_EnableHighDpiScaling)
        if hasattr(Qt, 'HighDpiScaleFactorRoundingPolicy'):
            QHDSFRP = Qt.HighDpiScaleFactorRoundingPolicy
            QADSFRP = QApplication.highDpiScaleFactorRoundingPolicy()
            policy_dict = {QHDSFRP.Ceil: 1, QHDSFRP.Floor: 2, QHDSFRP.PassThrough: 3, QHDSFRP.Round: 4, QHDSFRP.RoundPreferFloor: 5}
            if hasattr(QHDSFRP, 'Unset'): self.__hdpisfroundingpolicy = 3 if QADSFRP == QHDSFRP.Unset else policy_dict[QADSFRP]
            else: self.__hdpisfroundingpolicy = policy_dict[QADSFRP]
        dpi = self.dpi()
        self.__maximizedmgn_list = self.__getMaximizedMargin()
        self.__themeclr = 0
        self.__isdarktheme = isdarktheme()
        self.__titletextclr_l_ac, self.__titletextclr_d_ac, self.__titletextclr_l_in, self.__titletextclr_d_in, self.__menubtnclr_l_ac, self.__menubtnclr_d_ac, self.__menubtnclr_l_in, self.__menubtnclr_d_in = [Qt.black, Qt.white, QColor(*[99] * 3), QColor(*[155] * 3)] * 2
        self.__updatedpiconstants()
        self.__updateautohidetbwidth()
        self.__inminbtn, self.__inmaxbtn, self.__inclosebtn, self.__intitlebar, self.__inborder_t, self.__inborder_l, self.__inborder_b, self.__inborder_r = [False] * 8
        self.__captionfont = getcaptionfont()
        self.__mgn_l, self.__mgn_r, self.__mgn_t, self.__mgn_b = [0] * 4
        self.__bgLbl = BgLbl(self)
        self.__mainLayout = SystemVBoxLayout(self)
        self.setLayout(self.__mainLayout)
        self.__mainLayout.addWidget(self.__bgLbl)
        self.__bgLayout = SystemVBoxLayout(self)
        self.__bgLbl.setLayout(self.__bgLayout)
        self.__titleBar = TitleBar(self)
        self.__titleBarLayout = TitleBarLayout(self)
        self.__titleBar.setLayout(self.__titleBarLayout)
        self.__clientAreaLbl = ClientAreaLbl(self)
        self.clientArea = QWidget(self.__clientAreaLbl)
        self.__titleIconLayout = TitleIconLayout(self)
        self.__titleIconContainerLbl = TitleIconContainerLbl(self)
        self.__titleIconContainerLbl.setLayout(self.__titleIconLayout)
        self.__titleIconLbl = TitleIconLbl(self)
        self.__titleIconLayout.addWidget(self.__titleIconLbl)
        self.__titleTextLbl = TitleTextLbl(self)
        self.__minBtn, self.__maxBtn, self.__closeBtn = MinBtn(self), MaxBtn(self), CloseBtn(self)
        list(map(self.__bgLayout.addWidget, [self.__titleBar, self.__clientAreaLbl]))
        list(map(self.__titleBarLayout.addWidget, [self.__titleIconContainerLbl, self.__titleTextLbl, self.__minBtn, self.__maxBtn, self.__closeBtn]))
        self.setDarkTheme(0)
        self.__orig_setWindowTitle, self.setWindowTitle = self.setWindowTitle, self.__setWindowTitle
        self.__orig_setWindowIcon, self.setWindowIcon = self.setWindowIcon, self.__setWindowIcon
        self.__orig_setFixedSize, self.setFixedSize = self.setFixedSize, self.__setFixedSize
        self.__orig_setFixedWidth, self.setFixedWidth = self.setFixedWidth, self.__setFixedWidth
        self.__orig_setFixedHeight, self.setFixedHeight = self.setFixedHeight, self.__setFixedHeight
        if not ISPYSIDE1: self.windowHandle().screenChanged.connect(self.__updatencarea)
    def dpi(self):
        '''DPI divided by 96.0 is the scale factor of PySideX UI.
Example:
DPI = window.dpi()
window.resize(int(400.0 * DPI / 96.0), int(175.0 * DPI / 96.0))'''
        return self.__getdpibyrealdpi(self.realdpi())
    def realdpi(self):
        '''REALDPI divided by 96.0 is the scale factor of System UI.'''
        return self.__realdpi
    def hwnd(self):
        '''HWND is the window handle of this window.'''
        return self.__hwnd
    def isDarkTheme(self):
        '''Detect whether dark theme is enabled or not.
You can use 'setDarkTheme' to change setting.'''
        return self.__isdarktheme
    def setDarkTheme(self, themecolour=0):
        '''themecolour=0: Auto; themecolour=1: Light; themecolour=2: Dark'''
        self.__themeclr = themecolour
        try: self.__isdarktheme = {0: isdarktheme(), 1: False, 2: True}[themecolour]
        except:
            ErrorType = ValueError if type(themeclr) == int else TypeError
            raise ErrorType('Parameter themeclr must be 0, 1 or 2.')
        self.__minBtn.update()
        self.__maxBtn.update()
        self.__closeBtn.update()
        self.__titleBar.update()
        self.__clientAreaLbl.update()
        SWP_NOSIZE, SWP_NOMOVE, SWP_NOZORDER = 0x1, 0x2, 0x4
        hwnd = self.hwnd()
        try: list(map(ctypes.windll.dwmapi.DwmSetWindowAttribute, [hwnd] * 2, [19, 20], [ctypes.byref(ctypes.c_long(self.isDarkTheme()))] * 2, [ctypes.sizeof(ctypes.c_long(self.isDarkTheme()))] * 2))
        except: pass
        user32.SetWindowPos(hwnd, None, 0, 0, 0, 0, SWP_NOSIZE | SWP_NOMOVE | SWP_NOZORDER)
    def isAeroEnabled(self):
        '''Detect whether Aero is enabled or not.'''
        return isAeroEnabled()
    def setTitleTextColour(self, colour, theme=0, state=0):
        '''colour=0: Default; colour=Qt....: Qt.GlobalColor; colour=QColor(...): QColor
theme=0: Auto; theme=1: Light; theme=2: Dark
state=0: All; state=1: Active; state=2: Inactive'''
        if theme not in [0, 1, 2]:
            ErrorType = ValueError if type(theme) == int else TypeError
            raise ErrorType('Parameter theme must be 0, 1 or 2.')
        if state not in [0, 1, 2]:
            ErrorType = ValueError if type(state) == int else TypeError
            raise ErrorType('Parameter state must be 0, 1 or 2.')
        setlightclr, setdarkclr = theme in [0, 1], theme in [0, 2]
        setactiveclr, setinactiveclr = state in [0, 1], state in [0, 2]
        clr_l_ac, clr_d_ac, clr_l_in, clr_d_in = self.__titletextclr_l_ac, self.__titletextclr_d_ac, self.__titletextclr_l_in, self.__titletextclr_d_in
        if colour == 0:
            if setlightclr:
                if setactiveclr: clr_l_ac = Qt.black
                if setinactiveclr: clr_l_in = QColor(*[99] * 3)
            if setdarkclr:
                if setactiveclr: clr_d_ac = Qt.white
                if setinactiveclr: clr_d_in = QColor(*[155] * 3)
        elif type(colour) in [Qt.GlobalColor, QColor]:
            if setlightclr:
                if setactiveclr: clr_l_ac = colour
                if setinactiveclr: clr_l_in = colour
            if setdarkclr:
                if setactiveclr: clr_d_ac = colour
                if setinactiveclr: clr_d_in = colour
        else:
            ErrorType = ValueError if type(colour) == int else TypeError
            raise ErrorType('Parameter colour must be 0, %s or %s.' % (Qt.GlobalColor, QColor))
        self.__titletextclr_l_ac, self.__titletextclr_d_ac, self.__titletextclr_l_in, self.__titletextclr_d_in = clr_l_ac, clr_d_ac, clr_l_in, clr_d_in
        self.__titleTextLbl.update()
    def setMenuButtonColour(self, colour, theme=0, state=0):
        '''colour=0: Default; colour=Qt....: Qt.GlobalColor; colour=QColor(...): QColor
theme=0: Auto; theme=1: Light; theme=2: Dark
state=0: All; state=1: Active; state=2: Inactive'''
        if theme not in [0, 1, 2]:
            ErrorType = ValueError if type(theme) == int else TypeError
            raise ErrorType('Parameter theme must be 0, 1 or 2.')
        if state not in [0, 1, 2]:
            ErrorType = ValueError if type(state) == int else TypeError
            raise ErrorType('Parameter state must be 0, 1 or 2.')
        setlightclr, setdarkclr = theme in [0, 1], theme in [0, 2]
        setactiveclr, setinactiveclr = state in [0, 1], state in [0, 2]
        clr_l_ac, clr_d_ac, clr_l_in, clr_d_in = self.__menubtnclr_l_ac, self.__menubtnclr_d_ac, self.__menubtnclr_l_in, self.__menubtnclr_d_in
        if colour == 0:
            if setlightclr:
                if setactiveclr: clr_l_ac = Qt.black
                if setinactiveclr: clr_l_in = QColor(*[99] * 3)
            if setdarkclr:
                if setactiveclr: clr_d_ac = Qt.white
                if setinactiveclr: clr_d_in = QColor(*[155] * 3)
        elif type(colour) in [Qt.GlobalColor, QColor]:
            if setlightclr:
                if setactiveclr: clr_l_ac = colour
                if setinactiveclr: clr_l_in = colour
            if setdarkclr:
                if setactiveclr: clr_d_ac = colour
                if setinactiveclr: clr_d_in = colour
        else:
            ErrorType = ValueError if type(colour) == int else TypeError
            raise ErrorType('Parameter colour must be 0, %s or %s.' % (Qt.GlobalColor, QColor))
        self.__menubtnclr_l_ac, self.__menubtnclr_d_ac, self.__menubtnclr_l_in, self.__menubtnclr_d_in = clr_l_ac, clr_d_ac, clr_l_in, clr_d_in
        self.__minBtn.update()
        self.__maxBtn.update()
        self.__closeBtn.update()
    def __setWindowTitle(self, arg__1):
        self.__orig_setWindowTitle(arg__1)
        self.__titleTextLbl.update()
    def __setWindowIcon(self, icon):
        self.__orig_setWindowIcon(icon)
        self.__titleIconLbl.update()
    def __setFixedSize(self, *a, **kwa):
        self.__orig_setFixedSize(*a, **kwa)
        self.__resizable_h, self.__resizable_v = [False] * 2
        self.__defaultSWL()
    def __setFixedWidth(self, *a, **kwa):
        self.__orig_setFixedWidth(*a, **kwa)
        self.__resizable_h = False
        self.__defaultSWL()
    def __setFixedHeight(self, *a, **kwa):
        self.__orig_setFixedHeight(*a, **kwa)
        self.__resizable_v = False
        self.__defaultSWL()
    def setWindowFlag(self, arg__1, on=True):
        raise AttributeError('Function setWindowFlag has been deleted.')
    def setWindowFlags(self, type):
        raise AttributeError('Function setWindowFlags has been deleted.')
    def __handle_setWindowFlags(self):
        if ISPYSIDE1: self.__SWL(self.hwnd(), -4, self.__orig_BasicMH)
        self.__hwnd = gethwnd(self)
        BasicMHAddr = self.__BasicMHAddr
        if hasattr(user32, 'GetWindowLongPtrW'): self.__orig_BasicMH = user32.GetWindowLongPtrW(self.hwnd(), -4)
        else: self.__orig_BasicMH = user32.GetWindowLongW(self.hwnd(), -4)
        self.__orig_BasicMHFunc = self.__WNDPROC(self.__orig_BasicMH)
        self.__ncsizeinited = False
        if ISPYSIDE1:
            self.__SWL(self.hwnd(), -4, BasicMHAddr.value)
            ctypes.cdll.msvcrt._aligned_free(BasicMHAddr.value)
        self.__defaultSWL()
        if isAeroEnabled(): self.__setDWMEffect(self.__isblurwindow)
    def __setMBS(self, button, state=1):
        bgclr1, bgclr2, bgclr3 = [Qt.transparent] * 3
        if button == 1:
            if state == 1: bgclr1 = QColor(*[255 if self.isDarkTheme() else 0] * 3 + [25])
            elif state == 2: bgclr1 = QColor(*[255 if self.isDarkTheme() else 0] * 3 + [50])
        elif button == 2:
            if state == 1: bgclr2 = QColor(*[255 if self.isDarkTheme() else 0] * 3 + [25])
            elif state == 2: bgclr2 = QColor(*[255 if self.isDarkTheme() else 0] * 3 + [50])
        elif button == 3:
            if state == 1: bgclr3 = QColor(255, 0, 0, 199)
            elif state == 2: bgclr3 = QColor(255, 0, 0, 99)
        self.__minBtn.bgclr, self.__maxBtn.bgclr, self.__closeBtn.bgclr = bgclr1, bgclr2, bgclr3
        self.__titleTextLbl.update()
        self.__minBtn.update()
        self.__maxBtn.update()
        self.__closeBtn.update()
    def MessageHandler(self, hwnd, message, wParam, lParam):
        '''Example:
class MyOwnWindow(BlurWindow):
|->|...
|->|def MessageHandler(self, hwnd, message, wParam, lParam):
|->||->|print(hwnd, message, wParam, lParam)
|->||->|...'''
        pass
    def __BasicMH(self, hwnd, message, wParam, lParam):
        WM_SHOWWINDOW, WM_SETTINGCHANGE, WM_STYLECHANGED, WM_NCCALCSIZE, WM_NCHITTEST, WM_NCLBUTTONDOWN, WM_NCLBUTTONUP, WM_SYSCOMMAND, WM_LBUTTONUP, WM_DPICHANGED, WM_DWMCOMPOSITIONCHANGED = 0x18, 0x1a, 0x7d, 0x83, 0x84, 0xa1, 0xa2, 0x112, 0x2a2, 0x2e0, 0x31e
        SC_SIZE, SC_MOVE, SC_MINIMIZE, SC_MAXIMIZE, SC_CLOSE, SC_RESTORE = 0xf000, 0xf010, 0xf020, 0xf030, 0xf060, 0xf120
        HTCLIENT, HTCAPTION, HTMINBUTTON, HTMAXBUTTON, HTCLOSE = 0x1, 0x2, 0x8, 0x9, 0x14
        HTLEFT, HTRIGHT, HTTOP, HTTOPLEFT, HTTOPRIGHT, HTBOTTOM, HTBOTTOMLEFT, HTBOTTOMRIGHT, HTBORDER = list(range(0xa, 0x13))
        SPI_SETNONCLIENTMETRICS, SPI_SETWORKAREA = 0x2a, 0x2f
        try:
            dpi, realdpi = self.dpi(), self.realdpi()
            real_border_w = self.__real_border_w
            real_title_h = self.__real_title_h
            real_menubtn_w = self.__real_menubtn_w
            mgn_l, mgn_r, mgn_t, mgn_b = self.__mgn_l, self.__mgn_r, self.__mgn_t, self.__mgn_b
            resizable_h, resizable_v = self.__resizable_h, self.__resizable_v
            resizable_hv = resizable_h and resizable_v
        except: dpi, realdpi, real_border_w, real_title_h, real_menubtn_w, mgn_l, mgn_r, mgn_t, mgn_b, resizable_h, resizable_v, resizable_hv = [96] * 2 + [0] * 7 + [True] * 3
        windowrc = RECT()
        user32.GetWindowRect(hwnd, ctypes.byref(windowrc))
        windowx, windowy = windowrc.left, windowrc.top
        globalpos = POINT()
        try:
            user32.GetPhysicalCursorPos(ctypes.byref(globalpos))
            user32.PhysicalToLogicalPoint(self.hwnd(), ctypes.byref(globalpos))
        except: user32.GetCursorPos(ctypes.byref(globalpos))
        x, y = globalpos.x - windowx, globalpos.y - windowy
        w, h = windowrc.right - windowx, windowrc.bottom - windowy
        intitlebar = mgn_t <= y < real_title_h + mgn_t
        inminbtn = w - mgn_l - 3 * real_menubtn_w <= x < w - mgn_l - 2 * real_menubtn_w and intitlebar
        inmaxbtn = w - mgn_l - 2 * real_menubtn_w <= x < w - mgn_l - real_menubtn_w and intitlebar
        inclosebtn = w - mgn_l - real_menubtn_w <= x < w - mgn_l and intitlebar
        inborder_t, inborder_l, inborder_b, inborder_r = y <= real_border_w, x <= real_border_w, h - y <= real_border_w, w - x <= real_border_w
        self.__inminbtn, self.__inmaxbtn, self.__inclosebtn, self.__intitlebar, self.__inborder_t, self.__inborder_l, self.__inborder_b, self.__inborder_r = inminbtn, inmaxbtn, inclosebtn, intitlebar, inborder_t, inborder_l, inborder_b, inborder_r
        if message == WM_NCCALCSIZE:
            rc = ctypes.cast(lParam, ctypes.POINTER(NCCALCSIZE_PARAMS)).contents.rgrc[0] if wParam else ctypes.cast(lParam, ctypes.POINTER(RECT)).contents
            ISMAXIMIZED = user32.IsZoomed(hwnd)
            try: maximizedmgn_list = self.__maximizedmgn_list
            except: maximizedmgn_list = [0] * 2
            self.__mgn_l, self.__mgn_r, self.__mgn_t, self.__mgn_b = [0] * 4
            if ISMAXIMIZED:
                try:
                    f2 = lambda i, s: maximizedmgn_list[i] + getattr(self, '_CustomizedWindow__autohidetbwidth_' + s)
                    self.__mgn_l, self.__mgn_r, self.__mgn_t, self.__mgn_b = map(f2, [0] * 2 + [1] * 2, ['l', 'r', 't', 'b'])
                except: pass
            rc.left += self.__mgn_l
            rc.right -= self.__mgn_r
            rc.top += self.__mgn_t
            rc.bottom -= self.__mgn_b
            if hasattr(self, '_CustomizedWindow__ncsizeinited'):
                __ncsizeinited = self.__ncsizeinited
                if not __ncsizeinited:
                    self.__ncsizeinited = True
                else: return 0
            else: return 0
        if message == WM_NCHITTEST:
            VK_LBUTTON = 0x1
            islbuttonpressed = user32.GetKeyState(VK_LBUTTON) not in [0, 1]
            if not (self.isMaximized() or not (resizable_h or resizable_v)):
                if resizable_hv:
                    if inborder_t and inborder_l: res = HTTOPLEFT
                    elif inborder_t and inborder_r: res = HTTOPRIGHT
                    elif inborder_b and inborder_l: res = HTBOTTOMLEFT
                    elif inborder_b and inborder_r: res = HTBOTTOMRIGHT
                if not 'res' in dir():
                    if resizable_h:
                        if inborder_l: res = HTLEFT
                        elif inborder_r: res = HTRIGHT
                    if resizable_v:
                        if inborder_t: res = HTTOP
                        elif inborder_b: res = HTBOTTOM
            if not 'res' in dir():
                if inminbtn:
                    if not islbuttonpressed: self.__setMBS(1, 1)
                    res = HTMINBUTTON
                elif inmaxbtn:
                    if resizable_h or resizable_v:
                        if not islbuttonpressed: self.__setMBS(2, 1)
                        res = HTMAXBUTTON
                    else: res = HTBORDER
                elif inclosebtn:
                    if not islbuttonpressed: self.__setMBS(3, 1)
                    res = HTCLOSE
                elif intitlebar: res = HTCAPTION
                else: res = HTCLIENT
            if not 'res' in dir() and not (self.isMaximized() or resizable_h or resizable_v):
                if inborder_t or inborder_l or inborder_b or inborder_r: res = HTBORDER
            if res not in [HTMINBUTTON, HTMAXBUTTON, HTCLOSE]:
                if not islbuttonpressed: self.__setMBS(0)
            return res
        if message == WM_SHOWWINDOW:
            self.__updatencarea()
        if message == WM_NCLBUTTONDOWN:
            if wParam in [HTMINBUTTON, HTMAXBUTTON, HTCLOSE]:
                if wParam == HTMINBUTTON: self.__setMBS(1, 2)
                if wParam == HTMAXBUTTON: self.__setMBS(2, 2)
                if wParam == HTCLOSE: self.__setMBS(3, 2)
                return 0
        if message == WM_NCLBUTTONUP:
            self.__setMBS(0)
            PM = lambda arg: user32.PostMessageW(hwnd, WM_SYSCOMMAND, arg, 0)
            if wParam == HTMINBUTTON: PM(SC_MINIMIZE)
            elif wParam == HTMAXBUTTON:
                if self.isMaximized(): PM(SC_RESTORE)
                elif self.isFullScreen(): pass
                else: PM(SC_MAXIMIZE)
            elif wParam == HTCLOSE: PM(SC_CLOSE)
        if message == WM_LBUTTONUP:
            self.__setMBS(0)
        if message == WM_DPICHANGED:
            rc = RECT.from_address(lParam)
            realdpi = wParam >> 16
            self.__realdpi = realdpi
            self.__maximizedmgn_list = self.__getMaximizedMargin()
            if not self.__hdpiscalingenabled:
                if not resizable_h: self.__orig_setFixedWidth(rc.right - rc.left)
                if not resizable_v: self.__orig_setFixedHeight(rc.bottom - rc.top)
                SWP_NOZORDER = 0x4
                user32.SetWindowPos(hwnd, rc.left, rc.top, rc.right - rc.left, rc.bottom - rc.top, SWP_NOZORDER)
            self.__updatedpiconstants()
            self.__minBtn.update()
            self.__maxBtn.update()
            self.__closeBtn.update()
            self.__titleTextLbl.update()
            self.__titleIconLayout.updateMargin()
            self.__titleIconLbl.update()
            self.__clientAreaLbl.update()
            self.__updatencarea()
        if message == WM_SETTINGCHANGE:
            lParam_string = ctypes.c_wchar_p(lParam).value
            if wParam == SPI_SETWORKAREA:
                self.__updateautohidetbwidth()
                self.__updatencarea()
            if wParam == SPI_SETNONCLIENTMETRICS:
                self.__maximizedmgn_list = self.__getMaximizedMargin()
                self.__captionfont = getcaptionfont()
                self.__titleTextLbl.update()
            if self.__themeclr == 0 and lParam_string == 'ImmersiveColorSet': self.setDarkTheme(0)
        if message == WM_DWMCOMPOSITIONCHANGED:
            if isAeroEnabled(): self.__setDWMEffect(self.__isblurwindow)
            self.__bgLbl.update()
        if message == WM_STYLECHANGED:
            if hasattr(self, '_CustomizedWindow__ncsizeinited') and self.__ncsizeinited: self.__defaultSWL()
        messagehandlerres = self.MessageHandler(hwnd, message, wParam, lParam)
        if messagehandlerres is not None: return messagehandlerres
        if ISPYSIDE1: return self.__orig_BasicMHFunc(hwnd, message, wParam, lParam)
    def __getMaximizedMargin(self):
        SM_CXSIZEFRAME, SM_CYSIZEFRAME, SM_CXPADDEDBORDER = 32, 33, 92
        realdpi = self.realdpi()
        above14393 = hasattr(user32, 'GetSystemMetricsForDpi')
        Func = user32.GetSystemMetricsForDpi if above14393 else user32.GetSystemMetrics
        args = [Func, [SM_CXSIZEFRAME, SM_CXPADDEDBORDER, SM_CYSIZEFRAME, SM_CXPADDEDBORDER]]
        if above14393: args.append([realdpi] * 4)
        res = list(map(*args))
        return [sum(res[0:2]), sum(res[2:4])]
    def nativeEvent(self, eventType, msg):
        '''For PySide2/6, you should define MessageHandler instead of nativeEvent.'''
        _msg = MSG.from_address(msg.__int__())
        hwnd, message, wP, lP = _msg.hWnd, _msg.message, _msg.wParam, _msg.lParam
        basicmhres = self.__BasicMH(hwnd, message, wP, lP)
        if basicmhres is not None: return True, basicmhres
        return super(CustomizedWindow, self).nativeEvent(eventType, msg)
    def __setDWMEffect(self, blur=False, isEnableShadow=False):
        hwnd = self.hwnd()
        try:
            dwmapi = ctypes.windll.dwmapi
            dwmapi.DwmSetWindowAttribute(hwnd, 2, ctypes.byref(ctypes.c_long(2)), ctypes.sizeof(ctypes.c_long(2)))
            f1 = lambda l, r, t, b: dwmapi.DwmExtendFrameIntoClientArea(hwnd, ctypes.byref(MARGINS(l, r, t, b)))
            if blur:
                bb = DWM_BLURBEHIND()
                bb.dwFlags = 1
                bb.fEnable = 1
                w11_21h2_blur_code, w11_22h2_blur_code = setwin11blur(hwnd)
                if w11_22h2_blur_code:
                    f1(1, 1, 0, 0)
                    dwmapi.DwmEnableBlurBehindWindow(ctypes.c_long(hwnd), ctypes.byref(bb))
                else:
                    f1(*[-1] * 4)
                    return 3
                try:
                    AeroEffect = Win10BlurEffect()
                    w10_blur_code = AeroEffect.setAeroEffect(hwnd, isEnableShadow=isEnableShadow)
                    if w10_blur_code != 0: return 2
                except: pass
            else: f1(1, 1, 0, 0)
            return 1
        except: return 0
    def __getdpibyrealdpi(self, realdpi):
        realsf = realdpi / 96.0
        policy = self.__hdpisfroundingpolicy
        if self.__hdpiscalingenabled:
            sf = realsf
            if policy == 1: sf = int(realsf + 1 if realsf - int(realsf) > 0 else realsf)
            elif policy == 2: sf = int(realsf)
            elif policy == 4: sf = int(realsf + 1 if realsf - int(realsf) >= 0.5 else realsf)
            elif policy == 5: sf = int(realsf + 1 if realsf - int(realsf) > 0.5 else realsf)
            dpi = int(float(realdpi) / sf)
        else: dpi = realdpi
        return dpi
    def __updatedpiconstants(self):
        dpi, realdpi = self.dpi(), self.realdpi()
        f1, f2 = lambda n: int(n * dpi / 96.0), lambda n: int(n * realdpi / 96.0)
        self.__border_w, self.__real_border_w = f1(4), f2(4)
        self.__title_h, self.__real_title_h = f1(30), f2(30)
        self.__menubtn_w, self.__real_menubtn_w = f1(46), f2(46)
        self.__title_fontsize = f1(13)
        self.__titleicon_mgn = f1(7)
    def __updateautohidetbwidth(self):
        pos = getautohidetbpos()
        self.__autohidetbwidth_l, self.__autohidetbwidth_t, self.__autohidetbwidth_r, self.__autohidetbwidth_b = [2 if i == pos else 0 for i in range(4)]
    def splashScreen(self):
        '''You should call splashscreen.show after window.setWindowIcon, window.setDarkTheme,
and before window.setGeometry, window.move, window.resize,
call splashscreen.finish after window.show.
Example:
window.setWindowIcon(QIcon('Icon.ico'))
splashscreen = window.splashScreen()
splashscreen.show()
window.resize(int(400.0 * window.dpi() / 96.0), int(175.0 * window.dpi() / 96.0))
...
window.show()
splashscreen.finish(window)'''
        return SplashScreen(self)


class BlurWindow(CustomizedWindow):
    '''A blur window based on PySideX.
Blur effect is avaliable on Windows Vista and newer.'''
    pass


if __name__ == '__main__':
    try:
        QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    except: pass
    app = QApplication(sys.argv)
    window = BlurWindow()
    help(window.MessageHandler)
    clr_list = [[QColor(0, 0, 139), QColor(119, 235, 255)], [1, 2], [1] * 2]
    list(map(*[window.setTitleTextColour] + clr_list))
    help(window.setTitleTextColour)
    list(map(*[window.setMenuButtonColour] + clr_list))
    help(window.setTitleTextColour)
    window.setDarkTheme(0)
    help(window.setDarkTheme)
    window.setWindowIcon(QIcon('Icon.ico'))
    splashscreen = window.splashScreen()
    help(window.splashScreen)
    splashscreen.show()
    window.resize(int(400.0 * window.dpi() / 96.0), int(175.0 * window.dpi() / 96.0))
    window.setWindowTitle('Window')
    btn = QPushButton('Button', window.clientArea)
    btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
    lbl = QLabel('Label', window.clientArea)
    lbl.setStyleSheet('background: rgba(255, 0, 0, 159)')
    lbl.setSizePolicy(*[QSizePolicy.Expanding] * 2)
    mainlayout = QVBoxLayout()
    mainlayout.setContentsMargins(*[0] * 4)
    mainlayout.setSpacing(0)
    window.clientArea.setLayout(mainlayout)
    list(map(mainlayout.addWidget, [btn, lbl]))
    window.show()
    splashscreen.finish(window)
    getattr(app, 'exec')() if hasattr(app, 'exec') else app.exec_()
