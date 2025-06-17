class ShannonFanoCoding:
    def __init__(self):
        self.codes = {}

    def calculate_frequencies(self, text):
        """Calcula las frecuencias de cada carácter en el texto."""
        frequencies = {}
        for char in text:
            if char in frequencies:
                frequencies[char] += 1
            else:
                frequencies[char] = 1
        return frequencies

    def shannon_fano(self, symbols, code_prefix=''):
        """
        Asigna códigos Shannon-Fano recursivamente a los símbolos.

        Args:
            symbols (list): Lista de tuplas (símbolo, frecuencia).
            code_prefix (str): Prefijo del código actual.
        """
        if len(symbols) == 1:
            self.codes[symbols[0][0]] = code_prefix
            return

        total_frequency = sum(freq for _, freq in symbols)
        midpoint_frequency = 0
        midpoint_index = 0

        for i, (symbol, frequency) in enumerate(symbols):
            midpoint_frequency += frequency
            if midpoint_frequency >= total_frequency / 2:
                midpoint_index = i + 1
                break

        # Dividir los símbolos en dos grupos
        left_symbols = symbols[:midpoint_index]
        right_symbols = symbols[midpoint_index:]

        # Asignar códigos recursivamente
        self.shannon_fano(left_symbols, code_prefix + '0')
        self.shannon_fano(right_symbols, code_prefix + '1')

    def encode(self, text):
        """
        Codifica un texto utilizando el algoritmo de Shannon-Fano.

        Args:
            text (str): El texto a codificar.

        Returns:
            dict: Un diccionario que contiene el texto original, el texto codificado,
                  las frecuencias de los símbolos, los códigos asignados y el nombre del algoritmo.
        """
        frequencies = self.calculate_frequencies(text)
        sorted_symbols = sorted(frequencies.items(), key=lambda x: x[1], reverse=True)

        # Inicializar el diccionario de códigos
        self.codes = {}

        # Aplicar el algoritmo de Shannon-Fano
        self.shannon_fano([(symbol, freq) for symbol, freq in sorted_symbols])

        # Codificar el texto
        encoded_text = ''.join(self.codes[char] for char in text)

        # Construir representación del árbol para visualización
        tree_structure = self._build_tree_structure(sorted_symbols, self.codes)

        return {
            'original_text': text,
            'encoded_text': encoded_text,
            'frequencies': frequencies,
            'codes': self.codes.copy(),
            'sorted_symbols': sorted_symbols,
            'tree_structure': tree_structure,
            'algorithm': 'Shannon-Fano'
        }

    def _build_tree_structure(self, sorted_symbols, codes):
        """Construye una representación del árbol para visualización"""
        tree = {'char': None, 'children': {}, 'symbols': [s[0] for s in sorted_symbols]}
        
        # Construir árbol basado en los códigos generados
        for char, code in codes.items():
            current = tree
            for bit in code:
                if bit not in current['children']:
                    current['children'][bit] = {'char': None, 'children': {}, 'symbols': []}
                current = current['children'][bit]
            current['char'] = char
        
        return tree
