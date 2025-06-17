"""
Utilidad para calcular frecuencias de símbolos
Proporciona funciones para analizar la distribución de caracteres en el texto
"""

from collections import Counter

class FrequencyCalculator:
    """Calculadora de frecuencias de símbolos"""
    
    @staticmethod
    def calculate_frequencies(text):
        """Calcula las frecuencias de cada símbolo en el texto"""
        if not text:
            return {}
        
        # Usar Counter para contar frecuencias
        frequencies = Counter(text)
        
        # Convertir a diccionario regular
        return dict(frequencies)
    
    @staticmethod
    def calculate_probabilities(frequencies):
        """Calcula las probabilidades de cada símbolo"""
        if not frequencies:
            return {}
            
        total = sum(frequencies.values())
        if total == 0:
            return {}
            
        return {char: freq / total for char, freq in frequencies.items()}
    
    @staticmethod
    def get_sorted_symbols(frequencies, reverse=True):
        """Obtiene los símbolos ordenados por frecuencia"""
        if not frequencies:
            return []
        return sorted(frequencies.items(), key=lambda x: x[1], reverse=reverse)
    
    @staticmethod
    def print_frequencies(frequencies):
        """Imprime las frecuencias (para debugging)"""
        print("Frecuencias de caracteres:")
        for char, freq in sorted(frequencies.items(), key=lambda x: x[1], reverse=True):
            display_char = repr(char) if char in [' ', '\n', '\t'] else char
            print(f"  {display_char}: {freq}")
