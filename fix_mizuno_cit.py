"""
===========================================================
  Mizuno 16 Craft CIT - Auto-Fixer per Minecraft 1.20 / 1.21+
===========================================================
Questo script corregge automaticamente la rotazione dei modelli CIT
e risolve il problema dei modelli invisibili (trapdoor, cartelli,
quadri, fiori, ecc.) quando si usano Iris, CIT Resewn o EMF.

Come usarlo:
1. Metti questo script dentro la cartella estratta del resource pack
   (dove vedi le cartelle 'assets', 'pack.mcmeta', ecc.).
2. Fai doppio clic su questo file oppure eseguilo con:
   python fix_mizuno_cit.py
3. Troverai un file zip pronto per Minecraft chiamato:
   Mizuno_CIT_Fixed.zip
===========================================================
"""

import os
import json
import shutil
import zipfile

def main():
    print("==============================================")
    print("   Mizuno 16 Craft CIT - Full Auto-Fixer")
    print("==============================================")
    current_dir = os.path.dirname(os.path.abspath(__file__))
    assets_dir = os.path.join(current_dir, "assets")

    if not os.path.exists(assets_dir):
        print("\n[ERRORE] Cartella 'assets' non trovata!")
        print("Assicurati di mettere questo file dentro la cartella del resource pack.")
        input("\nPremi INVIO per uscire...")
        return

    print("\n[1/3] Creazione backup di sicurezza...")
    backup_dir = os.path.join(current_dir, "_backup_originale")
    if not os.path.exists(backup_dir):
        shutil.copytree(assets_dir, os.path.join(backup_dir, "assets"))
        print(" -> Backup salvato in '_backup_originale'")
    else:
        print(" -> Backup gia' presente, procedo...")

    print("\n[2/3] Correzione automatica di modelli, geometrie e rotazioni...")
    models = {}
    name_to_path = {}

    for root, _, files in os.walk(assets_dir):
        for f in files:
            if f.endswith(".json"):
                p = os.path.join(root, f)
                try:
                    with open(p, "r", encoding="utf-8") as fh:
                        data = json.load(fh)
                        if isinstance(data, dict):
                            models[p] = data
                            basename = os.path.splitext(f)[0]
                            name_to_path[basename] = p
                except Exception:
                    pass

    # Aggiorna il template cit_item se presente
    cit_item_path = name_to_path.get("cit_item")
    if cit_item_path and cit_item_path in models:
        disp = models[cit_item_path].setdefault("display", {})
        disp["fixed"] = {
            "rotation": [-90, 0, 0],
            "translation": [0, 0, -15],
            "scale": [2, 2, 2]
        }

    def resolve_model_complete(p, visited=None):
        if visited is None:
            visited = set()
        if p in visited:
            return {}
        visited.add(p)
        d = models.get(p, {})
        parent_ref = d.get("parent")

        parent_data = {}
        if parent_ref:
            clean_name = parent_ref.replace("./", "").split("/")[-1]
            par_path = name_to_path.get(clean_name)
            if par_path:
                parent_data = resolve_model_complete(par_path, visited)

        # 1. Texture merging & dereferencing
        merged_textures = dict(parent_data.get("textures", {}))
        if "textures" in d and isinstance(d["textures"], dict):
            merged_textures.update(d["textures"])

        for k in list(merged_textures.keys()):
            val = merged_textures[k]
            loop_guard = 0
            while isinstance(val, str) and val.startswith("#") and loop_guard < 10:
                var_name = val[1:]
                if var_name in merged_textures:
                    val = merged_textures[var_name]
                else:
                    break
                loop_guard += 1
            merged_textures[k] = val

        # 2. Inherit elements (geometria 3D)
        elements = d.get("elements") or parent_data.get("elements")

        # 3. Inherit display
        merged_display = dict(parent_data.get("display", {}))
        if "display" in d and isinstance(d["display"], dict):
            for k, v in d["display"].items():
                if isinstance(v, dict):
                    merged_display[k] = dict(v)
                else:
                    merged_display[k] = v

        return {
            "textures": merged_textures,
            "elements": elements,
            "display": merged_display
        }

    count = 0
    for p, d in models.items():
        if p.endswith("wall_torch.json"):
            continue

        resolved = resolve_model_complete(p)

        # Se il modello e' un derivato senza elementi, incorpora la geometria del genitore
        if "elements" not in d and resolved["elements"] is not None:
            d["elements"] = resolved["elements"]

        # Texture risolte
        if resolved["textures"]:
            d["textures"] = resolved["textures"]

        # Display risolto
        if resolved["display"]:
            if os.path.basename(p) == "cauldron_6.json" and "fixed" in resolved["display"]:
                resolved["display"]["fixed"]["rotation"] = [-90, 0, 0]
                resolved["display"]["fixed"]["translation"] = [0, 0, -15]
            d["display"] = resolved["display"]

        with open(p, "w", encoding="utf-8") as fh:
            json.dump(d, fh, indent="\t")
        count += 1

    print(f" -> Elaborati e corretti con successo {count} modelli!")

    print("\n[3/3] Compilazione pacchetto ZIP...")
    zip_path = os.path.join(current_dir, "Mizuno_CIT_Fixed.zip")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(current_dir):
            dirs[:] = [d for d in dirs if not d.startswith(".") and d != "_backup_originale"]
            for f in files:
                if f.startswith(".") or f == "Mizuno_CIT_Fixed.zip" or f.endswith(".py"):
                    continue
                full_path = os.path.join(root, f)
                rel_path = os.path.relpath(full_path, current_dir)
                zipf.write(full_path, rel_path)

    print(f"\n[COMPLETATO] Il pacchetto pronto e':\n{zip_path}")
    print("Ti basta copiare questo file zip nella cartella 'resourcepacks' di Minecraft!")
    input("\nPremi INVIO per chiudere...")

if __name__ == "__main__":
    main()
