import os

'''获取当前路径'''
basedir = os.path.abspath(os.path.dirname(__file__))  #绝对路径
# basedir = os.path.realpath(os.path.dirname(__file__))  #相对路径
dataroot = 'Images' #数据父路径

'''创建类Config来存储配置变量'''
class Config(object):

    dataroot = 'Images' #数据父路径
    
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    
    '''上传路径配置'''
    UPLOADS_DEFAULT_DEST = os.path.join(basedir,'Images')
    MAX_CONTENT_LENGTH = 1024*1024*64

    '''模型路径'''
    MODEL_PATH = os.path.join(basedir,'checkpoints\horse2zebra_pretrained\latest_net_G.pth')