# IAM როლი Lambda-ისთვის
resource "aws_iam_role" "lambda_role" {
  name = "lambda_execution_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

# Lambda ფუნქცია Bronze → Silver
resource "aws_lambda_function" "bronze_to_silver" {
  function_name    = "bronze_to_silver"
  role             = aws_iam_role.lambda_role.arn
  runtime          = "python3.12"
  handler          = "bronze_to_silver.lambda_handler"
  filename         = "C:/Users/Administrator/data-engineering-final-project/terragrunt/env/dev/lambda/bronze_to_silver.zip"
  source_code_hash = filebase64sha256("C:/Users/Administrator/data-engineering-final-project/terragrunt/env/dev/lambda/bronze_to_silver.zip")


  environment {
    variables = {
      BRONZE_BUCKET = var.bronze_bucket_name
      SILVER_BUCKET = var.silver_bucket_name
    }
  }
}

# Lambda ფუნქცია Silver → Gold
resource "aws_lambda_function" "silver_to_gold" {
  function_name    = "silver_to_gold"
  role             = aws_iam_role.lambda_role.arn
  runtime          = "python3.12"
  handler          = "silver_to_gold.lambda_handler"
  filename         = "C:/Users/Administrator/data-engineering-final-project/terragrunt/env/dev/lambda/silver_to_gold.zip"
  source_code_hash = filebase64sha256("C:/Users/Administrator/data-engineering-final-project/terragrunt/env/dev/lambda/silver_to_gold.zip")

  environment {
    variables = {
      SILVER_BUCKET = var.silver_bucket_name
      GOLD_BUCKET   = var.gold_bucket_name
    }
  }
}

# IAM პოლიტიკა Lambda-ისთვის (S3 და CloudWatch წვდომა)
resource "aws_iam_policy" "lambda_s3_access" {
  name        = "lambda_s3_access"
  description = "Allows Lambda to read from S3 and write logs to CloudWatch"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:ListBucket"
        ]
        Effect   = "Allow"
        Resource = [
          "arn:aws:s3:::${var.bronze_bucket_name}",
          "arn:aws:s3:::${var.bronze_bucket_name}/*",
          "arn:aws:s3:::${var.silver_bucket_name}",
          "arn:aws:s3:::${var.silver_bucket_name}/*",
          "arn:aws:s3:::${var.gold_bucket_name}",
          "arn:aws:s3:::${var.gold_bucket_name}/*"
        ]
      },
      {
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Effect   = "Allow"
        Resource = "arn:aws:logs:*:*:*"
      }
    ]
  })
}

# IAM პოლიტიკის მიბმა Lambda როლზე
resource "aws_iam_role_policy_attachment" "lambda_s3_attach" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = aws_iam_policy.lambda_s3_access.arn
}

# AWS Lambda-სთვის CloudWatch-ის მხარდაჭერის დამატება
resource "aws_iam_role_policy_attachment" "lambda_basic_execution" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}
