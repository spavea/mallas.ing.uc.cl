from typing import Literal

from unidecode import unidecode

from app.plan.courseinfo import CourseDetails, CourseInfo
from app.plan.validation.curriculum.tree import (
    SUPERBLOCK_PREFIX,
    Combination,
    Curriculum,
    CurriculumSpec,
    Leaf,
    Multiplicity,
)


def _skip_extras(curriculum: Curriculum):
    # Saltarse los ramos de 0 creditos del bloque de "Requisitos adicionales para
    # obtener el grado de Licenciado...", excepto por la Practica I
    # Razones:
    # - Hay un ramo que se llama "Aprendizaje Universitario" que no sale en Seguimiento
    #   Curricular, y ni idea que es
    # - El test de ingles tiene requisitos incumplibles de forma normal, por lo que el
    #   recomendador no logra colocarlo
    # - Es buena idea mantener la practica si, porque hay algunos ramos que tienen la
    #   practica de requisito.
    #   Tambien, la practica puede contar como optativo de fundamentos. Para que la
    #   practica no se pinte de Plan Comun, hay que dirigirla a otro bloque.
    # Esto significa que los cursos no tendran un bloque para el que contar y no se
    # generaran automaticamente. Sin embargo, si un estudiante los tiene entre sus
    # cursos tomados los cursos no se eliminan.

    for superblock in curriculum.root.children:
        if not isinstance(superblock, Combination):
            continue
        if not all(block.cap == 1 for block in superblock.children):
            continue
        superblock.children = [
            b
            for b in superblock.children
            if "Practica" in b.debug_name or "Práctica" in b.debug_name
        ]


# Tabla que mapea la primera palabra del nombre textual de un bloque academico del major
# a un nombre mas machine-readable
C2020_SUPERBLOCK_TABLE = {
    "ciencias": "PlanComun",
    "base": "PlanComun",
    "formacion": "FormacionGeneral",
    "major": "Major",
}
C2022_SUPERBLOCK_TABLE = {
    "matematicas": "PlanComun",
    "fundamentos": "PlanComun",
    "formacion": "FormacionGeneral",
    "major": "Major",
}


def _identify_superblocks(spec: CurriculumSpec, curriculum: Curriculum):
    # Cambia los codigos de los bloques academicos a nombres "machine readable".
    # Por ejemplo, cambia "Ingeniero Civil en Computación" a 'title'
    for superblock in curriculum.root.children:
        if not superblock.block_code.startswith(SUPERBLOCK_PREFIX):
            continue
        og_superblock_id = superblock.block_code[len(SUPERBLOCK_PREFIX) :]
        # Heuristica: tomar la primera palabra, normalizarla (quitarle los tildes y todo
        # a minúscula) y buscar en una tabla hardcodeada.
        id_words = unidecode(og_superblock_id).lower().split()
        if len(id_words) < 1:
            continue
        match spec.cyear.raw:
            case "C2020":
                superblock_table = C2020_SUPERBLOCK_TABLE
            case "C2022":
                superblock_table = C2022_SUPERBLOCK_TABLE
        superblock_id = superblock_table.get(id_words[0], og_superblock_id)
        superblock.block_code = f"{SUPERBLOCK_PREFIX}{superblock_id}"


# Identifica a los bloques de OFG de C2020.
C2020_OFG_BLOCK_CODE = "courses:!L1"


def _merge_c2020_ofgs(curriculum: Curriculum):
    # Junta los bloques de OFG de 10 creditos en un bloque grande de OFG
    # El codigo de lista para los OFG es `!L1`
    for superblock in curriculum.root.children:
        if not isinstance(superblock, Combination):
            continue
        # Junta todos los bloques que son OFG en una lista
        l1_blocks: list[Leaf] = [
            block
            for block in superblock.children
            if isinstance(block, Leaf) and block.block_code == C2020_OFG_BLOCK_CODE
        ]
        if len(l1_blocks) > 0:
            # Elimina todos los bloques que son OFG de `superblock.children`
            superblock.children = [
                block
                for block in superblock.children
                if block.block_code != C2020_OFG_BLOCK_CODE
            ]
            # Juntar todos los bloques OFG en un bloque y agregarlo de vuelta
            total_cap = sum(block.cap for block in l1_blocks)
            superblock.children.append(
                Leaf(
                    debug_name=l1_blocks[0].debug_name,
                    block_code=C2020_OFG_BLOCK_CODE,
                    name=l1_blocks[0].name,
                    cap=total_cap,
                    codes=l1_blocks[0].codes,
                ),
            )


def _allow_selection_duplication(courseinfo: CourseInfo, curriculum: Curriculum):
    # Los ramos de seleccion deportiva pueden contar hasta 2 veces (la misma sigla!)
    # Los ramos de seleccion deportiva se definen segun SIDING como los ramos DPT que
    # comienzan con "Seleccion"
    for superblock in curriculum.root.children:
        if not isinstance(superblock, Combination):
            continue
        for block in superblock.children:
            if isinstance(block, Leaf) and block.block_code == C2020_OFG_BLOCK_CODE:
                for code in block.codes:
                    if not code.startswith("DPT"):
                        continue
                    info = courseinfo.try_course(code)
                    if info is None:
                        continue
                    if info.name.startswith("Seleccion ") or info.name.startswith(
                        "Selección ",
                    ):
                        # Permitir que cuenten por el doble de creditos de lo normal
                        curriculum.multiplicity[code] = Multiplicity(
                            group={code},
                            credits=2 * info.credits,
                        )
                # Only do it once
                return


# Los cursos de optativo en ciencias.
C2020_OFG_SCIENCE_OPTS = {
    "BIO014",
    "EYP2355",
    "ELM2431",
    "EYP290I",
    "FIZ0314",
    "FIS1542",
    "FIZ0311",
    "FIZ0222",
    "FIZ0223",
    "FIZ0313",
    "FIZ1428",
    "MAT2205",
    "MAT255I",
    "MLM2221",
    "MLM2301",
    "MAT2305",
    "MLM2401",
    "MLM2411",
    "MLM251I",
    "MAT251I",
    "MLM2541",
    "MLM260I",
    "MAT2605",
    "QIM121",
    "QIM122",
    "QIM124",
    "QIM109A",
    "QIM130",
    "QIM200",
    "QUN1003",
    "MAT2565",
    "FIZ0315",
    "FIZ0312",
    "MAT380I",
    "FIS0104",
    "MAT270I",
    "QIM202",
    "FIZ0614",
    "FIZ2110",
}


def _ofg_classify(
    info: CourseDetails,
) -> Literal["limited"] | Literal["unlimited"] | Literal["science"]:
    if info.code in C2020_OFG_SCIENCE_OPTS:
        return "science"
    if info.credits != 5:
        return "unlimited"
    if info.code.startswith(("DPT", "RII", "CAR")) or info.code in (
        "MEB158",
        "MEB166",
        "MEB174",
    ):
        return "limited"
    return "unlimited"


def _ofg_is_limited(courseinfo: CourseInfo, code: str):
    info = courseinfo.try_course(code)
    if info is None:
        return True
    return _ofg_classify(info) == "limited"


def _ofg_is_unlimited(courseinfo: CourseInfo, code: str):
    info = courseinfo.try_course(code)
    if info is None:
        return True
    return _ofg_classify(info) != "unlimited"


def _ofg_is_science(courseinfo: CourseInfo, code: str):
    info = courseinfo.try_course(code)
    if info is None:
        return True
    return _ofg_classify(info) == "science"


def _limit_ofg10(courseinfo: CourseInfo, curriculum: Curriculum):
    # https://intrawww.ing.puc.cl/siding/dirdes/web_docencia/pre_grado/formacion_gral/alumno_2020/index.phtml
    # En el bloque de OFG hay algunos cursos de 5 creditos que en conjunto pueden
    # contribuir a lo mas 10 creditos:
    # - DPT (deportivos)
    # - RII (inglés)
    # - CAR (CARA)
    # - OFG plan antiguo (MEB158, MEB166 y MEB174)

    # Ademas, agrega hasta 10 creditos de optativo en ciencias.
    #
    # Se pueden tomar hasta 10 creditos de optativo de ciencias, que es una
    # lista separada que al parecer solo esta disponible en forma textual.
    # Los ramos de esta lista no son parte de la lista `!L1` que brinda
    # SIDING, y tampoco sabemos si esta disponible en otra lista.
    # La lista L3 se ve prometedora, incluso incluye un curso "ING0001
    # Optativo En Ciencias" generico, pero no es exactamente igual al listado
    # textual en SIDING.
    #
    # Referencias:
    # "Además, es válido para avance curricular de OFG máximo 1 curso
    # optativo en ciencias (10 cr.) de una lista de cursos Optativos de
    # Ciencia, o su equivalente, definida por el Comité Curricular de la
    # Escuela de Ingeniería."
    # https://intrawww.ing.puc.cl/siding/dirdes/web_docencia/pre_grado/optativos/op_ciencias/alumno_2020/index.phtml
    # https://intrawww.ing.puc.cl/siding/dirdes/web_docencia/pre_grado/formacion_gral/alumno_2020/index.phtml

    for superblock in curriculum.root.children:
        if not isinstance(superblock, Combination):
            continue
        for block_i, block in enumerate(superblock.children):
            if isinstance(block, Leaf) and block.block_code == C2020_OFG_BLOCK_CODE:
                # Segregar los cursos de 5 creditos que cumplan los requisitos
                limited: set[str] = set()
                unlimited: set[str] = set()
                science: set[str] = set()
                for code in block.codes:
                    if _ofg_is_limited(courseinfo, code):
                        limited.add(code)
                    if _ofg_is_unlimited(courseinfo, code):
                        unlimited.add(code)
                    if _ofg_is_science(courseinfo, code):
                        science.add(code)
                # Separar el bloque en 3
                limited_block = Leaf(
                    debug_name=f"{block.debug_name} (máx. 10 creds. DPT y otros)",
                    block_code=f"{C2020_OFG_BLOCK_CODE}:limited",
                    name=None,
                    cap=10,
                    codes=limited,
                )
                unlimited_block = Leaf(
                    debug_name=f"{block.debug_name} (genérico)",
                    block_code=f"{C2020_OFG_BLOCK_CODE}:unlimited",
                    name=None,
                    cap=block.cap,
                    codes=unlimited,
                )
                science_block = Leaf(
                    debug_name=f"{block.debug_name} (optativo de ciencias)",
                    block_code=f"{C2020_OFG_BLOCK_CODE}:science",
                    name=None,
                    cap=10,
                    codes=science,
                )
                block = Combination(
                    debug_name=block.debug_name,
                    block_code=f"{C2020_OFG_BLOCK_CODE}:root",
                    name=block.name,
                    cap=block.cap,
                    children=[
                        # Este orden es importante!
                        # El solver aun no soporta manejar el caso cuando ocurre
                        # "split-flow", que es cuando un curso divide su creditaje entre
                        # dos bloques.
                        # Esto *probablemente* no es legal, pero es *muy* dificil que
                        # ocurra realmente.
                        # Sin embargo, si las prioridades estan mal seteadas, puede
                        # ocurrir un caso en que el solver en su intento de optimizar
                        # cause split-flow
                        # Si estuviera `limited_block` primero, `unlimited_block`
                        # segundo y hubiera un ramo DPT de 5 creditos, se llenaria
                        # `limited_block` con el ramo DPT, y la siguiente equivalencia
                        # de 10 creditos se repartiria 5 en `limited_block` (porque
                        # quedan 5 creditos de espacio) y 5 en `unlimited_block`, porque
                        # `limited_block` tendria mas prioridad.
                        # Por ahora lo podemos arreglar invirtiendo las prioridades.
                        unlimited_block,
                        limited_block,
                        science_block,
                    ],
                )
                superblock.children[block_i] = block


def _c2020_defer_general_ofg(curriculum: Curriculum):
    # Hacer que los ramos de relleno de OFG se prefieran sobre los ramos de relleno de
    # teologico, para que no se autogenere un teologico y se tome el curso teologico
    # como OFG
    if "!L1" in curriculum.fillers:
        for filler in curriculum.fillers["!L1"]:
            filler.cost_offset -= 1


def _c2022_defer_free_area_ofg(curriculum: Curriculum):
    # Hacer que los ramos de relleno de area libre se prefieran sobre los ramos de
    # relleno de area restringida, para que no se autogenere un area restringida y se
    # tome el curso pasado como area libre
    if "!C10351" in curriculum.fillers:
        for filler in curriculum.fillers["!C10351"]:
            filler.cost_offset -= 1


def patch_major(
    courseinfo: CourseInfo,
    spec: CurriculumSpec,
    curr: Curriculum,
) -> Curriculum:
    """
    Aplicar reglas del plan comun y el major.
    """

    _skip_extras(curr)
    _identify_superblocks(spec, curr)

    match spec.cyear.raw:
        case "C2020":
            # NOTE: El orden en que se llama a estas funciones es importante
            _merge_c2020_ofgs(curr)
            _limit_ofg10(courseinfo, curr)
            _c2020_defer_general_ofg(curr)
            _allow_selection_duplication(courseinfo, curr)
        case "C2022":
            _c2022_defer_free_area_ofg(curr)
            _allow_selection_duplication(courseinfo, curr)

    return curr
