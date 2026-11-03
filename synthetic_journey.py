"""Disposable synthetic CLI check, no calendar provider/customer involved."""
import hashlib,json,pathlib,subprocess,sys,tempfile
from test_calendar_identity import cal,event
with tempfile.TemporaryDirectory() as td:
    a=pathlib.Path(td)/'before.ics';b=pathlib.Path(td)/'after.ics'
    a.write_bytes(cal(event('series',sequence=4),event('series','RECURRENCE-ID:20261105T120000Z\r\n',3),event('gone')))
    b.write_bytes(cal(event('new'),event('series','RECURRENCE-ID:20261105T120000Z\r\n',2).replace('DTSTART:20261104T120000Z','DTSTART:20261106T140000Z'),event('series',sequence=5)))
    digests=[hashlib.sha256(p.read_bytes()).hexdigest() for p in (a,b)]
    r=subprocess.run([sys.executable,'calendar_identity.py',str(a),str(b)],capture_output=True,text=True)
    assert r.returncode==0,r.stderr
    report=json.loads(r.stdout)
    assert report['shared_identities']==2 and report['added_event_positions']==[1] and report['removed_event_positions']==[3]
    assert len(report['sequence_regressions'])==1
    assert digests==[hashlib.sha256(p.read_bytes()).hexdigest() for p in (a,b)]
    print(json.dumps({'test_kind':'synthetic_operator_only','cli_exit':r.returncode,'inputs_unchanged':True,'report':report},indent=2))
