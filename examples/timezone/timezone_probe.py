"""Synthetic literal-timezone boundary checks; pass the calendar_identity.py path."""
import pathlib, tempfile, subprocess, sys, json, hashlib, os
if len(sys.argv) != 2:
    raise SystemExit('Usage: python timezone_probe.py /path/to/calendar_identity.py')
engine=pathlib.Path(sys.argv[1]).resolve(strict=True)
h=lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
original=h(engine)
def fixture(offset, utc=False):
    lines=['BEGIN:VCALENDAR','VERSION:2.0','PRODID:-//Fictional TZ probe//EN','BEGIN:VTIMEZONE','TZID:Experiment/Fixed','BEGIN:STANDARD','DTSTART:19700101T000000','TZOFFSETFROM:'+offset,'TZOFFSETTO:'+offset,'END:STANDARD','END:VTIMEZONE','BEGIN:VEVENT','UID:fictional-series','DTSTAMP:20261103T000000Z','DTSTART;TZID=Experiment/Fixed:20261104T120000',('RECURRENCE-ID:20261104T110000Z' if utc else 'RECURRENCE-ID;TZID=Experiment/Fixed:20261104T120000'),'SEQUENCE:2','END:VEVENT','END:VCALENDAR','']
    return '\r\n'.join(lines).encode()
cases=[('same_tzid_changed_definition',fixture('+0100'),fixture('+0200'),1),('equivalent_instant_different_representation',fixture('+0100'),fixture('+0100',True),0),('identical_control',fixture('+0100'),fixture('+0100'),1)]
results=[]
with tempfile.TemporaryDirectory(prefix='tz probe ') as td:
    for name,a,b,shared in cases:
        before=pathlib.Path(td)/'before.ics';after=pathlib.Path(td)/'after.ics';before.write_bytes(a);after.write_bytes(b)
        r=subprocess.run([sys.executable,str(engine),str(before),str(after)],capture_output=True,text=True,timeout=15)
        assert r.returncode==0,(name,r.stderr)
        report=json.loads(r.stdout);assert report['shared_identities']==shared,(name,report)
        assert report['added_event_positions']==([] if shared else [1])
        assert report['removed_event_positions']==([] if shared else [1])
        assert before.read_bytes()==a and after.read_bytes()==b
        assert 'fictional-series' not in r.stdout+r.stderr
        results.append({'case':name,'exit_code':r.returncode,'shared_identities':shared,'inputs_unchanged':True,'report':report})
assert h(engine)==original
print(json.dumps({'synthetic_only':True,'uid':os.getuid(),'python':sys.version.split()[0],'engine_sha256':original,'engine_unchanged':True,'cases':results},indent=2))
