"""Fictional file-layout boundary test; no vdirsyncer execution or servers."""
import pathlib, tempfile, subprocess, sys, hashlib, json, os, platform
project = pathlib.Path(sys.argv[1]).resolve()
engine = project / 'calendar_identity.py'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
original = sha(engine)
def calendar(exception=False):
    event = 'BEGIN:VEVENT\r\nUID:fictional@example.invalid\r\nDTSTAMP:20261103T000000Z\r\nDTSTART:20261104T120000Z\r\nEND:VEVENT\r\n'
    if exception:
        event += 'BEGIN:VEVENT\r\nUID:fictional@example.invalid\r\nRECURRENCE-ID:20261105T120000Z\r\nDTSTAMP:20261103T000000Z\r\nDTSTART:20261105T130000Z\r\nEND:VEVENT\r\n'
    return ('BEGIN:VCALENDAR\r\nVERSION:2.0\r\nPRODID:-//Fictional layout probe//EN\r\n' + event + 'END:VCALENDAR\r\n').encode()
results = []
with tempfile.TemporaryDirectory(prefix='fictional-layout-') as tmp:
    root = pathlib.Path(tmp)
    for name, exception, directory in [('renamed_item', False, False), ('recurrence_item', True, False), ('collection_directory', False, True)]:
        left = root / (name + '-before'); right = root / (name + '-after')
        left.mkdir(); right.mkdir()
        a = left / 'old-filename.ics'; b = right / 'unrelated-filename.ics'
        a.write_bytes(calendar(exception)); b.write_bytes(calendar(exception))
        before = [sha(a), sha(b)]
        p = subprocess.run([sys.executable, str(engine), str(left if directory else a), str(right if directory else b)], capture_output=True, text=True, timeout=10)
        report = json.loads(p.stdout) if p.returncode == 0 else None
        unchanged = before == [sha(a), sha(b)]
        if directory:
            ok = p.returncode == 2 and not p.stdout and bool(p.stderr)
        else:
            count = 2 if exception else 1
            ok = p.returncode == 0 and not p.stderr and report['before_events'] == count and report['after_events'] == count and report['shared_identities'] == count and report['added_event_positions'] == [] and report['removed_event_positions'] == []
        results.append({'case': name, 'exit': p.returncode, 'report': report, 'stderr': p.stderr, 'inputs_unchanged': unchanged, 'pass': ok and unchanged})
out = {'synthetic_only': True, 'vdirsyncer_executed': False, 'uid': os.getuid(), 'python': platform.python_version(), 'engine_sha256': original, 'engine_unchanged': sha(engine) == original, 'cases': results}
out['pass'] = all(x['pass'] for x in results) and out['engine_unchanged']
print(json.dumps(out, indent=2))
sys.exit(0 if out['pass'] else 1)
