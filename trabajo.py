import json
from typing import List, Dict

class Proyecto:
    def __init__(self, nombre: str):
        self.nombre = nombre
        self.tareas: List[Dict[str, str]] = []
        self.equipo: List[str] = []
        self.matriz_asignacion: List[List[int]] = []

    def agregar_tarea(self, tarea: str, estado: str = "Pendiente"):
        self.tareas.append({"nombre": tarea, "estado": estado})

    def agregar_miembro(self, miembro: str):
        self.equipo.append(miembro)

    def asignar_tareas(self):
        self.matriz_asignacion = [[0 for _ in range(len(self.tareas))] for _ in range(len(self.equipo))]

    def asignar_tarea(self, miembro_index: int, tarea_index: int):
        try:
            self.matriz_asignacion[miembro_index][tarea_index] = 1
        except IndexError:
            print(f"Error: Índices fuera de rango. Miembro: {miembro_index}, Tarea: {tarea_index}")

    def guardar_proyecto(self, archivo: str):
        datos = {
            "nombre": self.nombre,
            "tareas": self.tareas,
            "equipo": self.equipo,
            "matriz_asignacion": self.matriz_asignacion
        }
        try:
            with open(archivo, 'w') as f:
                json.dump(datos, f)
        except IOError as e:
            print(f"Error al guardar el archivo: {e}")

    def cargar_proyecto(self, archivo: str):
        try:
            with open(archivo, 'r') as f:
                datos = json.load(f)
                self.nombre = datos["nombre"]
                self.tareas = datos["tareas"]
                self.equipo = datos["equipo"]
                self.matriz_asignacion = datos["matriz_asignacion"]
        except (IOError, json.JSONDecodeError) as e:
            print(f"Error al cargar el archivo: {e}")

    def generar_reporte(self, nivel: int = 0) -> str:
        espacios = "  " * nivel
        reporte = f"{espacios}Proyecto: {self.nombre}\n"
        
        reporte += f"{espacios}Equipo:\n"
        for miembro in self.equipo:
            reporte += f"{espacios}  - {miembro}\n"
        
        reporte += f"{espacios}Tareas:\n"
        for i, tarea in enumerate(self.tareas):
            reporte += f"{espacios}  {i+1}. {tarea['nombre']} ({tarea['estado']})\n"
            reporte += self.generar_reporte_asignaciones(i, nivel + 2)
        
        return reporte

    def generar_reporte_asignaciones(self, tarea_index: int, nivel: int) -> str:
        espacios = "  " * nivel
        reporte = f"{espacios}Asignada a:\n"
        for i, asignacion in enumerate(self.matriz_asignacion):
            if asignacion[tarea_index] == 1:
                reporte += f"{espacios}  - {self.equipo[i]}\n"
        return reporte

# Ejemplo de uso
if __name__ == "__main__":
    proyecto = Proyecto("Sistema de Gestión de Inventario")
    
    # Agregar tareas
    proyecto.agregar_tarea("Diseño de base de datos")
    proyecto.agregar_tarea("Implementación de backend")
    proyecto.agregar_tarea("Desarrollo de interfaz de usuario")
    
    # Agregar miembros del equipo
    proyecto.agregar_miembro("Ana")
    proyecto.agregar_miembro("Carlos")
    proyecto.agregar_miembro("Elena")
    
    # Asignar tareas
    proyecto.asignar_tareas()
    proyecto.asignar_tarea(0, 0)  # Ana - Diseño de base de datos
    proyecto.asignar_tarea(1, 1)  # Carlos - Implementación de backend
    proyecto.asignar_tarea(2, 2)  # Elena - Desarrollo de interfaz de usuario
    
    # Guardar proyecto
    proyecto.guardar_proyecto("proyecto.json")
    
    # Cargar proyecto
    nuevo_proyecto = Proyecto("")
    nuevo_proyecto.cargar_proyecto("proyecto.json")
    
    # Generar y mostrar reporte
    print(nuevo_proyecto.generar_reporte())

