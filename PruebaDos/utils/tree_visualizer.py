"""
Utilidad para visualización de árboles de codificación
Crea representaciones gráficas de los árboles Huffman y Shannon-Fano
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.figure import Figure
import numpy as np

class TreeVisualizer:
    """Visualizador de árboles de codificación"""
    
    def __init__(self):
        self.node_radius = 0.3
        self.level_height = 1.5
        self.node_spacing = 1.0
        
    def visualize_huffman_tree(self, root):
        """Visualiza el árbol de Huffman"""
        if not root:
            fig, ax = plt.subplots(figsize=(10, 8))
            ax.text(0.5, 0.5, 'No hay árbol para visualizar', 
                   ha='center', va='center', transform=ax.transAxes)
            return fig
            
        # Calcular posiciones de nodos
        positions = {}
        self._calculate_positions_huffman(root, positions, 0, 0, 8)
        
        # Crear figura
        fig, ax = plt.subplots(figsize=(14, 10))
        
        # Dibujar conexiones primero
        self._draw_connections_huffman(ax, root, positions)
        
        # Dibujar nodos
        self._draw_nodes_huffman(ax, root, positions)
        
        # Configurar ejes
        ax.set_xlim(-10, 10)
        ax.set_ylim(-8, 2)
        ax.set_aspect('equal')
        ax.axis('off')
        ax.set_title('Árbol de Huffman', fontsize=16, fontweight='bold', pad=20)
        
        # Agregar leyenda
        legend_elements = [
            plt.Line2D([0], [0], marker='o', color='lightblue', 
                      markerfacecolor='lightblue', markersize=10, 
                      label='Nodo interno', linestyle='None'),
            plt.Line2D([0], [0], marker='o', color='lightgreen', 
                      markerfacecolor='lightgreen', markersize=10, 
                      label='Nodo hoja (símbolo)', linestyle='None'),
            plt.Line2D([0], [0], color='red', linewidth=2, 
                      label='Enlace "0"'),
            plt.Line2D([0], [0], color='blue', linewidth=2, 
                      label='Enlace "1"')
        ]
        ax.legend(handles=legend_elements, loc='upper right')
        
        plt.tight_layout()
        return fig
    
    def _calculate_positions_huffman(self, node, positions, x, y, width):
        """Calcula las posiciones de los nodos del árbol Huffman"""
        if not node:
            return
            
        positions[id(node)] = (x, y)
        
        if node.left or node.right:
            child_width = width / 2
            if node.left:
                self._calculate_positions_huffman(
                    node.left, positions, x - child_width/2, y - self.level_height, child_width
                )
            if node.right:
                self._calculate_positions_huffman(
                    node.right, positions, x + child_width/2, y - self.level_height, child_width
                )
    
    def _draw_connections_huffman(self, ax, node, positions):
        """Dibuja las conexiones del árbol Huffman"""
        if not node or id(node) not in positions:
            return
            
        x, y = positions[id(node)]
        
        if node.left and id(node.left) in positions:
            x_left, y_left = positions[id(node.left)]
            ax.plot([x, x_left], [y, y_left], 'r-', linewidth=2, alpha=0.7)
            # Etiqueta "0"
            mid_x, mid_y = (x + x_left) / 2, (y + y_left) / 2
            ax.text(mid_x - 0.1, mid_y + 0.1, '0', fontsize=12, fontweight='bold', 
                   color='red', ha='center', va='center',
                   bbox=dict(boxstyle="round,pad=0.1", facecolor='white', alpha=0.8))
            self._draw_connections_huffman(ax, node.left, positions)
            
        if node.right and id(node.right) in positions:
            x_right, y_right = positions[id(node.right)]
            ax.plot([x, x_right], [y, y_right], 'b-', linewidth=2, alpha=0.7)
            # Etiqueta "1"
            mid_x, mid_y = (x + x_right) / 2, (y + y_right) / 2
            ax.text(mid_x + 0.1, mid_y + 0.1, '1', fontsize=12, fontweight='bold', 
                   color='blue', ha='center', va='center',
                   bbox=dict(boxstyle="round,pad=0.1", facecolor='white', alpha=0.8))
            self._draw_connections_huffman(ax, node.right, positions)
    
    def _draw_nodes_huffman(self, ax, node, positions):
        """Dibuja los nodos del árbol Huffman"""
        if not node or id(node) not in positions:
            return
            
        x, y = positions[id(node)]
        
        # Determinar color y etiqueta
        if node.char is not None:
            # Nodo hoja
            color = 'lightgreen'
            display_char = node.char
            if node.char == ' ':
                display_char = 'ESP'
            elif node.char == '\n':
                display_char = 'NL'
            elif node.char == '\t':
                display_char = 'TAB'
            label = f"{display_char}\n({node.freq})"
        else:
            # Nodo interno
            color = 'lightblue'
            label = f"{node.freq}"
        
        # Dibujar círculo
        circle = plt.Circle((x, y), self.node_radius, color=color, 
                          ec='black', linewidth=2, zorder=3)
        ax.add_patch(circle)
        
        # Agregar texto
        ax.text(x, y, label, ha='center', va='center', fontsize=10, 
               fontweight='bold', zorder=4)
        
        # Recursión para hijos
        if node.left:
            self._draw_nodes_huffman(ax, node.left, positions)
        if node.right:
            self._draw_nodes_huffman(ax, node.right, positions)
    
    def visualize_shannon_fano_tree(self, results):
        """Visualiza el árbol de Shannon-Fano"""
        if not results or 'codes' not in results:
            fig, ax = plt.subplots(figsize=(10, 8))
            ax.text(0.5, 0.5, 'No hay datos para visualizar', 
                   ha='center', va='center', transform=ax.transAxes)
            return fig
        
        # Construir árbol a partir de los códigos
        tree_structure = self._build_tree_from_codes(results['codes'])
        
        # Crear figura
        fig, ax = plt.subplots(figsize=(14, 10))
        
        # Calcular posiciones
        positions = {}
        self._calculate_positions_sf(tree_structure, positions, 0, 0, 8, 0)
        
        # Dibujar conexiones
        self._draw_connections_sf(ax, tree_structure, positions)
        
        # Dibujar nodos
        self._draw_nodes_sf(ax, tree_structure, positions)
        
        # Configurar ejes
        ax.set_xlim(-10, 10)
        ax.set_ylim(-8, 2)
        ax.set_aspect('equal')
        ax.axis('off')
        ax.set_title('Árbol de Shannon-Fano', fontsize=16, fontweight='bold', pad=20)
        
        # Agregar leyenda
        legend_elements = [
            plt.Line2D([0], [0], marker='o', color='lightcoral', 
                      markerfacecolor='lightcoral', markersize=10, 
                      label='Nodo interno', linestyle='None'),
            plt.Line2D([0], [0], marker='o', color='lightgreen', 
                      markerfacecolor='lightgreen', markersize=10, 
                      label='Nodo hoja (símbolo)', linestyle='None'),
            plt.Line2D([0], [0], color='red', linewidth=2, 
                      label='Enlace "0"'),
            plt.Line2D([0], [0], color='blue', linewidth=2, 
                      label='Enlace "1"')
        ]
        ax.legend(handles=legend_elements, loc='upper right')
        
        plt.tight_layout()
        return fig
    
    def _build_tree_from_codes(self, codes):
        """Construye un árbol a partir de los códigos de Shannon-Fano"""
        root = {'char': None, 'children': {}}
        
        for char, code in codes.items():
            current = root
            for bit in code:
                if bit not in current['children']:
                    current['children'][bit] = {'char': None, 'children': {}}
                current = current['children'][bit]
            current['char'] = char
            
        return root
    
    def _calculate_positions_sf(self, node, positions, x, y, width, node_id):
        """Calcula las posiciones de los nodos del árbol Shannon-Fano"""
        positions[node_id] = (x, y, node)
        
        children = list(node['children'].items())
        if len(children) == 2:
            child_width = width / 2
            left_bit, left_child = children[0]
            right_bit, right_child = children[1]
            
            left_id = node_id * 2 + 1
            right_id = node_id * 2 + 2
            
            self._calculate_positions_sf(
                left_child, positions, x - child_width/2, y - self.level_height, 
                child_width, left_id
            )
            self._calculate_positions_sf(
                right_child, positions, x + child_width/2, y - self.level_height, 
                child_width, right_id
            )
    
    def _draw_connections_sf(self, ax, node, positions):
        """Dibuja las conexiones del árbol Shannon-Fano"""
        for node_id, (x, y, current_node) in positions.items():
            children = list(current_node['children'].items())
            
            if len(children) >= 1:
                left_bit, left_child = children[0]
                left_id = node_id * 2 + 1
                if left_id in positions:
                    x_left, y_left, _ = positions[left_id]
                    ax.plot([x, x_left], [y, y_left], 'r-', linewidth=2, alpha=0.7)
                    # Etiqueta
                    mid_x, mid_y = (x + x_left) / 2, (y + y_left) / 2
                    ax.text(mid_x - 0.1, mid_y + 0.1, left_bit, fontsize=12, 
                           fontweight='bold', color='red', ha='center', va='center',
                           bbox=dict(boxstyle="round,pad=0.1", facecolor='white', alpha=0.8))
            
            if len(children) >= 2:
                right_bit, right_child = children[1]
                right_id = node_id * 2 + 2
                if right_id in positions:
                    x_right, y_right, _ = positions[right_id]
                    ax.plot([x, x_right], [y, y_right], 'b-', linewidth=2, alpha=0.7)
                    # Etiqueta
                    mid_x, mid_y = (x + x_right) / 2, (y + y_right) / 2
                    ax.text(mid_x + 0.1, mid_y + 0.1, right_bit, fontsize=12, 
                           fontweight='bold', color='blue', ha='center', va='center',
                           bbox=dict(boxstyle="round,pad=0.1", facecolor='white', alpha=0.8))
    
    def _draw_nodes_sf(self, ax, node, positions):
        """Dibuja los nodos del árbol Shannon-Fano"""
        for node_id, (x, y, current_node) in positions.items():
            # Determinar color y etiqueta
            if current_node['char'] is not None:
                # Nodo hoja
                color = 'lightgreen'
                display_char = current_node['char']
                if current_node['char'] == ' ':
                    display_char = 'ESP'
                elif current_node['char'] == '\n':
                    display_char = 'NL'
                elif current_node['char'] == '\t':
                    display_char = 'TAB'
                label = display_char
            else:
                # Nodo interno
                color = 'lightcoral'
                label = ""
            
            # Dibujar círculo
            circle = plt.Circle((x, y), self.node_radius, color=color, 
                              ec='black', linewidth=2, zorder=3)
            ax.add_patch(circle)
            
            # Agregar texto
            if label:
                ax.text(x, y, label, ha='center', va='center', fontsize=10, 
                       fontweight='bold', zorder=4)
