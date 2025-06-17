import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd

from algorithms.huffman import HuffmanCoding
from algorithms.shannon_fano import ShannonFanoCoding
from utils.frequency_calculator import FrequencyCalculator
from utils.statistics import StatisticsCalculator
from utils.visualizer import DataVisualizer
from utils.pdf_exporter import PDFExporter
from utils.tree_visualizer import TreeVisualizer

class MainWindow:
    def __init__(self, master):
        self.master = master
        master.title("Compresión de Huffman y Shannon-Fano")

        self.text_data = ""
        self.huffman_results = None
        self.shannon_fano_results = None

        self.create_widgets()

    def create_widgets(self):
        # Sección de entrada de texto
        self.input_section = ttk.LabelFrame(self.master, text="Entrada de Texto", padding="10")
        self.input_section.pack(fill="both", expand=True, padx=10, pady=10)

        self.text_area = scrolledtext.ScrolledText(self.input_section, height=10, wrap=tk.WORD)
        self.text_area.pack(fill="both", expand=True)

        # Botones de acción
        self.action_section = ttk.Frame(self.master)
        self.action_section.pack(pady=5)

        self.compress_button = ttk.Button(self.action_section, text="Comprimir", command=self.compress_text)
        self.compress_button.pack(side=tk.LEFT, padx=5)

        self.clear_button = ttk.Button(self.action_section, text="Limpiar", command=self.clear_text)
        self.clear_button.pack(side=tk.LEFT, padx=5)

        # Sección de resultados
        self.results_section = ttk.Frame(self.master)
        self.results_section.pack(fill="both", expand=True, padx=10, pady=10)

        self.notebook = ttk.Notebook(self.results_section)
        self.notebook.pack(fill="both", expand=True)

        self.create_results_section()

    def create_results_section(self):
        # Pestaña de estadísticas
        self.stats_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.stats_frame, text="Estadísticas")

        # Pestaña de información general
        self.info_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.info_frame, text="Información General")

        # Pestaña de mensajes codificados
        self.encoded_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.encoded_frame, text="Mensajes Codificados")

        # Pestaña de decodificación
        self.decoding_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.decoding_frame, text="Proceso de Decodificación")

        # Pestaña de árboles
        self.trees_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.trees_frame, text="Árboles de Codificación")

    def compress_text(self):
        self.text_data = self.text_area.get("1.0", tk.END).strip()
        if not self.text_data:
            return

        from compression import huffman, shannon_fano

        # Comprimir con Huffman
        self.huffman_results = huffman.compress(self.text_data)

        # Comprimir con Shannon-Fano
        self.shannon_fano_results = shannon_fano.compress(self.text_data)

        self.update_results()

    def clear_text(self):
        self.text_area.delete("1.0", tk.END)
        self.text_data = ""
        self.huffman_results = None
        self.shannon_fano_results = None
        self.update_results()

    def update_results(self):
        self.update_stats()
        self.update_info()
        self.update_encoded_messages()
        self.update_decoding_process()
        self.update_trees()

    def update_stats(self):
        # Limpiar frame
        for widget in self.stats_frame.winfo_children():
            widget.destroy()

        if not self.huffman_results or not self.shannon_fano_results:
            return

        # Estadísticas de Huffman
        huffman_stats = ttk.LabelFrame(self.stats_frame, text="Huffman", padding="10")
        huffman_stats.pack(fill="x", padx=10, pady=5)

        ttk.Label(huffman_stats, text=f"Tamaño del texto original: {len(self.text_data) * 8} bits").pack()
        ttk.Label(huffman_stats, text=f"Tamaño comprimido: {len(self.huffman_results['encoded_text'])} bits").pack()
        compression_ratio = (len(self.text_data) * 8) / len(self.huffman_results['encoded_text'])
        ttk.Label(huffman_stats, text=f"Ratio de compresión: {compression_ratio:.2f}").pack()

        # Estadísticas de Shannon-Fano
        sf_stats = ttk.LabelFrame(self.stats_frame, text="Shannon-Fano", padding="10")
        sf_stats.pack(fill="x", padx=10, pady=5)

        ttk.Label(sf_stats, text=f"Tamaño del texto original: {len(self.text_data) * 8} bits").pack()
        ttk.Label(sf_stats, text=f"Tamaño comprimido: {len(self.shannon_fano_results['encoded_text'])} bits").pack()
        compression_ratio = (len(self.text_data) * 8) / len(self.shannon_fano_results['encoded_text'])
        ttk.Label(sf_stats, text=f"Ratio de compresión: {compression_ratio:.2f}").pack()

    def update_info(self):
        # Limpiar frame
        for widget in self.info_frame.winfo_children():
            widget.destroy()

        if not self.huffman_results or not self.shannon_fano_results:
            return

        # Información de Huffman
        huffman_info = ttk.LabelFrame(self.info_frame, text="Huffman", padding="10")
        huffman_info.pack(fill="x", padx=10, pady=5)

        codes_text = scrolledtext.ScrolledText(huffman_info, height=10)
        codes_text.pack(fill="both", expand=True)

        codes_info = "Símbolo -> Código\n" + "-" * 20 + "\n"
        for char, code in sorted(self.huffman_results['codes'].items()):
            display_char = char
            if char == ' ':
                display_char = '[ESPACIO]'
            elif char == '\n':
                display_char = '[NUEVA_LÍNEA]'
            elif char == '\t':
                display_char = '[TAB]'
            codes_info += f"'{display_char}' -> {code}\n"

        codes_text.insert(1.0, codes_info)
        codes_text.config(state=tk.DISABLED)

        # Información de Shannon-Fano
        sf_info = ttk.LabelFrame(self.info_frame, text="Shannon-Fano", padding="10")
        sf_info.pack(fill="x", padx=10, pady=5)

        codes_text = scrolledtext.ScrolledText(sf_info, height=10)
        codes_text.pack(fill="both", expand=True)

        codes_info = "Símbolo -> Código\n" + "-" * 20 + "\n"
        for char, code in sorted(self.shannon_fano_results['codes'].items()):
            display_char = char
            if char == ' ':
                display_char = '[ESPACIO]'
            elif char == '\n':
                display_char = '[NUEVA_LÍNEA]'
            elif char == '\t':
                display_char = '[TAB]'
            codes_info += f"'{display_char}' -> {code}\n"

        codes_text.insert(1.0, codes_info)
        codes_text.config(state=tk.DISABLED)

    def update_encoded_messages(self):
        """Actualiza la pestaña de mensajes codificados"""
        # Limpiar frame
        for widget in self.encoded_frame.winfo_children():
            widget.destroy()
        
        if not self.huffman_results or not self.shannon_fano_results:
            return
        
        # Frame principal con scroll
        canvas = tk.Canvas(self.encoded_frame)
        scrollbar = ttk.Scrollbar(self.encoded_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Mensaje original
        original_frame = ttk.LabelFrame(scrollable_frame, text="Mensaje Original", padding="10")
        original_frame.pack(fill="x", padx=10, pady=5)
        
        original_text = scrolledtext.ScrolledText(original_frame, height=6, width=100, wrap=tk.WORD)
        original_text.pack(fill="both", expand=True)
        original_text.insert(1.0, self.text_data)
        original_text.config(state=tk.DISABLED)
        
        # Mensaje codificado Huffman
        huffman_frame = ttk.LabelFrame(scrollable_frame, text="Mensaje Codificado - Huffman", padding="10")
        huffman_frame.pack(fill="x", padx=10, pady=5)
        
        huffman_encoded = scrolledtext.ScrolledText(huffman_frame, height=8, width=100, wrap=tk.WORD)
        huffman_encoded.pack(fill="both", expand=True)
        huffman_encoded.insert(1.0, self.huffman_results['encoded_text'])
        huffman_encoded.config(state=tk.DISABLED)
        
        # Información Huffman
        huffman_info = ttk.Frame(huffman_frame)
        huffman_info.pack(fill="x", pady=(5, 0))
        ttk.Label(huffman_info, text=f"Longitud: {len(self.huffman_results['encoded_text'])} bits").pack(side="left")
        ttk.Label(huffman_info, text=f"Tamaño original: {len(self.text_data) * 8} bits").pack(side="left", padx=(20, 0))
        
        # Mensaje codificado Shannon-Fano
        sf_frame = ttk.LabelFrame(scrollable_frame, text="Mensaje Codificado - Shannon-Fano", padding="10")
        sf_frame.pack(fill="x", padx=10, pady=5)
        
        sf_encoded = scrolledtext.ScrolledText(sf_frame, height=8, width=100, wrap=tk.WORD)
        sf_encoded.pack(fill="both", expand=True)
        sf_encoded.insert(1.0, self.shannon_fano_results['encoded_text'])
        sf_encoded.config(state=tk.DISABLED)
        
        # Información Shannon-Fano
        sf_info = ttk.Frame(sf_frame)
        sf_info.pack(fill="x", pady=(5, 0))
        ttk.Label(sf_info, text=f"Longitud: {len(self.shannon_fano_results['encoded_text'])} bits").pack(side="left")
        ttk.Label(sf_info, text=f"Tamaño original: {len(self.text_data) * 8} bits").pack(side="left", padx=(20, 0))
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def update_decoding_process(self):
        """Actualiza la pestaña del proceso de decodificación"""
        # Limpiar frame
        for widget in self.decoding_frame.winfo_children():
            widget.destroy()
        
        if not self.huffman_results or not self.shannon_fano_results:
            return
        
        # Notebook para separar los procesos
        decoding_notebook = ttk.Notebook(self.decoding_frame)
        decoding_notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Proceso Huffman
        huffman_decode_frame = ttk.Frame(decoding_notebook)
        decoding_notebook.add(huffman_decode_frame, text="Decodificación Huffman")
        self.create_decoding_demo(huffman_decode_frame, self.huffman_results, "Huffman")
        
        # Proceso Shannon-Fano
        sf_decode_frame = ttk.Frame(decoding_notebook)
        decoding_notebook.add(sf_decode_frame, text="Decodificación Shannon-Fano")
        self.create_decoding_demo(sf_decode_frame, self.shannon_fano_results, "Shannon-Fano")

    def create_decoding_demo(self, parent, results, algorithm):
        """Crea una demostración del proceso de decodificación"""
        # Frame principal con scroll
        canvas = tk.Canvas(parent)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Tabla de códigos
        codes_frame = ttk.LabelFrame(scrollable_frame, text=f"Tabla de Códigos - {algorithm}", padding="10")
        codes_frame.pack(fill="x", padx=10, pady=5)
        
        codes_text = scrolledtext.ScrolledText(codes_frame, height=8, width=80)
        codes_text.pack(fill="both", expand=True)
        
        codes_info = "Símbolo -> Código\n" + "-" * 20 + "\n"
        for char, code in sorted(results['codes'].items()):
            display_char = char
            if char == ' ':
                display_char = '[ESPACIO]'
            elif char == '\n':
                display_char = '[NUEVA_LÍNEA]'
            elif char == '\t':
                display_char = '[TAB]'
            codes_info += f"'{display_char}' -> {code}\n"
        
        codes_text.insert(1.0, codes_info)
        codes_text.config(state=tk.DISABLED)
        
        # Proceso de decodificación paso a paso
        process_frame = ttk.LabelFrame(scrollable_frame, text=f"Proceso de Decodificación - {algorithm}", padding="10")
        process_frame.pack(fill="x", padx=10, pady=5)
        
        process_text = scrolledtext.ScrolledText(process_frame, height=15, width=80)
        process_text.pack(fill="both", expand=True)
        
        # Simular decodificación paso a paso
        encoded = results['encoded_text'][:200]  # Limitar para demostración
        decoded_demo = self.simulate_decoding_process(encoded, results['codes'], algorithm)
        
        process_text.insert(1.0, decoded_demo)
        process_text.config(state=tk.DISABLED)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def simulate_decoding_process(self, encoded_text, codes, algorithm):
        """Simula el proceso de decodificación paso a paso"""
        # Crear diccionario inverso
        reverse_codes = {code: char for char, code in codes.items()}
        
        process_text = f"Decodificación paso a paso - {algorithm}\n"
        process_text += "=" * 50 + "\n\n"
        process_text += f"Mensaje codificado (primeros 200 bits): {encoded_text}\n\n"
        process_text += "Proceso de decodificación:\n"
        process_text += "-" * 30 + "\n"
        
        current_code = ""
        decoded_chars = []
        step = 1
        
        for i, bit in enumerate(encoded_text):
            current_code += bit
            
            if current_code in reverse_codes:
                char = reverse_codes[current_code]
                display_char = char
                if char == ' ':
                    display_char = '[ESPACIO]'
                elif char == '\n':
                    display_char = '[NL]'
                elif char == '\t':
                    display_char = '[TAB]'
                
                decoded_chars.append(char)
                process_text += f"Paso {step}: '{current_code}' -> '{display_char}'\n"
                process_text += f"   Decodificado hasta ahora: {''.join(decoded_chars)}\n\n"
                
                current_code = ""
                step += 1
                
                if step > 20:  # Limitar para no sobrecargar la interfaz
                    process_text += "... (proceso continúa)\n"
                    break
        
        if current_code:
            process_text += f"Código parcial restante: '{current_code}'\n"
        
        return process_text

    def update_trees(self):
        """Actualiza la pestaña de árboles de codificación"""
        # Limpiar frame
        for widget in self.trees_frame.winfo_children():
            widget.destroy()
        
        if not self.huffman_results or not self.shannon_fano_results:
            return
        
        # Notebook para separar los árboles
        trees_notebook = ttk.Notebook(self.trees_frame)
        trees_notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Árbol Huffman
        huffman_tree_frame = ttk.Frame(trees_notebook)
        trees_notebook.add(huffman_tree_frame, text="Árbol Huffman")
        
        # Árbol Shannon-Fano
        sf_tree_frame = ttk.Frame(trees_notebook)
        trees_notebook.add(sf_tree_frame, text="Árbol Shannon-Fano")
        
        # Crear visualizaciones
        from utils.tree_visualizer import TreeVisualizer
        tree_viz = TreeVisualizer()
        
        # Visualizar árbol Huffman
        if 'tree' in self.huffman_results:
            huffman_fig = tree_viz.visualize_huffman_tree(self.huffman_results['tree'])
            huffman_canvas = FigureCanvasTkAgg(huffman_fig, huffman_tree_frame)
            huffman_canvas.draw()
            huffman_canvas.get_tk_widget().pack(fill="both", expand=True)
        
        # Visualizar árbol Shannon-Fano
        sf_fig = tree_viz.visualize_shannon_fano_tree(self.shannon_fano_results)
        sf_canvas = FigureCanvasTkAgg(sf_fig, sf_tree_frame)
        sf_canvas.draw()
        sf_canvas.get_tk_widget().pack(fill="both", expand=True)

    def compress_text(self):
        self.process_text()

    def process_text(self):
        """Procesa el texto con ambos algoritmos"""
        self.text_data = self.text_area.get(1.0, tk.END).strip()
        
        if not self.text_data:
            messagebox.showwarning("Advertencia", "Por favor ingrese texto para procesar")
            return
            
        try:
            # Procesar con Huffman
            huffman = HuffmanCoding()
            self.huffman_results = huffman.encode(self.text_data)
            
            # Procesar con Shannon-Fano
            shannon_fano = ShannonFanoCoding()
            self.shannon_fano_results = shannon_fano.encode(self.text_data)
            
            # Actualizar interfaz
            self.update_results()
            
            messagebox.showinfo("Éxito", "Texto procesado correctamente")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al procesar el texto: {str(e)}")
