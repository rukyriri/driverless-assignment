"""Candidate solution for the assignment "Map, Data Association & Path Planning".

Run it with::

    python3 solution.py

The script executes the full pipeline step by step and stops at the first
step you have not implemented yet, with a reminder of what is missing.
Implement the three functions below (``associate``, ``correct_map``,
``find_path``), keeping their names and signatures unchanged.
"""

import math
from typing import List, Tuple

from map_generation import Map, Point, generate_map, generate_observations
from visualization import (
    visualize_association_n_correction,
    visualize_map_n_observations,
    visualize_path,
)

# ---------------------------------------------------------------------------
# Parameters of the run.
#
# Feel free to experiment with them, but note that your solution will also be
# evaluated with different values (especially with different random seeds).
# ---------------------------------------------------------------------------
NUM_POINTS = 40
X_RANGE = 20.0
Y_RANGE = 20.0
MAP_SEED = 453

NOISE_STD = 0.25
OBSERVATION_RATE = 0.8
OBSERVATIONS_SEED =6
#OWN VARIABLES
tipoCamino = 0

# ---------------------------------------------------------------------------
# Provided helper
# ---------------------------------------------------------------------------

def path_length(points: List[Point], path: List[int]) -> float:
    """Total Euclidean length of ``path`` over ``points``.

    Useful to measure how short your path is, e.g. when going for Bonus 1.
    The length is the sum of the Euclidean distances between the consecutive
    nodes of the path.
    """
    return sum(math.dist(points[a], points[b]) for a, b in zip(path, path[1:]))

#
#
def distancia(p, q)->float:
    sol = (p[0] - q[0])** 2 + (p[1] - q[1])**2
    return sol

#
# ---------------------------------------------------------------------------
# Step 3 -- Data association (yours to implement)
# ---------------------------------------------------------------------------

def associate(map_points: Map, observations: List[Point]) -> List[Tuple[int, int]]:
    n = NUM_POINTS
    sol = []
    distancias = []
    for i, a in enumerate(observations):
        for j, b in enumerate(map_points):
            distancias.append((distancia(a, b), i, j))
    distancias.sort()
    UM = []
    UO = []
    
    for i in range(len(distancias)):
        
        d, o, m = distancias[i]
        
        if m not in UM and o not in UO:
            UM.append(m)
            UO.append(o)
            sol.append((m, o))
                
    return sol
            

   
    
    """Associate every observation with the map point it was generated from.

    Given the map and the observations (noisy, incomplete and shuffled),
    recover the observation-to-map-point correspondence.

    Returns:
        The association couples as a list of ``(map_index, observation_index)``
        tuples, e.g. ``[(0, 12), (3, 5)]`` means that observation 12 was
        generated from map point 0, and observation 5 from map point 3.
    """
    raise NotImplementedError("Step 3 (data association) is yours to implement")


# ---------------------------------------------------------------------------
# Step 4 -- Map correction (yours to implement)
# ---------------------------------------------------------------------------

def correct_map(
    map_points: Map,
    observations: List[Point],
    associations: List[Tuple[int, int]],
) -> Map:
    for i, j in associations:
        map_points[i] = ((map_points[i][0] + observations[j][0]) / 2, (map_points[i][1] + observations[j][1]) / 2)
    return map_points

    """Correct the map, given the data association.

    For every association couple ``(i, j)``, the corrected position of map
    point ``i`` is the average (midpoint) of ``map_points[i]`` and
    ``observations[j]``. Map points without an associated observation keep
    their original position.

    Returns:
        The corrected map: a list of ``(x, y)`` tuples with the same length
        and the same order as ``map_points``.
    """
    raise NotImplementedError("Step 4 (map correction) is yours to implement")


# ---------------------------------------------------------------------------
# Step 5 -- Path finding (yours to implement)
# ---------------------------------------------------------------------------
def ordenarGraham(puntos, pivote):
    resto = [p for p in puntos if p != pivote]
    resto = sorted(
        resto,
        key=lambda p: math.atan2(p[1] - pivote[1], p[0] - pivote[0])
    )
    resto.insert(0, pivote)
    return resto
def cruz(p1, p2, p3):
    return (p2[0]-p1[0])*(p3[1]-p1[1]) - (p2[1]-p1[1])*(p3[0]-p1[0])
def hull(pivote, ordenados):
    pila = [pivote, ordenados[1]]
    for c in ordenados[2:]:
        while len(pila) >= 2 and cruz(pila[-2], pila[-1], c) <= 0:
            pila.pop()
        pila.append(c)
    return pila
def calcular_centro(puntos):
    aux = []
    for p in puntos:
        aux.append((distancia(p, (0, 0)), p))
    aux.sort()
    return aux[0][1]
def calculoGraham(p1, p2, p3):
    return (math.dist(p1, p3) + math.dist(p2, p3) - math.dist(p2, p1))
def find_path(corrected_map: Map) -> List[int]:
    if(tipoCamino == 1):
        sol = []
        aux = []
        for i, (x, y) in enumerate(corrected_map):
            aux.append((x, y, i))
        aux.sort()
        for i in aux:
            sol.append(i[2])
        return sol
    if(tipoCamino == 2):
        sol1 = []
        sol2 = []
        aux1 = []
        aux2 = []
        for i, (x, y) in enumerate(corrected_map):
            aux1.append((y, x, i))
            aux2.append((x, y, i))
        aux1.sort()
        aux2.sort()
        for i in aux1:
            sol1.append(i[2])
        for i in aux2:
            sol2.append(i[2])
        if(path_length(corrected_map, sol1) < path_length(corrected_map, sol2)):
            return sol1
        return sol2
    poligono = []
    aux = corrected_map.copy()
    aux.sort(key= lambda p: (p[1], p[0]))
    aux = ordenarGraham(aux, aux[0])
    hull_map = hull(aux[0], aux)
    indice = {p: i for i, p in enumerate(corrected_map)}
    poligono = [indice[p] for p in hull_map]
    centro = calcular_centro(corrected_map)
    resto = [p for p in corrected_map if p not in hull_map]
    aux = []
    for p in resto:
        aux.append((distancia(p, centro), p))  
    aux.sort(key = lambda x: x[0], reverse=True)
    
    for d, p in aux:
        distmin = math.inf
        for i, u in enumerate(hull_map):
            if distmin>calculoGraham(u, hull_map[(i+1)%len(hull_map)], p):
                distmin = calculoGraham(u, hull_map[(i+1)%len(hull_map)], p)
                pos = i
        hull_map.insert(pos+1, p)
    poligono = [indice[p] for p in hull_map]        
    return poligono
    
    """Find a path that visits every node of the corrected map exactly once.

    Return the path as a list of node indices in visit order, e.g.
    ``[4, 0, 11, 2, ...]``. A path that includes each node exactly once is
    usually called a *Hamiltonian path*: any permutation of the node indices
    is a formally valid answer, but:

    * **Bonus 1 (+1 point)**: use a heuristic or an algorithm (e.g. nearest
      neighbour, greedy insertion, 2-opt, ...) so that the total length of
      your path is clearly shorter than the worst possible path. You can
      measure it with :func:`path_length`.

    * **Bonus 2 (+1 point)**: no arrow of the path goes over a previous
      arrow (arrows that only touch at a shared node do not count as
      crossings). You can check it visually with ``visualize_path``.
    """
    raise NotImplementedError("Step 5 (path finding) is yours to implement")


# ---------------------------------------------------------------------------
# Pipeline
# ---------------------------------------------------------------------------

def main() -> None:
    # Step 1 -- Generate the map (provided) ---------------------------------
    map_points = generate_map(
        num_points=NUM_POINTS,
        x_range=X_RANGE,
        y_range=Y_RANGE,
        seed=MAP_SEED,
    )

    # Step 2 -- Generate the observations (provided) ------------------------
    observations = generate_observations(
        map_points,
        noise_std=NOISE_STD,
        observation_rate=OBSERVATION_RATE,
        seed=OBSERVATIONS_SEED,
    )
    visualize_map_n_observations(map_points, observations, X_RANGE, Y_RANGE)

    # Step 3 -- Data association (yours) -------------------------------------
    try:
        associations = associate(map_points, observations)
    except NotImplementedError:
        print("Step 3 is not implemented yet: fill in associate() in solution.py.")
        return

    # Step 4 -- Map correction (yours) ---------------------------------------
    try:
        corrected_map = correct_map(map_points, observations, associations)
    except NotImplementedError:
        print("Step 4 is not implemented yet: fill in correct_map() in solution.py.")
        return
    visualize_association_n_correction(
        map_points,
        observations,
        corrected_map,
        associations,
        X_RANGE,
        Y_RANGE,
    )

    # Step 5 -- Path finding (yours) -----------------------------------------
    try:
        path = find_path(corrected_map)
    except NotImplementedError:
        print("Step 5 is not implemented yet: fill in find_path() in solution.py.")
        return
    visualize_path(corrected_map, path)

    print(
        f"Pipeline complete: {len(associations)} associations over "
        f"{len(observations)} observations, path over {len(corrected_map)} "
        f"nodes with total length {path_length(corrected_map, path):.2f}."
    )


if __name__ == "__main__":
    main()
