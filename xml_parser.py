import xml.etree.ElementTree as ET
import json

def load_xml(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    return tree, root

def index_elements(element, index, id_attr_list=("id", "xmi:id", "uuid", "name")):
    el_id = None
    for attr in id_attr_list:
        if attr in element.attrib:
            el_id = element.attrib[attr]
            break
    if el_id:
        index[el_id] = element
    for child in element:
        index_elements(child, index, id_attr_list)

def _strip_ns(tag):
    return tag.split("}")[-1] if "}" in tag else tag

def build_tag_hierarchy(root):
    """
    Construit une hiérarchie 3 niveaux des balises :
    { M : { M2 : [M3, ...], ... }, ... }
    Parcourt : racine -> enfants (M) -> petits-enfants (M2) -> arrière-petits-enfants (M3)
    """
    hierarchy = {}
    for lvl1 in root:
        name1 = _strip_ns(lvl1.tag)
        if name1 not in hierarchy:
            hierarchy[name1] = {}
        for lvl2 in lvl1:
            name2 = _strip_ns(lvl2.tag)
            lst = hierarchy[name1].setdefault(name2, set())
            for lvl3 in lvl2:
                name3 = _strip_ns(lvl3.tag)
                if name3:
                    lst.add(name3)
    # convertir les sets en listes triées pour sérialisation
    for k1 in list(hierarchy.keys()):
        for k2 in list(hierarchy[k1].keys()):
            hierarchy[k1][k2] = sorted(hierarchy[k1][k2])
    return hierarchy

def save_tag_hierarchy(root, out_filename):
    hierarchy = build_tag_hierarchy(root)
    with open(out_filename, "w", encoding="utf-8") as f:
        json.dump(hierarchy, f, indent=2, ensure_ascii=False)
    return out_filename
