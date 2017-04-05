
import boto3

#print("Retrieving EC2 vpc")
#ec2 = boto3.resource('ec2')
#ec2client = boto3.client('ec2')
#response = ec2client.describe_vpcs()
#print(response)


print("")
print("")
print("")
print("Retrieving EC2 instances")

ec2client = boto3.client('ec2')
response = ec2client.describe_instances()
#print(response)
instances=[]

for reservation in response["Reservations"]:
	for instance in reservation["Instances"]:
		# This sample print will output entire Dictionary object
		#print(instance)
		# This will print will output the value of the Dictionary key 'InstanceId'
		print(instance["InstanceId"],instance["InstanceType"],instance["State"]["Name"])
		if (instance["State"]["Name"]=="stopped"):
			instances.append(instance["InstanceId"])
			
print("")
print("instances to start")
print(instances)
	
if (len(instances)>0):	
	startresp=ec2client.start_instances(InstanceIds=instances)
	#stopresp=ec2client.stop_instances(InstanceIds=instances)
	print("Started all instances")

#for i in vpc.instances.all():
#    print(i)
#		startresponse=ec2client.start_instances(instance["InstanceId"])	
