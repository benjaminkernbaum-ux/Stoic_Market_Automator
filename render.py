import html2image
import os

print("Gerando imagem PNG a partir do HTML...")
hti = html2image.Html2Image(output_path='output', size=(1080, 1080))
hti.screenshot(html_file='output/analise_btc.html', save_as='analise_btc.png')
print("Imagem gerada com sucesso: output/analise_btc.png")
