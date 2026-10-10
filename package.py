import zipfile
import shutil
import os
from modules.configs.MyConfig import config
import subprocess
from pathlib import Path
import nicegui
import scrcpy
import ncnn
import numpy
import time
import pponnxcr
import platform
import requests

def package_download_adb(platformstr = None):
    
    target_adb_path = os.path.join(os.getcwd(), "tools", "adb")
    downloadurls = {
        "Windows": "https://dl.google.com/android/repository/platform-tools-latest-windows.zip",
        "Darwin": "https://dl.google.com/android/repository/platform-tools-latest-darwin.zip",
        "Linux": "https://dl.google.com/android/repository/platform-tools-latest-linux.zip"
    }
    if not os.path.exists(target_adb_path):
        if platformstr and platformstr in downloadurls.keys():
            url = downloadurls[platformstr]
        elif platform.system() in downloadurls.keys():
            url = downloadurls[platform.system()]
        else:
            print(f"Unknown platform: {platform.system()}")
            return
        
        # download zip
        r = requests.get(url)
        with open("platform-tools-latest.zip", "wb") as f:
            f.write(r.content)
        target_adb_path_parent_folder = os.path.dirname(target_adb_path)
        # unzip to target_adb_path, rename the upper folder "playform-tools" to "adb"
        with zipfile.ZipFile("platform-tools-latest.zip", 'r') as z:
            z.extractall(target_adb_path_parent_folder)
        print(f"adb downloaded to: {target_adb_path_parent_folder}")
        package_rename(os.path.join(target_adb_path_parent_folder, "platform-tools"), target_adb_path)
        
        
    else:
        print(f"adb already exists: {target_adb_path}")

def package_copyfolder(src, dst):
    try:
        # 拷贝文件夹
        shutil.copytree(src, dst)
        print(f"{dst}文件夹已拷贝")
    except FileExistsError as e:
        print(f"{dst}文件夹已存在!")

def package_copyfile(src, dst):
    try:
        shutil.copyfile(src, dst)
        print(f"{dst}已拷贝")
    except FileExistsError as e:
        print(f"{dst}已存在!")

def package_rename(src, dst):
    try:
        os.rename(src, dst)
    except Exception as e:
        print(f"{dst}已存在!")
        
def package_create_folder(path):
    try:
        os.makedirs(path)
    except Exception as e:
        print(f"{path}创建时出错!")

def package_remove_file(path):
    try:
        os.remove(path)
    except Exception as e:
        print(f"{path}删除时出错!")

def package_remove_folder(path):
    try:
        shutil.rmtree(path)
    except Exception as e:
        print(f"{path}删除时出错!")

# ====================开始====================

# mainly for windows, download adb
package_download_adb(platformstr="Windows")

package_remove_folder("./dist")

# 获取 NumPy 的 DLL 路径
numpy_dist_path = Path(numpy.__file__).parent.parent
numpy_libs_dir = numpy_dist_path / "numpy.libs"

# 检查路径有效性
if not numpy_libs_dir.exists():
    raise RuntimeError(f"NumPy .libs directory not found: {numpy_libs_dir}")

# 打包main.py，名字为HBM
hbmcmd = [
    'pyinstaller',
    'main.py',
    '-n', 'HBM',
    '--icon', './DATA/icons/hb.ico',
    '--add-data', f'{Path(pponnxcr.__file__).parent}{os.pathsep}pponnxcr',
    '--add-binary', f'{numpy_libs_dir}{os.pathsep}.',
    '--hidden-import', 'numpy.core._multiarray_umath',
    '-y'
]
subprocess.call(hbmcmd)

# 打包GUI
guicmd = [
    'pyinstaller',
    'jsoneditor.py',
    '-n', 'HBM_GUI',
    # '--windowed', # prevent console appearing, only use with ui.run(native=True, ...)
    '--add-data', f'{Path(nicegui.__file__).parent}{os.pathsep}nicegui',
    '--add-binary', f'{numpy_libs_dir}{os.pathsep}.',
    '--hidden-import', 'numpy.core._multiarray_umath',
    '--icon', './DATA/icons/hb.ico',
    '-y'
]
subprocess.call(guicmd)

# 打包yolom.py
yolocmd = [
    'pyinstaller',
    'yolom.py',
    '-n', 'HBM_YOLO',
    '--add-data', f'{Path(scrcpy.__file__).parent}{os.pathsep}scrcpy',
    '--add-data', f'{Path(ncnn.__file__).parent}{os.pathsep}ncnn',
    '--add-binary', f'{numpy_libs_dir}{os.pathsep}.',
    '--hidden-import', 'numpy.core._multiarray_umath',
    '--icon', './DATA/icons/hb.ico',
    '-y'
]
subprocess.call(yolocmd)

# 当前目录
print("当前目录：", os.getcwd())
workdir = os.getcwd()

print("开始封装")


# 遍历./dist/HBM_GUI/_internal里的所有文件夹和文件，将它们拷贝到./dist/HBM/_internal，如果已存在则跳过
for dirpath, dirnames, filenames in os.walk(os.path.join('./dist', 'HBM_GUI', '_internal')):
    for filename in filenames:
        package_copyfile(os.path.join(dirpath, filename), os.path.join('./dist/HBM/_internal', filename))
    for dirname in dirnames:
        package_copyfolder(os.path.join(dirpath, dirname), os.path.join('./dist/HBM/_internal', dirname))
    # 走一层就终止
    break

for dirpath, dirnames, filenames in os.walk(os.path.join('./dist', 'HBM_YOLO', '_internal')):
    for filename in filenames:
        package_copyfile(os.path.join(dirpath, filename), os.path.join('./dist/HBM/_internal', filename))
    for dirname in dirnames:
        package_copyfolder(os.path.join(dirpath, dirname), os.path.join('./dist/HBM/_internal', dirname))
    # 走一层就终止
    break

package_copyfolder('./tools/adb', './dist/HBM/tools/adb')

# pytinstall的时候已经把pponnxcr和nicegui文件拷贝进去了
# package_copyfolder('./tools/pponnxcr', './dist/HBM/_internal/pponnxcr')


package_create_folder("./dist/HBM/DATA/CONFIGS")


# 这里只拷贝example.json，不拷贝其他的，因为其他的是用户的配置文件
# package_copyfolder("./HBM_CONFIGS", "./dist/HBM/HBM_CONFIGS")
package_create_folder("./dist/HBM/HBM_CONFIGS")
package_copyfile("./HBM_CONFIGS/example.json", "./dist/HBM/HBM_CONFIGS/example.json")
package_copyfolder("./DATA/assets", "./dist/HBM/DATA/assets")
package_copyfolder("./DATA/icons", "./dist/HBM/DATA/icons")
package_copyfolder("./DATA/ncnn", "./dist/HBM/DATA/ncnn")
package_copyfile("./DATA/ncnn/ncnn.bin", "./dist/HBM/DATA/ncnn/ncnn.bin")
package_copyfile("./DATA/ncnn/ncnn.param", "./dist/HBM/DATA/ncnn/ncnn.param")
package_copyfile("./DATA/assets/Demonstration.mp4", "./dist/HBM/DATA/assets/Demonstration.mp4")
package_copyfile("./DATA/touch.zip", "./dist/HBM/DATA/touch.zip")
package_copyfile("./dist/HBM_GUI/HBM_GUI.exe", "./dist/HBM/HBM_GUI.exe")
package_copyfile("./dist/HBM_YOLO/HBM_YOLO.exe", "./dist/HBM/HBM_YOLO.exe")

time.sleep(2)

# package_rename("./dist/HBM/HBM.exe", f"./dist/HBM/HBM.exe")
package_rename("./dist/HBM", f"./dist/HBM")

# gui已经脱离HBM.exe，不需要了
# package_remove_file("./HBM.exe")
# package_copyfile(f"./dist/HBM/HBM.exe", "./HBM.exe")

print("开始压缩")
time.sleep(2)

# 压缩./dist/HBM文件夹为HBM.zip
z = zipfile.ZipFile(f'./dist/HBM.zip', 'w', zipfile.ZIP_DEFLATED)
startdir = f"./dist/HBM"
for dirpath, dirnames, filenames in os.walk(startdir):
    for filename in filenames:
        z.write(os.path.join(dirpath, filename), arcname=os.path.join(dirpath, filename).replace("/dist",""))

print(f"完成，压缩包./dist/HBM.zip已生成")
print(f"压缩包大小为{os.path.getsize(f'./dist/HBM.zip')/1024/1024:.2f}MB")
