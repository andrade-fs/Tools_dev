# from imp import find_module
import requests
import json
import shutil
import bitly_api
import smtplib
import ssl
from PIL import Image
import cv2
import numpy as np
from bs4 import BeautifulSoup
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime import base
from turtle import pos
from email.mime.image import MIMEImage
import zipfile
from shutil import make_archive
import os
from email.mime.base import MIMEBase
from email import encoders

# SCRIPT TO NOTIFY NEW POST ON AMES WEB
# AVA SOLUCIONES TECONOLÓGICAS - by employee: SANTIAGO ANDRADE
# PLEASE READ READMEE!!
# ENJOY IT.

#----------------VARIABLES-------------------
BITLY_ACCESS_TOKEN ="0ad868f817d661b747aa5cbf9ea505f47c47b38a" #BITLY TOKEN
BASE_URL           = 'https://www.concellodeames.gal' #URL BASE OF AMES WEB
# CODE TO OPEN JSON
a_file = open("blog_update.json", "r")
diccionario = json.load(a_file)
a_file.close()

#FUNCTION TO SEND EMAIL
def sendEmail(href_post,title_post, name_image, resume_post):
    # # Please replace below with your email address and password
    x = bitly_api.Connection(access_token = BITLY_ACCESS_TOKEN)
    # CHANGE VALUE OF EMAIL!!!!
    # sender_email  = 'redessociales@avatools.com' 
    # password      = '*_Z9cx8t7.2022'
    sender_email  = 'a19santiagoaf@iessanclemente.net'
    password      = 'nbeluahypmboqlgt'
    receiver_email= 'santiago.andrade@avaforum.com'
  
    full_url = str(BASE_URL)+str(href_post)
    response = x.shorten(full_url)
    message = MIMEMultipart("alternative")
    message["Subject"] = "Nueva publicación en Concello de Ames"
    message["From"] = sender_email
    message["To"] = receiver_email
    
    # Adjuntamos Imagen
    file = open(name_image, "rb")
    attach_image = MIMEImage(file.read())
    attach_image.add_header('Content-Disposition', 'attachment; filename ='+name_image)
    
    # Abrimos el archivo que vamos a adjuntar
    archivo_adjunto = open('imagenes_ames.zip', 'rb')
    # Creamos un objeto MIME base
    adjunto_MIME = MIMEBase('application', 'octet-stream')
    # Y le cargamos el archivo adjunto
    adjunto_MIME.set_payload((archivo_adjunto).read())
    # Codificamos el objeto en BASE64
    encoders.encode_base64(adjunto_MIME)
    # Agregamos una cabecera al objeto
    adjunto_MIME.add_header('Content-Disposition', "attachment; filename=imagenes_ames.zip'")

    
    enlace_texto = "<p>Enlace en bitly: "+str(response['url'])+"</p>"
    text=  'Concello de Ames, subió una nueva entrada al blog, echale un vistazo: '
    html_enlace = "<a href='"+str(response['url'])+"'>"+str(title_post)+"</a>"
    html = """\
            <html>
                <body>
                    <h4>Buenas!</h4>
                    <p>¡Concello de Ames subió una nueva publicación!</p>
                    """+html_enlace+"""
                    """+enlace_texto+"""
                    <p>Te mostramos un breve resumen de la pág web:</p>
                    """+resume_post+"""
                    <p>Esto es un mensaje automatizado cualquier respuesta a este mensaje no será contestado.</p>
                    <p>Gracias!</p>
                    <p>AVA - Soluciones Tecnológicas</p>
                    <p><small>
                    =================================================<br>
                    Este mensaje y los adjuntos pueden contener información confidencial, no estando permitida su comunicación, reproducción o distribución. Si usted no es el destinatario final, le rogamos nos lo comunique y borre el mismo. De conformidad con lo que dispone el RGPD, LOPDGDD y demás normativa legal vigente en materia de protección de datos personales, le informamos que los datos personales serán tratados bajo la responsabilidad de AVA SOLUCIONES TECNOLÓGICAS, S.L. Puede ejercer los derechos de acceso, rectificación, portabilidad, supresión, limitación y oposición mandando un mensaje a ava.info@avaforum.com. Si considera que el tratamiento no se ajusta a la normativa vigente, podrá presentar una reclamación ante la autoridad de control en www.aepd.es. Para más información puede consultar nuestra política de privacidad en www.avaforum.com/politica-de-privacidad
                    This message and the attachments may contain confidential information, their communication, reproduction or distribution is not allowed. If you are not the final recipient, please let us know and delete it. In accordance with the provisions of the RGPD, LOPDGDD and other current legal regulations regarding the protection of personal data, we inform you that personal data will be treated under the responsibility of AVA SOLUCIONES TECNOLÓGICAS, S.L. You can exercise the rights of access, rectification, portability, deletion, limitation and opposition by sending a message to ava.info@avaforum.com. If you consider that the treatment does not comply with current regulations, you can file a claim with the control authority at www.aepd.es. For more information, you can consult our privacy policy at www.avaforum.com/politica-de-privacidad.<br>
                    ================================================= 
                    </small></p>
                </body>
            </html>
            """
                
    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)
    message.attach(attach_image)
    # Y finalmente lo agregamos al mensaje
    message.attach(adjunto_MIME)
    
    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )

def edit_image(filename, boolean = True):
    # Sum img
    marco_imagen = Image.open(r'Marco_Instgram.png')
    if(boolean):
        fondo_imagen = Image.open('./imagenes_originales/'+filename)
    else:
        fondo_imagen = Image.open('last_post_ames.jpg')
        
    mask_im      = Image.open(r'Marco_Instgram.png').convert("RGBA")
    marco        = Image.open(r'Marco_Instgram.png')

    # ------------------------[START] CODE TO RESIZE IMG TO MASK-------------------------    
    #IMAGEN DE FONDO REDIMENSIONADA
    fixed_height   = 1080
    height_percent = (fixed_height / float(fondo_imagen.size[1]))
    width_size     = int((float(fondo_imagen.size[0]) * float(height_percent)))
    image1         = fondo_imagen.resize((width_size, fixed_height))
    start_postion  = int((width_size - 1080) /2)

    
    #MASCARA
    marco_imagen.paste(image1,(-int(start_postion),0)) 
    marco_imagen.paste(marco,(0,0),mask_im)
    # marco_imagen.show()
    if(boolean):
        path ="./imagenes_editadas/resize_"+ filename
    else:
        path ="./last_post_ames_edited.jpg"
    marco_imagen.save(path, 'png')
    # ------------------------[END] CODE TO RESIZE IMG TO MASK--------------------------
    # ==================================================================================
    # ------------------------[START] CODE TO AJUST IMG TO MASK-------------------------
    if(float(fondo_imagen.size[1]) > float(fondo_imagen.size[0]) ): # ALARGADA
        print('ALARGADA')
        fixed_height        = 1080
        height_percent      = (fixed_height / float(fondo_imagen.size[1]))
        width_size          = int((float(fondo_imagen.size[0]) * float(height_percent)))
        fondo_imagen_resize = fondo_imagen.resize((width_size, fixed_height))
        start_postion_width = int((width_size - 1080) /2)
        start_postion_height= 0

    else:                                              # APAISADA
        print('APAISADA')
        fixed_width         = 1080
        width_percent       = (fixed_width / float(fondo_imagen.size[0]))
        height_size         = int((float(fondo_imagen.size[1]) * float(width_percent)))
        fondo_imagen_resize = fondo_imagen.resize((fixed_width, height_size))
        start_postion_width = 0
        start_postion_height= (int((1080- height_size  ) /2))

    #MASCARA
    marco_imagen = Image.open(r'Marco_Instgram.png')
    marco_imagen.paste(fondo_imagen_resize,(start_postion_width,start_postion_height)) 
    marco_imagen.paste(marco,(0,0),mask_im)
    # marco_imagen.show()
    path ="./imagenes_editadas/ajust_"+ filename
    
    marco_imagen.save(path, 'png')
    # ------------------------[END] CODE TO AJUST IMG TO MASK---------------------------
    # ==================================================================================    

def download_image(href, boolean = True):
    # Open the url image, set stream to True, this will return the stream content.
    request_image = requests.get(href, stream = True)
    extension_img = href.split("/")[-1].split('?')[0]
    filename      = extension_img
    if request_image.status_code == 200:
        # Set decode_content value to Trequest_imageue, otherwise the downloaded image file's size will be zero.
        request_image.raw.decode_content = True
        # Open a local file with wb ( write binary ) permission.
        if(boolean):
            with open('./imagenes_originales/'+filename,'wb') as f:
                shutil.copyfileobj(request_image.raw, f)    
                print('Image sucessfully Downloaded: ',filename)    
        else:
            with open('last_post_ames.jpg','wb') as f:
                shutil.copyfileobj(request_image.raw, f)    
                print('Image sucessfully Downloaded: ',filename)    
    else:
        print('Image Couldn\'t be retreived')
    edit_image(filename, boolean)    

    return filename

#FUNCTION TO SCRAPP SINGLE POST        
def scrapp_pos(href_post, title_post):
    post_url =  str(BASE_URL)+str(href_post)
    #START SCRAPPING WEB
    post          = requests.get(post_url)
    post_soup     = BeautifulSoup(post.content, "html.parser")
    listing_post  = post_soup.findAll("div",{"class":"field-item even"})
    listing_image = post_soup.findAll("img", alt=True)
    summary_post  = listing_post[1].find('p').get_text()
    src_img       = listing_post[-1].find('a')['href']
    filename      = src_img.split("/")[-1].split('?')[0]
    base_src      = src_img.replace(filename, '')
    
    print(filename.split('.')[1])
    
    if(filename.split('.')[1] == 'png' or filename.split('.')[1] == 'jpg' ):
        download_image(src_img, False)
    
    for index in range(len(listing_image)):        
        if(listing_image[index]['alt'] == title_post):
           src_img     =  base_src +  listing_image[index]['src'].split("/")[-1].split('?')[0]
           extension   = src_img.split('.')[1]
           print(extension)
           if(extension ==  'jpg' or extension == 'png'):
            name_image  = download_image(src_img)
    
    sendEmail(href_post, title_post,'last_post_ames_edited.jpg', summary_post)
    
def zipdir(path, ziph):
        # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file), 
                       os.path.relpath(os.path.join(root, file), 
                                       os.path.join(path, '..')))
      

#FUNCTION TO SEARCH IN ALL POST THE LATEST
def scrapp_all_post():
    
    #Define url to scrape
    URL = 'https://www.concellodeames.gal/gl/actualidade'
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    # listing_content = soup.findChild("span",{"class":"texto-titular"}).get_text(strip=True)
    listing_content = soup.findChild("span",{"class":"texto-titular"})

    href_post  = listing_content.find('a')['href']
    title_post = listing_content.find('a').get_text()
    if(diccionario["primera_entrada"] != None):
        if(diccionario["primera_entrada"] != title_post):
            diccionario["primera_entrada"] = title_post
            scrapp_pos(href_post, title_post)
         
            zipf = zipfile.ZipFile('imagenes_ames.zip', 'w', zipfile.ZIP_DEFLATED)
            zipdir('imagenes_editadas/', zipf)
            zipdir('imagenes_originales/', zipf)
            zipf.close()
            
            a_file = open("blog_update.json", "w")
            json.dump(diccionario, a_file)
            a_file.close()

#START
scrapp_all_post()        

# SAVE JSON SAVING CHANGES





