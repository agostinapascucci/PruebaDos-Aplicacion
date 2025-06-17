"""
Aplicación de Compresión de Datos - Huffman y Shannon-Fano
Punto de entrada principal de la aplicación
"""

import tkinter as tk
import sys
import os

# Agregar el directorio actual al path para importaciones
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui.main_window import MainWindow

def main():
    """Función principal que inicia la aplicación"""
    try:
        root = tk.Tk()
        root.state('zoomed')  # Maximizar ventana en Windows
        app = MainWindow(root)
        root.mainloop()
    except Exception as e:
        print(f"Error al iniciar la aplicación: {e}")
        input("Presione Enter para salir...")

def test_algorithms():
    """Función de prueba para verificar que los algoritmos funcionen correctamente"""
    print("Probando algoritmos de compresión...")
    
    # Texto de prueba
    test_text = "ABRACADABRA"
    print(f"Texto de prueba: '{test_text}'")
    
    try:
        # Probar Huffman
        from algorithms.huffman import HuffmanCoding
        huffman = HuffmanCoding()
        huffman_result = huffman.encode(test_text)
        
        print("\n--- Resultados Huffman ---")
        print(f"Frecuencias: {huffman_result['frequencies']}")
        print(f"Códigos: {huffman_result['codes']}")
        print(f"Texto codificado: {huffman_result['encoded_text']}")
        
        # Verificar decodificación
        decoded = huffman.decode(huffman_result['encoded_text'])
        print(f"Texto decodificado: '{decoded}'")
        print(f"¿Coincide?: {decoded == test_text}")
        
        # Probar Shannon-Fano
        from algorithms.shannon_fano import ShannonFanoCoding
        sf = ShannonFanoCoding()
        sf_result = sf.encode(test_text)
        
        print("\n--- Resultados Shannon-Fano ---")
        print(f"Frecuencias: {sf_result['frequencies']}")
        print(f"Códigos: {sf_result['codes']}")
        print(f"Texto codificado: {sf_result['encoded_text']}")
        
        print("\n¡Pruebas completadas exitosamente!")
        
    except Exception as e:
        print(f"Error en las pruebas: {e}")
        import traceback
        traceback.print_exc()

# Descomentar la siguiente línea para ejecutar pruebas antes de la interfaz
# test_algorithms()

if __name__ == "__main__":
    main()
