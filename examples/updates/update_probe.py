"""Synthetic repeated-export probe. Run using the product venv: script PROJECT."""
import hashlib, json, os, pathlib, platform, subprocess, sys, tempfile
project = pathlib.Path(sys.argv[1]).resolve()
engine = project / 'calendar_identity.py'
def sha(data): return hashlib.sha256(data).hexdigest()
def calendar(uid, start, sequence):
    return ('BEGIN:VCALENDAR\r\nVERSION:2.0\r\nPRODID:-//Fictional update probe//EN\r\nBEGIN:VEVENT\r\nUID:' + uid + '\r\nDTSTAMP:20261103T000000Z\r\nDTSTART:' + start + '\r\nSEQUENCE:' + str(sequence) + '\r\nSUMMARY:Fictional review\r\nEND:VEVENT\r\nEND:VCALENDAR\r\n').encode()
original = sha(engine.read_bytes())
base = calendar('review@example.invalid', '20261104T120000Z', 3)
cases = [
    ('identical_export', base, 1, [], [], []),
    ('changed_time_same_sequence', calendar('review@example.invalid', '20261104T130000Z', 3), 1, [], [], []),
    ('changed_time_increased_sequence', calendar('review@example.invalid', '20261104T130000Z', 4), 1, [], [], []),
    ('changed_uid_same_time', calendar('replacement@example.invalid', '20261104T120000Z', 3), 0, [1], [1], []),
]
results = []
with tempfile.TemporaryDirectory(prefix='fictional-updates-') as tmp:
    a, b = pathlib.Path(tmp)/'before.ics', pathlib.Path(tmp)/'after.ics'
    for name, after, shared, added, removed, regressions in cases:
        a.write_bytes(base); b.write_bytes(after)
        hashes = [sha(a.read_bytes()), sha(b.read_bytes())]
        p = subprocess.run([sys.executable, str(engine), str(a), str(b)], capture_output=True, text=True, timeout=10)
        r = json.loads(p.stdout)
        unchanged = hashes == [sha(a.read_bytes()), sha(b.read_bytes())]
        ok = (p.returncode == 0 and not p.stderr and r['before_events'] == r['after_events'] == 1 and r['shared_identities'] == shared and r['added_event_positions'] == added and r['removed_event_positions'] == removed and r['sequence_regressions'] == regressions and unchanged)
        results.append({'case': name, 'inputs_differ': base != after, 'exit': p.returncode, 'report': r, 'inputs_unchanged': unchanged, 'pass': ok})
engine_unchanged = original == sha(engine.read_bytes())
# Exclude explanatory text: the actual reported metrics cannot distinguish the first three cases.
metrics = lambda r: {k:r[k] for k in ('before_events','after_events','shared_identities','added_event_positions','removed_event_positions','sequence_regressions')}
indistinguishable = len({json.dumps(metrics(r['report']), sort_keys=True) for r in results[:3]}) == 1
out = {'synthetic_only': True, 'uid': os.getuid(), 'python': platform.python_version(), 'engine_sha256': original, 'engine_unchanged': engine_unchanged, 'cases': results, 'first_three_metrics_identical': indistinguishable, 'pass': all(r['pass'] for r in results) and engine_unchanged and indistinguishable}
print(json.dumps(out, indent=2))
sys.exit(0 if out['pass'] else 1)
