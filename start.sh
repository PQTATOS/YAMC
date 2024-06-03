#!/bin/bash

cd terraform-cfgs

terraform apply

touch ../.env

echo "SUBNET_ID=$(terraform output --raw subnet_id)" >> ../.env

echo "POSTGRES_HOST=$(terraform output --raw db_host_FQDN)" >> ../.env

mv ../.env ../source/backend/app