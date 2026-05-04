import re
import sys

def sty_to_cwl(sty_path, cwl_path):
    with open(sty_path, encoding="utf-8") as f:
        content = f.read()

    pattern = re.compile(
        r'\\(?:new|renew|provide)command\*?\{\\(\w+)\}(?:\[(\d+)\])?(?:\[([^\]]*)\])?'
    )

    lines = []
    for m in pattern.finditer(content):
        name = m.group(1)
        nargs = int(m.group(2)) if m.group(2) else 0
        default = m.group(3)
        cmd = f"\\{name}"
        if default:
            cmd += f"[{default}]"
            nargs -= 1
        for i in range(1, nargs + 1):
            cmd += "{%<arg" + str(i) + ">%}"
        lines.append(cmd)

    with open(cwl_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"Generato: {cwl_path} ({len(lines)} comandi)")

sty_to_cwl(sys.argv[1], sys.argv[2])
