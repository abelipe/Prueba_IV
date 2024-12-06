import pandas as pd
from munkres import Munkres, make_cost_matrix


class TaskAssignment:
    def __init__(self, cost_matrix: list[list[int]]):
        """
        Inicializa la matriz de costos y asegura que esté balanceada.
        :param cost_matrix: matriz de costos en formato bidimensional.
        """
        self.original_matrix = cost_matrix
        self.cost_matrix = [
            row[:] for row in cost_matrix
        ]  # Copia de la matriz original
        self.balance_matrix()

    def balance_matrix(self):
        """
        Balancea la matriz añadiendo filas o columnas ficticias con costo cero para igualar dimensiones.
        """
        rows = len(self.cost_matrix)
        cols = len(self.cost_matrix[0])
        print("\n=== Paso 1: Verificar balanceo de la matriz ===")
        print(f"Tamaño inicial: {rows} filas x {cols} columnas")

        if rows > cols:
            for row in self.cost_matrix:
                row.extend([0] * (rows - cols))
            print(f"Se añadieron {rows - cols} columnas ficticias con costo 0.")
        elif cols > rows:
            for _ in range(cols - rows):
                self.cost_matrix.append([0] * cols)
            print(f"Se añadieron {cols - rows} filas ficticias con costo 0.")
        else:
            print("La matriz ya está balanceada.")

        self.display_matrix("Matriz Balanceada")

    def display_matrix(self, title="Matriz Actual"):
        """
        Muestra la matriz en pantalla en formato de tabla.
        """
        print(f"\n{title}:")
        df = pd.DataFrame(self.cost_matrix)
        print(
            df.to_string(
                index=False,
                header=[f"Tarea {i+1}" for i in range(len(self.cost_matrix[0]))],
            )
        )

    def solve_with_munkres(self):
        """
        Resuelve el problema usando la librería Munkres.
        :return: solución y costo total.
        """
        print("\n=== Paso 2: Resolviendo con Munkres ===")
        munkres = Munkres()
        indexes = munkres.compute(self.cost_matrix)
        total_cost = sum(self.cost_matrix[row][col] for row, col in indexes)

        print("\nAsignaciones óptimas:")
        solution_table = []
        for row, col in indexes:
            solution_table.append(
                {
                    "Programador": f"Programador {row + 1}",
                    "Tarea": f"Tarea {col + 1}",
                    "Costo": self.cost_matrix[row][col],
                }
            )
        df = pd.DataFrame(solution_table)
        print(df.to_string(index=False))
        print(f"\nCosto Total (Munkres): {total_cost}\n")
        return indexes, total_cost

    def solve_without_library(self):
        """
        Resuelve el problema de asignación sin usar librerías.
        :return: solución y costo total.
        """
        print("\n=== Paso 3: Resolviendo sin librerías ===")
        num_rows = len(self.cost_matrix)
        num_cols = len(self.cost_matrix[0])
        used_cols = set()
        solution = []
        total_cost = 0

        for row in range(num_rows):
            min_cost = float("inf")
            selected_col = -1
            for col in range(num_cols):
                if col not in used_cols and self.cost_matrix[row][col] < min_cost:
                    min_cost = self.cost_matrix[row][col]
                    selected_col = col
            if selected_col != -1:
                solution.append((row, selected_col))
                total_cost += min_cost
                used_cols.add(selected_col)

        print("\nAsignaciones óptimas:")
        solution_table = []
        for row, col in solution:
            solution_table.append(
                {
                    "Programador": f"Programador {row + 1}",
                    "Tarea": f"Tarea {col + 1}",
                    "Costo": self.cost_matrix[row][col],
                }
            )
        df = pd.DataFrame(solution_table)
        print(df.to_string(index=False))
        print(f"\nCosto Total (Manual): {total_cost}\n")
        return solution, total_cost

    def optimize_assignment(self):
        """
        Ofrece opciones de optimización y muestra la solución paso a paso.
        """
        print("\n=== Opciones de Optimización ===")
        print("1. Optimizar usando Munkres")
        print("2. Optimizar sin librerías")
        choice = input("Seleccione una opción (1 o 2): ")

        if choice == "1":
            indexes, total_cost = self.solve_with_munkres()
        elif choice == "2":
            indexes, total_cost = self.solve_without_library()
        else:
            print("Opción no válida. Intente nuevamente.")
            return self.optimize_assignment()

        # Mostrar la matriz de solución final
        solution_matrix = [
            ["" for _ in range(len(self.cost_matrix[0]))]
            for _ in range(len(self.cost_matrix))
        ]
        for row, col in indexes:
            solution_matrix[row][col] = f"✓ ({self.cost_matrix[row][col]})"
        self.cost_matrix = solution_matrix
        self.display_matrix("Matriz de Solución")


# Ejemplo de uso del programa
if __name__ == "__main__":
    # Matriz de costos de ejemplo
    print("=== Matriz de Costos Inicial ===")
    #               Tarea 1, Tarea 2, Tarea N
    #Programador 1     10      5        N
    #Programador 2
    #Programador N
    
    cost_matrix = [
        [48, 48, 50, 44],
        [56, 60, 60, 68],
        [96, 94, 90, 85],
        [42, 44, 54, 46],
    ]
    df = pd.DataFrame(
        cost_matrix,
        columns=[f"Tarea {i+1}" for i in range(len(cost_matrix[0]))],
        index=[f"Programador {i+1}" for i in range(len(cost_matrix))],
    )
    print(df.to_string())

    # Instanciar la clase y resolver
    assignment = TaskAssignment(cost_matrix)
    assignment.optimize_assignment()
