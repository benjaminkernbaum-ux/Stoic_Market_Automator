import html2image
import os

print("Gerando imagem PNG do Post Dia 1...")
hti = html2image.Html2Image(output_path='output', size=(1080, 1080))
hti.screenshot(html_file='output/dia1_manha.html', save_as='dia1_manha.png')
print("Imagem gerada com sucesso: output/dia1_manha.png")
