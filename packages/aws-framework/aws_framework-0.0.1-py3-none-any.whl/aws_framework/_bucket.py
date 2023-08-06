from boto3 import Session

from ._config import cfg, creds
from ._decorators import asyncify
from ._types import *


class S3Client:
    """Boto3 S3 Client"""

    executor = ThreadPoolExecutor(max_workers=10)

    @property
    def client(self):
        """Create an S3 client"""
        return Session(**creds.dict()).client("s3")  # type: ignore

    @asyncify
    def create_bucket(self, bucket_name: str) -> Awaitable[None]:
        """Create an S3 bucket"""
        return cast(Awaitable[None], self.client.create_bucket(Bucket=bucket_name))

    @asyncify
    def delete_bucket(self, bucket_name: str) -> Awaitable[None]:
        """Delete an empty S3 bucket"""
        return cast(Awaitable[None], self.client.delete_bucket(Bucket=bucket_name))

    @asyncify
    def list_buckets(self) -> Awaitable[list[dict[str, Any]]]:
        """List all buckets on S3"""
        return cast(Awaitable[list[dict[str, Any]]], self.client.list_buckets())

    @asyncify
    def list_objects(self, bucket_name: str) -> Awaitable[list[dict[str, Any]]]:
        """List objects in an S3 bucket"""
        return cast(
            Awaitable[list[dict[str, Any]]],
            self.client.list_objects(Bucket=bucket_name),
        )

    @asyncify
    def put_object(
        self,
        bucket_name: str,
        key: str,
        body: bytes,
        content_type: str,
        acl: str = "public-read",
        content_disposition: str = "inline",
        **kwargs
    ) -> Awaitable[None]:
        """Upload an object to an S3 bucket"""
        return cast(
            Awaitable[None],
            self.client.put_object(
                Bucket=bucket_name,
                Key=key,
                Body=body,
                ContentType=content_type,
                ACL=acl,
                ContentDisposition=content_disposition,
                **kwargs
            ),
        )

    @asyncify
    def generate_presigned_url(
        self,
        key: str,
        bucket_name: str = cfg.AWS_S3_BUCKET,
        expiration: int = 3600,
        **kwargs
    ) -> Awaitable[str]:
        """Generate a presigned URL to share an S3 object"""
        return cast(
            Awaitable[str],
            self.client.generate_presigned_url(
                ClientMethod="get_object",
                Params={"Bucket": bucket_name, "Key": key},
                ExpiresIn=expiration,
                **kwargs
            ),
        )

    @asyncify
    def get_object(self, bucket_name: str, key: str) -> Awaitable[dict[str, Any]]:
        """Download an object from an S3 bucket"""
        return cast(
            Awaitable[dict[str, Any]],
            self.client.get_object(Bucket=bucket_name, Key=key),
        )

    @asyncify
    def delete_object(self, bucket_name: str, key: str) -> Awaitable[None]:
        """Delete an object from an S3 bucket"""
        return cast(
            Awaitable[None],
            self.client.delete_object(Bucket=bucket_name, Key=key),
        )
