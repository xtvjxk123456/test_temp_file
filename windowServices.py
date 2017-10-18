# coding:utf-8
import win32evtlog
import win32evtlogutil

flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ


class eventLogHandle:
    def __init__(self, logType):
        self.handletype = logType
        self.loghandle = win32evtlog.OpenEventLog('localhost', self.handletype)

    def __enter__(self):
        return self.loghandle

    def __exit__(self, exceptionType, exceptionValue, traceback):
        win32evtlog.CloseEventLog(self.loghandle)


class sourcenameRecord:
    def __init__(self, handle, readflag, logtype, logSourcename):
        self.records = []
        while True:
            records = win32evtlog.ReadEventLog(handle, readflag, 0)
            if not records:
                break
            for record in records:
                if str(record.SourceName) == logSourcename:
                    data = win32evtlogutil.SafeFormatMessage(record, logtype)#.encode("mbcs").replace('\r', '')
                    self.records.append({'id': record.EventID,'recordId':record.RecordNumber ,
                                         'data': data,'type':record.EventType,'sid':record.Sid,
                                         'strings':len(record.StringInserts)})

    @property
    def data(self):
        return self.records


def PrintEventLogInfo(records, outfile, sourceNames, logtype):
    import win32evtlogutil
    for record in records:
        try:
            for srcname in sourceNames:
                if str(record.SourceName) == srcname:
                    outfile.write('//////////////////////////////////////\n')
                    outfile.write(win32evtlogutil.SafeFormatMessage(record, logtype).encode("mbcs").replace('\r', ''))
        except:
            continue;


def writeMyLog():
    with eventLogHandle('Application') as myhandle:
        with open(r'E:\testtest.log', 'w') as f:
            # while True:
            #     records = win32evtlog.ReadEventLog(myhandle, flags, 0)
            #     sourceNames = ['AniPipePublisher', ]
            #     if not records:
            #         break;
            #     PrintEventLogInfo(records, f, sourceNames, 'Application')
            pubishlog = sourcenameRecord(myhandle, flags, 'Application', 'AniPipePublisher')
            for x in pubishlog.data:
                f.write(str(x)+'\n')


writeMyLog()
