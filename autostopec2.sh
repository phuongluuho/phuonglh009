#!/bin/bash

# Thiết lập access key và secret key
export AWS_ACCESS_KEY="YOUR_ACCESS_KEY"
export AWS_SECRET_KEY="YOUR_SECRET_KEY"
export AWS_REGION="YOUR_REGION"

# Lấy danh sách các instance IDs và trạng thái
instance_states=$(aws ec2 describe-instances --query 'Reservations[*].Instances[*].[InstanceId,State.Name]' --output text --region $AWS_REGION)

# Lặp qua từng dòng đầu ra từ lệnh describe-instances
while read -r instance_id state; do
    # Kiểm tra nếu trạng thái là "running" thì mới thực hiện lệnh stop
    if [ "$state" == "running" ]; then
        aws ec2 stop-instances --instance-ids "$instance_id" --region $AWS_REGION
        echo "Stopping instance: $instance_id"
    else
        # Nếu trạng thái không phải "running", thông báo trạng thái hiện tại của instance
        echo "Instance $instance_id is in state: $state"
    fi
done <<< "$instance_states"

# Kiểm tra nếu không có instance nào đang chạy
if [[ -z "$instance_states" ]]; then
    echo "No running instances found."
fi
