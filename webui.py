import gradio as gr

import blind_watermark
import hashlib

demo = gr.Blocks()

class BlindWatermarkUtil:
    def add_wm_text(pwd_wm_in : str,pwd_wm_pc : str,pwd_img_in : str,pwd_img_pc : str,img_in,text_in : str):
        pwd_wm = BlindWatermarkUtil.calc_pwd(pwd_wm_in,pwd_wm_pc)
        pwd_img = BlindWatermarkUtil.calc_pwd(pwd_img_in,pwd_img_pc)
        bwm_context = blind_watermark.WaterMark(password_wm=pwd_wm,password_img=pwd_img)
        bwm_context.read_img(img=img_in)
        bwm_context.read_wm(text_in,mode='str')
        len_wm = str(len(bwm_context.wm_bit))
        return (len_wm,bwm_context.embed())
    def add_wm_file(pwd_wm_in : str,pwd_wm_pc : str,pwd_img_in : str,pwd_img_pc : str,img_in,file_in : list[bytes]):
        pwd_wm = BlindWatermarkUtil.calc_pwd(pwd_wm_in,pwd_wm_pc)
        pwd_img = BlindWatermarkUtil.calc_pwd(pwd_img_in,pwd_img_pc)
        bwm_context = blind_watermark.WaterMark(password_wm=pwd_wm,password_img=pwd_img)
        bwm_context.read_img(img=img_in)
        bwm_context.read_wm(file_in,mode='bit')
        len_wm = str(len(bwm_context.wm_bit))
        return (len_wm,bwm_context.embed())
    def add_wm_img(pwd_wm_in : str,pwd_wm_pc : str,pwd_img_in : str,pwd_img_pc : str,img_in,img_wm_in : str):
        pwd_wm = BlindWatermarkUtil.calc_pwd(pwd_wm_in,pwd_wm_pc)
        pwd_img = BlindWatermarkUtil.calc_pwd(pwd_img_in,pwd_img_pc)
        bwm_context = blind_watermark.WaterMark(password_wm=pwd_wm,password_img=pwd_img)
        bwm_context.read_img(img=img_in)
        bwm_context.read_wm(img_wm_in,mode='img')
        len_wm = str(len(bwm_context.wm_bit))
        return (len_wm,bwm_context.embed())

    # def read_(pwd_wm_in : str,pwd_wm_pc : str,pwd_img_in : str,pwd_img_pc : str,img_in)
    def calc_pwd(password : str,process : str) -> int:
        if process == "int":
            return int(password)
        if process == "md5":
            return int(hashlib.md5(password.encode("UTF-8")).hexdigest(),base=16)
        if process == "sha256":
            return int(hashlib.sha256(password.encode("UTF-8")).hexdigest(),base=16)

with demo:
    with gr.Row():
        gr.Markdown("# 加密水印密码\n由于密码仅支持使用 int 类型,可以通过控制处理流程使得文本形式的密码变成 int.")
        password_wm_input = gr.Textbox(value="1",info="用于加密水印的密码",label="密码")
        password_wm_process_input = gr.Dropdown(["int","md5","sha256"],value='int',multiselect=False, label="控制流程",info="用于控制如何变换密码")
    with gr.Row():
        gr.Markdown("# 变换图片密码\n由于密码仅支持使用 int 类型,可以通过控制处理流程使得文本形式的密码变成 int.")
        password_img_input = gr.Textbox(value="1",info="用于加密水印的密码",label="密码")
        password_img_process_input = gr.Dropdown(["int","md5","sha256"],value='int',multiselect=False, label="控制流程",info="用于控制如何变换密码")
    image_input = gr.Image(label="用于操作的图片")
    with gr.Tabs():
        gr.Markdown("操作")
        with gr.TabItem("添加"):
            with gr.Tabs():
                with gr.TabItem("文本水印"):
                    with gr.Row():
                        text_wm_input = gr.Textbox("watermark text",info="隐藏入图片中的文字",label="内容")
                        text_wm_button = gr.Button("处理")
                with gr.TabItem("字节水印"):
                    with gr.Row():
                        gr.Markdown("实际上这个对应的是 bit 模式，由于没有较好的直接输入 bit 的方法，故改为二进制文件输入. 文件名无影响")
                        file_wm_input = gr.File(type="binary",label="内容")
                        file_wm_button = gr.Button("处理")
                with gr.TabItem("图片水印"):
                    with gr.Row():
                        img_wm_input = gr.Image(label="内容",type="filepath")
                        img_wm_button = gr.Button("处理")
            bitlen_output = gr.Textbox(label="水印大小")
            image_output = gr.Image(label="添加了肓水印的图片")
        with gr.TabItem("读取"):
            bitlen_input = gr.Textbox(label="水印大小")
            with gr.Tab():
                with gr.TabItem("文字"):
                    with gr.Row():
                        readtext_output = gr.Textbox(label="结果")
                        readtext_button = gr.Button("读取文字")
                with gr.TabItem("图片"):
                    with gr.Row():
                        readimg_output = gr.Image(label="结果")
                        readimg_button = gr.Button("读取图片")
    text_wm_button.click(BlindWatermarkUtil.add_wm_text,inputs=[password_wm_input,password_wm_process_input,password_img_input,password_img_process_input,image_input,text_wm_input],outputs=[bitlen_output,image_output])
    file_wm_button.click(BlindWatermarkUtil.add_wm_file,inputs=[password_wm_input,password_wm_process_input,password_img_input,password_img_process_input,image_input,file_wm_input],outputs=[bitlen_output,image_output])
    img_wm_button.click(BlindWatermarkUtil.add_wm_img,inputs=[password_wm_input,password_wm_process_input,password_img_input,password_img_process_input,image_input,img_wm_input],outputs=[bitlen_output,image_output])


demo.launch()