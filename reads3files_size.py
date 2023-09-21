
# Khai báo các thư viên cần thiết lấy lấy các hàm trong Python 
from __future__ import division  

from datetime import datetime, timedelta
import boto3
import math
import sys
import botocore

# Hàm chuyển đổi kích thước dữ liệu thành đơn vị đọc được theo kích cỡ như MB, GB
def human_readable_size(size):
    splitter = ["B", "KB", "MB", "GB", "TB", "PB"]
    splitter_index = 0
    while size > 1024 and splitter_index < 5:
        splitter_index += 1
        size = size / 1024
    size = '{:.2f}'.format(size)  # Định dạng kích thước với 2 chữ số thập phân
    return '{} {}'.format(size, splitter[splitter_index])

# Hàm lấy thông tin về các đối tượng trong một S3 bucket
def get_bucket_data(bucket_name):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)
    bucket_object_count = sum(1 for _ in bucket.objects.all())  # Đếm số đối tượng trong bucket
    total_bucket_size = 0
    print('Bucket name: {}'.format(bucket.name))
    print('Bucket created at: {}'.format(bucket.creation_date))
    print('Bucket objects:')
    for obj in bucket.objects.all():
        bucket_object = s3.Object(bucket.name, obj.key)
        total_bucket_size += int(bucket_object.content_length)  # Tính tổng kích cỡ của các đối tượng trong bucket

        size_hr = human_readable_size(int(bucket_object.content_length))
        # In thông tin về các đối tượng trong bucket, bao gồm kích thước
        print(' - (size: {:10}) {}'.format(size_hr, bucket_object.key))
    
    print('-------')
    print('Bucket object count: {}'.format(bucket_object_count))
    print('Total_bucket_size: {}'.format(human_readable_size(total_bucket_size)))
    print('-' * 20)

# Khởi tạo kết nối tới AWS S3 service
s3_resource = boto3.resource('s3', region_name='us-east-1')  # Sử dụng region 'us-east-1'
s3_client = boto3.client('s3')
bucket_list = s3_client.list_buckets()  # Lấy danh sách các bucket S3

try:
    # Vòng lặp chạy qua danh sách các bucket và lấy thông tin của chúng
    for bucket_info in bucket_list.get('Buckets'):
        get_bucket_data(bucket_info.get('Name'))
except botocore.exceptions.ClientError as e:
    print(e.response['Error']['Code'])
