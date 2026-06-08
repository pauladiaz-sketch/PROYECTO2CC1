import tkinter as tk
import colores as c 
import random

# ==========================================
# 1. TU CÓDIGO ORIGINAL (SIN ALTERAR)
# ==========================================
class Game(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.grid()
        self.master.title("2048")
        self.main_grid = tk.Frame(self, bg=c.GRID_COLOR, bd=3, width=600, height=600)
        self.main_grid.grid(pady=(100, 0))
        self.make_GUI()
        self.master.bind("<a>", self.left)
        self.master.bind("<d>", self.right)
        self.master.bind("<w>", self.up)
        self.master.bind("<s>", self.down)
        self.master.after(100, self.start_game)
        self.mainloop()

    def make_GUI(self):
        self.cells = []
        for i in range(4):
            row = []
            for j in range(4):
                cell_frame = tk.Frame(
                    self.main_grid, bg=c.EMPTY_CELL_COLOR,
                    width=150,
                    height=150
                )
                cell_frame.grid(row=i, column=j, padx=5, pady=5)
                cell_number = tk.Label(self.main_grid, bg=c.EMPTY_CELL_COLOR)
                cell_number.grid(row=i, column=j)
                cell_data = {"frame": cell_frame, "number": cell_number}
                row.append(cell_data)
            self.cells.append(row)

        score_frame = tk.Frame(self)
        score_frame.place(relx=0.85, y=45, anchor="center")
        tk.Label(score_frame, text="Score", font=c.SCORE_LABEL_FONT).grid(row=0)
        self.score_label = tk.Label(score_frame, text="0", font=c.SCORE_FONT)
        self.score_label.grid(row=1)

    def start_game(self):
        self.matrix=[[0]*4 for _ in range(4)]
        row=random.randint(0,3)
        col=random.randint(0,3)
        self.matrix[row][col]=2
        self.cells[row][col]["frame"].configure(bg=c.CELL_COLORS[2])
        self.cells[row][col]["number"].configure(bg=c.CELL_COLORS[2],fg=c.CELL_NUMBER_COLORS[2],font=c.CELL_NUMBER_FONTS[2], text="2")
        while(self.matrix[row][col]!=0):
            row=random.randint(0,3)
            col=random.randint(0,3)
        self.matrix[row][col]=2
        self.cells[row][col]["frame"].configure(bg=c.CELL_COLORS[2])
        self.cells[row][col]["number"].configure(bg=c.CELL_COLORS[2],fg=c.CELL_NUMBER_COLORS[2],font=c.CELL_NUMBER_FONTS[2], text="2")
        self.score=0

    def stack(self):
        new_matrix=[[0]*4 for _ in range(4)]
        for i in range(4):
            fill_position=0
            for j in range(4):
                if self.matrix[i][j]!=0:
                    new_matrix[i][fill_position]=self.matrix[i][j]
                    fill_position+=1
        self.matrix=new_matrix

    def combine(self):
        for i in range(4):
            for j in range(3):
                if self.matrix[i][j]!=0 and self.matrix[i][j]==self.matrix[i][j+1]:
                    self.matrix[i][j]*=2
                    self.matrix[i][j+1]=0
                    self.score+=self.matrix[i][j]

    def reverse(self):
        new_matrix=[]
        for i in range(4):
            new_matrix.append([])
            for j in range(4):
                new_matrix[i].append(self.matrix[i][3-j])
        self.matrix=new_matrix

    def transpose(self):
        new_matrix=[[0]*4 for _ in range(4)]
        for i in range(4):
            for j in range(4):
                new_matrix[i][j]=self.matrix[j][i]
        self.matrix=new_matrix

    def add_new_tile(self):
        row=random.randint(0,3)
        col=random.randint(0,3)
        while(self.matrix[row][col]!=0):
            row=random.randint(0,3)
            col=random.randint(0,3)
        self.matrix[row][col]=random.choice([2,4])

    def update_GUI(self):
        for i in range(4):
            for j in range(4):
                cell_value=self.matrix[i][j]
                if cell_value==0:
                    self.cells[i][j]["frame"].configure(bg=c.EMPTY_CELL_COLOR)
                    self.cells[i][j]["number"].configure(bg=c.EMPTY_CELL_COLOR, text="")
                else:
                    self.cells[i][j]["frame"].configure(bg=c.CELL_COLORS[cell_value])
                    self.cells[i][j]["number"].configure(bg=c.CELL_COLORS[cell_value],fg=c.CELL_NUMBER_COLORS[cell_value], font=c.CELL_NUMBER_FONTS[cell_value],text=str(cell_value))
        self.score_label.configure(text=self.score)
        self.update_idletasks()

    def left(self,event):
        self.stack()
        self.combine()
        self.stack()
        self.add_new_tile()
        self.update_GUI()

    def right (self,event):
        self.reverse()
        self.stack()
        self.combine()
        self.stack()
        self.reverse()
        self.add_new_tile()
        self.update_GUI()

    def up(self,event):
        self.transpose()
        self.stack()
        self.combine()
        self.stack()
        self.add_new_tile()
        self.update_GUI()

    def down (self,event):
        self.transpose()
        self.reverse()
        self.stack()
        self.combine()
        self.stack()
        self.reverse()
        self.transpose()
        self.add_new_tile()
        self.update_GUI()


# ==========================================
# 2. LOGICA INTELIGENTE PARA EL MODO 3 (IA)
# ==========================================
class IA2048:
    def decidir_movimiento(self, matriz_actual):
        # Evalúa las direcciones y elige la que deje las fichas más ordenadas en las esquinas
        pesos = [[2, 4, 8, 16], [32, 16, 8, 4], [64, 128, 256, 512], [8192, 4096, 2048, 1024]]
        mejor_dir = None
        mejor_score = -1
        
        for direccion in ["left", "right", "up", "down"]:
            matriz = [row[:] for row in matriz_actual]
            # Simulación rápida
            if direccion == "left":
                matriz = self._sim_stack(matriz)
            elif direccion == "right":
                matriz = [r[::-1] for r in self._sim_stack([r[::-1] for r in matriz])]
            elif direccion == "up":
                matriz = self._sim_transpose(self._sim_stack(self._sim_transpose(matriz)))
            elif direccion == "down":
                matriz = self._sim_transpose([r[::-1] for r in self._sim_stack([r[::-1] for r in self._sim_transpose(matriz)])])
                
            if matriz == matriz_actual:
                continue
                
            score_eval = sum(matriz[i][j] * pesos[i][j] for i in range(4) for j in range(4))
            if score_eval > mejor_score:
                mejor_score = score_eval
                mejor_dir = direccion
        return mejor_dir

    def _sim_stack(self, m):
        nm = [[0]*4 for _ in range(4)]
        for i in range(4):
            p = 0
            for j in range(4):
                if m[i][j] != 0:
                    nm[i][p] = m[i][j]; p += 1
        for i in range(4):
            for j in range(3):
                if nm[i][j] != 0 and nm[i][j] == nm[i][j+1]:
                    nm[i][j] *= 2; nm[i][j+1] = 0
        fnm = [[0]*4 for _ in range(4)]
        for i in range(4):
            p = 0
            for j in range(4):
                if nm[i][j] != 0:
                    fnm[i][p] = nm[i][j]; p += 1
        return fnm

    def _sim_transpose(self, m):
        return [[m[j][i] for j in range(4)] for i in range(4)]


# ==========================================
# 3. MODOS EXTRA (HEREDANDO DE TU CÓDIGO)
# ==========================================
class JuegoExtendido(Game):
    def __init__(self, modo, j1, j2):
        self.modo = modo
        self.nombre_j1 = j1
        self.nombre_j2 = j2 if modo == 2 else "Máquina"
        
        self.fase = 1  # 1 = Turno Jugador 1, 2 = Turno Jugador 2 / Máquina
        self.jugador_actual = self.nombre_j1
        self.movimientos_j1 = 0
        self.movimientos_j2 = 0
        self.cant_movimientos = 0
        
        self.historial_resultados = {}
        self.ia = IA2048()
        
        # Llamamos al constructor de tu Game original
        super().__init__()

    def make_GUI(self):
        super().make_GUI()
        # Añadimos un indicador visual extra en la parte superior para saber de quién es el turno
        self.lbl_turno = tk.Label(self, text=f"Turno actual: {self.jugador_actual}", font=("Helvetica", 14, "bold"))
        self.lbl_turno.place(x=20, y=40)
        
        # Atrapamos la tecla Enter para controlar los pasos de la IA en el modo 3
        self.master.bind("<Return>", self.ejecutar_paso_ia)

    def start_game(self):
        if self.fase == 1:
            # Ejecuta tu inicio normal y guarda el tablero original
            super().start_game()
            self.tablero_compartido = [row[:] for row in self.matrix]
        else:
            # IMPORTANTE: Primero limpiamos el tablero viejo ejecutando tu código original
            # para evitar que el "while" se quede trabado buscando celdas vacías
            super().start_game() 
            
            # Ahora sí, encima de esa limpieza, cargamos el tablero idéntico de la fase 1
            self.matrix = [row[:] for row in self.tablero_compartido]
            self.score = 0
            self.cant_movimientos = 0
            self.update_GUI()

    def update_GUI(self):
        super().update_GUI()
        
        # Console logs obligatorios según las especificaciones del PDF
        vacias = sum(row.count(0) for row in self.matrix)
        max_num = max(max(row) for row in self.matrix)
        print(f"[{self.jugador_actual}] Movimientos: {self.cant_movimientos} | Vacías: {vacias} | Mayor número: {max_num}")
        
        # === AQUÍ COLOCAS LAS VENTANILLAS ===
        if max_num >= 2048:
            mostrar_ventana_ganaste(self.master, self.score)   # <--- SE ABRE AL GANAR
            self.cambiar_o_terminar_fase(max_num)
        elif vacias == 0 and not self.verificar_movimientos_disponibles():
            mostrar_ventana_perdiste(self.master, self.score)  # <--- SE ABRE AL PERDER
            self.cambiar_o_terminar_fase(max_num)

    def verificar_movimientos_disponibles(self):
        for i in range(4):
            for j in range(3):
                if self.matrix[i][j] == self.matrix[i][j+1] or self.matrix[j][i] == self.matrix[j+1][i]:
                    return True
        return False

    # Sobrescribimos tus funciones de botones para llevar la cuenta de los movimientos válidos
    def left(self, event):
        if self.jugador_actual == "Máquina": return
        m_antes = [r[:] for r in self.matrix]
        super().left(event)
        if self.matrix != m_antes: self.cant_movimientos += 1

    def right(self, event):
        if self.jugador_actual == "Máquina": return
        m_antes = [r[:] for r in self.matrix]
        super().right(event)
        if self.matrix != m_antes: self.cant_movimientos += 1

    def up(self, event):
        if self.jugador_actual == "Máquina": return
        m_antes = [r[:] for r in self.matrix]
        super().up(event)
        if self.matrix != m_antes: self.cant_movimientos += 1

    def down(self, event):
        if self.jugador_actual == "Máquina": return
        m_antes = [r[:] for r in self.matrix]
        super().down(event)
        if self.matrix != m_antes: self.cant_movimientos += 1

    def ejecutar_paso_ia(self, event):
        if self.modo == 3 and self.jugador_actual == "Máquina":
            sig_mov = self.ia.decidir_movimiento(self.matrix)
            if sig_mov:
                self.cant_movimientos += 1
                if sig_mov == "left": super().left(None)
                elif sig_mov == "right": super().right(None)
                elif sig_mov == "up": super().up(None)
                elif sig_mov == "down": super().down(None)
            else:
                self.cambiar_o_terminar_fase(max(max(row) for row in self.matrix))

    def cambiar_o_terminar_fase(self, max_num):
        self.historial_resultados[self.jugador_actual] = {
            "score": self.score,
            "movimientos": self.cant_movimientos,
            "max_num": max_num
        }
        
        if self.fase == 1:
            self.fase = 2
            self.jugador_actual = self.nombre_j2
            self.lbl_turno.configure(text=f"Turno actual: {self.jugador_actual}")
            print(f"\n--- Fin del turno de {self.nombre_j1}. Cargando tablero idéntico para {self.jugador_actual}... ---\n")
            if self.modo == 3:
                print("-> Presione ENTER en la ventana para procesar cada movimiento de la Máquina.\n")
            self.start_game()
        else:
            self.mostrar_pantalla_ganador()

    def mostrar_pantalla_ganador(self):
        for widget in self.main_grid.winfo_children():
            widget.destroy()
            
        r1 = self.historial_resultados[self.nombre_j1]
        r2 = self.historial_resultados[self.nombre_j2]
        
        res_text = f"¡PARTIDA FINALIZADA!\n\n"
        res_text += f"{self.nombre_j1}: {r1['max_num']} Pts ({r1['movimientos']} Movs) | Score: {r1['score']}\n"
        res_text += f"{self.nombre_j2}: {r2['max_num']} Pts ({r2['movimientos']} Movs) | Score: {r2['score']}\n\n"
        
        # Comparación de reglas según PDF
        if r1['max_num'] > r2['max_num']:
            res_text += f"🏆 Ganador: {self.nombre_j1}"
        elif r2['max_num'] > r1['max_num']:
            res_text += f"🏆 Ganador: {self.nombre_j2}"
        else:
            if r1['movimientos'] < r2['movimientos']:
                res_text += f"🏆 Ganador: {self.nombre_j1} (Menos movimientos)"
            elif r2['movimientos'] < r1['movimientos']:
                res_text += f"🏆 Ganador: {self.nombre_j2} (Menos movimientos)"
            else:
                res_text += "🤝 ¡Empate absoluto!"
                
        lbl_final = tk.Label(self.main_grid, text=res_text, font=("Helvetica", 14, "bold"), bg=c.GRID_COLOR, fg="#ffffff")
        lbl_final.place(relx=0.5, rely=0.5, anchor="center")


# ==========================================
# 4. MENÚ DE BIENVENIDA ANTES DE INICIAR
# ==========================================
class MenuPrincipal(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.master.title("2048 - Menú Principal")
        self.grid(padx=40, pady=40)
        
        tk.Label(self, text="PROYECTO 2048", font=("Helvetica", 18, "bold")).grid(row=0, columnspan=2, pady=10)
        
        tk.Label(self, text="Nombre Jugador 1:").grid(row=1, column=0, sticky="w", pady=5)
        self.ent_j1 = tk.Entry(self)
        self.ent_j1.grid(row=1, column=1, pady=5)
        self.ent_j1.insert(0, "Jugador 1")
        
        tk.Label(self, text="Nombre Jugador 2:").grid(row=2, column=0, sticky="w", pady=5)
        self.ent_j2 = tk.Entry(self)
        self.ent_j2.grid(row=2, column=1, pady=5)
        self.ent_j2.insert(0, "Jugador 2")
        
        tk.Button(self, text="Modo 1: Clásico (Normal)", width=25, bg="#C4FA89", command=lambda: self.lanzar(1)).grid(row=3, columnspan=2, pady=5)
        tk.Button(self, text="Modo 2: Jugador vs Jugador", width=25, bg="#A3F244", command=lambda: self.lanzar(2)).grid(row=4, columnspan=2, pady=5)
        tk.Button(self, text="Modo 3: Jugador vs Máquina", width=25, bg="#93F022", command=lambda: self.lanzar(3)).grid(row=5, columnspan=2, pady=5)

    def lanzar(self, modo):
        j1 = self.ent_j1.get()
        j2 = self.ent_j2.get()
        self.destroy()
        
        if modo == 1:
            # Lanza tu código base original sin alteraciones
            Game()
        else:
            # Lanza la extensión con los modos añadidos
            JuegoExtendido(modo, j1, j2)

# ==========================================
# VENTANAS EMERGENTES DE FIN DE JUEGO (EXTRAS)
# ==========================================
def mostrar_ventana_ganaste(parent, score):
    # Crea una ventana flotante sobre el juego
    ventana_ganar = tk.Toplevel(parent)
    ventana_ganar.title("¡Felicidades!")
    ventana_ganar.geometry("300x200")
    ventana_ganar.configure(bg=c.WINNER_BG) # Usa el color de colores.py
    ventana_ganar.resizable(False, False)
    
    # Asegura que el usuario tenga que atender esta ventana antes de regresar al juego
    ventana_ganar.grab_set() 
    
    tk.Label(
        ventana_ganar, 
        text="¡HAS GANADO!", 
        font=("Helvetica", 18, "bold"), 
        bg=c.WINNER_BG, 
        fg="#ffffff"
    ).pack(pady=20)
    
    tk.Label(
        ventana_ganar, 
        text=f"Alcanzaste la ficha 2048\nScore total: {score}", 
        font=("Helvetica", 12), 
        bg=c.WINNER_BG, 
        fg="#ffffff"
    ).pack(pady=10)
    
    tk.Button(
        ventana_ganar, 
        text="Aceptar", 
        font=("Helvetica", 10, "bold"),
        command=ventana_ganar.destroy
    ).pack(pady=15)

def mostrar_ventana_perdiste(parent, score):
    ventana_perder = tk.Toplevel(parent)
    ventana_perder.title("Fin del Juego")
    ventana_perder.geometry("300x200")
    ventana_perder.configure(bg=c.LOSER_BG) # Usa el color de colores.py
    ventana_perder.resizable(False, False)
    
    ventana_perder.grab_set()
    
    tk.Label(
        ventana_perder, 
        text="FIN DEL JUEGO", 
        font=("Helvetica", 18, "bold"), 
        bg=c.LOSER_BG, 
        fg=c.GAME_OVER_FONT_COLOR
    ).pack(pady=20)
    
    tk.Label(
        ventana_perder, 
        text=f"No quedan movimientos posibles.\nScore final: {score}", 
        font=("Helvetica", 12), 
        bg=c.LOSER_BG, 
        fg=c.GAME_OVER_FONT_COLOR
    ).pack(pady=10)
    
    tk.Button(
        ventana_perder, 
        text="Aceptar", 
        font=("Helvetica", 10, "bold"),
        command=ventana_perder.destroy
    ).pack(pady=15)


if __name__ == "__main__":
    ventana = tk.Tk()
    app = MenuPrincipal(ventana)
    ventana.mainloop()
