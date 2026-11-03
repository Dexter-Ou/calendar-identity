"""Synthetic CLI probe; run with the tested product venv and source path."""
import sys, pathlib, tempfile, subprocess, hashlib, json, os, platform
project=pathlib.Path(sys.argv[1]).resolve(); engine=project/'calendar_identity.py'
def digest(b): return hashlib.sha256(b).hexdigest()
def cal(uid):
 return ('BEGIN:VCALENDAR\r\nVERSION:2.0\r\nPRODID:-//Fictional Unicode probe//EN\r\nBEGIN:VEVENT\r\nUID:'+uid+'\r\nDTSTAMP:20261103T000000Z\r\nDTSTART:20261104T120000Z\r\nEND:VEVENT\r\nEND:VCALENDAR\r\n').encode('utf-8')
cases=[('identical_unicode','caf\u00e9@example.invalid','caf\u00e9@example.invalid',1),('canonical_spelling_change','caf\u00e9@example.invalid','cafe\u0301@example.invalid',0),('folded_unicode','caf\u00e9@exam\r\n ple.invalid','caf\u00e9@example.invalid',1)]
results=[]; original=digest(engine.read_bytes())
with tempfile.TemporaryDirectory(prefix='fictional-unicode-') as tmp:
 for name,left,right,shared in cases:
  a=pathlib.Path(tmp)/'before.ics'; b=pathlib.Path(tmp)/'after.ics'; a.write_bytes(cal(left)); b.write_bytes(cal(right)); hashes=[digest(a.read_bytes()),digest(b.read_bytes())]
  p=subprocess.run([sys.executable,str(engine),str(a),str(b)],capture_output=True,text=True,timeout=10)
  r=json.loads(p.stdout); unchanged=hashes==[digest(a.read_bytes()),digest(b.read_bytes())]
  expected_positions=[] if shared else [1]
  ok=p.returncode==0 and r['shared_identities']==shared and r['added_event_positions']==expected_positions and r['removed_event_positions']==expected_positions and unchanged and not p.stderr
  results.append({'case':name,'exit':p.returncode,'report':r,'input_sha256':hashes,'inputs_unchanged':unchanged,'pass':ok})
engine_unchanged=original==digest(engine.read_bytes())
out={'synthetic_only':True,'uid':os.getuid(),'python':platform.python_version(),'engine_sha256':original,'engine_unchanged':engine_unchanged,'cases':results,'pass':all(r['pass'] for r in results) and engine_unchanged}
print(json.dumps(out,indent=2)); sys.exit(0 if out['pass'] else 1)
