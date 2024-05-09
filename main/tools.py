import yaml

    
def _read_json(path, file_type="txt"):
    
    commontext = _read(path, file_type)

    if not commontext:
        return False
    
    dicttext = {}
    for text in commontext.split("\n"):
        text = text.split("-")
        try:
            dicttext[text[0]] = text[1]
        except IndexError:
            continue

    return dicttext

def _read_yaml(path):

    text = _read(path, file_type="yaml")

    if not text:
        return False
    
    return text
    

def _read(path, file_type="yaml"):

    try:
        with open(path, 'r', encoding='utf-8') as f:
            if file_type == "yaml":
                return yaml.safe_load(f)
            else:
                return f.read()
    except FileNotFoundError:
        return False


def _write(path, content, file_type="txt", kind="w", is_line=True):

    if is_line:
        content = "\r%s" % content

    with open(path, kind, encoding='utf-8') as f:
        if file_type != "yaml":
            f.write(content)


class read_file:

    json = _read_json
    yaml = _read_yaml


class write_file:
    txt = _write
        