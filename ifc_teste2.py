import ifcopenshell
import ifcopenshell.geom
from shapely.geometry import shape
from shapely import wkt
from collections import Counter

# ===============================================================
# CONFIGURAÇÃO DO MOTOR GEOMÉTRICO
# ===============================================================
settings = ifcopenshell.geom.settings()
settings.set(settings.USE_WORLD_COORDS, True)


# ===============================================================
# Função: converter geometria IFC para polígono Shapely
# ===============================================================
def ifc_shape_to_shapely(ifc_shape):
    # Converte a geometria IFC para WKT
    wkt_rep = ifc_shape.geometry.wkt
    return wkt.loads(wkt_rep)


# ===============================================================
# Função: obter storey ao qual o espaço pertence
# ===============================================================
def get_storey(space):
    if not hasattr(space, "Decomposes"):
        return None
    for rel in space.Decomposes:
        if rel.RelatingObject.is_a("IfcBuildingStorey"):
            return rel.RelatingObject
    return None


# ===============================================================
# Função: pegar todos os elementos contidos no storey
# ===============================================================
def get_elements_from_storey(storey):
    elements = []
    if hasattr(storey, "ContainsElements"):
        for rel in storey.ContainsElements:
            elements += rel.RelatedElements
    return elements


# ===============================================================
# Função: verificar se o elemento toca/intersecta o espaço
# ===============================================================
def element_intersects_space(ifc, space, element):
    try:
        s_geom = ifcopenshell.geom.create_shape(settings, space)
        e_geom = ifcopenshell.geom.create_shape(settings, element)

        s_poly = shape(wkt.loads(s_geom.geometry.wkt))
        e_poly = shape(wkt.loads(e_geom.geometry.wkt))

        return s_poly.intersects(e_poly)

    except:
        return False


# ===============================================================
# Função: pegar elementos que pertencem ao espaço
# ===============================================================
def get_elements_in_space(ifc, space):
    storey = get_storey(space)
    if storey is None:
        return []

    storey_elements = get_elements_from_storey(storey)

    elements_in_space = []
    for el in storey_elements:
        if element_intersects_space(ifc, space, el):
            elements_in_space.append(el)

    return elements_in_space


# ===============================================================
# PROCESSAMENTO PRINCIPAL
# ===============================================================
def process_ifc(file_path):
    ifc = ifcopenshell.open(file_path)
    spaces = ifc.by_type("IfcSpace")

    results = {}

    for space in spaces:
        print(f"Processando espaço: {space.LongName or space.Name}")

        elements = get_elements_in_space(ifc, space)
        counter = Counter(el.is_a() for el in elements)

        results[space] = counter

        print("→ Elementos encontrados:")
        for typ, qty in counter.items():
            print(f"   {typ}: {qty}")
        print("-----------------------\n")

    return results


# ===============================================================
# EXECUTAR
# ===============================================================
process_ifc("MB-1.04.04.00-6B3-1001-1_v32.ifc")
