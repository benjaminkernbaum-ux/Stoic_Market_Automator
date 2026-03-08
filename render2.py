import html2image
import os

print("Gerando imagem PNG a partir do novo HTML...")
hti = html2image.Html2Image(output_path='output', size=(1080, 1080))
hti.screenshot(html_file='output/psicologia_trader.html', save_as='psicologia_trader.png')
print("Imagem gerada com sucesso: output/psicologia_trader.png")
