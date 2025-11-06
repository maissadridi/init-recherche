def same_element(el1, el2):
    """Compare le contenu et les attributs de deux éléments."""
    if el1.tag != el2.tag:
        return False
    if el1.text != el2.text:
        return False
    if el1.attrib != el2.attrib:
        return False
    return True

def compare_indexes(src_index, tgt_index):
    added = []
    removed = []
    modified = []

    for el_id in src_index:
        if el_id not in tgt_index:
            added.append(el_id)
        elif not same_element(src_index[el_id], tgt_index[el_id]):
            modified.append(el_id)

    for el_id in tgt_index:
        if el_id not in src_index:
            removed.append(el_id)

    return {"added": added, "removed": removed, "modified": modified}
