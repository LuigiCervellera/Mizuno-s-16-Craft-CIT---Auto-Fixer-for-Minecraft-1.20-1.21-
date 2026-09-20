"""
===========================================================
  Mizuno 16 Craft CIT - Auto-Fixer for Minecraft 1.20 / 1.21+
===========================================================
This script automatically fixes CIT model rotations when using
modern mods such as Iris, CIT Resewn, or EMF.

How to use:
1. Place this script inside the extracted resource pack folder
   (where you can see 'assets', 'pack.mcmeta', etc.).
2. Double-click this file or run it with:
   python fix_mizuno_cit.py
3. You will find a ready-to-use zip file for Minecraft named:
   Mizuno_CIT_Fixed.zip
===========================================================
"""

import os
import json
import shutil
import zipfile

def main():
    print("--- Mizuno CIT Auto-Fixer ---")
    current_dir = os.path.dirname(os.path.abspath(__file__))
    assets_dir = os.path.join(current_dir, "assets")

    if not os.path.exists(assets_dir):
        print("\n[ERROR] 'assets' folder not found!")
        print("Make sure to place this file inside the resource pack folder.")
        input("\nPress ENTER to exit...")
        return

    print("\n[1/3] Creating safety backup...")
    backup_dir = os.path.join(current_dir, "_backup_original")
    if not os.path.exists(backup_dir):
        shutil.copytree(assets_dir, os.path.join(backup_dir, "assets"))
        print(" -> Backup saved to '_backup_original'")
    else:
        print(" -> Backup already exists, proceeding...")

    print("\n[2/3] Automatically fixing models...")
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

    # Update cit_item template if present
    cit_item_path = name_to_path.get("cit_item")
    if cit_item_path and cit_item_path in models:
        disp = models[cit_item_path].setdefault("display", {})
        disp["fixed"] = {
            "rotation": [-90, 0, 0],
            "translation": [0, 0, -15],
            "scale": [2, 2, 2]
        }

    def get_inherited_display(p, visited=None):
        if visited is None:
            visited = set()
        if p in visited:
            return {}
        visited.add(p)
        d = models.get(p, {})
        parent_ref = d.get("parent")
        res_display = {}
        if parent_ref:
            clean_name = parent_ref.replace("./", "").split("/")[-1]
            par_path = name_to_path.get(clean_name)
            if par_path:
                res_display = get_inherited_display(par_path, visited)
        if "display" in d and isinstance(d["display"], dict):
            for k, v in d["display"].items():
                if isinstance(v, dict):
                    res_display[k] = dict(v)
                else:
                    res_display[k] = v
        return res_display

    count = 0
    for p, d in models.items():
        if p.endswith("wall_torch.json"):
            continue
        inherited_disp = get_inherited_display(p)
        if not inherited_disp:
            continue

        if os.path.basename(p) == "cauldron_6.json" and "fixed" in inherited_disp:
            inherited_disp["fixed"]["rotation"] = [-90, 0, 0]
            inherited_disp["fixed"]["translation"] = [0, 0, -15]

        d["display"] = inherited_disp
        with open(p, "w", encoding="utf-8") as fh:
            json.dump(d, fh, indent="\t")
        count += 1

    print(f" -> Successfully fixed {count} models!")

    print("\n[3/3] Building ZIP package...")
    zip_path = os.path.join(current_dir, "Mizuno_CIT_Fixed.zip")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(current_dir):
            dirs[:] = [d for d in dirs if not d.startswith(".") and d not in ("_backup_original", "_backup_originale")]
            for f in files:
                if f.startswith(".") or f == "Mizuno_CIT_Fixed.zip" or f.endswith(".py"):
                    continue
                full_path = os.path.join(root, f)
                rel_path = os.path.relpath(full_path, current_dir)
                zipf.write(full_path, rel_path)

    print(f"\n[DONE] The package is ready:\n{zip_path}")
    print("Just copy this zip file to Minecraft's 'resourcepacks' folder!")
    input("\nPress ENTER to close...")

if __name__ == "__main__":
    main()
