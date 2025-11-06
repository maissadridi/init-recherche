import xml.etree.ElementTree as ET

def apply_changes(target_root, diff, src_index, policy_func):
    applied = {"added": [], "removed": [], "modified": []}

    # Ajouts
    for el_id in diff["added"]:
        element = src_index[el_id]
        if policy_func(element):
            parent = target_root  # simplification : insertion à la racine
            parent.append(element)
            applied["added"].append(el_id)

    # Suppressions
    for el_id in diff["removed"]:
        for elem in target_root.findall(".//*"):
            if el_id in elem.attrib.values():
                parent = find_parent(target_root, elem)
                if parent is not None:
                    parent.remove(elem)
                    applied["removed"].append(el_id)
                break

    # Modifications
    for el_id in diff["modified"]:
        if el_id in src_index:
            element = src_index[el_id]
            if policy_func(element):
                for elem in target_root.findall(".//*"):
                    if el_id in elem.attrib.values():
                        elem.attrib.update(element.attrib)
                        elem.text = element.text
                        applied["modified"].append(el_id)
                        break
    return applied

def find_parent(root, child):
    for elem in root.iter():
        for e in elem:
            if e is child:
                return elem
    return None
