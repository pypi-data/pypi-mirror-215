# pylint:disable=line-too-long
import logging

from ...sim_type import SimTypeFunction,     SimTypeShort, SimTypeInt, SimTypeLong, SimTypeLongLong, SimTypeDouble, SimTypeFloat,     SimTypePointer,     SimTypeChar,     SimStruct,     SimTypeFixedSizeArray,     SimTypeBottom,     SimUnion,     SimTypeBool
from ...calling_conventions import SimCCStdcall, SimCCMicrosoftAMD64
from .. import SIM_PROCEDURES as P
from . import SimLibrary


_l = logging.getLogger(name=__name__)


lib = SimLibrary()
lib.set_default_cc('X86', SimCCStdcall)
lib.set_default_cc('AMD64', SimCCMicrosoftAMD64)
lib.set_library_names("icm32.dll")
prototypes = \
    {
        #
        'CMCheckColors': SimTypeFunction([SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0), SimTypePointer(SimUnion({"gray": SimStruct({"gray": SimTypeShort(signed=False, label="UInt16")}, name="GRAYCOLOR", pack=False, align=None), "rgb": SimStruct({"red": SimTypeShort(signed=False, label="UInt16"), "green": SimTypeShort(signed=False, label="UInt16"), "blue": SimTypeShort(signed=False, label="UInt16")}, name="RGBCOLOR", pack=False, align=None), "cmyk": SimStruct({"cyan": SimTypeShort(signed=False, label="UInt16"), "magenta": SimTypeShort(signed=False, label="UInt16"), "yellow": SimTypeShort(signed=False, label="UInt16"), "black": SimTypeShort(signed=False, label="UInt16")}, name="CMYKCOLOR", pack=False, align=None), "XYZ": SimStruct({"X": SimTypeShort(signed=False, label="UInt16"), "Y": SimTypeShort(signed=False, label="UInt16"), "Z": SimTypeShort(signed=False, label="UInt16")}, name="XYZCOLOR", pack=False, align=None), "Yxy": SimStruct({"Y": SimTypeShort(signed=False, label="UInt16"), "x": SimTypeShort(signed=False, label="UInt16"), "y": SimTypeShort(signed=False, label="UInt16")}, name="YxyCOLOR", pack=False, align=None), "Lab": SimStruct({"L": SimTypeShort(signed=False, label="UInt16"), "a": SimTypeShort(signed=False, label="UInt16"), "b": SimTypeShort(signed=False, label="UInt16")}, name="LabCOLOR", pack=False, align=None), "gen3ch": SimStruct({"ch1": SimTypeShort(signed=False, label="UInt16"), "ch2": SimTypeShort(signed=False, label="UInt16"), "ch3": SimTypeShort(signed=False, label="UInt16")}, name="GENERIC3CHANNEL", pack=False, align=None), "named": SimStruct({"dwIndex": SimTypeInt(signed=False, label="UInt32")}, name="NAMEDCOLOR", pack=False, align=None), "hifi": SimStruct({"channel": SimTypeFixedSizeArray(SimTypeChar(label="Byte"), 8)}, name="HiFiCOLOR", pack=False, align=None), "Anonymous": SimStruct({"reserved1": SimTypeInt(signed=False, label="UInt32"), "reserved2": SimTypePointer(SimTypeBottom(label="Void"), offset=0)}, name="_Anonymous_e__Struct", pack=False, align=None)}, name="<anon>", label="None"), label="LPArray", offset=0), SimTypeInt(signed=False, label="UInt32"), SimTypeInt(signed=False, label="COLORTYPE"), SimTypePointer(SimTypeChar(label="Byte"), label="LPArray", offset=0)], SimTypeInt(signed=True, label="Int32"), arg_names=["hcmTransform", "lpaInputColors", "nColors", "ctInput", "lpaResult"]),
        #
        'CMCheckRGBs': SimTypeFunction([SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0), SimTypePointer(SimTypeBottom(label="Void"), offset=0), SimTypeInt(signed=False, label="BMFORMAT"), SimTypeInt(signed=False, label="UInt32"), SimTypeInt(signed=False, label="UInt32"), SimTypeInt(signed=False, label="UInt32"), SimTypePointer(SimTypeChar(label="Byte"), offset=0), SimTypePointer(SimTypeFunction([SimTypeInt(signed=False, label="UInt32"), SimTypeInt(signed=False, label="UInt32"), SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0)], SimTypeInt(signed=True, label="Int32"), arg_names=["param0", "param1", "param2"]), offset=0), SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0)], SimTypeInt(signed=True, label="Int32"), arg_names=["hcmTransform", "lpSrcBits", "bmInput", "dwWidth", "dwHeight", "dwStride", "lpaResult", "pfnCallback", "ulCallbackData"]),
        #
        'CMConvertColorNameToIndex': SimTypeFunction([SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0), SimTypePointer(SimTypePointer(SimTypeChar(label="SByte"), offset=0), label="LPArray", offset=0), SimTypePointer(SimTypeInt(signed=False, label="UInt32"), label="LPArray", offset=0), SimTypeInt(signed=False, label="UInt32")], SimTypeInt(signed=True, label="Int32"), arg_names=["hProfile", "paColorName", "paIndex", "dwCount"]),
        #
        'CMConvertIndexToColorName': SimTypeFunction([SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0), SimTypePointer(SimTypeInt(signed=False, label="UInt32"), label="LPArray", offset=0), SimTypePointer(SimTypePointer(SimTypeChar(label="SByte"), offset=0), label="LPArray", offset=0), SimTypeInt(signed=False, label="UInt32")], SimTypeInt(signed=True, label="Int32"), arg_names=["hProfile", "paIndex", "paColorName", "dwCount"]),
        #
        'CMCreateDeviceLinkProfile': SimTypeFunction([SimTypePointer(SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0), label="LPArray", offset=0), SimTypeInt(signed=False, label="UInt32"), SimTypePointer(SimTypeInt(signed=False, label="UInt32"), label="LPArray", offset=0), SimTypeInt(signed=False, label="UInt32"), SimTypeInt(signed=False, label="UInt32"), SimTypePointer(SimTypePointer(SimTypeChar(label="Byte"), offset=0), offset=0)], SimTypeInt(signed=True, label="Int32"), arg_names=["pahProfiles", "nProfiles", "padwIntents", "nIntents", "dwFlags", "lpProfileData"]),
        #
        'CMCreateMultiProfileTransform': SimTypeFunction([SimTypePointer(SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0), label="LPArray", offset=0), SimTypeInt(signed=False, label="UInt32"), SimTypePointer(SimTypeInt(signed=False, label="UInt32"), label="LPArray", offset=0), SimTypeInt(signed=False, label="UInt32"), SimTypeInt(signed=False, label="UInt32")], SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0), arg_names=["pahProfiles", "nProfiles", "padwIntents", "nIntents", "dwFlags"]),
        #
        'CMCreateProfileW': SimTypeFunction([SimTypePointer(SimStruct({"lcsSignature": SimTypeInt(signed=False, label="UInt32"), "lcsVersion": SimTypeInt(signed=False, label="UInt32"), "lcsSize": SimTypeInt(signed=False, label="UInt32"), "lcsCSType": SimTypeInt(signed=True, label="Int32"), "lcsIntent": SimTypeInt(signed=True, label="Int32"), "lcsEndpoints": SimStruct({"ciexyzRed": SimStruct({"ciexyzX": SimTypeInt(signed=True, label="Int32"), "ciexyzY": SimTypeInt(signed=True, label="Int32"), "ciexyzZ": SimTypeInt(signed=True, label="Int32")}, name="CIEXYZ", pack=False, align=None), "ciexyzGreen": SimStruct({"ciexyzX": SimTypeInt(signed=True, label="Int32"), "ciexyzY": SimTypeInt(signed=True, label="Int32"), "ciexyzZ": SimTypeInt(signed=True, label="Int32")}, name="CIEXYZ", pack=False, align=None), "ciexyzBlue": SimStruct({"ciexyzX": SimTypeInt(signed=True, label="Int32"), "ciexyzY": SimTypeInt(signed=True, label="Int32"), "ciexyzZ": SimTypeInt(signed=True, label="Int32")}, name="CIEXYZ", pack=False, align=None)}, name="CIEXYZTRIPLE", pack=False, align=None), "lcsGammaRed": SimTypeInt(signed=False, label="UInt32"), "lcsGammaGreen": SimTypeInt(signed=False, label="UInt32"), "lcsGammaBlue": SimTypeInt(signed=False, label="UInt32"), "lcsFilename": SimTypeFixedSizeArray(SimTypeChar(label="Char"), 260)}, name="LOGCOLORSPACEW", pack=False, align=None), offset=0), SimTypePointer(SimTypePointer(SimTypeBottom(label="Void"), offset=0), offset=0)], SimTypeInt(signed=True, label="Int32"), arg_names=["lpColorSpace", "lpProfileData"]),
        #
        'CMCreateTransform': SimTypeFunction([SimTypePointer(SimStruct({"lcsSignature": SimTypeInt(signed=False, label="UInt32"), "lcsVersion": SimTypeInt(signed=False, label="UInt32"), "lcsSize": SimTypeInt(signed=False, label="UInt32"), "lcsCSType": SimTypeInt(signed=True, label="Int32"), "lcsIntent": SimTypeInt(signed=True, label="Int32"), "lcsEndpoints": SimStruct({"ciexyzRed": SimStruct({"ciexyzX": SimTypeInt(signed=True, label="Int32"), "ciexyzY": SimTypeInt(signed=True, label="Int32"), "ciexyzZ": SimTypeInt(signed=True, label="Int32")}, name="CIEXYZ", pack=False, align=None), "ciexyzGreen": SimStruct({"ciexyzX": SimTypeInt(signed=True, label="Int32"), "ciexyzY": SimTypeInt(signed=True, label="Int32"), "ciexyzZ": SimTypeInt(signed=True, label="Int32")}, name="CIEXYZ", pack=False, align=None), "ciexyzBlue": SimStruct({"ciexyzX": SimTypeInt(signed=True, label="Int32"), "ciexyzY": SimTypeInt(signed=True, label="Int32"), "ciexyzZ": SimTypeInt(signed=True, label="Int32")}, name="CIEXYZ", pack=False, align=None)}, name="CIEXYZTRIPLE", pack=False, align=None), "lcsGammaRed": SimTypeInt(signed=False, label="UInt32"), "lcsGammaGreen": SimTypeInt(signed=False, label="UInt32"), "lcsGammaBlue": SimTypeInt(signed=False, label="UInt32"), "lcsFilename": SimTypeFixedSizeArray(SimTypeChar(label="Byte"), 260)}, name="LOGCOLORSPACEA", pack=False, align=None), offset=0), SimTypePointer(SimTypeBottom(label="Void"), offset=0), SimTypePointer(SimTypeBottom(label="Void"), offset=0)], SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0), arg_names=["lpColorSpace", "lpDevCharacter", "lpTargetDevCharacter"]),
        #
        'CMCreateTransformW': SimTypeFunction([SimTypePointer(SimStruct({"lcsSignature": SimTypeInt(signed=False, label="UInt32"), "lcsVersion": SimTypeInt(signed=False, label="UInt32"), "lcsSize": SimTypeInt(signed=False, label="UInt32"), "lcsCSType": SimTypeInt(signed=True, label="Int32"), "lcsIntent": SimTypeInt(signed=True, label="Int32"), "lcsEndpoints": SimStruct({"ciexyzRed": SimStruct({"ciexyzX": SimTypeInt(signed=True, label="Int32"), "ciexyzY": SimTypeInt(signed=True, label="Int32"), "ciexyzZ": SimTypeInt(signed=True, label="Int32")}, name="CIEXYZ", pack=False, align=None), "ciexyzGreen": SimStruct({"ciexyzX": SimTypeInt(signed=True, label="Int32"), "ciexyzY": SimTypeInt(signed=True, label="Int32"), "ciexyzZ": SimTypeInt(signed=True, label="Int32")}, name="CIEXYZ", pack=False, align=None), "ciexyzBlue": SimStruct({"ciexyzX": SimTypeInt(signed=True, label="Int32"), "ciexyzY": SimTypeInt(signed=True, label="Int32"), "ciexyzZ": SimTypeInt(signed=True, label="Int32")}, name="CIEXYZ", pack=False, align=None)}, name="CIEXYZTRIPLE", pack=False, align=None), "lcsGammaRed": SimTypeInt(signed=False, label="UInt32"), "lcsGammaGreen": SimTypeInt(signed=False, label="UInt32"), "lcsGammaBlue": SimTypeInt(signed=False, label="UInt32"), "lcsFilename": SimTypeFixedSizeArray(SimTypeChar(label="Char"), 260)}, name="LOGCOLORSPACEW", pack=False, align=None), offset=0), SimTypePointer(SimTypeBottom(label="Void"), offset=0), SimTypePointer(SimTypeBottom(label="Void"), offset=0)], SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0), arg_names=["lpColorSpace", "lpDevCharacter", "lpTargetDevCharacter"]),
        #
        'CMCreateTransformExt': SimTypeFunction([SimTypePointer(SimStruct({"lcsSignature": SimTypeInt(signed=False, label="UInt32"), "lcsVersion": SimTypeInt(signed=False, label="UInt32"), "lcsSize": SimTypeInt(signed=False, label="UInt32"), "lcsCSType": SimTypeInt(signed=True, label="Int32"), "lcsIntent": SimTypeInt(signed=True, label="Int32"), "lcsEndpoints": SimStruct({"ciexyzRed": SimStruct({"ciexyzX": SimTypeInt(signed=True, label="Int32"), "ciexyzY": SimTypeInt(signed=True, label="Int32"), "ciexyzZ": SimTypeInt(signed=True, label="Int32")}, name="CIEXYZ", pack=False, align=None), "ciexyzGreen": SimStruct({"ciexyzX": SimTypeInt(signed=True, label="Int32"), "ciexyzY": SimTypeInt(signed=True, label="Int32"), "ciexyzZ": SimTypeInt(signed=True, label="Int32")}, name="CIEXYZ", pack=False, align=None), "ciexyzBlue": SimStruct({"ciexyzX": SimTypeInt(signed=True, label="Int32"), "ciexyzY": SimTypeInt(signed=True, label="Int32"), "ciexyzZ": SimTypeInt(signed=True, label="Int32")}, name="CIEXYZ", pack=False, align=None)}, name="CIEXYZTRIPLE", pack=False, align=None), "lcsGammaRed": SimTypeInt(signed=False, label="UInt32"), "lcsGammaGreen": SimTypeInt(signed=False, label="UInt32"), "lcsGammaBlue": SimTypeInt(signed=False, label="UInt32"), "lcsFilename": SimTypeFixedSizeArray(SimTypeChar(label="Byte"), 260)}, name="LOGCOLORSPACEA", pack=False, align=None), offset=0), SimTypePointer(SimTypeBottom(label="Void"), offset=0), SimTypePointer(SimTypeBottom(label="Void"), offset=0), SimTypeInt(signed=False, label="UInt32")], SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0), arg_names=["lpColorSpace", "lpDevCharacter", "lpTargetDevCharacter", "dwFlags"]),
        #
        'CMCheckColorsInGamut': SimTypeFunction([SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0), SimTypePointer(SimStruct({"rgbtBlue": SimTypeChar(label="Byte"), "rgbtGreen": SimTypeChar(label="Byte"), "rgbtRed": SimTypeChar(label="Byte")}, name="RGBTRIPLE", pack=False, align=None), label="LPArray", offset=0), SimTypePointer(SimTypeChar(label="Byte"), offset=0), SimTypeInt(signed=False, label="UInt32")], SimTypeInt(signed=True, label="Int32"), arg_names=["hcmTransform", "lpaRGBTriple", "lpaResult", "nCount"]),
        #
        'CMCreateProfile': SimTypeFunction([SimTypePointer(SimStruct({"lcsSignature": SimTypeInt(signed=False, label="UInt32"), "lcsVersion": SimTypeInt(signed=False, label="UInt32"), "lcsSize": SimTypeInt(signed=False, label="UInt32"), "lcsCSType": SimTypeInt(signed=True, label="Int32"), "lcsIntent": SimTypeInt(signed=True, label="Int32"), "lcsEndpoints": SimStruct({"ciexyzRed": SimStruct({"ciexyzX": SimTypeInt(signed=True, label="Int32"), "ciexyzY": SimTypeInt(signed=True, label="Int32"), "ciexyzZ": SimTypeInt(signed=True, label="Int32")}, name="CIEXYZ", pack=False, align=None), "ciexyzGreen": SimStruct({"ciexyzX": SimTypeInt(signed=True, label="Int32"), "ciexyzY": SimTypeInt(signed=True, label="Int32"), "ciexyzZ": SimTypeInt(signed=True, label="Int32")}, name="CIEXYZ", pack=False, align=None), "ciexyzBlue": SimStruct({"ciexyzX": SimTypeInt(signed=True, label="Int32"), "ciexyzY": SimTypeInt(signed=True, label="Int32"), "ciexyzZ": SimTypeInt(signed=True, label="Int32")}, name="CIEXYZ", pack=False, align=None)}, name="CIEXYZTRIPLE", pack=False, align=None), "lcsGammaRed": SimTypeInt(signed=False, label="UInt32"), "lcsGammaGreen": SimTypeInt(signed=False, label="UInt32"), "lcsGammaBlue": SimTypeInt(signed=False, label="UInt32"), "lcsFilename": SimTypeFixedSizeArray(SimTypeChar(label="Byte"), 260)}, name="LOGCOLORSPACEA", pack=False, align=None), offset=0), SimTypePointer(SimTypePointer(SimTypeBottom(label="Void"), offset=0), offset=0)], SimTypeInt(signed=True, label="Int32"), arg_names=["lpColorSpace", "lpProfileData"]),
        #
        'CMTranslateRGB': SimTypeFunction([SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0), SimTypeInt(signed=False, label="UInt32"), SimTypePointer(SimTypeInt(signed=False, label="UInt32"), offset=0), SimTypeInt(signed=False, label="UInt32")], SimTypeInt(signed=True, label="Int32"), arg_names=["hcmTransform", "ColorRef", "lpColorRef", "dwFlags"]),
        #
        'CMTranslateRGBs': SimTypeFunction([SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0), SimTypePointer(SimTypeBottom(label="Void"), offset=0), SimTypeInt(signed=False, label="BMFORMAT"), SimTypeInt(signed=False, label="UInt32"), SimTypeInt(signed=False, label="UInt32"), SimTypeInt(signed=False, label="UInt32"), SimTypePointer(SimTypeBottom(label="Void"), offset=0), SimTypeInt(signed=False, label="BMFORMAT"), SimTypeInt(signed=False, label="UInt32")], SimTypeInt(signed=True, label="Int32"), arg_names=["hcmTransform", "lpSrcBits", "bmInput", "dwWidth", "dwHeight", "dwStride", "lpDestBits", "bmOutput", "dwTranslateDirection"]),
        #
        'CMCreateTransformExtW': SimTypeFunction([SimTypePointer(SimStruct({"lcsSignature": SimTypeInt(signed=False, label="UInt32"), "lcsVersion": SimTypeInt(signed=False, label="UInt32"), "lcsSize": SimTypeInt(signed=False, label="UInt32"), "lcsCSType": SimTypeInt(signed=True, label="Int32"), "lcsIntent": SimTypeInt(signed=True, label="Int32"), "lcsEndpoints": SimStruct({"ciexyzRed": SimStruct({"ciexyzX": SimTypeInt(signed=True, label="Int32"), "ciexyzY": SimTypeInt(signed=True, label="Int32"), "ciexyzZ": SimTypeInt(signed=True, label="Int32")}, name="CIEXYZ", pack=False, align=None), "ciexyzGreen": SimStruct({"ciexyzX": SimTypeInt(signed=True, label="Int32"), "ciexyzY": SimTypeInt(signed=True, label="Int32"), "ciexyzZ": SimTypeInt(signed=True, label="Int32")}, name="CIEXYZ", pack=False, align=None), "ciexyzBlue": SimStruct({"ciexyzX": SimTypeInt(signed=True, label="Int32"), "ciexyzY": SimTypeInt(signed=True, label="Int32"), "ciexyzZ": SimTypeInt(signed=True, label="Int32")}, name="CIEXYZ", pack=False, align=None)}, name="CIEXYZTRIPLE", pack=False, align=None), "lcsGammaRed": SimTypeInt(signed=False, label="UInt32"), "lcsGammaGreen": SimTypeInt(signed=False, label="UInt32"), "lcsGammaBlue": SimTypeInt(signed=False, label="UInt32"), "lcsFilename": SimTypeFixedSizeArray(SimTypeChar(label="Char"), 260)}, name="LOGCOLORSPACEW", pack=False, align=None), offset=0), SimTypePointer(SimTypeBottom(label="Void"), offset=0), SimTypePointer(SimTypeBottom(label="Void"), offset=0), SimTypeInt(signed=False, label="UInt32")], SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0), arg_names=["lpColorSpace", "lpDevCharacter", "lpTargetDevCharacter", "dwFlags"]),
        #
        'CMDeleteTransform': SimTypeFunction([SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0)], SimTypeInt(signed=True, label="Int32"), arg_names=["hcmTransform"]),
        #
        'CMGetInfo': SimTypeFunction([SimTypeInt(signed=False, label="UInt32")], SimTypeInt(signed=False, label="UInt32"), arg_names=["dwInfo"]),
        #
        'CMGetNamedProfileInfo': SimTypeFunction([SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0), SimTypePointer(SimStruct({"dwFlags": SimTypeInt(signed=False, label="UInt32"), "dwCount": SimTypeInt(signed=False, label="UInt32"), "dwCountDevCoordinates": SimTypeInt(signed=False, label="UInt32"), "szPrefix": SimTypeFixedSizeArray(SimTypeChar(label="SByte"), 32), "szSuffix": SimTypeFixedSizeArray(SimTypeChar(label="SByte"), 32)}, name="NAMED_PROFILE_INFO", pack=False, align=None), offset=0)], SimTypeInt(signed=True, label="Int32"), arg_names=["hProfile", "pNamedProfileInfo"]),
        #
        'CMIsProfileValid': SimTypeFunction([SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0), SimTypePointer(SimTypeInt(signed=True, label="Int32"), offset=0)], SimTypeInt(signed=True, label="Int32"), arg_names=["hProfile", "lpbValid"]),
        #
        'CMTranslateColors': SimTypeFunction([SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0), SimTypePointer(SimUnion({"gray": SimStruct({"gray": SimTypeShort(signed=False, label="UInt16")}, name="GRAYCOLOR", pack=False, align=None), "rgb": SimStruct({"red": SimTypeShort(signed=False, label="UInt16"), "green": SimTypeShort(signed=False, label="UInt16"), "blue": SimTypeShort(signed=False, label="UInt16")}, name="RGBCOLOR", pack=False, align=None), "cmyk": SimStruct({"cyan": SimTypeShort(signed=False, label="UInt16"), "magenta": SimTypeShort(signed=False, label="UInt16"), "yellow": SimTypeShort(signed=False, label="UInt16"), "black": SimTypeShort(signed=False, label="UInt16")}, name="CMYKCOLOR", pack=False, align=None), "XYZ": SimStruct({"X": SimTypeShort(signed=False, label="UInt16"), "Y": SimTypeShort(signed=False, label="UInt16"), "Z": SimTypeShort(signed=False, label="UInt16")}, name="XYZCOLOR", pack=False, align=None), "Yxy": SimStruct({"Y": SimTypeShort(signed=False, label="UInt16"), "x": SimTypeShort(signed=False, label="UInt16"), "y": SimTypeShort(signed=False, label="UInt16")}, name="YxyCOLOR", pack=False, align=None), "Lab": SimStruct({"L": SimTypeShort(signed=False, label="UInt16"), "a": SimTypeShort(signed=False, label="UInt16"), "b": SimTypeShort(signed=False, label="UInt16")}, name="LabCOLOR", pack=False, align=None), "gen3ch": SimStruct({"ch1": SimTypeShort(signed=False, label="UInt16"), "ch2": SimTypeShort(signed=False, label="UInt16"), "ch3": SimTypeShort(signed=False, label="UInt16")}, name="GENERIC3CHANNEL", pack=False, align=None), "named": SimStruct({"dwIndex": SimTypeInt(signed=False, label="UInt32")}, name="NAMEDCOLOR", pack=False, align=None), "hifi": SimStruct({"channel": SimTypeFixedSizeArray(SimTypeChar(label="Byte"), 8)}, name="HiFiCOLOR", pack=False, align=None), "Anonymous": SimStruct({"reserved1": SimTypeInt(signed=False, label="UInt32"), "reserved2": SimTypePointer(SimTypeBottom(label="Void"), offset=0)}, name="_Anonymous_e__Struct", pack=False, align=None)}, name="<anon>", label="None"), label="LPArray", offset=0), SimTypeInt(signed=False, label="UInt32"), SimTypeInt(signed=False, label="COLORTYPE"), SimTypePointer(SimUnion({"gray": SimStruct({"gray": SimTypeShort(signed=False, label="UInt16")}, name="GRAYCOLOR", pack=False, align=None), "rgb": SimStruct({"red": SimTypeShort(signed=False, label="UInt16"), "green": SimTypeShort(signed=False, label="UInt16"), "blue": SimTypeShort(signed=False, label="UInt16")}, name="RGBCOLOR", pack=False, align=None), "cmyk": SimStruct({"cyan": SimTypeShort(signed=False, label="UInt16"), "magenta": SimTypeShort(signed=False, label="UInt16"), "yellow": SimTypeShort(signed=False, label="UInt16"), "black": SimTypeShort(signed=False, label="UInt16")}, name="CMYKCOLOR", pack=False, align=None), "XYZ": SimStruct({"X": SimTypeShort(signed=False, label="UInt16"), "Y": SimTypeShort(signed=False, label="UInt16"), "Z": SimTypeShort(signed=False, label="UInt16")}, name="XYZCOLOR", pack=False, align=None), "Yxy": SimStruct({"Y": SimTypeShort(signed=False, label="UInt16"), "x": SimTypeShort(signed=False, label="UInt16"), "y": SimTypeShort(signed=False, label="UInt16")}, name="YxyCOLOR", pack=False, align=None), "Lab": SimStruct({"L": SimTypeShort(signed=False, label="UInt16"), "a": SimTypeShort(signed=False, label="UInt16"), "b": SimTypeShort(signed=False, label="UInt16")}, name="LabCOLOR", pack=False, align=None), "gen3ch": SimStruct({"ch1": SimTypeShort(signed=False, label="UInt16"), "ch2": SimTypeShort(signed=False, label="UInt16"), "ch3": SimTypeShort(signed=False, label="UInt16")}, name="GENERIC3CHANNEL", pack=False, align=None), "named": SimStruct({"dwIndex": SimTypeInt(signed=False, label="UInt32")}, name="NAMEDCOLOR", pack=False, align=None), "hifi": SimStruct({"channel": SimTypeFixedSizeArray(SimTypeChar(label="Byte"), 8)}, name="HiFiCOLOR", pack=False, align=None), "Anonymous": SimStruct({"reserved1": SimTypeInt(signed=False, label="UInt32"), "reserved2": SimTypePointer(SimTypeBottom(label="Void"), offset=0)}, name="_Anonymous_e__Struct", pack=False, align=None)}, name="<anon>", label="None"), label="LPArray", offset=0), SimTypeInt(signed=False, label="COLORTYPE")], SimTypeInt(signed=True, label="Int32"), arg_names=["hcmTransform", "lpaInputColors", "nColors", "ctInput", "lpaOutputColors", "ctOutput"]),
        #
        'CMTranslateRGBsExt': SimTypeFunction([SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0), SimTypePointer(SimTypeBottom(label="Void"), offset=0), SimTypeInt(signed=False, label="BMFORMAT"), SimTypeInt(signed=False, label="UInt32"), SimTypeInt(signed=False, label="UInt32"), SimTypeInt(signed=False, label="UInt32"), SimTypePointer(SimTypeBottom(label="Void"), offset=0), SimTypeInt(signed=False, label="BMFORMAT"), SimTypeInt(signed=False, label="UInt32"), SimTypePointer(SimTypeFunction([SimTypeInt(signed=False, label="UInt32"), SimTypeInt(signed=False, label="UInt32"), SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0)], SimTypeInt(signed=True, label="Int32"), arg_names=["param0", "param1", "param2"]), offset=0), SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0)], SimTypeInt(signed=True, label="Int32"), arg_names=["hcmTransform", "lpSrcBits", "bmInput", "dwWidth", "dwHeight", "dwInputStride", "lpDestBits", "bmOutput", "dwOutputStride", "lpfnCallback", "ulCallbackData"]),
    }

lib.set_prototypes(prototypes)
