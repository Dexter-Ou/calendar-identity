"""Synthetic parser boundary probe, not a Thunderbird export or import test."""
import sys,subprocess,tempfile,pathlib,json,hashlib,os,platform
if len(sys.argv) != 2:
 raise SystemExit('Usage: newline_probe.py /absolute/path/calendar_identity.py')
engine=pathlib.Path(sys.argv[1]).resolve(); h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
engine_hash=h(engine)
prefix=b'BEGIN:VCALENDAR\r\nVERSION:2.0\r\nPRODID:-//Fictional probe//EN\r\nBEGIN:VEVENT\r\nUID:fictional-newline@example.invalid\r\nDTSTART:20261103T120000Z\r\nSEQUENCE:0\r\n'
suffix=b'\r\nEND:VEVENT\r\nEND:VCALENDAR\r\n'
cases={'escaped-control':b'DESCRIPTION:Fictional first\\nFictional second','raw-lf-text':b'DESCRIPTION:Fictional first\nFictional second','raw-lf-property-shaped':b'DESCRIPTION:Fictional first\nX-FICTIONAL:second'}
results=[]
with tempfile.TemporaryDirectory(prefix='newline probe ') as d:
 root=pathlib.Path(d); before=root/'before.ics'; before.write_bytes(prefix+cases['escaped-control']+suffix)
 for name,description in cases.items():
  after=root/(name+'.ics'); after.write_bytes(prefix+description+suffix); hashes=[h(before),h(after)]
  p=subprocess.run([sys.executable,str(engine),str(before),str(after)],capture_output=True,text=True,timeout=15)
  results.append({'case':name,'exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr,'inputs_unchanged':hashes==[h(before),h(after)],'fixture_sha256':hashes[1]})
failures=[]
for row in results:
 expected=2 if row['case']=='raw-lf-text' else 0
 if row['exit']!=expected or not row['inputs_unchanged']:
  failures.append(row['case'])
 if expected==0 and row['exit']==0:
  report=json.loads(row['stdout'])
  if report.get('shared_identities')!=1 or report.get('added_event_positions')!=[] or report.get('removed_event_positions')!=[]:
   failures.append(row['case']+' identity counts')
 if expected==2 and (row['stdout'] or json.loads(row['stderr']).get('error')!='Parser reported invalid properties'):
  failures.append(row['case']+' diagnostic')
if h(engine)!=engine_hash:
 failures.append('engine changed')
print(json.dumps({'synthetic_only':True,'failures':failures,'passed':not failures,'python':platform.python_version(),'uid':os.getuid(),'engine_sha256':engine_hash,'engine_unchanged':h(engine)==engine_hash,'cases':results},indent=2))

raise SystemExit(1 if failures else 0)
