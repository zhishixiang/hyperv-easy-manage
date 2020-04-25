import subprocess
import os,shutil
programstatus = True
while programstatus:
    def printMenu():
        print("********************************")
        print("****      1--新建虚拟机      ****")
        print("****      2--删除虚拟机      ****")
        print("****      3--开启虚拟机      ****")
        print("****      4--关闭虚拟机      ****")
        print("****      5--查看虚拟机列表  ****")
        print("****      6--修改虚拟机配置  ****")
        print("****      7--创建虚拟机快照  ****")
        print("****      8--删除虚拟机快照  ****")
        print("****      0--退出           ****")
        print("********************************")
    def getvm():
        (getvmstatus,getvm) = subprocess.getstatusoutput('powershell get-vm')
        print(getvm)
    def startvm(vmname):
        print("正在开启虚拟机%s..."%(vmname))
        (startvmstatus,startvm) = subprocess.getstatusoutput("powershell start-vm %s"%(vmname))
        if startvmstatus == 0:
            print("开启虚拟机%s成功！"%(vmname))
        else:
            print("开启虚拟机%s失败！可能是虚拟机不存在或者未安装Hyper-V组件！"%(vmname))
    def stopvm(vmname):
        print("正在关闭虚拟机%s..."%(vmname))
        (stopvmstatus,stopvm) = subprocess.getstatusoutput("powershell stop-vm %s"%(vmname))
        if stopvmstatus == 0:
            print("关闭虚拟机%s成功！"%(vmname))
        else:
            print("关闭虚拟机%s失败！可能是虚拟机不存在或者未安装Hyper-V组件！")
    def createvm(vmname,vmimg,vmmem,vmswitch):
        print("正在创建虚拟机中")
        (createvmstatus,createvm) =  subprocess.getstatusoutput("powershell New-vm -VHDPath %s -Generation 1 -MemoryStartupBytes %sGB -Name %s -SwitchName %s"%(vmpath,vmmem,vmname,vmswitch))
        if createvmstatus == 0:
            print("创建虚拟机%s成功！"%(vmname))
        else:
            print("创建虚拟机%s失败！请检查路径是否正常设置以及Hyper-V组件是否正常安装！"%(vmname))
    def copyvmimage(dirname,vmver):
        global path
        global vmpath
        path = os.path.join("E:\\hy",dirname)
        vmpath = os.path.join("E:\\temp",vmver)
        print("正在新建文件夹")
        os.mkdir(path)
        print("正在移动镜像文件，速度取决于当前硬盘性能。。。")
        shutil.copy(vmpath,path)
    def setvmconfig(vmname,vmoperate,vmcfg):
        if vmoperate == 1:
            (setvmstatus,setvm) = subprocess.getstatusoutput("powershell Set-VM -Name %s -ProcessorCount %s"%(vmname,vmcfg))
            if setvmstatus == 0:
                print("更改虚拟机%s核心数量为%s成功！"%(vmname,vmcfg))
            elif setvmstatus == 1:
                print("更改虚拟机失败！可能是虚拟机不存在或者超出了所允许的最大值！")
        elif vmoperate == 2:
            (setvmstatus,setvm) = subprocess.getstatusoutput("powershell Set-VM -Name %s -DynamicMemory -MemoryMaximumBytes %s -Passthru | Start-VM"%(vmname,vmcfg))
            if setvmstatus == 0:
                print("更改虚拟机%s内存大小为%sMB成功！"%(vmname,vmcfg))
            elif setvmstatus == 1:
                print("更改虚拟机失败！可能是虚拟机不存在或者超出了所允许的最大值！")
    try:
        printMenu()
        operate = 0
        operate = int(input("请输入你想执行的操作:"))
    except ValueError:
        print("爷让你输入一个数字，你没有输入，给爷爬")
    if operate == 5:
        getvm()
    elif operate == 3:
        getvm()
        vmname = str(input("请输入想要开启的虚拟机:"))
        startvm(vmname)
    elif operate == 4:
        getvm()
        vmname = str(input("请输入想要关闭的虚拟机："))
        stopvm(vmname)
    elif operate == 0:
        programstatus = False
    elif operate == 1:
        print("1 = Windows Server 2012")
        vmimg = int(input("请输入你想创建的系统版本(输入对应数字):"))
        vmname = input("给虚拟机起个名吧:")
        vmmem = input("你想给虚拟机分多少内存(单位：GB)：")
        vmswitch = input("请指定一个虚拟交换机(默认为wan)：")
        if vmimg == 1:
            copyvmimage(vmname,"WinServer2012.vhdx")
            createvm(vmname,vmimg,vmmem,vmswitch)
    elif operate == 6:
        confirmstatus = input("该操作需要虚拟机关机状态下执行，请确认是否已经关机(确认扣1不确认扣2)")
        if confirmstatus == "1":
            getvm()
            print("1=cpu核心数量 2=内存大小")
            vmname = input("请输入你想修改的虚拟机名字:")
            vmoperate = int(input("请输入你想更改的虚拟机参数（请输入一个数字）:"))
            if vmoperate == 1:
                vmcfg = int(input("请输入更改后的cpu核心数量"))
                setvmconfig(vmname,vmoperate,vmcfg)
            if vmoperate == 2:
                vmcfg = int(input("请输入更改后的内存大小(单位:MB):"))
                setvmconfig(vmname,vmoperate,vmcfg)
        else:
            pass
