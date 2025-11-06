import argparse
import json
from xml_parser import load_xml, index_elements, save_tag_hierarchy
from xml_compare import compare_indexes
from xml_patch import apply_changes
from policy import allowed_to_copy
from report import generate_report

def main():
    parser = argparse.ArgumentParser(description="Démonstrateur XML - Comparaison et patch automatique")
    parser.add_argument("source", help="Fichier XML source (version la plus récente)")
    parser.add_argument("target", help="Fichier XML cible (version à mettre à jour)")
    parser.add_argument("--out", default="patched.xml", help="Fichier XML corrigé en sortie")
    parser.add_argument("--report", default="report.json", help="Fichier rapport JSON en sortie")
    parser.add_argument("--tags", default="tags_hierarchy.json", help="Fichier JSON de la hiérarchie des balises (M/M2/M3)")
    args = parser.parse_args()

    # Lecture des deux fichiers XML
    src_tree, src_root = load_xml(args.source)
    tgt_tree, tgt_root = load_xml(args.target)

    # Indexation des éléments
    src_index = {}
    tgt_index = {}
    index_elements(src_root, src_index)
    index_elements(tgt_root, tgt_index)

    # Génération de la hiérarchie des balises (M / M2 / M3)
    save_tag_hierarchy(src_root, args.tags)

    # Comparaison
    diff = compare_indexes(src_index, tgt_index)

    # Application du patch avec politique de confidentialité
    applied = apply_changes(tgt_root, diff, src_index, allowed_to_copy)

    # Génération du rapport
    report = generate_report(diff, applied)
    with open(args.report, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    # Sauvegarde du XML patché
    tgt_tree.write(args.out, encoding="utf-8", xml_declaration=True)
    print(f"✅ Patch terminé.\n- XML corrigé : {args.out}\n- Rapport : {args.report}\n- Hiérarchie balises : {args.tags}")

if __name__ == "__main__":
    main()
