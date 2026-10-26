#!/usr/bin/env python3
import os

import aws_cdk as cdk

from adjust_layer_directory import adjust_layer_directory
from stack.iac_stack import IacStack

print("Starting the CDK")

print("Adjusting the layer directory")
adjust_layer_directory()
print("Finished adjusting the layer directory")


app = cdk.App()

aws_region = os.environ.get("AWS_REGION")
aws_account_id = os.environ.get("AWS_ACCOUNT_ID")
stack_name = os.environ.get("STACK_NAME")
# Prefira STAGE (setado no workflow). Em branches infra/<x>, o synth
# passa so o prefixo "infra" para evitar "/" em nomes de recurso.
stage = (os.environ.get("STAGE") or os.environ.get("GITHUB_REF_NAME") or "dev").capitalize()

tags = {
    'project': 'PortfolioApi',
    'stage': stage,
    'stack': stack_name,
    'owner': 'DevCommunity',
}

IacStack(
    app, 
    stack_id=stack_name, 
    stack_name=stack_name,
    stage=stage,
    env=cdk.Environment(
        account=aws_account_id,
        region=aws_region
        ), 
    tags=tags
)

app.synth()