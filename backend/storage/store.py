"""
Storage Manager

Handles local and S3 storage for rendered images.
"""

import os
import shutil
from pathlib import Path
from typing import Optional


class StorageManager:
    """Manages file storage for renders."""
    
    def __init__(self):
        self.storage_type = os.getenv("STORAGE_TYPE", "local")
        self.local_base = Path(__file__).parent.parent / "samples" / "output"
        self.local_base.mkdir(parents=True, exist_ok=True)
        
    def save_file(self, source_path: str, destination_name: Optional[str] = None) -> str:
        """
        Save file to configured storage backend.
        
        Args:
            source_path: Path to source file
            destination_name: Optional custom filename
            
        Returns:
            Public URL or path to saved file
        """
        if self.storage_type == "s3":
            return self._save_to_s3(source_path, destination_name)
        else:
            return self._save_local(source_path, destination_name)
    
    def _save_local(self, source_path: str, destination_name: Optional[str]) -> str:
        """Save to local filesystem."""
        source = Path(source_path)
        
        if destination_name:
            dest = self.local_base / destination_name
        else:
            dest = self.local_base / source.name
            
        shutil.copy(source, dest)
        
        # Return relative path from backend root
        rel_path = dest.relative_to(Path(__file__).parent.parent)
        return f"/{rel_path.as_posix()}"
    
    def _save_to_s3(self, source_path: str, destination_name: Optional[str]) -> str:
        """Save to S3 bucket."""
        try:
            import boto3
            
            s3_client = boto3.client(
                's3',
                aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
                aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
                region_name=os.getenv("AWS_REGION", "us-east-1")
            )
            
            bucket = os.getenv("S3_BUCKET")
            key = destination_name or Path(source_path).name
            
            s3_client.upload_file(source_path, bucket, f"renders/{key}")
            
            # Return public URL
            return f"https://{bucket}.s3.amazonaws.com/renders/{key}"
            
        except Exception as e:
            print(f"S3 upload failed: {e}. Falling back to local storage.")
            return self._save_local(source_path, destination_name)
