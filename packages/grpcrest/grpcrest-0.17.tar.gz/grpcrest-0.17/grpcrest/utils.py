import platform, os, sys, subprocess
def identify_platform():
    path=os.path.realpath(__file__).replace("utils.py","")
    os_name=(platform.platform()).lower()
    print("OS Details:"+os_name)
    command_output=""
    try:
        if("windows" in os_name and "64" in os_name):
            path+="grpcurl_1.8.7_windows_x86_64/"
            command=path+"grpcurl.exe -help"
        elif("linux" in os_name and "arm" in os_name):
            path+="grpcurl_1.8.7_linux_arm64/"
            command=path+"grpcurl -help"
        elif("linux" in os_name and "64" in os_name):
            path+="grpcurl_1.8.7_linux_x86_64/"
            command=path+"grpcurl -help"
        elif("macos" in os_name):
            path=''
            os.system("brew install grpcurl")
            command="grpcurl -help"
        else:
            print("unsupported OS")
            sys.exit(1)
        command_output=subprocess.getoutput(command)
        if("Usage:" in command_output):
            print("grpcurl resolved successfully")
        else:
            path=''
            print("grpcurl wasn't installed correctly, kindly consider installing grpcurl manually before using this module")
            sys.exit(1)
    except Exception as e:
        print(e)
        path=''
        print("grpcurl wasn't installed correctly, kindly consider installing grpcurl manually before using this module")
        sys.exit(1)
    return path

