import html2image
import os

print("Gerando imagem PNG para o post de Disciplina...")
hti = html2image.Html2Image(output_path='output', size=(1080, 1080))
hti.screenshot(html_file='output/disciplina_edge.html', save_as='disciplina_edge.png')
print("Imagem gerada com sucesso: output/disciplina_edge.png")
