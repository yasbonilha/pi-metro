import torch
import cv2
from groundingdino.util.inference import load_model, load_image, predict, annotate
import matplotlib.pyplot as plt

# ---------------------------------------------------------
# 1. Carregar o modelo
# ---------------------------------------------------------
# Existem pesos diferentes; este é o padrão mais usado:
config_path = "GroundingDINO_SwinB.cfg.py"
weights_path = "groundingdino_swinb_cogcoor.pth"

def process_image(IMAGE_PATH,TEXT_PROMPT):
  model = load_model(config_path, weights_path)

  # Carregar a imagem
  image_source, image = load_image(IMAGE_PATH)

  boxes, logits, phrases = predict(
      model=model,
      image=image,
      caption=TEXT_PROMPT,
      box_threshold=0.35,
      text_threshold=0.35,
      device="cpu"
  )

  # Anotar a imagem com as detecções
  annotated_frame = annotate(
      image_source=image_source,
      boxes=boxes, # caixas detectadas
      logits=logits, # scores de confiança
      phrases=phrases # nomes dos objetos detectados
  )

  return annotated_frame

image_path = 'beam.png'
text_prompt = "vertical support concrete pillar"
IMG_FINAL= process_image(image_path, text_prompt)

plt.figure(figsize=(12, 12))
plt.imshow(cv2.cvtColor(IMG_FINAL, cv2.COLOR_BGR2RGB))
plt.axis('off')
plt.show()