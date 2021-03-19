from flask import Flask,request,jsonify
from Create import use_model
from Myconfig import dataroot,basedir
from flask import render_template
from flask import redirect,url_for
import os
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed,FileRequired
from wtforms import StringField,PasswordField,BooleanField,SubmitField,FileField
from wtforms.validators import DataRequired
from wtforms.validators import Email,EqualTo,ValidationError
import string,random

import shutil

myweb = Flask(__name__)

from Myconfig import Config
myweb.config.from_object(Config)

#使用bootstrap渲染前端
from flask_bootstrap import Bootstrap
bootstrap = Bootstrap(myweb)

from flask_uploads import UploadSet,configure_uploads,patch_request_class

'''配置上传集 photo ,设置上传类型为PNG,png,jpeg'''
photo = UploadSet('images',['PNG','png','jpeg','jpg'])
configure_uploads(myweb,photo)
patch_request_class(myweb,size=None)

def model_horse2zebra():
    source_data_path = dataroot
    model_name = 'horse2zebra_pretrained'
    use_model(source_data_path,model_name)

def human2cartoongirl():
    source_data_path = dataroot
    model_name = 'human2cartoongirl_cyclegan'
    use_model(source_data_path,model_name)


class UploadForm(FlaskForm):
    icon = FileField('',validators=[FileRequired(message='请选择图片'),FileAllowed(photo,message='错误的文件类型')])
    submit = SubmitField('保存')
    

    '''生成随机的图片名称'''
    def random_name(self,shuffix,length=64):
        Str = string.ascii_letters+string.digits
        return ''.join(random.choice(Str) for i in range(length))+'.'+shuffix

    '''执行图片的缩放'''
    def img_zoom(self,path,prefix):
        img = Image.open(path)
        img.thumbnail((50,50))
        pathTup = os.path.split(path)
        path = os.path.join(pathTup[0],prefix+pathTup[1])
        img.save(path)

@myweb.route('/',methods=['GET','POST'])
@myweb.route('/index',methods=['GET','POST'])
def index_page():
    '''从前端获取数据并保存到服务器'''
    form = UploadForm()
    if form.validate_on_submit():
        icon = request.files.get('icon')
        suffix = icon.filename.split('.')[-1] #获取后缀

        while True:
            imgName = form.random_name(suffix)
            path = os.path.join(myweb.config['UPLOADS_DEFAULT_DEST'],imgName)

            if not os.path.exists(path):
                break

        photo.save(icon,name=imgName)
        img_url = photo.url(imgName)

        #图片上传后重定向到图片处理界面
        #return redirect(url_for('pixel'))
    return render_template('index.html',title='Image2Image',form=form)
    
@myweb.route('/pixel',methods=['GET','POST'])
def pixel():
    #使用模型进行处理
    model_horse2zebra()
    #使用内置库删掉上传的图片
    # shutil.rmtree(os.path.join(basedir,'Images/images'))
    return render_template('pixel.html')

#最开始应该在原图选项，有多个选项    


if __name__ == "__main__":
    myweb.run(host='0.0.0.0',port='5000',debug=True)