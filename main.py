import os
import random
from PIL import Image
import json

# Konfigurasi
width, height = 512, 512  # Dimensi gambar
layer_path = "./layers"
output_images_path = "./output/images"
output_metadata_path = "./output/metadata"
total_nfts = 10000  # Jumlah NFT yang ingin dibuat

# Urutan layers
layers_order = [
    {"name": "Background", "required": True},
    {"name": "Body", "required": True},
    {"name": "Head", "required": True},
    {"name": "Eyes", "required": True},
    {"name": "Accessories", "required": True},
    {"name": "Mouth", "required": True},
    {"name": "Cap", "required": True},
    {"name": "Nose", "required": False},
    {"name": "Legs", "required": True},
    {"name": "Weapon", "required": True},
]

# Membaca traits dari folder layers
def get_traits(layer_name):
    folder = os.path.join(layer_path, layer_name)
    return [file for file in os.listdir(folder) if file.endswith(".png")] if os.path.exists(folder) else []

# Membuat kombinasi unik
def create_unique_combination(traits_list):
    combination = {}
    for layer in layers_order:
        traits = traits_list[layer["name"]]
        if layer["required"]:
            combination[layer["name"]] = random.choice(traits)
        else:
            combination[layer["name"]] = random.choice(traits) if random.random() < 0.5 else None
    return combination

# Mengecek duplikasi
def is_duplicate(combinations, new_combination):
    return any(existing == new_combination for existing in combinations)

# Membuat gambar NFT
def draw_nft(traits, nft_id):
    base_image = Image.new("RGBA", (width, height), (255, 255, 255, 0))
    for layer in layers_order:
        trait = traits[layer["name"]]
        if trait:
            layer_image_path = os.path.join(layer_path, layer["name"], trait)
            layer_image = Image.open(layer_image_path).convert("RGBA")
            base_image.paste(layer_image, (0, 0), layer_image)
    output_path = os.path.join(output_images_path, f"{nft_id}.png")
    base_image.save(output_path)

# Menyimpan metadata
def save_metadata(traits, nft_id):
    metadata = {
        "id": nft_id,
        "attributes": [
            {"trait_type": layer["name"], "value": traits[layer["name"]].replace(".png", "") if traits[layer["name"]] else None}
            for layer in layers_order
        ],
    }
    output_path = os.path.join(output_metadata_path, f"{nft_id}.json")
    with open(output_path, "w") as metadata_file:
        json.dump(metadata, metadata_file, indent=4)

# Proses utama
def generate_nfts():
    os.makedirs(output_images_path, exist_ok=True)
    os.makedirs(output_metadata_path, exist_ok=True)

    traits_list = {layer["name"]: get_traits(layer["name"]) for layer in layers_order}
    combinations = []

    for i in range(total_nfts):
        while True:
            new_combination = create_unique_combination(traits_list)
            if not is_duplicate(combinations, new_combination):
                combinations.append(new_combination)
                break

        draw_nft(new_combination, i + 1)
        save_metadata(new_combination, i + 1)
        print(f"Generated NFT #{i + 1}")

    print("All NFTs have been generated!")

if __name__ == "__main__":
    generate_nfts()
