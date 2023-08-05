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
lib.set_library_names("diagnosticdataquery.dll")
prototypes = \
    {
        #
        'DdqCreateSession': SimTypeFunction([SimTypeInt(signed=False, label="DdqAccessLevel"), SimTypePointer(SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0), offset=0)], SimTypeInt(signed=True, label="Int32"), arg_names=["accessLevel", "hSession"]),
        #
        'DdqCloseSession': SimTypeFunction([SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0)], SimTypeInt(signed=True, label="Int32"), arg_names=["hSession"]),
        #
        'DdqGetSessionAccessLevel': SimTypeFunction([SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0), SimTypePointer(SimTypeInt(signed=False, label="DdqAccessLevel"), offset=0)], SimTypeInt(signed=True, label="Int32"), arg_names=["hSession", "accessLevel"]),
        #
        'DdqGetDiagnosticDataAccessLevelAllowed': SimTypeFunction([SimTypePointer(SimTypeInt(signed=False, label="DdqAccessLevel"), offset=0)], SimTypeInt(signed=True, label="Int32"), arg_names=["accessLevel"]),
        #
        'DdqGetDiagnosticRecordStats': SimTypeFunction([SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0), SimTypePointer(SimStruct({"producerNames": SimTypePointer(SimTypePointer(SimTypeChar(label="Char"), offset=0), offset=0), "producerNameCount": SimTypeInt(signed=False, label="UInt32"), "textToMatch": SimTypePointer(SimTypeChar(label="Char"), offset=0), "categoryIds": SimTypePointer(SimTypeInt(signed=True, label="Int32"), offset=0), "categoryIdCount": SimTypeInt(signed=False, label="UInt32"), "privacyTags": SimTypePointer(SimTypeInt(signed=True, label="Int32"), offset=0), "privacyTagCount": SimTypeInt(signed=False, label="UInt32"), "coreDataOnly": SimTypeInt(signed=True, label="Int32")}, name="DIAGNOSTIC_DATA_SEARCH_CRITERIA", pack=False, align=None), offset=0), SimTypePointer(SimTypeInt(signed=False, label="UInt32"), offset=0), SimTypePointer(SimTypeLongLong(signed=True, label="Int64"), offset=0), SimTypePointer(SimTypeLongLong(signed=True, label="Int64"), offset=0)], SimTypeInt(signed=True, label="Int32"), arg_names=["hSession", "searchCriteria", "recordCount", "minRowId", "maxRowId"]),
        #
        'DdqGetDiagnosticRecordPayload': SimTypeFunction([SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0), SimTypeLongLong(signed=True, label="Int64"), SimTypePointer(SimTypePointer(SimTypeChar(label="Char"), offset=0), offset=0)], SimTypeInt(signed=True, label="Int32"), arg_names=["hSession", "rowId", "payload"]),
        #
        'DdqGetDiagnosticRecordLocaleTags': SimTypeFunction([SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0), SimTypePointer(SimTypeChar(label="Char"), offset=0), SimTypePointer(SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0), offset=0)], SimTypeInt(signed=True, label="Int32"), arg_names=["hSession", "locale", "hTagDescription"]),
        #
        'DdqFreeDiagnosticRecordLocaleTags': SimTypeFunction([SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0)], SimTypeInt(signed=True, label="Int32"), arg_names=["hTagDescription"]),
        #
        'DdqGetDiagnosticRecordLocaleTagAtIndex': SimTypeFunction([SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0), SimTypeInt(signed=False, label="UInt32"), SimTypePointer(SimStruct({"privacyTag": SimTypeInt(signed=True, label="Int32"), "name": SimTypePointer(SimTypeChar(label="Char"), offset=0), "description": SimTypePointer(SimTypeChar(label="Char"), offset=0)}, name="DIAGNOSTIC_DATA_EVENT_TAG_DESCRIPTION", pack=False, align=None), offset=0)], SimTypeInt(signed=True, label="Int32"), arg_names=["hTagDescription", "index", "tagDescription"]),
        #
        'DdqGetDiagnosticRecordLocaleTagCount': SimTypeFunction([SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0), SimTypePointer(SimTypeInt(signed=False, label="UInt32"), offset=0)], SimTypeInt(signed=True, label="Int32"), arg_names=["hTagDescription", "tagDescriptionCount"]),
        #
        'DdqGetDiagnosticRecordProducers': SimTypeFunction([SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0), SimTypePointer(SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0), offset=0)], SimTypeInt(signed=True, label="Int32"), arg_names=["hSession", "hProducerDescription"]),
        #
        'DdqFreeDiagnosticRecordProducers': SimTypeFunction([SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0)], SimTypeInt(signed=True, label="Int32"), arg_names=["hProducerDescription"]),
        #
        'DdqGetDiagnosticRecordProducerAtIndex': SimTypeFunction([SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0), SimTypeInt(signed=False, label="UInt32"), SimTypePointer(SimStruct({"name": SimTypePointer(SimTypeChar(label="Char"), offset=0)}, name="DIAGNOSTIC_DATA_EVENT_PRODUCER_DESCRIPTION", pack=False, align=None), offset=0)], SimTypeInt(signed=True, label="Int32"), arg_names=["hProducerDescription", "index", "producerDescription"]),
        #
        'DdqGetDiagnosticRecordProducerCount': SimTypeFunction([SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0), SimTypePointer(SimTypeInt(signed=False, label="UInt32"), offset=0)], SimTypeInt(signed=True, label="Int32"), arg_names=["hProducerDescription", "producerDescriptionCount"]),
        #
        'DdqGetDiagnosticRecordProducerCategories': SimTypeFunction([SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0), SimTypePointer(SimTypeChar(label="Char"), offset=0), SimTypePointer(SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0), offset=0)], SimTypeInt(signed=True, label="Int32"), arg_names=["hSession", "producerName", "hCategoryDescription"]),
        #
        'DdqFreeDiagnosticRecordProducerCategories': SimTypeFunction([SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0)], SimTypeInt(signed=True, label="Int32"), arg_names=["hCategoryDescription"]),
        #
        'DdqGetDiagnosticRecordCategoryAtIndex': SimTypeFunction([SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0), SimTypeInt(signed=False, label="UInt32"), SimTypePointer(SimStruct({"id": SimTypeInt(signed=True, label="Int32"), "name": SimTypePointer(SimTypeChar(label="Char"), offset=0)}, name="DIAGNOSTIC_DATA_EVENT_CATEGORY_DESCRIPTION", pack=False, align=None), offset=0)], SimTypeInt(signed=True, label="Int32"), arg_names=["hCategoryDescription", "index", "categoryDescription"]),
        #
        'DdqGetDiagnosticRecordCategoryCount': SimTypeFunction([SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0), SimTypePointer(SimTypeInt(signed=False, label="UInt32"), offset=0)], SimTypeInt(signed=True, label="Int32"), arg_names=["hCategoryDescription", "categoryDescriptionCount"]),
        #
        'DdqIsDiagnosticRecordSampledIn': SimTypeFunction([SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0), SimTypePointer(SimTypeBottom(label="Guid"), offset=0), SimTypePointer(SimTypeBottom(label="Guid"), offset=0), SimTypePointer(SimTypeChar(label="Char"), offset=0), SimTypePointer(SimTypeInt(signed=False, label="UInt32"), offset=0), SimTypePointer(SimTypeChar(label="Char"), offset=0), SimTypePointer(SimTypeInt(signed=False, label="UInt32"), offset=0), SimTypePointer(SimTypeLongLong(signed=False, label="UInt64"), offset=0), SimTypePointer(SimTypeInt(signed=True, label="Int32"), offset=0)], SimTypeInt(signed=True, label="Int32"), arg_names=["hSession", "providerGroup", "providerId", "providerName", "eventId", "eventName", "eventVersion", "eventKeywords", "isSampledIn"]),
        #
        'DdqGetDiagnosticRecordPage': SimTypeFunction([SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0), SimTypePointer(SimStruct({"producerNames": SimTypePointer(SimTypePointer(SimTypeChar(label="Char"), offset=0), offset=0), "producerNameCount": SimTypeInt(signed=False, label="UInt32"), "textToMatch": SimTypePointer(SimTypeChar(label="Char"), offset=0), "categoryIds": SimTypePointer(SimTypeInt(signed=True, label="Int32"), offset=0), "categoryIdCount": SimTypeInt(signed=False, label="UInt32"), "privacyTags": SimTypePointer(SimTypeInt(signed=True, label="Int32"), offset=0), "privacyTagCount": SimTypeInt(signed=False, label="UInt32"), "coreDataOnly": SimTypeInt(signed=True, label="Int32")}, name="DIAGNOSTIC_DATA_SEARCH_CRITERIA", pack=False, align=None), offset=0), SimTypeInt(signed=False, label="UInt32"), SimTypeInt(signed=False, label="UInt32"), SimTypeLongLong(signed=True, label="Int64"), SimTypePointer(SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0), offset=0)], SimTypeInt(signed=True, label="Int32"), arg_names=["hSession", "searchCriteria", "offset", "pageRecordCount", "baseRowId", "hRecord"]),
        #
        'DdqFreeDiagnosticRecordPage': SimTypeFunction([SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0)], SimTypeInt(signed=True, label="Int32"), arg_names=["hRecord"]),
        #
        'DdqGetDiagnosticRecordAtIndex': SimTypeFunction([SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0), SimTypeInt(signed=False, label="UInt32"), SimTypePointer(SimStruct({"rowId": SimTypeLongLong(signed=True, label="Int64"), "timestamp": SimTypeLongLong(signed=False, label="UInt64"), "eventKeywords": SimTypeLongLong(signed=False, label="UInt64"), "fullEventName": SimTypePointer(SimTypeChar(label="Char"), offset=0), "providerGroupGuid": SimTypePointer(SimTypeChar(label="Char"), offset=0), "producerName": SimTypePointer(SimTypeChar(label="Char"), offset=0), "privacyTags": SimTypePointer(SimTypeInt(signed=True, label="Int32"), offset=0), "privacyTagCount": SimTypeInt(signed=False, label="UInt32"), "categoryIds": SimTypePointer(SimTypeInt(signed=True, label="Int32"), offset=0), "categoryIdCount": SimTypeInt(signed=False, label="UInt32"), "isCoreData": SimTypeInt(signed=True, label="Int32"), "extra1": SimTypePointer(SimTypeChar(label="Char"), offset=0), "extra2": SimTypePointer(SimTypeChar(label="Char"), offset=0), "extra3": SimTypePointer(SimTypeChar(label="Char"), offset=0)}, name="DIAGNOSTIC_DATA_RECORD", pack=False, align=None), offset=0)], SimTypeInt(signed=True, label="Int32"), arg_names=["hRecord", "index", "record"]),
        #
        'DdqGetDiagnosticRecordCount': SimTypeFunction([SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0), SimTypePointer(SimTypeInt(signed=False, label="UInt32"), offset=0)], SimTypeInt(signed=True, label="Int32"), arg_names=["hRecord", "recordCount"]),
        #
        'DdqGetDiagnosticReportStoreReportCount': SimTypeFunction([SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0), SimTypeInt(signed=False, label="UInt32"), SimTypePointer(SimTypeInt(signed=False, label="UInt32"), offset=0)], SimTypeInt(signed=True, label="Int32"), arg_names=["hSession", "reportStoreType", "reportCount"]),
        #
        'DdqCancelDiagnosticRecordOperation': SimTypeFunction([SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0)], SimTypeInt(signed=True, label="Int32"), arg_names=["hSession"]),
        #
        'DdqGetDiagnosticReport': SimTypeFunction([SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0), SimTypeInt(signed=False, label="UInt32"), SimTypePointer(SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0), offset=0)], SimTypeInt(signed=True, label="Int32"), arg_names=["hSession", "reportStoreType", "hReport"]),
        #
        'DdqFreeDiagnosticReport': SimTypeFunction([SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0)], SimTypeInt(signed=True, label="Int32"), arg_names=["hReport"]),
        #
        'DdqGetDiagnosticReportAtIndex': SimTypeFunction([SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0), SimTypeInt(signed=False, label="UInt32"), SimTypePointer(SimStruct({"signature": SimStruct({"eventName": SimTypeFixedSizeArray(SimTypeChar(label="Char"), 65), "parameters": SimTypeFixedSizeArray(SimStruct({"name": SimTypeFixedSizeArray(SimTypeChar(label="Char"), 129), "value": SimTypeFixedSizeArray(SimTypeChar(label="Char"), 260)}, name="DIAGNOSTIC_REPORT_PARAMETER", pack=False, align=None), 10)}, name="DIAGNOSTIC_REPORT_SIGNATURE", pack=False, align=None), "bucketId": SimTypeBottom(label="Guid"), "reportId": SimTypeBottom(label="Guid"), "creationTime": SimStruct({"dwLowDateTime": SimTypeInt(signed=False, label="UInt32"), "dwHighDateTime": SimTypeInt(signed=False, label="UInt32")}, name="FILETIME", pack=False, align=None), "sizeInBytes": SimTypeLongLong(signed=False, label="UInt64"), "cabId": SimTypePointer(SimTypeChar(label="Char"), offset=0), "reportStatus": SimTypeInt(signed=False, label="UInt32"), "reportIntegratorId": SimTypeBottom(label="Guid"), "fileNames": SimTypePointer(SimTypePointer(SimTypeChar(label="Char"), offset=0), offset=0), "fileCount": SimTypeInt(signed=False, label="UInt32"), "friendlyEventName": SimTypePointer(SimTypeChar(label="Char"), offset=0), "applicationName": SimTypePointer(SimTypeChar(label="Char"), offset=0), "applicationPath": SimTypePointer(SimTypeChar(label="Char"), offset=0), "description": SimTypePointer(SimTypeChar(label="Char"), offset=0), "bucketIdString": SimTypePointer(SimTypeChar(label="Char"), offset=0), "legacyBucketId": SimTypeLongLong(signed=False, label="UInt64"), "reportKey": SimTypePointer(SimTypeChar(label="Char"), offset=0)}, name="DIAGNOSTIC_REPORT_DATA", pack=False, align=None), offset=0)], SimTypeInt(signed=True, label="Int32"), arg_names=["hReport", "index", "report"]),
        #
        'DdqGetDiagnosticReportCount': SimTypeFunction([SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0), SimTypePointer(SimTypeInt(signed=False, label="UInt32"), offset=0)], SimTypeInt(signed=True, label="Int32"), arg_names=["hReport", "reportCount"]),
        #
        'DdqExtractDiagnosticReport': SimTypeFunction([SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0), SimTypeInt(signed=False, label="UInt32"), SimTypePointer(SimTypeChar(label="Char"), offset=0), SimTypePointer(SimTypeChar(label="Char"), offset=0)], SimTypeInt(signed=True, label="Int32"), arg_names=["hSession", "reportStoreType", "reportKey", "destinationPath"]),
        #
        'DdqGetDiagnosticRecordTagDistribution': SimTypeFunction([SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0), SimTypePointer(SimTypePointer(SimTypeChar(label="Char"), offset=0), label="LPArray", offset=0), SimTypeInt(signed=False, label="UInt32"), SimTypePointer(SimTypePointer(SimStruct({"privacyTag": SimTypeInt(signed=True, label="Int32"), "eventCount": SimTypeInt(signed=False, label="UInt32")}, name="DIAGNOSTIC_DATA_EVENT_TAG_STATS", pack=False, align=None), offset=0), label="LPArray", offset=0), SimTypePointer(SimTypeInt(signed=False, label="UInt32"), offset=0)], SimTypeInt(signed=True, label="Int32"), arg_names=["hSession", "producerNames", "producerNameCount", "tagStats", "statCount"]),
        #
        'DdqGetDiagnosticRecordBinaryDistribution': SimTypeFunction([SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0), SimTypePointer(SimTypePointer(SimTypeChar(label="Char"), offset=0), label="LPArray", offset=0), SimTypeInt(signed=False, label="UInt32"), SimTypeInt(signed=False, label="UInt32"), SimTypePointer(SimTypePointer(SimStruct({"moduleName": SimTypePointer(SimTypeChar(label="Char"), offset=0), "friendlyModuleName": SimTypePointer(SimTypeChar(label="Char"), offset=0), "eventCount": SimTypeInt(signed=False, label="UInt32"), "uploadSizeBytes": SimTypeLongLong(signed=False, label="UInt64")}, name="DIAGNOSTIC_DATA_EVENT_BINARY_STATS", pack=False, align=None), offset=0), label="LPArray", offset=0), SimTypePointer(SimTypeInt(signed=False, label="UInt32"), offset=0)], SimTypeInt(signed=True, label="Int32"), arg_names=["hSession", "producerNames", "producerNameCount", "topNBinaries", "binaryStats", "statCount"]),
        #
        'DdqGetDiagnosticRecordSummary': SimTypeFunction([SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0), SimTypePointer(SimTypePointer(SimTypeChar(label="Char"), offset=0), label="LPArray", offset=0), SimTypeInt(signed=False, label="UInt32"), SimTypePointer(SimStruct({"optInLevel": SimTypeInt(signed=False, label="UInt32"), "transcriptSizeBytes": SimTypeLongLong(signed=False, label="UInt64"), "oldestEventTimestamp": SimTypeLongLong(signed=False, label="UInt64"), "totalEventCountLast24Hours": SimTypeInt(signed=False, label="UInt32"), "averageDailyEvents": SimTypeFloat(size=32)}, name="DIAGNOSTIC_DATA_GENERAL_STATS", pack=False, align=None), offset=0)], SimTypeInt(signed=True, label="Int32"), arg_names=["hSession", "producerNames", "producerNameCount", "generalStats"]),
        #
        'DdqSetTranscriptConfiguration': SimTypeFunction([SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0), SimTypePointer(SimStruct({"hoursOfHistoryToKeep": SimTypeInt(signed=False, label="UInt32"), "maxStoreMegabytes": SimTypeInt(signed=False, label="UInt32"), "requestedMaxStoreMegabytes": SimTypeInt(signed=False, label="UInt32")}, name="DIAGNOSTIC_DATA_EVENT_TRANSCRIPT_CONFIGURATION", pack=False, align=None), offset=0)], SimTypeInt(signed=True, label="Int32"), arg_names=["hSession", "desiredConfig"]),
        #
        'DdqGetTranscriptConfiguration': SimTypeFunction([SimTypePointer(SimTypeInt(signed=True, label="Int"), label="IntPtr", offset=0), SimTypePointer(SimStruct({"hoursOfHistoryToKeep": SimTypeInt(signed=False, label="UInt32"), "maxStoreMegabytes": SimTypeInt(signed=False, label="UInt32"), "requestedMaxStoreMegabytes": SimTypeInt(signed=False, label="UInt32")}, name="DIAGNOSTIC_DATA_EVENT_TRANSCRIPT_CONFIGURATION", pack=False, align=None), offset=0)], SimTypeInt(signed=True, label="Int32"), arg_names=["hSession", "currentConfig"]),
    }

lib.set_prototypes(prototypes)
