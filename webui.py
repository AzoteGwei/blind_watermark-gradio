LANGUAGE = 'en' # change this to zh to use chinese

import gradio as gr
import numpy as np
import blind_watermark
import hashlib
import base64
import math
import binascii
import cv2

demo = gr.Blocks()

class BlindWatermarkUtil:
    def add_wm_text(pwd_wm_in : str,pwd_wm_pc : str,pwd_img_in : str,pwd_img_pc : str,img_in,text_in : str):
        pwd_wm = BlindWatermarkUtil.calc_pwd(pwd_wm_in,pwd_wm_pc)
        pwd_img = BlindWatermarkUtil.calc_pwd(pwd_img_in,pwd_img_pc)
        bwm_context = blind_watermark.WaterMark(password_wm=pwd_wm,password_img=pwd_img)
        bwm_context.read_img(img=img_in)
        bwm_context.read_wm(text_in,mode='str')
        return (str(len(bwm_context.wm_bit)),(np.rint(bwm_context.embed())).astype(int))
    def add_wm_bit(pwd_wm_in : str,pwd_wm_pc : str,pwd_img_in : str,pwd_img_pc : str,img_in,bit_in : str):
        pwd_wm = BlindWatermarkUtil.calc_pwd(pwd_wm_in,pwd_wm_pc)
        pwd_img = BlindWatermarkUtil.calc_pwd(pwd_img_in,pwd_img_pc)
        bwm_context = blind_watermark.WaterMark(password_wm=pwd_wm,password_img=pwd_img)
        bwm_context.read_img(img=img_in)
        bwm_context.read_wm(base64.b64decode(bit_in),mode='bit')
        return (str(len(bwm_context.wm_bit)),(np.rint(bwm_context.embed())).astype(int))
    def add_wm_img(pwd_wm_in : str,pwd_wm_pc : str,pwd_img_in : str,pwd_img_pc : str,img_in,img_wm_in):
        pwd_wm = BlindWatermarkUtil.calc_pwd(pwd_wm_in,pwd_wm_pc)
        pwd_img = BlindWatermarkUtil.calc_pwd(pwd_img_in,pwd_img_pc)
        bwm_context = blind_watermark.WaterMark(password_wm=pwd_wm,password_img=pwd_img)
        bwm_context.read_img(img=img_in)
        bwm_context.read_wm(img_wm_in,mode='img')
        wm = cv2.imread(filename=img_wm_in, flags=cv2.IMREAD_GRAYSCALE)
        return (str(wm.shape[0])+','+str(wm.shape[1]),(np.rint(bwm_context.embed())).astype(int))
    
    def read_wm_text(pwd_wm_in : str,pwd_wm_pc : str,pwd_img_in : str,pwd_img_pc : str,img_in,bitlen : str):
        pwd_wm = BlindWatermarkUtil.calc_pwd(pwd_wm_in,pwd_wm_pc)
        pwd_img = BlindWatermarkUtil.calc_pwd(pwd_img_in,pwd_img_pc)
        bwm_context = blind_watermark.WaterMark(password_wm=pwd_wm,password_img=pwd_img)
        return bwm_context.extract(embed_img=img_in,wm_shape=int(bitlen),mode='str')
    def read_wm_bit(pwd_wm_in : str,pwd_wm_pc : str,pwd_img_in : str,pwd_img_pc : str,img_in,bitlen : str):
        pwd_wm = BlindWatermarkUtil.calc_pwd(pwd_wm_in,pwd_wm_pc)
        pwd_img = BlindWatermarkUtil.calc_pwd(pwd_img_in,pwd_img_pc)
        bwm_context = blind_watermark.WaterMark(password_wm=pwd_wm,password_img=pwd_img)
        return base64.b64encode(bwm_context.extract(embed_img=img_in,wm_shape=int(bitlen),mode='bit'))
    def read_wm_img(pwd_wm_in : str,pwd_wm_pc : str,pwd_img_in : str,pwd_img_pc : str,img_in,bitlen : str):
        if ',' in list(bitlen):
            x,y = map(int,bitlen.split(','))
        else:
            y = int(math.ceil(math.sqrt(int(bitlen))))
            x = int(math.floor(bitlen/y))
        pwd_wm = BlindWatermarkUtil.calc_pwd(pwd_wm_in,pwd_wm_pc)
        pwd_img = BlindWatermarkUtil.calc_pwd(pwd_img_in,pwd_img_pc)
        bwm_context = blind_watermark.WaterMark(password_wm=pwd_wm,password_img=pwd_img)
        return np.rint(bwm_context.extract(embed_img=img_in,wm_shape=(x,y),mode='img')).astype(int)

    def quick_fill(bitlen_in,img_in):
        return (bitlen_in,img_in)

    def calc_pwd(password : str,process : str) -> int:
        if process == "int":
            return int(password)
        if process == "crc32":
            return binascii.crc32(password.encode('UTF-8'))
        if process == "md5":
            pwd = int(hashlib.md5(password.encode("UTF-8")).hexdigest(),base=16)
        if process == "sha256":
            pwd = int(hashlib.sha256(password.encode("UTF-8")).hexdigest(),base=16)
        return pwd % 4294967295

class i18n:
    language = LANGUAGE
    TRANSLATIONS = {
        'zh' : {
            'gr_desc':"# Blind Watermark UI\n\n这是对[原项目](https://github.com/guofei9987/blind_watermark)制作的 Gradio 前端.\n\n前端由 [Azote](https://github.com/AzoteGwei/blind_watermark-gradio/) 完成. ![MIT License](https://camo.githubusercontent.com/3bddfe59271999ba8484481b958c8d5b9904eef2dd1432379edc8d3ac955fca9/68747470733a2f2f696d672e736869656c64732e696f2f707970692f6c2f626c696e645f77617465726d61726b2e737667) \n\n 请注意，使用文本进行水印并不稳定，使用二维码来传递水印可以获得更好的读取率。",
            'pwd_wm_desc': "# 加密水印密码\n由于密码仅支持使用 int 类型,可以通过控制处理流程使得文本形式的密码变成 int.",
            'pwd_img_desc': "# 变换图片密码\n由于密码仅支持使用 int 类型,可以通过控制处理流程使得文本形式的密码变成 int.",
            'pwd_wm':"用于加密水印的密码",
            'pwd_img':"用于变换图像的密码",
            'pwd':"密码",
            'ctrl_process':"控制流程",
            'ctrl_desc':"用于控制如何变换密码",
            'ctrl_warn':"**请注意! 如果使用了非标准的密码(即非 int 类型),所有的散列结果将会对10进制下 `4294967295` 取模!!!**",
            'pic_in':"用于操作的图片",
            'add':"添加",
            'read':"读取",
            'wm':"水印",
            'str_wm':"文本水印",
            'bit_wm':"二进制水印",
            'img_wm':"图片水印",
            'process':"处理",
            'b64_wm':"Base64编码的二进制内容",
            'content':"内容",
            'wm_bitlen':"水印大小",
            'result':"结果",
            'quickfill':"一键将结果填入到操作处",
            'b64_result':"Base64编码的二进制结果",
            'img_bitlen':"读取图片需要知道水印的长宽，请使用 `长,宽` 的方式输入 bitlen. 若传入一个数字,则自动尝试图片."

        },
        'en' : {
            'gr_desc':"# Blind Watermark UI\n\nThis is a gradio frontend of the [Original Blind Watermark Project](https://github.com/guofei9987/blind_watermark)\n\nFrontend was written by [Azote](https://github.com/AzoteGwei/blind_watermark-gradio/). ![MIT License](https://camo.githubusercontent.com/3bddfe59271999ba8484481b958c8d5b9904eef2dd1432379edc8d3ac955fca9/68747470733a2f2f696d672e736869656c64732e696f2f707970692f6c2f626c696e645f77617465726d61726b2e737667) \n\n Please note that watermarking with text is not stable, and using a QR code to deliver the watermark gives a better read rate. \n\n This Space has a Chinese version, please `duplicate this Space` and edit the first line of webui.py to switch the language.",
            'pwd_wm_desc': "# Watermark Encrypten Password\nSince only int type is supported for passwords, it is possible to control the processing flow so that a textual password becomes an int.",
            'pwd_img_desc': "# Image Diffusion Password\nSince only int type is supported for passwords, it is possible to control the processing flow so that a textual password becomes an int.",
            'pwd_wm':"Watermark Encrypten Password",
            'pwd_img':"Image Diffusion Password",
            'pwd':"Password",
            'ctrl_process':"Control Steps",
            'ctrl_desc':"Determine how to process the password.",
            'ctrl_warn':"**Please note! If a non-standard password is used (i.e. not of int type), all hash results will be modulo `4294967295` in decimal!!!**",
            'pic_in':"Picture to be processed",
            'add':"Add",
            'read':"Read",
            'wm':"Watermark",
            'str_wm':"Text Watermark",
            'bit_wm':"Binary Watermark",
            'img_wm':"Picture Watermark",
            'process':"Process",
            'b64_wm':"Base64 Encoded Binary Watermark",
            'content':"Content",
            'wm_bitlen':"Watermark Size",
            'result':"Result",
            'quickfill':"Fill in the results to the input",
            'b64_result':"Base64 Encoded Result",
            'img_bitlen':"To read the image you need to know the length and width of the watermark, enter the bitlen using `length,width`. If you pass in a number, the image is automatically tried."
        }
    }
    def getTranslation(token):
        if not i18n.language in i18n.TRANSLATIONS:
            return 'ILLEGAL LANGUAGE'
        if not token in i18n.TRANSLATIONS[i18n.language]:
            return 'ILLEGAL TOKEN'
        return i18n.TRANSLATIONS[i18n.language][token]
    def fetchLanguage(request : gr.Request):
        if request.headers["Accept-Language"].split(",")[0].lower().startswith("zh"):
            i18n.language = 'zh'
        else:
            i18n.language = 'en'

with demo:
    # demo.load(i18n.fetchLanguage,outputs=[demo])
    gr.Markdown(i18n.getTranslation('gr_desc'))
    with gr.Row():
        with gr.Column():
            with gr.Row():
                gr.Markdown(i18n.getTranslation('pwd_wm_desc'))
                password_wm_input = gr.Textbox(value="1",info=i18n.getTranslation('pwd_wm'),label=i18n.getTranslation('pwd'))
                password_wm_process_input = gr.Dropdown(["int","crc32","md5","sha256"],value='int',multiselect=False, label=i18n.getTranslation('ctrl_process'),info=i18n.getTranslation('ctrl_desc'))
            with gr.Row():
                gr.Markdown(i18n.getTranslation('pwd_img_desc'))
                password_img_input = gr.Textbox(value="1",info=i18n.getTranslation('pwd_img'),label=i18n.getTranslation('pwd'))
                password_img_process_input = gr.Dropdown(["int","crc32","md5","sha256"],value='int',multiselect=False, label=i18n.getTranslation('ctrl_process'),info=i18n.getTranslation('ctrl_desc'))
        gr.Markdown(i18n.getTranslation('ctrl_warn'))
    image_input = gr.Image(label=i18n.getTranslation('pic_in'))
    with gr.Tabs():
        with gr.TabItem(i18n.getTranslation('add')):
            with gr.Tabs():
                with gr.TabItem(i18n.getTranslation('str_wm')):
                    with gr.Row():
                        text_wm_input = gr.Textbox("watermark text",info=i18n.getTranslation('wm'),label=i18n.getTranslation("content"))
                        text_wm_button = gr.Button(i18n.getTranslation("process"))
                with gr.TabItem(i18n.getTranslation('bit_wm')):
                    with gr.Row():
                        bit_wm_input = gr.Textbox(label=i18n.getTranslation('b64_wm'))
                        bit_wm_button = gr.Button(i18n.getTranslation("process"))
                with gr.TabItem(i18n.getTranslation('img_wm')):
                    with gr.Row():
                        img_wm_input = gr.Image(label=i18n.getTranslation("content"),type='filepath')
                        img_wm_button = gr.Button(i18n.getTranslation("process"))
            bitlen_output = gr.Textbox(label=i18n.getTranslation("wm_bitlen"))
            image_output = gr.Image(label=i18n.getTranslation("result"))
            quick_fill_button = gr.Button(i18n.getTranslation("quickfill"))
        with gr.TabItem(i18n.getTranslation('read')):
            bitlen_input = gr.Textbox(label=i18n.getTranslation("wm_bitlen"))
            with gr.Tabs():
                with gr.TabItem(i18n.getTranslation('str_wm')):
                    with gr.Row():
                        readtext_output = gr.Textbox(label=i18n.getTranslation("result"))
                        readtext_button = gr.Button(i18n.getTranslation("process"))
                with gr.TabItem(i18n.getTranslation('bit_wm')):
                    with gr.Row():
                        readbit_output = gr.Textbox(label=i18n.getTranslation("b64_result"))
                        readbit_button = gr.Button(i18n.getTranslation("process"))
                with gr.TabItem(i18n.getTranslation('img_wm')):
                    with gr.Row():
                        gr.Markdown(i18n.getTranslation("img_bitlen"))
                        readimg_output = gr.Image(label=i18n.getTranslation("result"))
                        readimg_button = gr.Button(i18n.getTranslation("process"))
    text_wm_button.click(BlindWatermarkUtil.add_wm_text,inputs=[password_wm_input,password_wm_process_input,password_img_input,password_img_process_input,image_input,text_wm_input],outputs=[bitlen_output,image_output])
    bit_wm_button.click(BlindWatermarkUtil.add_wm_bit,inputs=[password_wm_input,password_wm_process_input,password_img_input,password_img_process_input,image_input,bit_wm_input],outputs=[bitlen_output,image_output])
    img_wm_button.click(BlindWatermarkUtil.add_wm_img,inputs=[password_wm_input,password_wm_process_input,password_img_input,password_img_process_input,image_input,img_wm_input],outputs=[bitlen_output,image_output])
    readtext_button.click(BlindWatermarkUtil.read_wm_text,inputs=[password_wm_input,password_wm_process_input,password_img_input,password_img_process_input,image_input,bitlen_input],outputs=[readtext_output])
    readbit_button.click(BlindWatermarkUtil.read_wm_bit,inputs=[password_wm_input,password_wm_process_input,password_img_input,password_img_process_input,image_input,bitlen_input],outputs=[readbit_output])
    readimg_button.click(BlindWatermarkUtil.read_wm_img,inputs=[password_wm_input,password_wm_process_input,password_img_input,password_img_process_input,image_input,bitlen_input],outputs=[readimg_output])
    quick_fill_button.click(BlindWatermarkUtil.quick_fill,inputs=[bitlen_output,image_output],outputs=[bitlen_input,image_input])

blind_watermark.bw_notes.close()

if __name__ == "__main__":
    demo.launch()