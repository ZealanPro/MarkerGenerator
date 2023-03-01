# coding: cp1251
#by z04a, stalgrim
from PIL import Image, ImageDraw, ImageFont
import qrcode, hashlib
from alive_progress import alive_bar
import time, sys

#���������� � ��� ��� ����� ���������� ��� ������� �������
import argparse
parser = argparse.ArgumentParser(description='mark generator')
parser.add_argument('library', type=str, help='Library name') 
parser.add_argument('-l','--legacy', action='store_true', help='use legacy renderer') #���� ��� ������������� ����������� �������
parser.add_argument('-b','--blank', action='store_true', help='do not draw arrows') #���� ��� ���������� ��������� �������
parser.add_argument('-t','--text', action='store_true', help='disable text') #���� ��� ���������� ��������� ������
args = parser.parse_args()

DEFAULT_IDENTIFIER = "3257b0ae1f8d05fed50a757017a93688" #md5 ������������� ����������

LIBRARY_HASH = hashlib.md5(args.library.encode('utf-8')).hexdigest() #md5 ������������� ����������

def create(room, ruroom):
    
    #������ ������ ��� ��������� qr ����

    ROOM_HASH = hashlib.md5(room.encode('utf-8')).hexdigest() #md5 ������������� ��������

    FINAL_HASH = DEFAULT_IDENTIFIER + " " + LIBRARY_HASH + " " + ROOM_HASH #������ � ���� ������

    #---------------

    result_file.write(f'{FINAL_HASH} {room} {ruroom}') #������ ���������� � ������� � result.txt

    upscaleqr_size = 1150 #����������, �� �������� ����� ���������������� qr ��� (1150x1150 � �������)

    width = 2808 #�������� ������ �����
    height = 1984 #�������� ������ �����
    
    #�������� qr ����
    qrimg = qrcode.make(FINAL_HASH)
    upqr = qrimg.resize((upscaleqr_size,upscaleqr_size),resample=1)

    for i in range(1,3):
        if(i == 2):
            width = 1984
            height = 2808
        #�������� ����
        newImg = Image.new(mode = "RGB", size = (width,height), color = (255,255,255))

        #���������� ������������� ��������� ## DEPRECATED. PLEASE DO NOT USE.
        if args.legacy:
            x = 0
            for number in range(40):
                img1 = ImageDraw.Draw(newImg)
                img1.line([(x - width,0),(x,height)], fill="black", width = 12)
                x += width/15
        #----------------

        if not args.legacy: #����� ������
            if(i == 1):
                newImg.paste(diag_hor,(0,0))
            else:
                newImg.paste(diag_ver,(0,0))
            
        
        #������� qr ���� � ����� �����������
        newImg.paste(upqr, (int(width/2 - upscaleqr_size/2), int(height/2 - upscaleqr_size/2)))

        #������� �������
        if not args.blank:
            newImg.paste(arrow,(width-320,int(height/2-982/2)),arrow.convert('RGBA'))
            newImg.paste(arrow,(160,int(height/2-982/2)),arrow.convert('RGBA'))

        #������� ��������
        if not args.text:
            vot = Image.new(mode = "RGB", size = (width,80), color = (255, 255, 255))
            newImg.paste(vot, (0,height-80))
            idraw = ImageDraw.Draw(newImg)
            idraw.line((0,height-80,width,height-80), fill=0,width=8)
            font = ImageFont.truetype("src/newFont.ttf", size=80)
            bbox = idraw.textbbox((0,height-80),ruroom,font=font) #��� ����, ����� ��������� ����� �� ������ ������
            idraw.text((width/2-(bbox[2]/2),height-80), ruroom, font=font, fill=(0, 0, 0))
        #����������
        if i == 1:
            imgName = "result_hor/hor-" + args.library + "-" + room + ".png"
            newImg.save(imgName)
        else:
            imgName = "result_ver/vert-" + args.library + "-" + room + ".png"
            newImg.save(imgName)

#---------------main code---------------#
        
#������� ������� ��������� ����        
try:
    #��������� � ������ ����
    result_file = open('result.txt', 'w') #��������� ����, � ������� ����� ������ ���������
    result_file.write('APPHASH  LIBRARYHASH  ROOMHASH  ROOM  RU_ROOM\n')
    with open("library.txt", "r",encoding="UTF-8") as file:
        list_data = [] #��������� ������ ������
        listru_data = []
        for item in file:
            items = item.split(" ",1) #����� ������ �� ������� �������
            list_data.append(items[0]) #��������� ������� � ������
            listru_data.append(items[1]) #��������� ������� �������� ������ � ������
    file.close()
except:
    print('ERR: File not found. Did you put your data in library.txt?')
    sys.exit() # ���� ���� �� ������, ��������� �����������.

if(args.legacy): #�������������� ��� ������������� ����������� �������
    print('WRN: using LEGACY_RENDERER is deprecated.')

try:
    diag_hor = Image.open('src/diag_hor.png')
    diag_ver = Image.open('src/diag_ver.png')
    arrow = Image.open('src/arrow.png').convert('RGBA')
except:
    print('ERR: src images not found')
    sys.exit() # ���� ���� �� ������, ��������� �����������.

#����� ���������
with alive_bar(len(list_data)) as bar: 
    for i in range(0,len(list_data)):
        create(list_data[i], listru_data[i])
        bar(i/100 * (100 / len(list_data)))

result_file.close()

    

           


