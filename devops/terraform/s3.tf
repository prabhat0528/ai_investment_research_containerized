# Random suffix for globally unique S3 bucket naming
resource "random_id" "bucket_suffix" {
  byte_length = 4
}

# S3 Bucket for Research Reports, Transcripts, and Vector Embeddings
resource "aws_s3_bucket" "report_storage" {
  bucket        = "ai-investment-reports-${var.environment}-${random_id.bucket_suffix.hex}"
  force_destroy = var.environment == "prod" ? false : true

  tags = {
    Name        = "ai-investment-report-storage"
    Environment = var.environment
  }
}

# S3 Bucket Ownership Controls
resource "aws_s3_bucket_ownership_controls" "report_storage_ownership" {
  bucket = aws_s3_bucket.report_storage.id

  rule {
    object_ownership = "BucketOwnerEnforced"
  }
}

# Block all public access for security compliance
resource "aws_s3_bucket_public_access_block" "report_storage_block" {
  bucket = aws_s3_bucket.report_storage.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# Server-Side Encryption (AES256)
resource "aws_s3_bucket_server_side_encryption_configuration" "report_storage_encryption" {
  bucket = aws_s3_bucket.report_storage.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# Lifecycle rule to archive older reports to Glacier to optimize cloud cost
resource "aws_s3_bucket_lifecycle_configuration" "report_storage_lifecycle" {
  bucket = aws_s3_bucket.report_storage.id

  rule {
    id     = "archive-old-audits"
    status = "Enabled"

    transition {
      days          = 90
      storage_class = "GLACIER"
    }

    expiration {
      days = 365
    }
  }
}
