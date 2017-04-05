
import boto3

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
createresponse=ec2resource.create_instances(ImageId='ami-22190d46', MinCount=1, MaxCount=1,InstanceType='t2.micro',SecurityGroupIds=['sg-c861dda1'])
print(createresponse)



