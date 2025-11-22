import torch
import cv2
from groundingdino.util.inference import Model
import matplotlib.pyplot as plt

config_path = "GroundingDINO_SwinB.cfg.py"
weights_path = "groundingdino_swinb_cogcoor.pth"

model = Model(
    model_config_path=config_path,
    model_checkpoint_path=weights_path,
    device="cuda" if torch.cuda.is_available() else "cpu"
)

image_path = "beam.png"
image = cv2.imread(image_path)
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

prompts = ["construction beam", "metal scaffolding", "vertical concrete pillar", "wall"]

results = {}

for prompt in prompts:
    detections = model.predict_with_caption(
        image_rgb,
        caption=prompt,
        box_threshold=0.35,
        text_threshold=0.35
    )

    boxes, phrases = detections
    count = len(boxes)
    results[prompt] = {
        "count": count,
        "boxes": boxes,
        "phrases": phrases
    }

# ---------------------------------------------------------
# 5. Mostrar resultados
# ---------------------------------------------------------
for prompt, info in results.items():
    print(f"Prompt: {prompt}")
    print(f"Quantidade detectada: {info['count']}")
    print("Frases:", info["phrases"])
    print()
