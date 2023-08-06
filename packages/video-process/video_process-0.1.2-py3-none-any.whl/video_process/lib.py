import json
import os
from sts.sts import Sts
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client

# 腾讯云 COS 配置
BUCKET_NAME = os.environ.get("BUCKET_NAME")
COS_REGION = os.environ.get("COS_REGION", "ap-beijing")
COS_SECRET_ID = os.environ.get("COS_SECRET_ID")
COS_SECRET_KEY = os.environ.get("COS_SECRET_KEY")


def get_credential_demo(allow_prefix):
    config = {
        # 请求URL，域名部分必须和domain保持一致
        # 使用外网域名时：https://sts.tencentcloudapi.com/
        # 使用内网域名时：https://sts.internal.tencentcloudapi.com/
        "url": "https://sts.tencentcloudapi.com/",
        # 域名，非必须，默认为 sts.tencentcloudapi.com
        # 内网域名：sts.internal.tencentcloudapi.com
        "domain": "sts.tencentcloudapi.com",
        # 临时密钥有效时长，单位是秒
        "duration_seconds": 1800,
        "secret_id": COS_SECRET_ID,
        # 固定密钥
        "secret_key": COS_SECRET_KEY,
        # 设置网络代理
        # 'proxy': {
        #     'http': 'xx',
        #     'https': 'xx'
        # },
        # 换成你的 bucket
        "bucket": BUCKET_NAME,
        # 换成 bucket 所在地区
        "region": COS_REGION,
        # 这里改成允许的路径前缀，可以根据自己网站的用户登录态判断允许上传的具体路径
        # 例子： a.jpg 或者 a/* 或者 * (使用通配符*存在重大安全风险, 请谨慎评估使用)
        "allow_prefix": allow_prefix,
        # 密钥的权限列表。简单上传和分片需要以下的权限，其他权限列表请看 https://cloud.tencent.com/document/product/436/31923
        "allow_actions": [
            # 简单上传
            "name/cos:PutObject",
            "name/cos:PostObject",
            # 分片上传
            "name/cos:InitiateMultipartUpload",
            "name/cos:ListMultipartUploads",
            "name/cos:ListParts",
            "name/cos:UploadPart",
            "name/cos:CompleteMultipartUpload",
        ],
        # 临时密钥生效条件，关于condition的详细设置规则和COS支持的condition类型可以参考 https://cloud.tencent.com/document/product/436/71306
        # "condition": {},
    }

    try:
        sts = Sts(config)
        response = sts.get_credential()
        response["region"] = config["region"]
        response["bucket"] = config["bucket"]
        print("get data : " + json.dumps(dict(response), indent=4))
    except Exception as e:
        raise e
    return response


def get_cos_url(key):
    token = None  # 如果使用永久密钥不需要填入 token，如果使用临时密钥需要填入，临时密钥生成和使用指引参见 https://cloud.tencent.com/document/product/436/14048
    scheme = "https"  # 指定使用 http/https 协议来访问 COS，默认为 https，可不填

    config = CosConfig(
        Region=COS_REGION,
        SecretId=COS_SECRET_ID,
        SecretKey=COS_SECRET_KEY,
        Token=token,
        Scheme=scheme,
    )
    client = CosS3Client(config)

    # 生成URL
    url = client.get_object_url(Bucket=BUCKET_NAME, Key=key)
    return url


def upload_file(key, file_path):
    token = None  # 如果使用永久密钥不需要填入 token，如果使用临时密钥需要填入，临时密钥生成和使用指引参见 https://cloud.tencent.com/document/product/436/14048
    scheme = "https"  # 指定使用 http/https 协议来访问 COS，默认为 https，可不填

    config = CosConfig(
        Region=COS_REGION,
        SecretId=COS_SECRET_ID,
        SecretKey=COS_SECRET_KEY,
        Token=token,
        Scheme=scheme,
    )
    client = CosS3Client(config)

    # 上传文件
    response = client.upload_file(
        Bucket=BUCKET_NAME,
        LocalFilePath=file_path,
        Key=key,
        PartSize=10,
        MAXThread=10,
        EnableMD5=False,
    )
    return response["ETag"]


if __name__ == "__main__":
    get_credential_demo(["t1.jpg", "t2.jpg"])
    get_cos_url("71e52c67f5094e44b92ccaed93db15c5.jpg")
