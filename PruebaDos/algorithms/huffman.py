"""
Capa de Funcionalidad - Algoritmo de Huffman
Implementa la codificación y decodificación usando el algoritmo de Huffman
"""

import heapq
from collections import defaultdict, Counter
from utils.frequency_calculator import FrequencyCalculator

class HuffmanNode:
    """Nodo del árbol de Huffman"""
    def __init__(self, char=None, freq=0, left=None, right=None):
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right
        
    def __lt__(self, other):
        return self.freq < other.freq
    
    def __eq__(self, other):
        if other is None:
            return False
        if not isinstance(other, HuffmanNode):
            return False
        return self.freq == other.freq

class HuffmanCoding:
    """Implementación del algoritmo de Huffman"""
    
    def __init__(self):
        self.root = None
        self.codes = {}
        self.reverse_codes = {}
        
    def build_tree(self, frequencies):
        """Construye el árbol de Huffman usando cola de prioridad"""
        if not frequencies:
            return None
            
        # Caso especial: solo un carácter
        if len(frequencies) == 1:
            char, freq = list(frequencies.items())[0]
            self.root = HuffmanNode(char, freq)
            return self.root
        
        # Crear heap con nodos hoja
        heap = []
        for char, freq in frequencies.items():
            node = HuffmanNode(char, freq)
            heapq.heappush(heap, node)
            
        # Construir árbol combinando nodos
        while len(heap) > 1:
            # Tomar los dos nodos con menor frecuencia
            left = heapq.heappop(heap)
            right = heapq.heappop(heap)
            
            # Crear nodo interno
            merged_freq = left.freq + right.freq
            merged = HuffmanNode(freq=merged_freq, left=left, right=right)
            
            # Agregar de vuelta al heap
            heapq.heappush(heap, merged)
            
        self.root = heap[0] if heap else None
        return self.root
        
    def generate_codes(self, node=None, code=""):
        """Genera los códigos de Huffman recursivamente"""
        if node is None:
            node = self.root
            
        if node is None:
            return
        
        # Caso especial: árbol con un solo nodo (un carácter)
        if node.char is not None and node.left is None and node.right is None:
            self.codes[node.char] = "0"  # Asignar código "0" para un solo carácter
            self.reverse_codes["0"] = node.char
            return
            
        # Si es nodo hoja (tiene carácter)
        if node.char is not None:
            self.codes[node.char] = code
            self.reverse_codes[code] = node.char
            return
            
        # Recursión para nodos internos
        if node.left is not None:
            self.generate_codes(node.left, code + "0")
        if node.right is not None:
            self.generate_codes(node.right, code + "1")
        
    def encode(self, text):
        """Codifica el texto usando Huffman"""
        if not text:
            return None
            
        # Calcular frecuencias
        freq_calc = FrequencyCalculator()
        frequencies = freq_calc.calculate_frequencies(text)
        
        # Construir árbol
        self.build_tree(frequencies)
        
        # Limpiar códigos anteriores
        self.codes = {}
        self.reverse_codes = {}
        
        # Generar códigos
        self.generate_codes()
        
        # Verificar que se generaron códigos
        if not self.codes:
            raise ValueError("No se pudieron generar códigos de Huffman")
        
        # Codificar texto
        encoded_text = ""
        for char in text:
            if char in self.codes:
                encoded_text += self.codes[char]
            else:
                raise ValueError(f"Carácter '{char}' no encontrado en códigos")
            
        return {
            'original_text': text,
            'encoded_text': encoded_text,
            'frequencies': frequencies,
            'codes': self.codes.copy(),
            'reverse_codes': self.reverse_codes.copy(),
            'tree': self.root,
            'algorithm': 'Huffman'
        }
        
    def decode(self, encoded_text, root=None):
        """Decodifica el texto usando el árbol de Huffman"""
        if root is None:
            root = self.root
            
        if not encoded_text or root is None:
            return ""
        
        # Caso especial: árbol con un solo nodo
        if root.char is not None and root.left is None and root.right is None:
            # Cada bit representa el mismo carácter
            return root.char * len(encoded_text)
            
        decoded_text = ""
        current = root
        
        for bit in encoded_text:
            if bit == "0":
                current = current.left
            elif bit == "1":
                current = current.right
            else:
                raise ValueError(f"Bit inválido: {bit}")
                
            # Si llegamos a una hoja
            if current is None:
                raise ValueError("Código inválido en la decodificación")
                
            if current.char is not None:
                decoded_text += current.char
                current = root
                
        return decoded_text
    
    def get_tree_info(self):
        """Obtiene información detallada del árbol para visualización"""
        if not self.root:
            return None
        
        def traverse_tree(node, depth=0, path=""):
            if not node:
                return []
            
            info = {
                'depth': depth,
                'char': node.char,
                'freq': node.freq,
                'is_leaf': node.char is not None,
                'id': id(node),
                'path': path,
                'code': self.codes.get(node.char, "") if node.char else ""
            }
            
            result = [info]
            
            if node.left:
                result.extend(traverse_tree(node.left, depth + 1, path + "0"))
            if node.right:
                result.extend(traverse_tree(node.right, depth + 1, path + "1"))
            
            return result
        
        return traverse_tree(self.root)
    
    def print_codes(self):
        """Imprime los códigos generados (para debugging)"""
        print("Códigos de Huffman:")
        for char, code in sorted(self.codes.items()):
            display_char = repr(char) if char in [' ', '\n', '\t'] else char
            print(f"  {display_char}: {code}")
