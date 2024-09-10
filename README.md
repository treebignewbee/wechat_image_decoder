1.单独使用：
python wechat_image_decoder.py <file_or_directory_path>

2.在项目或其他脚本中调用：
from wechat_image_decoder import WeChatImageDecoder

decoder = WeChatImageDecoder()

# 处理单个微信图片文件
result = decoder.process_single_wechat_image("/path/to/wechat_image.dat")

# 处理包含微信图片的整个目录
results = decoder.process_wechat_images_in_directory("/path/to/wechat_images_directory")
