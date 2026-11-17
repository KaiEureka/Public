"""Fill run times from the re-run log into the appendix C template: appC.template.md -> src/appC.md."""
import re, sys
log = sys.argv[1] if len(sys.argv) > 1 else "code/rerun_logs/times.tsv"
times, done = {}, False
for line in open(log, encoding="utf-8"):
    parts = line.rstrip("\n").split("\t")
    if parts[0] == "ALLDONE":
        done = True
    elif len(parts) == 4 and parts[3] == "0":
        times[f"{parts[0]}_{parts[1]}"] = int(parts[2])

def fmt(sec):
    if sec < 1:
        return "不到 1 秒"
    if sec < 90:
        return f"约 {sec} 秒"
    return f"约 {sec / 60:.1f} 分钟" if sec < 600 else f"约 {round(sec / 60)} 分钟"

def minutes(sec):
    return f"{sec / 60:.1f}"

s = open("appC.template.md", encoding="utf-8").read()
s = re.sub(r"@@m:([\w.-]+)@@", lambda m: minutes(times[m.group(1)]) if m.group(1) in times else "（待测）", s)
s = re.sub(r"@@T:([\w.-]+)@@", lambda m: fmt(times[m.group(1)]) if m.group(1) in times else "（待测）", s)
# the reproduction verdict is written by hand after comparing the logs with the book
verdict = open("repro_verdict.txt", encoding="utf-8").read().strip() if done else ""
s = s.replace("@@REPRO@@", verdict)
open("src/appC.md", "w", encoding="utf-8").write(s)
missing = re.findall(r"（待测）", s)
print(f"filled {len(times)} timings; {len(missing)} still pending; all done: {done}")
