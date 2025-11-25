import ifcopenshell

ifc = ifcopenshell.open("MB-1.04.04.00-6B3-1001-1_v32.ifc")
spaces = ifc.by_type("IfcSpace")
print(f"Total de spaces: {len(spaces)}")

elementos = {}
i = 0


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

for space in spaces:
    i+=1
    storey = get_storey(space)
    elementos[storey] = {'mínimo': True}
    storey_elements = get_storey_elements(storey)
    for element in storey_elements:
        el = element.is_a()
        if el not in elementos[storey].keys():
            elementos[storey][el] = 1
        else:
            aux = elementos[storey][el]
            aux+=1
            elementos[storey][el] = aux


print(len(elementos.keys()))
print(i)
