import glob
import re
import sys
import typing as tg

usage = """Checks annotated (and unannotated) abstracts files for errors.
  Knows about annotation syntax. 
  Reads codebook.md for list of allowed codes (pattern: "code `name-of-code`").
  Reads all abstracts files and checks for syntax errors and undefined codes.
  Reports problems on stdout.
"""

def configure_argparser(subparser):
    subparser.add_argument('workdir',
                           help="Directory where sample-who-what.txt and abstracts.?/* live")
    subparser.add_argument('--codebook', type=str, default="codebook.md",
                           help="filename of codebook to check against")


def check_codings(codebookname: str, workdir: str):
    codes, globalcodes = allowed_codes(codebookname)
    files = sorted(glob.glob(f"{workdir}/abstracts.?/*.txt"))
    print(f"checking {len(files)} files")
    errors: int = 0
    for file in files:
        errors += report_errors(file, codes, globalcodes)
    sys.exit(errors)  # 0 if no errors, number of errors otherwise

def allowed_codes(codebookname: str) -> tg.Tuple[tg.Set[str], tg.Set[str]]:
    with open(codebookname, 'rt', encoding='utf8') as cb:
        codebook = cb.read()
    codes = re.findall(r"code `([\w-]+(?::N)?)`", codebook, flags=re.IGNORECASE)
    globalcodes = re.findall(r"Code `#([\w-]+)`", codebook, flags=re.IGNORECASE)
    return (codes, globalcodes)


def report_errors(file: str, codes: tg.Set[str], globalcodes: tg.Set[str]) -> int:
    def report():
        if errors:
            print(f"---- {file}:\n" + '\n'.join(errors))
    with open(file, 'rt', encoding='utf8') as f:
        content = f.read()
    #----- check annotation-ish stuff:
    allstuff = re.findall(r"\n(\{\{[^}]*\})\n|\n(\{[^{]*\}\})\n|\n(.+\{\{.*\}\})|\n(\{\{.*\}\})\n", content)
        # 4 cases: brace missing at end, or at start, no complete line, valid pattern
    errors = []
    for closing1, opening1, other, valid  in allstuff:
        # only one of the four is non-empty
        if closing1:
            errors.append(f"second closing brace appears to be missing: '{closing1}'\n")
        elif opening1:
            errors.append(f"second opening brace appears to be missing: '{opening1}'\n")
        elif other:
            errors.append("{{}}" f" annotation must be alone on a line: '{other}'\n")
        elif valid:
            errors.extend(report_errors_within_braces(valid, codes))
        else:
            assert False, "WTF? This was supposed to never happen!"
        if len(errors) > 3:  # don't overwhelm with too many messages
            errors.append("too many problems in this file, stopping.\n")
            report()
            return len(errors)
    #----- check global codes:
    errors.extend(report_errors_in_globalcodes(content, globalcodes))
    #----- finish:
    report()
    return len(errors)


def report_errors_within_braces(annotation: str, codes: tg.Set[str]) -> tg.Sequence[str]:
    annotation = annotation[2:-2]  # strip off the braces front and back
    annotation_regexp = r"([\w-]+\??)(:\d+)?"  # we simply ignore commas and blanks (and any non-word garbage symbols)
    allcodes = re.findall(annotation_regexp, annotation)
    errors = []
    for code, num in allcodes:
        result = check_code(code, num, codes)
        if result:
            errors.append(result)
    return errors


def check_code(code: str, num: str, codes: tg.Set[str]) -> tg.Optional[str]:
    # print(f"check_code({code}, {num})")
    if not num and code[-1] == '?':
        code = code[:-1]  # strip off trailing question mark
    exists_bare, exists_with_num = (code in codes), (f"{code}:N" in codes)
    if num and not exists_with_num:
        return (f"%s: '{code}:{num}'" % ("should not have a count" if exists_bare else "unknown code (with count)"))
    if not num and not exists_bare:
        return (f"%s: '{code}'" % ("needs a count" if exists_with_num else "unknown code"))
    return None


def report_errors_in_globalcodes(content: str, globalcodes: tg.Set[str]) -> tg.Sequence[str]:
    ...  # TODO
    return []
