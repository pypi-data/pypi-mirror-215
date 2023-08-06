
# -*- coding: utf-8 -*-
import urllib.request
import json
import requests
import os
import shutil
import re



# def break_words(stuff):
#     """This function will break up words for us."""
#     words = stuff.split(' ')
#     return words

# def sort_words(words):
#     """Sorts the words.""" # 文档字符串，是注释的一种
#     return sorted(words)

# def print_first_word(words):
#     """Prints the first word after popping it off."""
#     word = words.pop(0)
#     print(word)

# def print_last_word(words):
#     """Print the last word after popping it off."""
#     word = words.pop(-1)
#     print(word)

# def sort_sentence(sentence):
#     """Takes in a full sentence and returns the sorted words"""
#     words = break_words(sentence)
#     return sort_words(words)  # 没懂这个函数

# def print_first_and_last(sentence):
#     """Prints the first and last words of the sentence."""
#     words = break_words(sentence)
#     print_first_word(words)
#     print_last_word(words)

# def print_first_and_last_sorted(sentence):
#     """Sorts the words then prints the first and last one."""
#     words = sort_sentence(sentence)
#     print_first_word(words)
#     print_last_word(words)


# get help
def hello_jkzhou():
    """If you need help or have a better idea, send me an e-mail."""
    print("如果需要帮助，可以给我发邮件: zhouqiling.bjfu@foxmail.com")
    print("也可以描述你的需求，给pydatawork提一个功能建议：\npydatawork功能建议收集表：https://docs.qq.com/form/page/DZVNabWlkRUtldWtJ")



# get a card
def current_folder_name(path):
    """
    path:一个路径，可以是文件夹路径，也可以是文件路径
    结果：返回current_folder_name
    """
    # 判断路径是文件夹路径还是文件路径
    if os.path.isdir(path):
        # 如果是文件夹路径
        current_folder_name = os.path.basename(path)
    else:
        # 如果是文件路径
        current_folder_name = os.path.basename(os.path.dirname(path))
    return current_folder_name



def file_name(path):
    """
    path:一个路径，可以是文件夹路径，也可以是文件路径
    结果：返回file_name,当path为文件夹路径值，返回的值为空值
    """
    # 判断路径是文件夹路径还是文件路径
    if os.path.isdir(path):
        # 如果是文件夹路径
        file_name = None
    else:
        # 如果是文件路径
        file_name = os.path.basename(path)
    return file_name


# get a program
def get_weibo(path,id,weibo_name):
    """
    path: 内容存放路径
    id: 微博id
    weibo_name: 内容存放路径下文件夹的名字

    示例：获取梅西的微博id，获取其微博内容

    import pydatawork as dw 

    path="/home/Desktop/pydatawork"
    id="5934019851" # 梅西的微博id。在网页版上能获得链接，链接中u后面的内容即为id ,梅西微博的id为 5934019851  https://weibo.com/u/5934019851
    weibo_name="mx"

    dw.get_weibo(path,id,weibo_name)

    """
    path = path
    id = id # 在微博上获取

    proxy_addr = "122.241.72.191:808"
    weibo_name = weibo_name # 可以自定义名字


    def use_proxy(url, proxy_addr):
        req = urllib.request.Request(url)
        req.add_header("User-Agent",
                    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0")
        proxy = urllib.request.ProxyHandler({'http': proxy_addr})
        opener = urllib.request.build_opener(proxy, urllib.request.HTTPHandler)
        urllib.request.install_opener(opener)
        data = urllib.request.urlopen(req).read().decode('utf-8', 'ignore')
        return data


    def get_containerid(url):
        data = use_proxy(url, proxy_addr)
        content = json.loads(data).get('data')
        for data in content.get('tabsInfo').get('tabs'):
            if (data.get('tab_type') == 'weibo'):
                containerid = data.get('containerid')
        return containerid


    def get_userInfo(id):
        url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value=' + id
        data = use_proxy(url, proxy_addr)
        content = json.loads(data).get('data')
        profile_image_url = content.get('userInfo').get('profile_image_url')
        description = content.get('userInfo').get('description')
        profile_url = content.get('userInfo').get('profile_url')
        verified = content.get('userInfo').get('verified')
        guanzhu = content.get('userInfo').get('follow_count')
        name = content.get('userInfo').get('screen_name')
        fensi = content.get('userInfo').get('followers_count')
        gender = content.get('userInfo').get('gender')
        urank = content.get('userInfo').get('urank')
        print("微博昵称：" + name + "\n" + "微博主页地址：" + profile_url + "\n" + "微博头像地址：" + profile_image_url + "\n" + "是否认证：" + str(verified) + "\n" + "微博说明：" + description + "\n" + "关注人数：" + str(guanzhu) + "\n" + "粉丝数：" + str(fensi) + "\n" + "性别：" + gender + "\n" + "微博等级：" + str(urank) + "\n")


    def get_weibo(id, file):
        global pic_num
        pic_num = 0
        i = 1
        while True:
            url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value=' + id
            weibo_url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value=' + id + '&containerid=' + get_containerid(url) + '&page=' + str(i)
            try:
                data = use_proxy(weibo_url, proxy_addr)
                content = json.loads(data).get('data')
                cards = content.get('cards')
                if (len(cards) > 0):
                    for j in range(len(cards)):
                        print("-----正在爬取第" + str(i) + "页，第" + str(j) + "条微博------")
                        card_type = cards[j].get('card_type')
                        if (card_type == 9):
                            mblog = cards[j].get('mblog')
                            attitudes_count = mblog.get('attitudes_count')
                            comments_count = mblog.get('comments_count')
                            created_at = mblog.get('created_at')
                            reposts_count = mblog.get('reposts_count')
                            scheme = cards[j].get('scheme')
                            text = mblog.get('text')
                            if mblog.get('pics') != None:
                                # print(mblog.get('original_pic'))
                                # print(mblog.get('pics'))
                                pic_archive = mblog.get('pics')
                                for _ in range(len(pic_archive)):
                                    pic_num += 1
                                    print(pic_archive[_]['large']['url'])
                                    imgurl = pic_archive[_]['large']['url']
                                    img = requests.get(imgurl)
                                    # f = open(path + weibo_name + '\\' + str(pic_num) + str(imgurl[-4:]),'ab')  # 存储图片，多媒体文件需要参数b（二进制文件）# 原始代码
                                    f = open(os.path.join(path, weibo_name, str(pic_num) + str(imgurl[-4:])), 'ab') # 存储图片，多媒体文件需要参数b（二进制文件）
                                    f.write(img.content)  # 多媒体存储content
                                    f.close()

                            with open(file, 'a', encoding='utf-8') as fh:
                                fh.write("----第" + str(i) + "页，第" + str(j) + "条微博----" + "\n")
                                fh.write("微博地址：" + str(scheme) + "\n" + "发布时间：" + str(
                                    created_at) + "\n" + "微博内容：" + text + "\n" + "点赞数：" + str(
                                    attitudes_count) + "\n" + "评论数：" + str(comments_count) + "\n" + "转发数：" + str(
                                    reposts_count) + "\n")
                    i += 1
                else:
                    break
            except Exception as e:
                print(e)
                i += 1  # 添加这一行
                pass

    # # 在指定路径下，先建立一个名为weibo的文件夹
    # if os.path.isdir(os.path.join(path,"weibo")):
    #     pass
    # else:
    #     os.mkdir(os.path.join(path,"weibo"))

    if os.path.isdir(os.path.join(path,weibo_name)):
        pass
    else:
        os.mkdir(os.path.join(path,weibo_name))
    file = os.path.join(path, weibo_name, weibo_name + ".txt")

    get_userInfo(id)
    get_weibo(id, file)
    print("微博数据获取完毕")
    # 该程序最初来源：http://www.omegaxyz.com/2018/02/13/python_weibo/



def rename_folder_numeric_serialize(path):
    """
    path:文件夹路径。给定一个文件夹路径，获取其中子文件夹的名字，根据子文件夹的名字，从左到右进行比较，按数值从小到大对子文件夹排序，再从1开始对子文件夹进行序列化重命名。
    """

    # 定义一个函数，将输入的字符串按照数字和非数字的部分进行分割，并将数字部分转换为整数
    def split_key(s): # 【一个字符串一个字符串处理】
        parts = [] # 初始化一个空列表，用于存储分割后的字符串
        current_part = "" # 初始化一个空字符串，用于存储当前正在处理的部分
        for c in s: # 遍历字符串中的每个字符
            if c.isalnum(): # 如果当前字符是字母或数字
                current_part += c # 将其添加到 current_part 变量中
            else: # 如果当前字符是非字母和数字的符号
                if current_part: # 如果 current_part 不为空
                    if current_part.isdigit(): # 如果 current_part 是数字
                        current_part = int(current_part) # 将其转换为整数
                    parts.append(current_part) # 将 current_part 添加到 parts 列表中
                    current_part = "" # 将 current_part 重置为空字符串
        if current_part: # 如果 current_part 不为空
            if current_part.isdigit(): # 如果 current_part 是数字
                current_part = int(current_part) # 将其转换为整数
            parts.append(current_part) # 将 current_part 添加到 parts 列表中
            # print(parts)
            # exit()
        return parts # 返回分割后的字符串列表

        
    # 定义文件夹路径
    images_path = path

    # 获取images_path下的所有子文件夹
    subfolders = [f.path for f in os.scandir(images_path) if f.is_dir()]

    # 对子文件夹按名字进行递增排序 @ 知识卡片 键函数。把subfolders中的每个元素，传给split_key按规则进行处理，并返回一个键，按返回的键进行排序。
    subfolders.sort(key=split_key)

    # 对排序后的子文件夹从1开始序列化，序列化的值加在原文件名末尾，以_进行拼接
    for i, folder in enumerate(subfolders, start=1): # 遍历排序后的子文件夹，从1开始序列化 @ 知识卡片
        new_name = f"{folder}_{i}" # 将序列化的值加在原文件名末尾，以_进行拼接
        os.rename(folder, new_name) # 重命名文件夹 @ 知识卡片
        print(os.path.basename(new_name)) # 打印重命名后的文件夹名字，不包括路径



def obsidian_move_md_or_canvas_linked_images(images_path,folder_path,target_folder):
    """
    提取obsidian中.md文档、.canvas文档中链接的图片，实现附件管理、库空间管理、笔记归档。
    需要指定三个路径：
    images_path:图片附件所在的文件夹。通常是笔记库的附件文件夹
    folder_path:待整理的md、canvas文档所在文件夹（可包括多层级子文件夹，会遍历）。通常临时建立一个文件夹,将待整理的笔记存进去
    target_folder:提前准备的文件夹，可以建在任意位置，用于存放提取出来的图片
    执行结束后，可以将文档和对应的图片一起进行归档，实现笔记管理的目的。
    """

    # 001-图片文件夹:原始库的附件文件夹路径
    images_path = images_path
    # 002-文件夹路径：准备移动归档的文件夹，里面包含.md和.canvas格式的文件
    folder_path = folder_path
    # 003-图片移动的目标文件夹：通常，在002中建立一个文件夹，用于存放图片即可
    target_folder = target_folder

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".md"):
            # 将md文件打印出来
                print(file)
            # 处理markdown文档
                with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                    content = f.read()
                    # 查找文档中的图片
                    images = re.findall(r"\!\[\[(.*?)\]\]", content) # @@知识卡片 正则匹配
                    # exit()
                    for image_name in images:
                        # 在images文件夹中查找对应图片
                        for image_root, _, image_files in os.walk(images_path):
                            if image_name in image_files:
                                # 移动图片到指定文件夹
                                shutil.move(os.path.join(image_root, image_name), os.path.join(target_folder, image_name))
                                # 打印移动过程
                                print(f"moving:{os.path.join(image_root, image_name)}--->{os.path.join(target_folder, image_name)}")
            # exit()

            # 处理canvas文档
            elif file.endswith(".canvas"):
                # 将canvas文件打印出来
                print(file)
                with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                    content = f.read() # @知识卡片 不必非用json的读取方式
                    # 查找文档中的图片
                    # images = re.findall(r'"file":"(.*?\.png)"', content) # @知识卡片 匹配形如"file":"Pasted image 20230531214326.png"的字符串，得到的是绝对路径
                    images = re.findall(r'"file":"(.*?)"', content) # @知识卡片 匹配形如"file":"Pasted image 20230531214326.png"的字符串，得到的是绝对路径。不用指定png、jpeg等格式。
                    # print(images)
                    for file_path in images:
                        # print(file_path)
                        image_name = os.path.basename(file_path) #  @知识卡片 从绝对路径中提取文件名。Pasted image 20230531214326.png
                        # 在images文件夹中查找对应图片
                        for image_root, _, image_files in os.walk(images_path):
                            if image_name in image_files:
                                # 移动图片到指定文件夹
                                shutil.move(os.path.join(image_root, image_name), os.path.join(target_folder, image_name))
                                # 打印移动过程
                                print(f"moving:{os.path.join(image_root, image_name)}--->{os.path.join(target_folder, image_name)}")

    # 统计附件整理情况
    images_list = os.listdir(target_folder)
    num_images = len(images_list)

    print(f"\n已整理{num_images}个附件！")



def move_all_files(folder_path, target_folder, file_type_list):
    """
    folder_path:待整理文件夹，可包含多层级子文件夹
    target_folder:目标文件夹
    file_type_list:一个列表，里面存放需要移动的文件类别的后缀类型，如[".jpg",".zip",".png",".gz",".whl",".md"]，注意，要带点“.”。其中“.gz”表示“.tar.gz”这一类
    实现效果：将待整理文件夹及其子文件夹中指定类型的全部文件移动到目标文件夹
    """

    # 获取文件夹中的文件列表
    files = os.listdir(folder_path)

    # 遍历文件列表
    for file in files:
        # 获取文件的绝对路径
        file_path = os.path.join(folder_path, file)

        # 如果文件是一个文件夹，递归调用函数来遍历它
        if os.path.isdir(file_path):
            move_all_files(file_path, target_folder, file_type_list)
        else:
            # 获取文件的后缀，看其是否在file_type_list中, 如果在其中，将其移动到目标文件夹
            file_extension = os.path.splitext(file_path)[-1]
            if file_extension in file_type_list:
                # 判断路径是否存在
                target_path = os.path.join(target_folder, file)
                if os.path.exists(target_path):
                    print(f"{file} already exists in the target folder. Skipping...")
                else:
                    print(f"Moving {file} to {target_folder}")
                    shutil.move(file_path, target_folder)
            else:
                continue




def copy_all_files(folder_path, target_folder, file_type_list):
    """
    folder_path:待整理文件夹，可包含多层级子文件夹
    target_folder:目标文件夹
    file_type_list:一个列表，里面存放需要复制的文件类别的后缀类型，如[".jpg",".zip",".png",".gz",".whl",".md"]，注意，要带点“.”。其中“.gz”表示“.tar.gz”这一类
    实现效果：将待整理文件夹及其子文件夹中指定类型的全部文件复制到目标文件夹
    """

    # 获取文件夹中的文件列表
    files = os.listdir(folder_path)

    # 遍历文件列表
    for file in files:
        # 获取文件的绝对路径
        file_path = os.path.join(folder_path, file)

        # 如果文件是一个文件夹，递归调用函数来遍历它
        if os.path.isdir(file_path):
            copy_all_files(file_path, target_folder, file_type_list)
        else:
            # 获取文件的后缀，看其是否在file_type_list中, 如果在其中，将其复制到目标文件夹
            file_extension = os.path.splitext(file_path)[-1]
            if file_extension in file_type_list:
                # 判断路径是否存在
                target_path = os.path.join(target_folder, file)
                if os.path.exists(target_path):
                    print(f"{file} already exists in the target folder. Skipping...")
                else:
                    print(f"Copying {file} to {target_folder}")
                    shutil.copy(file_path, target_folder)
            else:
                continue




def move_files(folder_path, target_folder, file_type_list):
    """
    folder_path:待整理文件夹
    target_folder:目标文件夹
    file_type_list:一个列表，里面存放需要移动的文件类别的后缀类型，如[".jpg",".zip",".png",".gz",".whl",".md"]，注意，要带点“.”。其中“.gz”表示“.tar.gz”这一类
    实现效果：将待整理文件夹中(注：不包括子文件夹)指定类型的文件移动到目标文件夹
    """

    # 获取文件夹中的文件列表
    files = os.listdir(folder_path)

    # 遍历文件列表
    for file in files:
        # 获取文件的绝对路径
        file_path = os.path.join(folder_path, file)

        # 如果文件是一个文件夹，忽略
        if os.path.isdir(file_path):
            continue
        else:
            # 获取文件的后缀，看其是否在file_type_list中, 如果在其中，将其移动到目标文件夹
            file_extension = os.path.splitext(file_path)[-1]
            if file_extension in file_type_list:
                # 判断路径是否存在
                target_path = os.path.join(target_folder, file)
                if os.path.exists(target_path):
                    print(f"{file} already exists in the target folder. Skipping...")
                else:
                    print(f"Moving {file} to {target_folder}")
                    shutil.move(file_path, target_folder)
            else:
                continue




def copy_files(folder_path, target_folder, file_type_list):
    """
    folder_path:待整理文件夹
    target_folder:目标文件夹
    file_type_list:一个列表，里面存放需要复制的文件类别的后缀类型，如[".jpg",".zip",".png",".gz",".whl",".md"]，注意，要带点“.”。其中“.gz”表示“.tar.gz”这一类
    实现效果：将待整理文件夹中(注：不包括子文件夹)指定类型的文件复制到目标文件夹
    """

    # 获取文件夹中的文件列表
    files = os.listdir(folder_path)

    # 遍历文件列表
    for file in files:
        # 获取文件的绝对路径
        file_path = os.path.join(folder_path, file)

        # 如果文件是一个文件夹，忽略
        if os.path.isdir(file_path):
            continue
        else:
            # 获取文件的后缀，看其是否在file_type_list中, 如果在其中，将其复制到目标文件夹
            file_extension = os.path.splitext(file_path)[-1]
            if file_extension in file_type_list:
                # 判断路径是否存在
                target_path = os.path.join(target_folder, file)
                if os.path.exists(target_path):
                    print(f"{file} already exists in the target folder. Skipping...")
                else:
                    print(f"Copying {file} to {target_folder}")
                    shutil.copy(file_path, target_folder)
            else:
                continue

