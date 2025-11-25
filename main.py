import torch
import cv2
from groundingdino.util.inference import Model
import matplotlib.pyplot as plt
import ifcopenshell

def detect_images(image_path):

    config_path = "GroundingDINO_SwinB.cfg.py"
    weights_path = "groundingdino_swinb_cogcoor.pth"
    prompts = {
        "wall": [
            "wall",
            "exposed brick masonry wall",
            "smooth concrete wall",
            "white painted drywall partition",
            "concrete block wall",
            "glass infill wall",
            "ceramic tiled wall",
            "lightweight partition wall",
            "wood cladding wall"
        ],
        "covering": [
            "covering",
            "pitched ceramic tile roof",
            "corrugated metal roof sheet",
            "flat concrete roof slab",
            "green vegetated roof",
            "fiber cement roof panel",
            "translucent polycarbonate roof",
            "timber roof cladding",
            "white membrane roof"
        ],
        "door": [
            "door",
            "wood pivot door",
            "sliding glass door",
            "swing metal door",
            "rolling shutter door",
            "fire rated door with panic bar",
            "folding accordion door",
            "double wood hinged door"
        ],
        "stair": [
            "stair",
            "concrete stair flight",
            "metal stair structure",
            "stair with glass railing",
            "spiral staircase",
            "wooden stair steps",
            "stair with metal handrail",
            "prefabricated modular stair"
        ],
        "curtainwall": [
            "curtainwall",
            "glass curtain wall with vertical mullions",
            "unitized curtain wall panels",
            "reflective blue glass curtain wall",
            "silkscreen printed glass curtain wall",
            "structural glazing façade",
            "curtain wall with projecting vents"
        ],
        "sanitary terminal": [
            "sanitary terminal",
            "porcelain toilet bowl",
            "pedestal sink",
            "countertop washbasin",
            "wall mounted urinal",
            "bidet fixture",
            "wall mounted shower head",
            "single lever faucet"
        ],
        "slab": [
            "slab",
            "exposed concrete slab",
            "ribbed reinforced slab",
            "precast beam and block slab",
            "steel deck slab",
            "hollow core precast slab"
        ],
        "building element proxy": [
            "building element proxy",
            "generic metal structural element",
            "temporary cladding panel",
            "temporary protection barrier",
            "undefined prefabricated module",
            "technical service box",
            "generic support element"
        ],
        "discrete accessory": [
            "discrete accessory",
            "exposed metal bracket",
            "pipe connection fitting",
            "cable clamp fastener",
            "identification plate",
            "metal door hinge",
            "ventilation grille"
        ],
        "window": [
            "window",
            "aluminum sliding window",
            "outward tilting window",
            "top hung awning window",
            "fixed glass panel window",
            "louvered window",
            "vertical sash window",
            "wood framed window",
            "hole where a window would fit",
        ],
        "railing": [
            "railing",
            "metal tubular railing",
            "tempered glass railing",
            "wood railing system",
            "wall mounted handrail",
            "steel cable railing"
        ],
        "furniture": [
            "furniture"
        ],
        "waste terminal": [
            "waste terminal",
            "floor drain grate",
            "siphoned drain box cover",
            "wall mounted sewage outlet",
            "stormwater collection grate",
            "linear drain channel",
            "toilet discharge outlet"
        ]
    }


    model = Model(
        model_config_path=config_path,
        model_checkpoint_path=weights_path,
        device="cuda" if torch.cuda.is_available() else "cpu"
    )

    image = cv2.imread(image_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    results = {}

    for prompt in prompts:
        detections = model.predict_with_caption(
            image_rgb,
            caption= ". ".join(prompts[prompt]),
            box_threshold=0.35,
            text_threshold=0.35
        )

        boxes, phrases = detections
        count = len(boxes)
        results[prompt] = {
            "count": count,
            "boxes": boxes,
            "phrases": phrases,
            "category": prompt,
        }

    return results

def get_storey(space):
    for rel in space.Decomposes:
        if rel.RelatingObject.is_a("IfcBuildingStorey"):
            return rel.RelatingObject
    return None

def get_storey_elements(storey):
    elements = []
    for rel in storey.ContainsElements:
        elements.extend(rel.RelatedElements)
    return elements

def process_ifc(file):
    ifc = ifcopenshell.open(file)
    spaces = ifc.by_type("IfcSpace")

    translator = {
    'IfcWall' : 'wall',
    'IfcCovering' : 'covering',
    'IfcDoor' : 'door',
    'IfcStairFlight' : 'stair',
    'IfcCurtainWall' : 'curtainwall',
    'IfcSanitaryTerminal' : 'sanitary terminal',
    'IfcSlab' : 'slab',
    'IfcBuildingElementProxy' : 'building element proxy',
    'IfcDiscreteAccessory' : 'discrete accessory',
    'IfcWindow' : 'window',
    'IfcRailing' : 'railing',
    'IfcFurniture' : 'furniture',
    'IfcStair' : 'stair',
    'IfcWasteTerminal': 'waste terminal',
    }

    elems = {}

    for space in spaces:

        storey = get_storey(space)
        storey_elements = get_storey_elements(storey)

        if storey not in elems:
            elems[storey] = {}
        for element in storey_elements:
            el = translator[element.is_a()]
            if el not in elems[storey].keys():
                elems[storey][el] = 1
            else:
                aux = elems[storey][el]
                aux+=1
                elems[storey][el] = aux
    
    return elems

results_images = detect_images('beam.png').keys()
results_ifc = process_ifc("MB-1.04.04.00-6B3-1001-1_v32.ifc")

print(results_images)
print(results_ifc)

