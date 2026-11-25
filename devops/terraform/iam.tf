# IAM Role for EC2 Instance (Least-Privilege RBAC)
resource "aws_iam_role" "ec2_role" {
  name = "ai-investment-ec2-role-${var.environment}"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      }
    ]
  })

  tags = {
    Name = "ai-investment-ec2-iam-role"
  }
}

# IAM Policy for S3 Document and Financial Report Storage
resource "aws_iam_policy" "s3_access_policy" {
  name        = "ai-investment-s3-policy-${var.environment}"
  description = "Allows EC2 instance to upload and read financial research PDFs and vector embeddings"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:ListBucket",
          "s3:DeleteObject"
        ]
        Resource = [
          aws_s3_bucket.report_storage.arn,
          "${aws_s3_bucket.report_storage.arn}/*"
        ]
      },
      {
        Effect = "Allow"
        Action = [
          "cloudwatch:PutMetricData",
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = "*"
      }
    ]
  })
}

# Attach Policy to Role
resource "aws_iam_role_policy_attachment" "ec2_s3_attach" {
  role       = aws_iam_role.ec2_role.name
  policy_arn = aws_iam_policy.s3_access_policy.arn
}

# Instance Profile attached to EC2
resource "aws_iam_instance_profile" "ec2_profile" {
  name = "ai-investment-instance-profile-${var.environment}"
  role = aws_iam_role.ec2_role.name
}
