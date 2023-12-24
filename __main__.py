import pulumi
import pulumi_awsx as awsx
import pulumi_eks as eks

# Create VPC
pu_vpc = awsx.ec2.Vpc("pu-vpc",
    enable_dns_hostnames=True,
    cidr_block="10.202.0.0/16",
    tags={"Name": "pu-vpc"},
)

# Create the EKS cluster
pu_cluster = eks.Cluster("pu-cluster",
    vpc_id=pu_vpc.vpc_id,
    public_subnet_ids=pu_vpc.public_subnet_ids,
    private_subnet_ids=pu_vpc.private_subnet_ids,
    instance_type="t3.medium",
    desired_capacity=3,
    min_size=2,
    max_size=5,
    node_associate_public_ip_address=False,
    endpoint_private_access=False,
    endpoint_public_access=True,
)

# Export values to use elsewhere
pulumi.export("kubeconfig", pu_cluster.kubeconfig)
pulumi.export("vpcId", pu_vpc.vpc_id)