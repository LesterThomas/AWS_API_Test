import time
import boto3
import requests

#print("Retrieving EC2 vpc")
#ec2 = boto3.resource('ec2')
#ec2client = boto3.client('ec2')
#response = ec2client.describe_vpcs()
#print(response)


print("")
print("")
print("")

ec2resource = boto3.resource('ec2')
#print(response)

print("Creating new image")
createresponse=ec2resource.create_instances(ImageId='ami-5be0f43f', MinCount=1, MaxCount=1,InstanceType='t2.micro',SecurityGroupIds=['sg-fd0c8394'])
print (createresponse[0].private_ip_address)
jsonString={"connection":"tcp:" + str(createresponse[0].private_ip_address) + ":14550"}
print(jsonString)
#time.sleep(60)
r = requests.post('http://droneapi.ddns.net:1235/vehicle', json = jsonString)


print(r.status_code)
print(r.content)

#print(createresponse[0]["PrivateIpAddress"])



