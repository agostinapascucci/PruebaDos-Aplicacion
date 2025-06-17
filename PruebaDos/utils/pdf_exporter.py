"""
Utilidad para exportar resultados a PDF
Genera un reporte completo con todas las estadísticas y gráficos
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.legends import Legend
import tempfile
import os
from datetime import datetime

from utils.statistics import StatisticsCalculator
from utils.visualizer import DataVisualizer

class PDFExporter:
    """Exportador de resultados a PDF"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=18,
            spaceAfter=30,
            alignment=1  # Center
        )
        
    def export_results(self, filename, original_text, huffman_results, shannon_fano_results):
        """Exporta todos los resultados a un archivo PDF"""
        doc = SimpleDocTemplate(filename, pagesize=A4)
        story = []
        
        # Título
        story.append(Paragraph("Reporte de Compresión de Datos", self.title_style))
        story.append(Paragraph(f"Generado el: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}", 
                              self.styles['Normal']))
        story.append(Spacer(1, 20))
        
        # Información del texto original
        story.append(Paragraph("Información del Texto Original", self.styles['Heading2']))
        text_info = [
            ['Longitud del texto:', str(len(original_text))],
            ['Caracteres únicos:', str(len(set(original_text)))],
            ['Primeros 200 caracteres:', original_text[:200] + ('...' if len(original_text) > 200 else '')]
        ]
        
        text_table = Table(text_info, colWidths=[2*inch, 4*inch])
        text_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(text_table)
        story.append(Spacer(1, 20))
        
        # Estadísticas comparativas
        story.append(Paragraph("Comparación de Algoritmos", self.styles['Heading2']))
        stats_calc = StatisticsCalculator()
        comparison = stats_calc.compare_algorithms(huffman_results, shannon_fano_results)
        
        comp_data = [['Métrica', 'Huffman', 'Shannon-Fano', 'Mejor']]
        for metric, values in comparison.items():
            comp_data.append([
                metric,
                values['huffman'],
                values['shannon_fano'],
                'Huffman' if values['winner'] == 'huffman' else 'Shannon-Fano'
            ])
        
        comp_table = Table(comp_data, colWidths=[2*inch, 1.5*inch, 1.5*inch, 1.5*inch])
        comp_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(comp_table)
        story.append(PageBreak())
        
        # Tabla detallada de Huffman
        story.append(Paragraph("Tabla Detallada - Algoritmo de Huffman", self.styles['Heading2']))
        huffman_table_data = stats_calc.create_detailed_table(huffman_results)
        huffman_headers = ['Símbolo', 'Freq.', 'Prob.', 'Código', 'Long.', 'Info.', 'Entropía', 'Bits', 'L.Prom.']
        
        huffman_full_data = [huffman_headers] + huffman_table_data[:15]  # Limitar a 15 filas
        
        huffman_table = Table(huffman_full_data, colWidths=[0.7*inch] * 9)
        huffman_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(huffman_table)
        story.append(PageBreak())
        
        # Tabla detallada de Shannon-Fano
        story.append(Paragraph("Tabla Detallada - Algoritmo de Shannon-Fano", self.styles['Heading2']))
        sf_table_data = stats_calc.create_detailed_table(shannon_fano_results)
        sf_full_data = [huffman_headers] + sf_table_data[:15]  # Usar los mismos headers
        
        sf_table = Table(sf_full_data, colWidths=[0.7*inch] * 9)
        sf_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(sf_table)
        story.append(Spacer(1, 20))
        
        # Códigos generados
        story.append(Paragraph("Códigos Generados", self.styles['Heading2']))
        
        # Huffman codes
        story.append(Paragraph("Códigos Huffman:", self.styles['Heading3']))
        huffman_codes_text = ", ".join([f"'{k}': {v}" for k, v in list(huffman_results['codes'].items())[:20]])
        story.append(Paragraph(huffman_codes_text, self.styles['Normal']))
        story.append(Spacer(1, 10))
        
        # Shannon-Fano codes
        story.append(Paragraph("Códigos Shannon-Fano:", self.styles['Heading3']))
        sf_codes_text = ", ".join([f"'{k}': {v}" for k, v in list(shannon_fano_results['codes'].items())[:20]])
        story.append(Paragraph(sf_codes_text, self.styles['Normal']))
        
        # Construir PDF
        doc.build(story)
