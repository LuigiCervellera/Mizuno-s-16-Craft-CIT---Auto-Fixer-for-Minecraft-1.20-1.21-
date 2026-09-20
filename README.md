# 🛠️ Mizuno's 16 Craft CIT - Auto-Fixer for Minecraft 1.20 / 1.21+

A lightweight Python patcher to automatically fix rotated/sideways 3D CIT models in **Mizuno's 16 Craft CIT** when using modern Fabric/NeoForge mod loaders (**Iris**, **CIT Resewn**, **EMF/ETF**).

---

## ❓ The Issue

In modern Minecraft versions (1.20+, 1.21+) using Fabric or NeoForge (with Iris / CIT Resewn / EMF), relative template inheritance (`"parent": "./cit_item"`) is no longer resolved by the standard model loader.

When placing an item in a floor-mounted item frame, the game tilts the item frame by +90°. Without explicit display transformations, 3D items (baskets, bread boards, mugs, decor) inherit this tilt and stand vertically on their side/edge.

### 💡 What this script does
This script safely parses all **1,014 model files** in the pack:
- 🛡️ Creates an automatic safety backup.
- 🪑 Injects `"rotation": [-90, 0, 0]` and proper block offset into all tabletop/floor models so they sit upright.
- 🖼️ Preserves wall (`cit_item_wall`) and ceiling (`cit_item_ceiling`) orientations so signs, paintings, and lamps don't stick out of walls.
- 📦 Automatically compiles a ready-to-use `Mizuno_CIT_Fixed.zip` for Minecraft.

---

## 🚀 How to Use (Beginner-Friendly)

### Requirements
- **Python 3.x** installed ([Download Python](https://www.python.org/downloads/)).  
  *(Make sure to check **"Add Python to PATH"** during installation).*

### Step-by-step
1. Download the official **Mizuno's 16 Craft CIT** pack
2. Unzip / extract the resource pack into a folder.
3. Download [`fix_mizuno_cit.py`](./fix_mizuno_cit.py) from this repository and place it inside the extracted pack folder (where the `assets` folder and `pack.mcmeta` are located).
4. **Double-click `fix_mizuno_cit.py`** (or open a terminal and run `python fix_mizuno_cit.py`).
5. Once finished, a new file named **`Mizuno_CIT_Fixed.zip`** will be created in the folder.
6. Move `Mizuno_CIT_Fixed.zip` into your `.minecraft/resourcepacks/` folder, enable it in Minecraft, and enjoy!

---

## ⚖️ Disclaimer & Credits

- **Mizuno's 16 Craft** is created by **Mizuno** ([Official Blog](https://mizunomcmemo.blogspot.com/)).
- This repository does **NOT** redistribute any textures, original models, or copyrighted assets. It only provides a local automation patch script.
- Please support the original creator by downloading the pack directly from their official blog.
