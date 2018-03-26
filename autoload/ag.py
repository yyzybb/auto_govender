# -*- coding:utf8 -*-
import vim, os

filename = vim.eval("s:abs_filename")

def log(info):
    f = open("/tmp/ag.log", "a+")
    f.write(info + '\n')
    f.close()

log("-" * 40)
log(filename)

# 找到git仓库根目录
def getGitRootPath():
    stdin, stdout, stderr = os.popen3("git status")
    if stderr.read() != "":
        # 不在git仓库中
        return ""

    directory = filename
    while directory != os.path.dirname(directory):
        directory = os.path.dirname(directory)
        if os.path.isdir(os.path.join(directory, ".git")):
            return directory

    return ""


# 找到vendor的软链接文件
def getVendorSymbolLink():
    gitRoot = getGitRootPath()
    if gitRoot == "":
        return ""

    vendorDir = os.path.join(gitRoot, "vendor")
    if not os.path.isdir(vendorDir):
        return ""

    dirList = []
    directory = filename
    while directory != gitRoot:
        directory = os.path.dirname(directory)
        dirList.append(directory)
        #log("dir:%s" % directory)

    vendorChildren = os.listdir(vendorDir)
    for d in vendorChildren:
        d = os.path.join(vendorDir, d)
        #log("vd:%s" % d)
        if not os.path.isdir(d):
            continue

        if not os.path.islink(d):
            continue

        originDir = os.readlink(d)
        originDir = os.path.join(os.path.dirname(d), originDir)
        originDir = os.path.normpath(originDir)
        #log("originDir: %s" % originDir)

        for fold in dirList:
            if fold != originDir:
                continue

            #log("match dir:%s" % originDir)
            subpath = os.path.relpath(os.path.dirname(filename), fold)
            dst = os.path.join(d, subpath)
            #log("dest: %s" % dst)
            return dst

    return ""

# 编译软链接文件
def compile(symFile):
    directory = os.path.dirname(symFile)
    cmd = "cd %s && go install" % (directory)
    stdin, stdout, stderr = os.popen3(cmd)
    log("run cmd:%s" % cmd)
    log("stdout:%s" % stdout.read())
    log("stderr:%s" % stderr.read())

symFile = getVendorSymbolLink()
if symFile != "":
    compile(symFile)
