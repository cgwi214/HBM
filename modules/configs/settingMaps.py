
import hashlib

def configname2screenshotname(configfilename):
    """
    根据config文件名，返回截图文件名
    config文件名包含后缀不包含路径
    """
    screenshotfilehash = hashlib.sha1(configfilename.encode('utf-8')).hexdigest()
    # 如果长度大于8，截取前8位
    if len(screenshotfilehash) > 8:
        screenshotfilehash = screenshotfilehash[:8]
    # 如果长度小于8，补0
    elif len(screenshotfilehash) < 8:
        screenshotfilehash = screenshotfilehash.zfill(8)
    return screenshotfilehash + ".png"