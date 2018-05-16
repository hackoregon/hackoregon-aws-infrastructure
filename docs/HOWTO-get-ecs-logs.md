#GETTING LOGS FROM ECS

## Step 1: Find the public IP address of BastionHost
1. Log in AWS Console
2. Go to AWS CloudFormation under `Service` > `Management Tools`
3. On column `Stack Name`, click on the link named `<your stack name>-BastionHost-<a string>`. For example, `hacko18-BastionHost-10CS5LU2DG10L`
4. Under the `Resoures` section, click on the link on `Physical ID` column. You will be directed to the `Instances` section of the `Service`/`EC2` page. There will be 1 row in the table.
5. In the description of the pre-selected ec2 instance, look for the value of `IPv4 Public IP` field. This is the public IP address of the BastionHost.

## Step 2: Find the private IP address of the EC2 instance that hosts the ECS containers
1. Log in AWS Console
2. Go to `Services` > `Elastic Container Service`
3. Under the `ECS Instances` tab, on column `Service Name`, find the container instance that you want to get logs from by clicking on each of them one by one under the `Container Instance` column and look at what `Task Definition` they are running
4. Once you found the container instance you're looking for, go back to the table in \#3 above and click its corresponding link under the `EC2 Instance` column
5. Get the private IP address of this EC2 instance the same way as described in \#5 of Step 1 above.

## Step 3: Get all the logs 
1. Copy your aws account private key to the BastionHost by `scp -i <path to your aws account's private key> <**absolute path** to your aws account's private key> ec2-user@<BastionHost ip>
2. ssh into the BastionHost by `ssh -i <path to your aws account's private key file> ec2-user@<BastionHost's IP> ec2-user@<BastionHost ip>
3. Once you are in BastionHost, use `ls` to confirm you have the private key at the current directory. Then, ssh into the EC2 instance by `ssh -i <path to the private key> ec2-user@<EC2 instance's private IP>
4. Once you are in that EC2 instance, get the AWS ECS Log Collector by `curl -O https://raw.githubusercontent.com/awslabs/ecs-logs-collector/master/ecs-logs-collector.sh`
5. Run the script with `sudo bash ./ecs-logs-collector.sh`
6. There will be a archived file of all the logs named `collect.tgz` at the same director as you ran the script. Verify that this file exists and has a good amount of info by `ls -lh collect.tgz`
7. Exit the EC2 Instance (you are now back in the BastionHost)
8. Transfer the archived log file from the EC2 instance to BastionHost (where you are now) with `scp -i <path to your private key on BastionHost> ec2-user@<private IP of EC2 instance>:/home/ec2-user/collect.tgz .` (don't miss the dot at the end of this command)
9. Exit the BastionHost (you are now back in your local machine)
10. Transfer the archived log file from BastionHost to your local machine by `scp -i <path to your private key> ec2-user@<IP of BastionHost>:/home/ec2-user/collect.tgz .`
11. Verify the archived log file is finally in your local machine by `ls -lh ./collect.tgz`
12. Extract the archived log file with `tar xzfv collect.tgz`
13. All the ECS logs is in `./collect/system/` directory

TODO:
[ ] Write a script that get the IPs
[ ] Write a wrapper script around this AWS logs collector