import sys

import boto3
from pprint import pprint


# print(session.get_available_resources())


# -------------------------------------- Key Pairs --------------------------------------
# response = ec2_client.describe_key_pairs()
# key_pairs = response["KeyPairs"]
# for key_pair in key_pairs:
#     print("KeyPair Name:", key_pair["KeyName"])
# ----------------------------------------------------------------------------------------

# ------------------------------------ Create Instance ------------------------------------
# instance_params = {
#     "ImageId": "ami-04e601abe3e1a910f",  # Replace with the desired Amazon Machine Image (AMI) ID
#     "InstanceType": "t2.micro",  # Replace with the desired instance type
#     "KeyName": "project-key",   # Replace with the name of your EC2 key pair
#     "MinCount": 1,
#     "MaxCount": 1
# }
#
# instances = ec2_resource.create_instances(**instance_params)
# for instance in instances:
#     print("Instance ID:", instance.instance_id)
#     print("Public IP:", instance.public_ip_address)
#     print("Private IP:", instance.private_ip_address)

# ---------------------------------------------------------------------------------------

# print(f"response {response['Reservations'][0]['Instances'][0]['InstanceId']}")
# print(INSTANCE_ID)

class OptimoInstance:
    def __init__(self):
        self.session = boto3.session.Session(profile_name="terraform01", region_name="eu-central-1")
        self.ec2_resource = self.session.resource("ec2")
        self.ec2_client = self.session.client("ec2")
        self.INSTANCE_ID = self.ec2_client.describe_instances()['Reservations'][0]['Instances'][0]['InstanceId']
        self.instance = self.ec2_resource.Instance(self.INSTANCE_ID)

    # Printing Instance response
    def __str__(self):
        response = self.ec2_client.describe_instances()
        pprint(response)
        print("Instance ID:", self.instance.instance_id)
        print("Instance Type:", self.instance.instance_type)
        print("Public IP:", self.instance.public_ip_address)
        print("Private IP:", self.instance.private_ip_address)
        print('Launch Time', self.instance.launch_time)
        print('Availability Zone', self.instance.placement['AvailabilityZone'])
        print(f"The instance is {self.instance.state['Name']}")
        return "[+] Here is the instance description for you"

    def start_instance(self):
        # print(instance.state['Name'])
        if self.instance.state['Name'] == 'running':
            print(f"Instance {self.INSTANCE_ID} is already running")
            return True
        self.instance.start()
        self.instance.wait_until_running()
        return True

    def stop_instance(self):
        if self.instance.state['Name'] == 'stopped':
            print(f"Instance {self.INSTANCE_ID} is already stopped")
            return True
        self.instance.stop()
        self.instance.wait_until_stopped()
        return True


myinstance = OptimoInstance()
myinstance.stop_instance()
print(myinstance)