def restart():
    import os,sys
    print(sys.executable)
    print(*([sys.executable]+sys.argv))
    # 如果环境中同时安装python2和python3 请修改python为python3
    os.execl(sys.executable, "python", *sys.argv)

