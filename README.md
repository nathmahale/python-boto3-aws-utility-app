# python-boto3-aws-utility-app

This is a simple Python GUI application built using Python out-of-box Tkinter and AWS boto3 library.
The group of tasks are divided in 4 broad categories

- EC2
- ASG
- CloudFormation
- CodeDeploy
- S3


> Please install Python 3.7.3 and other dependant libraries from `./requirements.txt` using the following command 

``` python
pip install -r requirements.txt
```

> Please get SAML token , before running the application

``` powershell
aws-azure-login.cmd login --profile saml
```

> AWS EC2 Keypair location, please update the below location with keypair location in `boto3automationlibrary.py`

``` python
private_key_pair = r'<<location>>/keypair.pem'
```

![Home menu](./images/home-menu.jpg)


> **EC2 management**

- Generic EC2 instances operations --> like starting, rebooting, terminating EC2 instance,
adding EC2 tags.
- Change EC2 instance type --> change instance type of a stopped instance
- Get Windows password --> Retrieve Administrator password
- Delete AMI --> Delete snapshot and de-register AMI
- Change LoadBalancer target --> changes loadBalancer target


![ec2 menu](./images/ec2-menu-item1.jpg)


> **ASG management**

- ASG process management --> Resume/ Suspend ASG processes
- Detach EC2 from ASG --> This allows an instance to be detached from ASG, please check
DesiredCapacity value, before executing this.
- Modify ASG capacity --> Change max, min, DesiredCapacity


![ec2 menu](./images/asg-menu-item1.jpg)

>**CloudFormation management**

- List cfn stack outputs [ *WIP* ]
- Delete cfn stack
  
![cfn menu](./images/cfn-menu-item1.jpg)

> **CodeDeploy management**

- Trigger deployment --> Select app, env and component eg *vots-ops-app*
- List deployment targets --> List deployment targets of codeDeploy application
- Update deployment target --> Updates deployment target [ updating multiple targets to be added ]
  
![codeDeploy menu](./images/codeDeploy-menu-item1.jpg)

> **S3 management**

- Upload file to S3 location
- Copy file in same S3 bucket
- Copy filein different S3 buckets in same AWS account


![s3 menu](./images/s3-menu-item1.jpg)

> **Wish List**

- Add test cases using Python moto library
- Add more AWS services like SSM, CloudWatch Logs, etc
