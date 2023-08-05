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
lib.set_library_names("ndfapi.dll")
prototypes = \
    {
        #
        'NdfCreateIncident': SimTypeFunction([SimTypePointer(SimTypeChar(label="Char"), offset=0), SimTypeInt(signed=False, label="UInt32"), SimTypePointer(SimStruct({"pwszName": SimTypePointer(SimTypeChar(label="Char"), offset=0), "type": SimTypeInt(signed=False, label="ATTRIBUTE_TYPE"), "Anonymous": SimUnion({"Boolean": SimTypeInt(signed=True, label="Int32"), "Char": SimTypeChar(label="Byte"), "Byte": SimTypeChar(label="Byte"), "Short": SimTypeShort(signed=True, label="Int16"), "Word": SimTypeShort(signed=False, label="UInt16"), "Int": SimTypeInt(signed=True, label="Int32"), "DWord": SimTypeInt(signed=False, label="UInt32"), "Int64": SimTypeLongLong(signed=True, label="Int64"), "UInt64": SimTypeLongLong(signed=False, label="UInt64"), "PWStr": SimTypePointer(SimTypeChar(label="Char"), offset=0), "Guid": SimTypeBottom(label="Guid"), "LifeTime": SimStruct({"startTime": SimStruct({"dwLowDateTime": SimTypeInt(signed=False, label="UInt32"), "dwHighDateTime": SimTypeInt(signed=False, label="UInt32")}, name="FILETIME", pack=False, align=None), "endTime": SimStruct({"dwLowDateTime": SimTypeInt(signed=False, label="UInt32"), "dwHighDateTime": SimTypeInt(signed=False, label="UInt32")}, name="FILETIME", pack=False, align=None)}, name="LIFE_TIME", pack=False, align=None), "Address": SimStruct({"family": SimTypeShort(signed=False, label="UInt16"), "data": SimTypeFixedSizeArray(SimTypeBottom(label="CHAR"), 126)}, name="DIAG_SOCKADDR", pack=False, align=None), "OctetString": SimStruct({"dwLength": SimTypeInt(signed=False, label="UInt32"), "lpValue": SimTypePointer(SimTypeChar(label="Byte"), offset=0)}, name="OCTET_STRING", pack=False, align=None)}, name="<anon>", label="None")}, name="HELPER_ATTRIBUTE", pack=False, align=None), label="LPArray", offset=0), SimTypePointer(SimTypePointer(SimTypeBottom(label="Void"), offset=0), offset=0)], SimTypeInt(signed=True, label="Int32"), arg_names=["helperClassName", "celt", "attributes", "handle"]),
        #
        'NdfCreateWinSockIncident': SimTypeFunction([SimTypePointer(SimTypeInt(signed=False, label="UInt"), label="UIntPtr", offset=0), SimTypePointer(SimTypeChar(label="Char"), offset=0), SimTypeShort(signed=False, label="UInt16"), SimTypePointer(SimTypeChar(label="Char"), offset=0), SimTypePointer(SimStruct({"Revision": SimTypeChar(label="Byte"), "SubAuthorityCount": SimTypeChar(label="Byte"), "IdentifierAuthority": SimStruct({"Value": SimTypeFixedSizeArray(SimTypeChar(label="Byte"), 6)}, name="SID_IDENTIFIER_AUTHORITY", pack=False, align=None), "SubAuthority": SimTypePointer(SimTypeInt(signed=False, label="UInt32"), offset=0)}, name="SID", pack=False, align=None), offset=0), SimTypePointer(SimTypePointer(SimTypeBottom(label="Void"), offset=0), offset=0)], SimTypeInt(signed=True, label="Int32"), arg_names=["sock", "host", "port", "appId", "userId", "handle"]),
        #
        'NdfCreateWebIncident': SimTypeFunction([SimTypePointer(SimTypeChar(label="Char"), offset=0), SimTypePointer(SimTypePointer(SimTypeBottom(label="Void"), offset=0), offset=0)], SimTypeInt(signed=True, label="Int32"), arg_names=["url", "handle"]),
        #
        'NdfCreateWebIncidentEx': SimTypeFunction([SimTypePointer(SimTypeChar(label="Char"), offset=0), SimTypeInt(signed=True, label="Int32"), SimTypePointer(SimTypeChar(label="Char"), offset=0), SimTypePointer(SimTypePointer(SimTypeBottom(label="Void"), offset=0), offset=0)], SimTypeInt(signed=True, label="Int32"), arg_names=["url", "useWinHTTP", "moduleName", "handle"]),
        #
        'NdfCreateSharingIncident': SimTypeFunction([SimTypePointer(SimTypeChar(label="Char"), offset=0), SimTypePointer(SimTypePointer(SimTypeBottom(label="Void"), offset=0), offset=0)], SimTypeInt(signed=True, label="Int32"), arg_names=["UNCPath", "handle"]),
        #
        'NdfCreateDNSIncident': SimTypeFunction([SimTypePointer(SimTypeChar(label="Char"), offset=0), SimTypeShort(signed=False, label="UInt16"), SimTypePointer(SimTypePointer(SimTypeBottom(label="Void"), offset=0), offset=0)], SimTypeInt(signed=True, label="Int32"), arg_names=["hostname", "queryType", "handle"]),
        #
        'NdfCreateConnectivityIncident': SimTypeFunction([SimTypePointer(SimTypePointer(SimTypeBottom(label="Void"), offset=0), offset=0)], SimTypeInt(signed=True, label="Int32"), arg_names=["handle"]),
        #
        'NdfCreateNetConnectionIncident': SimTypeFunction([SimTypePointer(SimTypePointer(SimTypeBottom(label="Void"), offset=0), offset=0), SimTypeBottom(label="Guid")], SimTypeInt(signed=True, label="Int32"), arg_names=["handle", "id"]),
        #
        'NdfCreatePnrpIncident': SimTypeFunction([SimTypePointer(SimTypeChar(label="Char"), offset=0), SimTypePointer(SimTypeChar(label="Char"), offset=0), SimTypeInt(signed=True, label="Int32"), SimTypePointer(SimTypeChar(label="Char"), offset=0), SimTypePointer(SimTypePointer(SimTypeBottom(label="Void"), offset=0), offset=0)], SimTypeInt(signed=True, label="Int32"), arg_names=["cloudname", "peername", "diagnosePublish", "appId", "handle"]),
        #
        'NdfCreateGroupingIncident': SimTypeFunction([SimTypePointer(SimTypeChar(label="Char"), offset=0), SimTypePointer(SimTypeChar(label="Char"), offset=0), SimTypePointer(SimTypeChar(label="Char"), offset=0), SimTypePointer(SimTypeChar(label="Char"), offset=0), SimTypePointer(SimStruct({"iAddressCount": SimTypeInt(signed=True, label="Int32"), "Address": SimTypePointer(SimStruct({"lpSockaddr": SimTypePointer(SimStruct({"sa_family": SimTypeShort(signed=False, label="UInt16"), "sa_data": SimTypeFixedSizeArray(SimTypeBottom(label="CHAR"), 14)}, name="SOCKADDR", pack=False, align=None), offset=0), "iSockaddrLength": SimTypeInt(signed=True, label="Int32")}, name="SOCKET_ADDRESS", pack=False, align=None), offset=0)}, name="SOCKET_ADDRESS_LIST", pack=False, align=None), offset=0), SimTypePointer(SimTypeChar(label="Char"), offset=0), SimTypePointer(SimTypePointer(SimTypeBottom(label="Void"), offset=0), offset=0)], SimTypeInt(signed=True, label="Int32"), arg_names=["CloudName", "GroupName", "Identity", "Invitation", "Addresses", "appId", "handle"]),
        #
        'NdfExecuteDiagnosis': SimTypeFunction([SimTypePointer(SimTypeBottom(label="Void"), offset=0), SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0)], SimTypeInt(signed=True, label="Int32"), arg_names=["handle", "hwnd"]),
        #
        'NdfCloseIncident': SimTypeFunction([SimTypePointer(SimTypeBottom(label="Void"), offset=0)], SimTypeInt(signed=True, label="Int32"), arg_names=["handle"]),
        #
        'NdfDiagnoseIncident': SimTypeFunction([SimTypePointer(SimTypeBottom(label="Void"), offset=0), SimTypePointer(SimTypeInt(signed=False, label="UInt32"), offset=0), SimTypePointer(SimTypePointer(SimStruct({"pwszDescription": SimTypePointer(SimTypeChar(label="Char"), offset=0), "rootCauseID": SimTypeBottom(label="Guid"), "rootCauseFlags": SimTypeInt(signed=False, label="UInt32"), "networkInterfaceID": SimTypeBottom(label="Guid"), "pRepairs": SimTypePointer(SimStruct({"repair": SimStruct({"guid": SimTypeBottom(label="Guid"), "pwszClassName": SimTypePointer(SimTypeChar(label="Char"), offset=0), "pwszDescription": SimTypePointer(SimTypeChar(label="Char"), offset=0), "sidType": SimTypeInt(signed=False, label="UInt32"), "cost": SimTypeInt(signed=True, label="Int32"), "flags": SimTypeInt(signed=False, label="UInt32"), "scope": SimTypeInt(signed=False, label="REPAIR_SCOPE"), "risk": SimTypeInt(signed=False, label="REPAIR_RISK"), "UiInfo": SimStruct({"type": SimTypeInt(signed=False, label="UI_INFO_TYPE"), "Anonymous": SimUnion({"pwzNull": SimTypePointer(SimTypeChar(label="Char"), offset=0), "ShellInfo": SimStruct({"pwszOperation": SimTypePointer(SimTypeChar(label="Char"), offset=0), "pwszFile": SimTypePointer(SimTypeChar(label="Char"), offset=0), "pwszParameters": SimTypePointer(SimTypeChar(label="Char"), offset=0), "pwszDirectory": SimTypePointer(SimTypeChar(label="Char"), offset=0), "nShowCmd": SimTypeInt(signed=False, label="UInt32")}, name="ShellCommandInfo", pack=False, align=None), "pwzHelpUrl": SimTypePointer(SimTypeChar(label="Char"), offset=0), "pwzDui": SimTypePointer(SimTypeChar(label="Char"), offset=0)}, name="<anon>", label="None")}, name="UiInfo", pack=False, align=None), "rootCauseIndex": SimTypeInt(signed=True, label="Int32")}, name="RepairInfo", pack=False, align=None), "repairRank": SimTypeShort(signed=False, label="UInt16")}, name="RepairInfoEx", pack=False, align=None), offset=0), "repairCount": SimTypeShort(signed=False, label="UInt16")}, name="RootCauseInfo", pack=False, align=None), offset=0), offset=0), SimTypeInt(signed=False, label="UInt32"), SimTypeInt(signed=False, label="UInt32")], SimTypeInt(signed=True, label="Int32"), arg_names=["Handle", "RootCauseCount", "RootCauses", "dwWait", "dwFlags"]),
        #
        'NdfRepairIncident': SimTypeFunction([SimTypePointer(SimTypeBottom(label="Void"), offset=0), SimTypePointer(SimStruct({"repair": SimStruct({"guid": SimTypeBottom(label="Guid"), "pwszClassName": SimTypePointer(SimTypeChar(label="Char"), offset=0), "pwszDescription": SimTypePointer(SimTypeChar(label="Char"), offset=0), "sidType": SimTypeInt(signed=False, label="UInt32"), "cost": SimTypeInt(signed=True, label="Int32"), "flags": SimTypeInt(signed=False, label="UInt32"), "scope": SimTypeInt(signed=False, label="REPAIR_SCOPE"), "risk": SimTypeInt(signed=False, label="REPAIR_RISK"), "UiInfo": SimStruct({"type": SimTypeInt(signed=False, label="UI_INFO_TYPE"), "Anonymous": SimUnion({"pwzNull": SimTypePointer(SimTypeChar(label="Char"), offset=0), "ShellInfo": SimStruct({"pwszOperation": SimTypePointer(SimTypeChar(label="Char"), offset=0), "pwszFile": SimTypePointer(SimTypeChar(label="Char"), offset=0), "pwszParameters": SimTypePointer(SimTypeChar(label="Char"), offset=0), "pwszDirectory": SimTypePointer(SimTypeChar(label="Char"), offset=0), "nShowCmd": SimTypeInt(signed=False, label="UInt32")}, name="ShellCommandInfo", pack=False, align=None), "pwzHelpUrl": SimTypePointer(SimTypeChar(label="Char"), offset=0), "pwzDui": SimTypePointer(SimTypeChar(label="Char"), offset=0)}, name="<anon>", label="None")}, name="UiInfo", pack=False, align=None), "rootCauseIndex": SimTypeInt(signed=True, label="Int32")}, name="RepairInfo", pack=False, align=None), "repairRank": SimTypeShort(signed=False, label="UInt16")}, name="RepairInfoEx", pack=False, align=None), offset=0), SimTypeInt(signed=False, label="UInt32")], SimTypeInt(signed=True, label="Int32"), arg_names=["Handle", "RepairEx", "dwWait"]),
        #
        'NdfCancelIncident': SimTypeFunction([SimTypePointer(SimTypeBottom(label="Void"), offset=0)], SimTypeInt(signed=True, label="Int32"), arg_names=["Handle"]),
        #
        'NdfGetTraceFile': SimTypeFunction([SimTypePointer(SimTypeBottom(label="Void"), offset=0), SimTypePointer(SimTypePointer(SimTypeChar(label="Char"), offset=0), offset=0)], SimTypeInt(signed=True, label="Int32"), arg_names=["Handle", "TraceFileLocation"]),
    }

lib.set_prototypes(prototypes)
