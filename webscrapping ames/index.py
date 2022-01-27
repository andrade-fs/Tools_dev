#!/usr/bin/python3
# -*- coding: utf-8 -*-

# ATD - Para instalar dependencias en python 2.7
# Ejemplo "requests"
# sudo apt-get install python-requests

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
import shutil
import time

# SCRIPT TO NOTIFY NEW POST ON AMES WEB
# AVA SOLUCIONES TECONOLOGICAS - by employee: SANTIAGO ANDRADE
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
def sendEmail(href_post,title_post, name_image, resume_post,filename_zip ):
    # # Please replace below with your email address and password
    x = bitly_api.Connection(access_token = BITLY_ACCESS_TOKEN)
    # CHANGE VALUE OF EMAIL!!!!
    
    sender_email  = 'redessociales@avatools.com' 
    password      = '*_Z9cx8t7.2022'
    
    # sender_email  = 'a19santiagoaf@iessanclemente.net'
    # password      = 'nbeluahypmboqlgt'
    
    # receiver_email= 'redessociales@avatools.com'
    receiver_email= 'a19santiagoaf@iessanclemente.net'

    full_url = str(BASE_URL)+str(href_post)
    response = x.shorten(full_url)
    message = MIMEMultipart("alternative")
    message["Subject"] = "Nueva publicaciOn en Concello de Ames"
    message["From"] = sender_email
    message["To"] = receiver_email
    
    # Adjuntamos Imagen Editada
    file = open('./repo_temp/'+name_image, "rb")
    attach_image = MIMEImage(file.read())
    attach_image.add_header('Content-Disposition', 'attachment; filename ='+name_image)
    
    
    #ATTACH .ZIP ON EMAIL
        # # Abrimos el archivo que vamos a adjuntar
        # archivo_adjunto = open('imagenes_ames.zip', 'rb')
        # # Creamos un objeto MIME base
        # adjunto_MIME = MIMEBase('application', 'octet-stream')
        # # Y le cargamos el archivo adjunto
        # adjunto_MIME.set_payload((archivo_adjunto).read())
        # # Codificamos el objeto en BASE64
        # encoders.encode_base64(adjunto_MIME)
        # # Agregamos una cabecera al objeto
        # adjunto_MIME.add_header('Content-Disposition', "attachment; filename=imagenes_ames.zip")

    
    enlace_texto = "<p>Enlace en bitly: "+str(response['url'])+"</p>"
    text=  'Concello de Ames, ha subido una nueva entrada al blog, echale un vistazo: '
    html_enlace = "<a href='"+str(response['url'])+"'>"+str(title_post.encode('utf-8'))+"</a>"
    html = """\
            <html>
                <body>
                    <h4>Buenas!</h4>
                    <p>Concello de Ames ha subido una nueva publicacion!</p>
                    """+html_enlace+"""
                    """+enlace_texto+"""
                    <p>Te mostramos un breve resumen de la pagina web:</p>
                    """+resume_post+"""
                    <p>Esto es un mensaje automatizado. Cualquier respuesta a este mensaje no va a ser contestado.</p>
                    <p>Gracias!</p>
                    <p>AVA Soluciones Tecnologicas</p>
                    <p><small>
                    <br>=================================================<br>
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
    # Y finalmente lo agregamos el zip al mensaje
        # message.attach(adjunto_MIME)
    
    # Create secure connection with server and send email
    # context = ssl.create_default_context()
    # with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    #     server.login(sender_email, password)
    #     server.sendmail(
    #         sender_email, receiver_email, message.as_string()
    #     )

    with smtplib.SMTP("mail.avatools.com", 25) as server:
        server.login(sender_email, password)
        server.sendmail(
        sender_email, receiver_email, message.as_string()
    )




def edit_image(filename, boolean = True):
    # Sum img
    marco_imagen = Image.open(r'./bases_img/Marco_Instgram.png')
    if(boolean):
        fondo_imagen = Image.open('./repo_temp/imagenes_originales/'+filename)
    else:
        fondo_imagen = Image.open('./repo_temp/last_post_ames.jpg')
        
    mask_im      = Image.open(r'./bases_img/Marco_Instgram.png').convert("RGBA")
    marco        = Image.open(r'./bases_img/Marco_Instgram.png')

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
        path ="./repo_temp/imagenes_editadas/resize_"+ filename
    else:
        path ="./repo_temp/last_post_ames_edited.jpg"
    marco_imagen.save(path, 'png')
    # ------------------------[END] CODE TO RESIZE IMG TO MASK--------------------------
    # ==================================================================================
    # ------------------------[START] CODE TO AJUST IMG TO MASK-------------------------
    if(float(fondo_imagen.size[1]) > float(fondo_imagen.size[0]) ): # ALARGADA
        fixed_height        = 1080
        height_percent      = (fixed_height / float(fondo_imagen.size[1]))
        width_size          = int((float(fondo_imagen.size[0]) * float(height_percent)))
        fondo_imagen_resize = fondo_imagen.resize((width_size, fixed_height))
        start_postion_width = int((width_size - 1080) /2)
        start_postion_height= 0

    else:                                              # APAISADA
        fixed_width         = 1080
        width_percent       = (fixed_width / float(fondo_imagen.size[0]))
        height_size         = int((float(fondo_imagen.size[1]) * float(width_percent)))
        fondo_imagen_resize = fondo_imagen.resize((fixed_width, height_size))
        start_postion_width = 0
        start_postion_height= (int((1080- height_size  ) /2))

    #MASCARA
    marco_imagen = Image.open(r"./bases_img/Marco_Instgram.png")
    marco_imagen.paste(fondo_imagen_resize,(start_postion_width,start_postion_height)) 
    marco_imagen.paste(marco,(0,0),mask_im)
    # marco_imagen.show()
    path ="./repo_temp/imagenes_editadas/ajust_"+ filename
    
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
            with open('./repo_temp/imagenes_originales/'+filename,'wb') as f:
                shutil.copyfileobj(request_image.raw, f)    
                print('Image sucessfully Downloaded: ',filename)    
        else:
            with open('./repo_temp/last_post_ames.jpg','wb') as f:
                shutil.copyfileobj(request_image.raw, f)    
                print('Image sucessfully Downloaded: ',filename)    
    else:
        print('Image Couldn\'t be retreived')
    edit_image(filename, boolean)    

    return filename

#FUNCTION TO SCRAPP SINGLE POST        
def scrapp_pos(href_post, title_post, url_bitly):
    #UNCOMMENT AND EDIT FOR STATIC URL
    #post_url = 'https://www.concellodeames.gal/gl/novas/ponse-en-marcha-campana-o-bus-que-me-leva-para-informar-dos-horarios-e-linas-do-transporte'
    
    #DINAMIC POST
    post_url =  str(BASE_URL)+str(href_post)
    
    #START SCRAPPING WEB
    post           = requests.get(post_url)
    post_soup      = BeautifulSoup(post.content, "html.parser")
    
    try:  #Search main container with principal img
        div_img_princ  = post_soup.find("div",{"class":"field field-name-field-imagen field-type-image field-label-hidden"})
        src_img_prin   = div_img_princ.findChildren('img')[0]['src']  #Find img to get SRC
            #Now we split te src, to get base src, because multimedia img are smallest than original, because the path changes
        filename_img   = src_img_prin.split("/")[-1].split('?')[0]
        base_src       = src_img_prin.replace(filename_img, '')  
        # print(base_src)  # UNCOMMET THIS LINE, TO UNDERSTAND BETTER WHY I DECIDE TO SPLIT THE SRC.
        
        download_image(src_img_prin, False) #Send download singles img, to attach in email
    except:
        print('Could not find base html')
        
   
    try: #Search main container of summary post
        div_summary    = post_soup.findAll("div",{"class":"field-item even"})
        summary_post   = div_summary[1].find('p').get_text()
    except:
        print("Could not find summary Post") 
        
   
    try: #Search multimedia if is possible.
        div_multimedia = post_soup.findAll("div",{"id":"block-multimedia-1"})[0].findChildren('ul')
        img_multimedia = div_multimedia[0].findAll('img')
        
        for index in range(len(img_multimedia)):  #Send to download function.
            src_img       =  base_src + img_multimedia[index]['src'].split("/")[-1].split('?')[0]
            name_image    =  download_image(src_img) 
    except:
          print("Could not find multimedia img") 
        
    try:
        f= open("./repo_temp/README_AMES.txt","w+")
        f.write('AVA SOLUCIONES TECNOLOGICAS  \r\n')
        f.write('Titulo: ' + str(title_post))
        f.write('\r\n Enlace original: ' +str(post_url))
        f.write('\r\n Enlace BitLy: '+str(url_bitly))
        f.write(' \r\n Resumen: '+ summary_post)
        f.close()
    except:
        print('ERROR creating: file.txt')
        
    return summary_post
        
def zipdir(path, ziph):
        # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file), 
                       os.path.relpath(os.path.join(root, file), 
                                       os.path.join(path, '..')))

def delete_tmp_ifles(folder):
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file) 
        try: 
            if os.path.isfile(file_path): 
                os.unlink(file_path) 
            else:
                delete_tmp_ifles(file_path)
        except Exception: 
            print('Error removing tmp files')
            
def remove_file(path):
    # removing the file
	if not os.remove(path):
		print("{path} is removed successfully")
	else:
		print("Unable to delete the {path}")

def get_file_or_folder_age(path):
	ctime = os.stat(path).st_ctime
	return ctime

def delete_week_files(folder):
    days    = 7;
    seconds = time.time() - (days * 24 * 60 *60)
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        if os.path.isfile(file_path):
            if seconds >= get_file_or_folder_age(file_path):
                remove_file(file_path)
    
def generate_bitly(path):
    x = bitly_api.Connection(access_token = BITLY_ACCESS_TOKEN)

    full_url = str(BASE_URL)+str(path)
    response = x.shorten(full_url)['url']
    return response

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
    print(title_post)
   
    if(diccionario["primera_entrada"] != None):
        if(diccionario["primera_entrada"] != title_post):
            diccionario["primera_entrada"] = title_post
            #SEARCH POST, DOWNLOAD IMG...
            url_bitly     = generate_bitly(href_post)
            summary_post  = scrapp_pos(href_post, title_post, url_bitly)
            
            # GENERATE .ZIP
            zipf = zipfile.ZipFile('./repo_zip/'+str(title_post[0:10]).replace(" ", "")+'_.zip', 'w', zipfile.ZIP_DEFLATED)
            zipdir('repo_temp/', zipf)
            zipf.close()
            
            #SEND EMIAL
            sendEmail(href_post, title_post,'last_post_ames_edited.jpg', summary_post,'./repo_zip/'+str(title_post[0:10]).replace(" ", "")+'_.zip' )
            
            #DELETE TMP FILES
            folder_tmp = './repo_temp'
            folder_zip = './repo_zip'
            delete_tmp_ifles(folder_tmp)
            delete_week_files(folder_zip)
            
            #UPDATE JSON WITH NAME OF LAST POST
            a_file = open("blog_update.json", "w")
            json.dump(diccionario, a_file)
            a_file.close()

#START
scrapp_all_post()        

# SAVE JSON SAVING CHANGES