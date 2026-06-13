#!/usr/bin/env python3
"""
Grafo de artefactos para gestionar dependencias, bloqueo e invalidaciÃ³n.
"""

from __future__ import annotations

from collections import deque


class ArtifactGraph:
    """Grafo acÃ­clico dirigido simple para plan y reglas."""

    def __init__(self) -> None:
        self.deps: dict[str, set[str]] = {}
        self.states: dict[str, str] = {}

    def add_artifact(self, name: str, depends_on: list[str] | None = None) -> None:
        """AÃ±ade un nodo al grafo con sus dependencias."""
        self.deps[name] = set(depends_on or [])
        self.states[name] = "pending"

    def mark_completed(self, name: str) -> None:
        """Marca un artefacto como completado."""
        if name in self.states:
            self.states[name] = "completed"

    def invalidate(self, name: str) -> None:
        """Marca un artefacto como stale e invalida dependientes en cascada."""
        if name not in self.states or self.states[name] == "stale":
            return

        self.states[name] = "stale"
        for artifact, dependencies in self.deps.items():
            if name in dependencies:
                self.invalidate(artifact)

    def get_ready_tasks(self) -> list[str]:
        """Retorna tareas cuyos requisitos estÃ¡n completados."""
        ready: list[str] = []
        for name, dependencies in self.deps.items():
            if self.states.get(name) == "pending" and all(
                self.states.get(dep) == "completed" for dep in dependencies
            ):
                ready.append(name)
        return ready

    def get_build_order(self) -> list[str]:
        """Calcula el orden topolÃ³gico y detecta ciclos."""
        in_degree = {
            node: len(dependencies) for node, dependencies in self.deps.items()
        }
        queue = deque(node for node, degree in in_degree.items() if degree == 0)
        order: list[str] = []

        while queue:
            node = queue.popleft()
            order.append(node)
            for dependent, dependencies in self.deps.items():
                if node in dependencies:
                    in_degree[dependent] -= 1
                    if in_degree[dependent] == 0:
                        queue.append(dependent)

        if len(order) != len(self.deps):
            nodes_in_cycle = [node for node, degree in in_degree.items() if degree > 0]
            raise ValueError(
                f"Ciclo detectado en el grafo de artefactos: {nodes_in_cycle}"
            )

        return order

    def get_blocked(self) -> dict[str, list[str]]:
        """Identifica tareas bloqueadas y sus dependencias pendientes."""
        blocked: dict[str, list[str]] = {}
        for name, dependencies in self.deps.items():
            if self.states.get(name) != "completed":
                unresolved = [
                    dep for dep in dependencies if self.states.get(dep) != "completed"
                ]
                if unresolved:
                    blocked[name] = unresolved
        return blocked


if __name__ == "__main__":
    graph = ArtifactGraph()
    graph.add_artifact("WP-Fase1")
    graph.add_artifact("WP-Fase2", ["WP-Fase1"])

    print(f"Orden de construcciÃ³n: {graph.get_build_order()}")
    graph.mark_completed("WP-Fase1")
    print(f"Tareas listas: {graph.get_ready_tasks()}")
    print(f"Tareas bloqueadas: {graph.get_blocked()}")

    graph.invalidate("WP-Fase1")
    print(f"Fase2 state after invalidation: {graph.states['WP-Fase2']}")

