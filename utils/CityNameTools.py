def formatCityName(name: str) -> str:
    if '自治州' in name:
        return name.replace('自治州', '')

    if name[-1] in ['市', '区']:      # TODO
        return name[:-1]

    return name

def isNameEquivalent(name1: str, name2: str) -> bool:
    if name1 in name2 or name2 in name1:
        return True

    if formatCityName(name1) in formatCityName(name2) or formatCityName(name2) in formatCityName(name1):
        return True

    return False

