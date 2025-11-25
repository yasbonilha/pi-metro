import torch
import cv2
from groundingdino.util.inference import load_model, load_image, predict, annotate
import matplotlib.pyplot as plt
import ifcopenshell

def detect_images(image_path):

    config_path = "GroundingDINO_SwinB.cfg.py"
    weights_path = "groundingdino_swinb_cogcoor.pth"

    model = load_model(config_path, weights_path)
    model.eval()

    # --------------------------
    # 2. Carregar imagem
    # --------------------------

    image_source, image_tensor = load_image(image_path)

    # --------------------------
    # 3. Definir prompt textual
    # --------------------------
    prompt_text = "chair. black chair."

    # --------------------------
    # 4. Executar predição
    # --------------------------
    boxes, logits, phrases = predict(
        model=model,
        image=image_tensor,
        caption=prompt_text,
        box_threshold=0.35,
        text_threshold=0.25
    )

    print("Boxes:", boxes)
    print("Confidences:", logits)
    print("Labels:", phrases)

    # --------------------------
    # 5. Desenhar as predições na imagem
    # --------------------------
    annotated_frame = annotate(image_source, boxes, logits, phrases)

    # Salvar resultado
    output_path = "resultado_groundingdino.jpg"
    cv2.imwrite(output_path, annotated_frame)

    print("Imagem anotada salva em:", output_path)

i1 = detect_images('WhatsApp Image 2025-11-25 at 19.49.05 (1).jpeg')
i2 = detect_images('WhatsApp Image 2025-11-25 at 19.49.05.jpeg')