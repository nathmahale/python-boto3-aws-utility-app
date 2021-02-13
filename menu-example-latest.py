from _cffi_backend import callback
from boto3automationlibrary import *
import sys

## Enter the absolute path location of atomationLibrary.py to make it accessible during the tool's runtime
sys.path.append(
    r"<<location>>")


def getDGTarget():
    getDGTWindow = Toplevel(rootObject)
    getDGTWindow.geometry('200x250')
    getDGTWindow.title("Get Deployment target")

    getDGTLabel = Label(getDGTWindow, text="CD app name",
                        font=subMenuFontStyle1)
    getDGTLabel.grid(row=0, sticky=NW)

    getDGTTextEntry = Entry(
        getDGTWindow, font=subMenuFontStyle1, bg=getRandomColor(), fg=getRandomColor())
    getDGTTextEntry.grid(row=1)

    submitButton = Button(getDGTWindow, text="Submit", font=submitButtonStyle, bg=submitButtonBGColor, fg=getRandomColor(),
                          command=lambda: messagebox.showinfo("showinfo", getCodeDeployDGTarget(getDGTTextEntry.get())))
    submitButton.grid(row=2, sticky=NW)

    exitButton = Button(getDGTWindow, text="Exit App", font=exitButtonStyle,
                        bg=exitButtonBGColor, fg=exitButtonFGColor, command=getDGTWindow.quit)
    exitButton.grid(row=3, sticky=NW)


def changeEC2InstanceTypeWrapper():
    getEC2InstanceWindow = Toplevel(rootObject)
    getEC2InstanceWindow.geometry("")
    getEC2InstanceWindow.title("EC2 change instance type")

    instanceIDLabel = Label(getEC2InstanceWindow,
                            text="Instance ID", font=subMenuFontStyle1)
    instanceIDLabel.grid(row=0, sticky=NW)
    instanceIDTextEntry = Entry(getEC2InstanceWindow, font=subMenuFontStyle1)
    instanceIDTextEntry.grid(row=1)

    instanceTypeLabel = Label(getEC2InstanceWindow,
                              text="Instance Type", font=subMenuFontStyle1)
    instanceTypeLabel.grid(row=2, sticky=NW)
    instanceTypeTextEntry = Entry(getEC2InstanceWindow, font=subMenuFontStyle1)
    instanceTypeTextEntry.grid(row=3)

    submitButton = Button(getEC2InstanceWindow, text="Submit", font=submitButtonStyle, bg=submitButtonBGColor, fg=getRandomColor(),
                          command=lambda: messagebox.showinfo("showinfo", changeEC2InstanceType(instanceIDTextEntry.get(), instanceTypeTextEntry.get())))
    submitButton.grid(row=4, sticky=NW)

    exitButton = Button(getEC2InstanceWindow, text="Exit App", font=exitButtonStyle,
                        bg=exitButtonBGColor, fg=exitButtonFGColor, command=getEC2InstanceWindow.quit)
    exitButton.grid(row=5, sticky=NW)


def retrieveWindowsEC2PasswordClipboard(instanceID, choice):
    retrieveEC2PasswordWindow = Toplevel(rootObject)
    retrieveEC2PasswordWindow.geometry('325x200')
    retrieveEC2PasswordWindow.title("Retrieve Windows Password")
    passwordContent = Text(retrieveEC2PasswordWindow)
    passwordData = getWindowsPassword(instanceID, choice)

    passwordContent.insert(1.0, str('Private IP is\n'))
    passwordContent.insert(2.0, str(passwordData[0]))
    passwordContent.insert(3.0, str('\nPassword is\n'))
    passwordContent.insert(4.0, str(passwordData[1]))
    passwordContent.pack()


def getEC2PasswordWrapper():
    getEC2InstanceWindow = Toplevel(rootObject)
    getEC2InstanceWindow.geometry('')
    getEC2InstanceWindow.title("Get Windows Password")
    Label(getEC2InstanceWindow, text="Instance ID",
          font=subMenuFontStyle1, justify=LEFT).pack(anchor=NW)

    instanceIDTextEntry = Entry(getEC2InstanceWindow, font=subMenuFontStyle1)
    instanceIDTextEntry.pack(anchor=W)
    v = IntVar()
    for val, envNameListing in enumerate(envList):
        R = Radiobutton(getEC2InstanceWindow, text=envNameListing[0], bd=3, bg="green", activebackground="cyan",
                        padx=10, font=subMenuFontStyle2, variable=v, indicatoron=0,
                        command=lambda: retrieveWindowsEC2PasswordClipboard(
                            instanceIDTextEntry.get(), v.get()),
                        value=val, anchor=W, width=10)
        R.pack(anchor=W, padx=5, pady=5)

    exitButton = Button(getEC2InstanceWindow, text="Exit App", font=exitButtonStyle,
                        bg=exitButtonBGColor, fg=exitButtonFGColor, command=getEC2InstanceWindow.quit)
    exitButton.pack(anchor=W)


def EC2GenericCommandWrapper(choice, instanceID):
    if int(choice) == 0:
        return(terminateEC2Instance(instanceID))
    elif int(choice) == 1:
        return(stopEC2Instance(instanceID))
    elif int(choice) == 2:
        return(startEC2Instance(instanceID))
    elif int(choice) == 3:
        return(rebootEC2Instance(instanceID))
    elif int(choice) == 4:
        return(enableTerminationProtection(instanceID))
    elif int(choice) == 5:
        return(disableTerminationProtection(instanceID))
    elif int(choice) == 6:
        return(addCPMTag(instanceID))
    elif int(choice) == 7:
        return(tagExtendedOfficeHoursEC2(instanceID))
    elif int(choice) == 8:
        return(addRDSTag(instanceID))


def EC2ManagementWrapper():
    getEC2InstanceWindow = Toplevel(rootObject)
    getEC2InstanceWindow.geometry("")
    getEC2InstanceWindow.title("EC2 change instance type")

    instanceIDLabel = Label(getEC2InstanceWindow,
                            text="Instance ID", font=subMenuFontStyle1)
    instanceIDLabel.grid(row=0, sticky=NW)
    instanceIDTextEntry = Entry(getEC2InstanceWindow, font=subMenuFontStyle1)
    instanceIDTextEntry.grid(row=1, sticky=NW)

    v = IntVar()
    for val, ec2operation in enumerate(ec2ManagementMenu):
        Radiobutton(getEC2InstanceWindow,
                    text=ec2operation[0],
                    padx=20,
                    font=subMenuFontStyle2,
                    variable=v,
                    value=val).grid(sticky=NW)

    submitButton = Button(getEC2InstanceWindow, text="Submit", font=submitButtonStyle,
                          command=lambda: messagebox.showinfo("showinfo", EC2GenericCommandWrapper(v.get(), instanceIDTextEntry.get())))
    submitButton.grid(sticky=NW)

    exitButton = Button(getEC2InstanceWindow, text="Exit App", font=exitButtonStyle,
                        bg=exitButtonBGColor, fg=exitButtonFGColor, command=getEC2InstanceWindow.quit)
    exitButton.grid(sticky=NW)


def getStackOutput():
    stackOutputWindow = Toplevel(rootObject)
    stackOutputWindow.geometry("")
    stackOutputWindow.title("Get Deployment target")

    stackOutputLabel = Label(
        stackOutputWindow, text="CD app name", font=subMenuFontStyle1)
    stackOutputLabel.grid(row=0, sticky=NW)
    stackOutputTextEntry = Entry(stackOutputWindow, font=subMenuFontStyle1)
    stackOutputTextEntry.grid(row=1)

    submitButton = Button(stackOutputWindow, text="Submit", font=submitButtonStyle,
                          command=lambda: messagebox.showinfo("showinfo", describeStack(stackOutputTextEntry.get())))
    submitButton.grid(row=2, sticky=NW)

    exitButton = Button(stackOutputWindow, text="Exit App", font=exitButtonStyle,
                        bg=exitButtonBGColor, fg=exitButtonFGColor, command=stackOutputWindow.quit)
    exitButton.grid(row=3, sticky=NW)


def copyS3():
    s3CopyWindow = Toplevel(rootObject)
    s3CopyWindow.geometry("")
    s3CopyWindow.title("Upload file to S3")

    s3CopyFromLabel = Label(
        s3CopyWindow, text="Please enter fileName of ZIP from local downLoadsDir", font=subMenuFontStyle1)
    s3CopyFromLabel.grid(row=0, sticky=NW)
    s3CopyFromTextEntry = Entry(s3CopyWindow, font=subMenuFontStyle1)
    s3CopyFromTextEntry.grid(row=1, sticky=NW)

    s3CopyToBucketLabel = Label(
        s3CopyWindow, text="Please enter bucket name", font=subMenuFontStyle1)
    s3CopyToBucketLabel.grid(row=2, sticky=NW)
    s3CopyToBucketTextEntry = Entry(s3CopyWindow, font=subMenuFontStyle1)
    s3CopyToBucketTextEntry.grid(row=3, sticky=NW)

    s3CopyToBucketKeyLabel = Label(
        s3CopyWindow, text="Please enter key name", font=subMenuFontStyle1)
    s3CopyToBucketKeyLabel.grid(row=4, sticky=NW)
    s3CopyToBucketKeyTextEntry = Entry(s3CopyWindow, font=subMenuFontStyle1)
    s3CopyToBucketKeyTextEntry.grid(row=5, sticky=NW)

    submitButton = Button(s3CopyWindow, text="Submit", font=submitButtonStyle, bg=submitButtonBGColor, fg=getRandomColor(),
                          command=lambda: messagebox.showinfo("showinfo",
                                                              uploadToS3Location(s3CopyFromTextEntry.get(), s3CopyToBucketTextEntry.get(), s3CopyToBucketKeyTextEntry.get())))
    submitButton.grid(row=6, sticky=NW)

    exitButton = Button(s3CopyWindow, text="Exit App", font=exitButtonStyle,
                        bg=exitButtonBGColor, fg=exitButtonFGColor, command=s3CopyWindow.quit)
    exitButton.grid(row=7, sticky=NW)


def copyBetweenSameS3():
    s3SameCopyWindow = Toplevel(rootObject)
    s3SameCopyWindow.geometry('')
    s3SameCopyWindow.title("Copy file in same S3 bucket")
    radio_buttons = {item: IntVar()
                     for item in s3BucketNameList}
    var1= tk.StringVar()


    s3CopyFromKeyLabel = Label(
        s3SameCopyWindow, text="Enter fromKey", font=subMenuFontStyle2)
    s3CopyFromKeyLabel.pack(anchor=W)
    s3CopyFromKeyTextEntry = Entry(
        s3SameCopyWindow, font=subMenuFontStyle2, width=60)
    s3CopyFromKeyTextEntry.pack(anchor=W)

    for item in s3BucketNameList:
        Radiobutton(s3SameCopyWindow, text=item, font=subMenuFontStyle2,
                    bg=radioButtonBGColor, selectcolor=color["green"], activebackground=color["orange"], value=item, var=var1).pack(anchor=W)

    s3CopyToKeyLabel = Label(
        s3SameCopyWindow, text="Enter toKey", font=subMenuFontStyle2)
    s3CopyToKeyLabel.pack(anchor=W)
    s3CopyToKeyTextEntry = Entry(
        s3SameCopyWindow, font=subMenuFontStyle2, width=60)
    s3CopyToKeyTextEntry.pack(anchor=W)

    submitButton = Button(s3SameCopyWindow, text="Submit", font=submitButtonStyle, bg=submitButtonBGColor, fg=getRandomColor(),
                          command=lambda: messagebox.showinfo("showinfo",
                                                              copyBetweenSameS3Buckets(var1.get(), s3CopyFromKeyTextEntry.get(), s3CopyToKeyTextEntry.get())))
    submitButton.pack(anchor=W)

    exitButton = Button(s3SameCopyWindow, text="Exit App", font=exitButtonStyle,
                        bg=exitButtonBGColor, fg=exitButtonFGColor, command=s3SameCopyWindow.quit)
    exitButton.pack(anchor=W)


def copyBetweenS3Buckets():
    s3IntraCopyWindow = Toplevel(rootObject)
    s3IntraCopyWindow.geometry('')
    s3IntraCopyWindow.title("Copy file between S3 buckets")
    radio_buttons = {item: IntVar()
                     for item in s3BucketNameList}
    # Radiobutton variables:
    var1, var2 = tk.IntVar(), tk.IntVar()

    Label(s3IntraCopyWindow, text="FromS3Bucket", font=subMenuFontStyle2,
          bg=radioButtonBGColor).pack(anchor=W)

    # Radiobutton set1:
    for item in s3BucketNameList:
        Radiobutton(s3IntraCopyWindow, text=item, font=subMenuFontStyle2,
                    bg=radioButtonBGColor, selectcolor=color["green"], activebackground=color["orange"], value=item, var=var1).pack(anchor=W)

    # label text2:
    Label(s3IntraCopyWindow, text="ToS3Bucket", font=subMenuFontStyle2,
          bg=radioButtonBGColor).place(x=300, y=0)
    # set y-coordinate:
    y = 20
    # Radiobutton set2:
    for item in s3BucketNameList:
        Radiobutton(s3IntraCopyWindow, text=item, font=subMenuFontStyle2,
                    bg=radioButtonBGColor, selectcolor=color["green"], activebackground=color["orange"], value=item, var=var2).place(x=300, y=y)
        y += 26

    s3CopyFromKeyLabel = Label(
        s3IntraCopyWindow, text="Please enter from key eg: folder1/folder2/file1.txt", font=subMenuFontStyle2)
    s3CopyFromKeyLabel.pack(anchor=W)

    s3CopyFromKeyTextEntry = Entry(
        s3IntraCopyWindow, font=subMenuFontStyle1, width=60)
    s3CopyFromKeyTextEntry.pack(anchor=W)

    s3CopyToKeyLabel = Label(
        s3IntraCopyWindow, text="Please enter to key eg:folder1/folder2/file1.txt", font=subMenuFontStyle2)
    s3CopyToKeyLabel.pack(anchor=W)
    s3CopyToKeyTextEntry = Entry(
        s3IntraCopyWindow, font=subMenuFontStyle1, width=60)
    s3CopyToKeyTextEntry.pack(anchor=W)

    submitButton = Button(s3IntraCopyWindow, text="Submit", font=submitButtonStyle, bg=submitButtonBGColor, fg=getRandomColor(),
                          command=lambda: messagebox.showinfo("showinfo",
                                                              copyBetweenSameS3Buckets(s3CopyBucketTextEntry.get(), s3CopyFromKeyTextEntry.get(), s3CopyToKeyTextEntry.get())))
    submitButton.pack(anchor=W)

    exitButton = Button(s3IntraCopyWindow, text="Exit App", font=exitButtonStyle,
                        bg=exitButtonBGColor, fg=exitButtonFGColor, command=s3IntraCopyWindow.quit)
    exitButton.pack(anchor=W)


def deleteAMI():
    deleteAMIWindow = Toplevel(rootObject)
    deleteAMIWindow.geometry('300x200')
    deleteAMIWindow.title("Delete AMI")

    amiLabel = Label(deleteAMIWindow, text="Please enter AMI ID",
                     font=subMenuFontStyle1)
    amiLabel.grid(row=0, sticky=NW)
    amiTextEntry = Entry(deleteAMIWindow, font=subMenuFontStyle1, width=30)
    amiTextEntry.grid(row=1)

    submitButton = Button(deleteAMIWindow, text="Submit", font=submitButtonStyle,
                          command=lambda: messagebox.showinfo("showinfo", deregisterAMIdeleteSnapshots(amiTextEntry.get())))
    submitButton.grid(row=2, sticky=NW)

    exitButton = Button(deleteAMIWindow, text="Exit App", font=exitButtonStyle,
                        bg=exitButtonBGColor, fg=exitButtonFGColor, command=deleteAMIWindow.quit)
    exitButton.grid(row=3, sticky=NW)


def deleteStackFunction():
    deleteStackWindow = Toplevel(rootObject)
    deleteStackWindow.geometry('')
    deleteStackWindow.title("Delete CloudFormation Stack")

    stackLabel = Label(deleteStackWindow,
                       text="Please enter Stack name", font=subMenuFontStyle2)
    stackLabel.grid(row=0, sticky=NW)
    stackEntryTextEntry = Entry(deleteStackWindow, font=subMenuFontStyle1, width=50)
    stackEntryTextEntry.grid(row=1)

    submitButton = Button(deleteStackWindow, text="Submit", font=submitButtonStyle,
                          command=lambda: messagebox.showinfo("showinfo", deleteStack(stackEntryTextEntry.get())))
    submitButton.grid(row=2, sticky=NW)

    exitButton = Button(deleteStackWindow, text="Exit App", font=exitButtonStyle,
                        bg=exitButtonBGColor, fg=exitButtonFGColor, command=deleteStackWindow.quit)
    exitButton.grid(row=3, sticky=NW)


def ASGProcessMgmt():
    asgProcessMgmtWindow = Toplevel(rootObject)
    asgProcessMgmtWindow.geometry('')
    asgProcessMgmtWindow.title("ASG process management")
    Label(asgProcessMgmtWindow,
          text="Please enter only ASG suffix as mentioned below\n eg: 'XOB0S0XNA9RT'\n application-env-asg-XZHOZIBFBGS1-AutoScalingGroup-XOB0S0XNA9RT", font=subMenuFontStyle2, justify=LEFT).pack(anchor=NW)
    asgSuffixTextEntry = Entry(
        asgProcessMgmtWindow, font=subMenuFontStyle1, justify=LEFT)
    asgSuffixTextEntry.pack(anchor=NW)
    check_boxes = {item: IntVar()
                   for item in asgProcessList}  # create dict of check_boxes

    def confirmASGList():
        asgSelectedList.clear()
        for key, value in check_boxes.items():
            if (value.get()):
                asgSelectedList.append(key)
        return(asgSelectedList)

    def clearASGList():
        for item in asgProcessList:
            check_boxes[item].set(0)

    def ASGManage(ASGSuffix, operation):
        asgSelectedList.clear()
        for key, value in check_boxes.items():
            if (value.get()):
                asgSelectedList.append(key)

        if int(operation) == 10:
            return(resumeASGProcesses(ASGSuffix, asgSelectedList))
        elif int(operation) == 100:
            return(suspendASGProcesses(ASGSuffix, asgSelectedList))

    for item in asgProcessList:
        C = Checkbutton(asgProcessMgmtWindow, text=item, font=subMenuFontStyle2,
                        variable=check_boxes[item], anchor=W,  onvalue=1, offvalue=0, height=1, width=40, justify=LEFT)
        C.pack(anchor=W, padx=5, pady=5)

    v = IntVar()
    Radiobutton(asgProcessMgmtWindow, text="Resume ASG Process(es)", font=subMenuFontStyle2,
                variable=v, value=10).pack(anchor=W, padx=5, pady=5)
    Radiobutton(asgProcessMgmtWindow, text="Suspend ASG Process(es)", font=subMenuFontStyle2,
                variable=v, value=100).pack(anchor=W, padx=5, pady=5)

    Button(asgProcessMgmtWindow, text="Submit", activebackground="red", bd=3, bg="green", font=submitButtonStyle,
           command=lambda: messagebox.showinfo("showinfo", ASGManage(asgSuffixTextEntry.get(), v.get()))).pack(anchor=W)
    Button(asgProcessMgmtWindow, text="Clear All ", command=clearASGList, activebackground="red", font=submitButtonStyle,
           bd=3, bg="green").pack(anchor=W)

    Button(asgProcessMgmtWindow, text="Exit App", font=exitButtonStyle,
           bg=exitButtonBGColor, fg=exitButtonFGColor, command=asgProcessMgmtWindow.quit).pack(anchor=W)

def detachInstanceFromASG():
    asgInstanceDetachWindow = Toplevel(rootObject)
    asgInstanceDetachWindow.geometry('')
    asgInstanceDetachWindow.title("Detach Instance from ASG")
    Label(asgInstanceDetachWindow,
          text="Please enter only ASG suffix as mentioned below\n eg: 'XOB0S0XNA9RT' \n application-env-asg-XZHOZIBFBGS1-AutoScalingGroup-XOB0S0XNA9RT", font=subMenuFontStyle2, justify=LEFT).pack(anchor=NW)
    asgSuffixTextEntry = Entry(
        asgInstanceDetachWindow, font=subMenuFontStyle1, justify=LEFT)
    asgSuffixTextEntry.pack(anchor=NW)

    Label(asgInstanceDetachWindow,
          text="Please enter instance-ID", font=subMenuFontStyle2, justify=LEFT).pack(anchor=NW)
    instanceIDTextEntry = Entry(
        asgInstanceDetachWindow, font=subMenuFontStyle1, justify=LEFT)
    instanceIDTextEntry.pack(anchor=NW)

    Button(asgInstanceDetachWindow, text="Submit", activebackground="red", bd=3, bg="green", font=submitButtonStyle,
           command=lambda: messagebox.showinfo("showinfo", detachEC2InstanceFromASG(asgSuffixTextEntry.get(), instanceIDTextEntry.get()))).pack(anchor=W)
    Button(asgInstanceDetachWindow, text="Exit App", font=exitButtonStyle,
           bg=exitButtonBGColor, fg=exitButtonFGColor, command=asgInstanceDetachWindow.quit).pack(anchor=W)

def modifyASGCapacity():
   modifyASGCapacityWindow = Toplevel(rootObject)
   modifyASGCapacityWindow.geometry('')
   modifyASGCapacityWindow.title("Modify ASG capacity")
   Label(modifyASGCapacityWindow,
          text="Please enter only ASG suffix as mentioned below\n eg: 'XOB0S0XNA9RT'\n application-env-asg-XZHOZIBFBGS1-AutoScalingGroup-XOB0S0XNA9RT", font=subMenuFontStyle2, justify=LEFT).pack(anchor=NW)
   asgSuffixTextEntry = Entry(
        modifyASGCapacityWindow, font=subMenuFontStyle2, justify=LEFT, width=15)
   asgSuffixTextEntry.pack(anchor=NW)

   Label(modifyASGCapacityWindow,
          text="desiredCapacity", font=subMenuFontStyle2, justify=LEFT).pack(anchor=NW)
   desiredCapacityTextEntry = Entry(
        modifyASGCapacityWindow, font=subMenuFontStyle1, justify=LEFT, width=5)
   desiredCapacityTextEntry.pack(anchor=NW)

   Label(modifyASGCapacityWindow,
          text="minInstance", font=subMenuFontStyle2, justify=LEFT).pack(anchor=NW)
   minInstanceTextEntry = Entry(
        modifyASGCapacityWindow, font=subMenuFontStyle1, justify=LEFT, width=5)
   minInstanceTextEntry.pack(anchor=NW)

   Label(modifyASGCapacityWindow,
          text="maxInstance", font=subMenuFontStyle2, justify=LEFT).pack(anchor=NW)
   maxInstanceTextEntry = Entry(
        modifyASGCapacityWindow, font=subMenuFontStyle1, justify=LEFT, width=5)
   maxInstanceTextEntry.pack(anchor=NW)

   Button(modifyASGCapacityWindow, text="Submit", activebackground="red", bd=3, bg="green", font=submitButtonStyle,
           command=lambda: messagebox.showinfo("showinfo", modifyASGCapacityFunction(asgSuffixTextEntry.get(), desiredCapacityTextEntry.get(), minInstanceTextEntry.get(), maxInstanceTextEntry.get()))).pack(anchor=W)
   Button(modifyASGCapacityWindow, text="Exit App", font=exitButtonStyle,
           bg=exitButtonBGColor, fg=exitButtonFGColor, command=modifyASGCapacityWindow.quit).pack(anchor=W)

def updateDGTarget():
    updateDGTWindow = Toplevel(rootObject)
    updateDGTWindow.geometry('450x650')
    updateDGTWindow.title("Update Deployment Target")

    getDGTLabel = Label(updateDGTWindow, text="App Name",
                        font=subMenuFontStyle2)
    getDGTLabel.pack(anchor=W)

    app_radio_buttons = {item: IntVar()
                     for item in appNameList}

    env_name_radio_buttons = {item: IntVar()
                     for item in envNameList}

    component_name_radio_buttons = {item: IntVar()
                     for item in componentNameList}
    
    # Radiobutton variables:
    var1, var2, var3 = tk.StringVar() , tk.StringVar(), tk.StringVar()
    y = 20

    for item in appNameList:
        Radiobutton(updateDGTWindow, text=item, font=subMenuFontStyle2,
                    bg=radioButtonBGColor, selectcolor=color["green"], activebackground=color["orange"], value=item, var=var1).pack(anchor=W)

    Label(updateDGTWindow, text="Env Name", font=subMenuFontStyle2,
          bg=radioButtonBGColor).place(x=100, y=0)

    for item in envNameList:
        Radiobutton(updateDGTWindow, text=item, font=subMenuFontStyle2,
                    bg=radioButtonBGColor, selectcolor=color["green"], activebackground=color["orange"], value=item, var=var2).place(x=100, y=y)
        y += 30

    Label(updateDGTWindow, text="Component Name", font=subMenuFontStyle2,
          bg=radioButtonBGColor).place(x=200, y=0)

    y = 20
    for item in componentNameList:
        Radiobutton(updateDGTWindow, text=item, font=subMenuFontStyle2,
                    bg=radioButtonBGColor, selectcolor=color["green"], activebackground=color["orange"], value=item, var=var3).place(x=200, y=y)
        y += 30

    Label(updateDGTWindow,
          text="Please enter only ASG suffix\n eg: XOB0S0XNA9RT \n application-env-asg-XZHOZIBFBGS1-AutoScalingGroup-XOB0S0XNA9RT", font=subMenuFontStyle2, justify=LEFT).place(x=0, y=450)
    asgSuffixTextEntry = Entry(
        updateDGTWindow, font=subMenuFontStyle1, justify=LEFT, width=20)
    asgSuffixTextEntry.place(x=0, y=520)

    Button(updateDGTWindow, text="Submit", font=submitButtonStyle, bg=submitButtonBGColor, fg=getRandomColor(),
                          command=lambda: messagebox.showinfo("showinfo", updateCodeDeployDGTarget(var1.get(), var2.get(), var3.get(), asgSuffixTextEntry.get()))).place(x=0, y=550)

    Button(updateDGTWindow, text="Exit App", font=exitButtonStyle,
                        bg=exitButtonBGColor, fg=exitButtonFGColor, command=updateDGTWindow.quit).place(x=0, y=580)

def loadBalancerTargetChange():
    loadBalancerTargetChange = Toplevel(rootObject)
    loadBalancerTargetChange.geometry('425x580')
    loadBalancerTargetChange.title("Update Loadbalancer target")

    getDGTLabel = Label(loadBalancerTargetChange, text="App name",
                        font=subMenuFontStyle2)
    getDGTLabel.pack(anchor=W)

    app_radio_buttons = {item: IntVar()
                     for item in appNameList}

    env_name_radio_buttons = {item: IntVar()
                     for item in envNameList}

    component_name_radio_buttons = {item: IntVar()
                     for item in componentNameList}
    
    port_radio_buttons = {item: IntVar()
                     for item in portList}

    # Radiobutton variables:
    var1, var2, var3 = tk.StringVar() , tk.StringVar(), tk.StringVar()
    var4, var5 = tk.IntVar(), tk.IntVar()


    # y = 230
    y = 140
    for item in appNameList:
        Radiobutton(loadBalancerTargetChange, text=item, font=subMenuFontStyle2,
                    bg=radioButtonBGColor, selectcolor=color["green"], activebackground=color["orange"], value=item, var=var1).pack(anchor=W)

    Label(loadBalancerTargetChange, text="TargetGroup Operation", font=subMenuFontStyle2,
          bg=radioButtonBGColor).place(x=0, y=330)
    registerRadioButton = Radiobutton(loadBalancerTargetChange, text='register', font=subMenuFontStyle2,
                bg=radioButtonBGColor, selectcolor=color["green"], activebackground=color["orange"], value=0, var= var5)
    deregisterRadioButton = Radiobutton(loadBalancerTargetChange, text='deregister', font=subMenuFontStyle2,
                bg=radioButtonBGColor, selectcolor=color["green"], activebackground=color["orange"], value=1, var= var5)
    registerRadioButton.place(x=0, y=350)
    deregisterRadioButton.place(x=0, y=380)

    Label(loadBalancerTargetChange, text="Env Name", font=subMenuFontStyle2,
          bg=radioButtonBGColor).place(x=0, y=120)

    for item in envNameList:
        Radiobutton(loadBalancerTargetChange, text=item, font=subMenuFontStyle2,
                    bg=radioButtonBGColor, selectcolor=color["green"], activebackground=color["orange"], value=item, var=var2).place(x=0, y=y)
        y += 30

    Label(loadBalancerTargetChange, text="Component Name", font=subMenuFontStyle2,
          bg=radioButtonBGColor).place(x=160, y=0)

    y = 20
    for item in componentNameList:
        Radiobutton(loadBalancerTargetChange, text=item, font=subMenuFontStyle2,
                    bg=radioButtonBGColor, selectcolor=color["green"], activebackground=color["orange"], value=item, var=var3).place(x=160, y=y)
        y += 30

    Label(loadBalancerTargetChange, text="Port Number", font=subMenuFontStyle2,
          bg=radioButtonBGColor).place(x=290, y=0)
    
    y=20
    for item in portList:
        Radiobutton(loadBalancerTargetChange, text=item, font=subMenuFontStyle2,
                    bg=radioButtonBGColor, selectcolor=color["green"], activebackground=color["orange"], value=item, var=var4).place(x=290, y=y)
        y += 30

    Label(loadBalancerTargetChange,
          text="Please enter instance-ID", font=subMenuFontStyle2, justify=LEFT).place(x=0, y=450)
    instanceIDTextEntry = Entry(
        loadBalancerTargetChange, font=subMenuFontStyle1, justify=LEFT, width=25)
    instanceIDTextEntry.place(x=0, y=470)

    Button(loadBalancerTargetChange, text="Submit", font=submitButtonStyle, bg=submitButtonBGColor, fg=getRandomColor(),
                          command=lambda: messagebox.showinfo("showinfo", updateCodeDeployDGTarget(var1.get(), var2.get(), var3.get(), asgSuffixTextEntry.get()))).place(x=0, y=500)

    Button(loadBalancerTargetChange, text="Exit App", font=exitButtonStyle,
                        bg=exitButtonBGColor, fg=exitButtonFGColor, command=loadBalancerTargetChange.quit).place(x=0, y=530)

def onExit(self):
    self.quit()

rootObject = Tk()
rootObject.geometry('300x275')
rootObject.title("boto3 utility")

customFontStyle = font.Font(family='Candara', size=15, weight=BOLD)
subMenuFontStyle1 = font.Font(family='Bahnschrift', size=13)
subMenuFontStyle2 = font.Font(family='Bahnschrift', size=10)
exitButtonStyle = font.Font(family='Cambria', size=10, weight=BOLD)
submitButtonStyle = font.Font(family='Cambria', size=10, weight=BOLD)

exitButton = Button(rootObject, text="Exit App", font=exitButtonStyle, bg=exitButtonBGColor, fg=exitButtonFGColor, command=rootObject.quit,
                    relief=RIDGE, justify=LEFT, anchor=W)
# rootObject.config(menu=exitMenu().menubar)


# EC2
menubutton0 = Menubutton(rootObject, text=masterMenuList[0], font=customFontStyle, bg=mainmenuBGColor, fg=mainmenuFGColor, relief=RAISED, anchor=W)
menubutton0.menu = Menu(menubutton0)
menubutton0["menu"] = menubutton0.menu
menubutton0.menu.add_command(label="Generic EC2 instance operations",
                             font=subMenuFontStyle1, command=EC2ManagementWrapper)
menubutton0.menu.add_command(label="Change EC2 instance type",
                             font=subMenuFontStyle1, command=changeEC2InstanceTypeWrapper)
menubutton0.menu.add_command(label="Get Windows password",
                             font=subMenuFontStyle1, command=getEC2PasswordWrapper)
menubutton0.menu.add_command(
    label="Delete AMI", font=subMenuFontStyle1, command=deleteAMI)
menubutton0.menu.add_command(
    label="Change Loadbalancer Target", font=subMenuFontStyle1, command=loadBalancerTargetChange)

# ASG
menubutton1 = Menubutton(rootObject, text=masterMenuList[1], font=customFontStyle, bg=mainmenuBGColor, fg=mainmenuFGColor, relief=RIDGE, justify=LEFT, anchor=W)
menubutton1.menu = Menu(menubutton1)
menubutton1["menu"] = menubutton1.menu
menubutton1.menu.add_command(
    label="ASG process management", font=subMenuFontStyle1, command=ASGProcessMgmt)
menubutton1.menu.add_command(
    label="Detach EC2 from ASG", font=subMenuFontStyle1, command=detachInstanceFromASG)
menubutton1.menu.add_command(
    label="Modify ASG capacity", font=subMenuFontStyle1, command=modifyASGCapacity)

# CFN
menubutton2 = Menubutton(rootObject, text=masterMenuList[2], font=customFontStyle, bg=mainmenuBGColor, fg=mainmenuFGColor, relief=GROOVE, justify=LEFT, anchor=W)
menubutton2.menu = Menu(menubutton2)
menubutton2["menu"] = menubutton2.menu
menubutton2.menu.add_command(
    label="List stack outputs", font=subMenuFontStyle1, command=getStackOutput)
menubutton2.menu.add_command(
    label="Delete cfn stack", font=subMenuFontStyle1, command=deleteStackFunction)

# CodeDeploy
menubutton3 = Menubutton(rootObject, text=masterMenuList[3], font=customFontStyle, bg=mainmenuBGColor, fg=mainmenuFGColor, relief=RIDGE, justify=LEFT, anchor=W)
menubutton3.menu = Menu(menubutton3)
menubutton3["menu"] = menubutton3.menu
menubutton3.menu.add_command(
    label="Trigger codeDeploy deployment", font=subMenuFontStyle1)
menubutton3.menu.add_command(
    label="List deployment target(s)", font=subMenuFontStyle1, command=getDGTarget)
menubutton3.menu.add_command(
    label="Update deployment target", font=subMenuFontStyle1, command=updateDGTarget)

# S3 copy
menubutton4 = Menubutton(rootObject, text=masterMenuList[4], font=customFontStyle, bg=mainmenuBGColor, fg=mainmenuFGColor,
                         relief=RIDGE, justify=LEFT, anchor=W)
menubutton4.menu = Menu(menubutton4)
menubutton4["menu"] = menubutton4.menu
menubutton4.menu.add_command(
    label="Upload file to S3 location", font=subMenuFontStyle1, command=copyS3)
menubutton4.menu.add_command(label="Copy file in same S3 bucket",
                             font=subMenuFontStyle1, command=copyBetweenSameS3)
menubutton4.menu.add_command(label="Copy file in different S3 buckets in same AWS a/c",
                             font=subMenuFontStyle1, command=copyBetweenS3Buckets)

menubutton0.pack(fill=BOTH, expand=True)
menubutton1.pack(fill=BOTH, expand=True)
menubutton2.pack(fill=BOTH, expand=True)
menubutton3.pack(fill=BOTH, expand=True)
menubutton4.pack(fill=BOTH, expand=True)

exitButton.pack(fill=BOTH, expand=True)


## Tool's main entry point
rootObject.mainloop()
