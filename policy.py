def allowed_to_copy(element):
    """
    Politique simple :
    - Si conf="2" => trop sensible, on ne copie pas.
    - Si export="true" => autorisé.
    - Sinon, autorisé par défaut.
    """
    conf = element.attrib.get("conf")
    if conf == "2":
        return False
    export = element.attrib.get("export", "true")
    return export.lower() == "true"
