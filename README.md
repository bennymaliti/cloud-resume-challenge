# Cloud Resume Challenge - AWS

This repository contains my implementation of the [Cloud Resume Challenge](https://cloudresumechallenge.dev/docs/the-challenge/aws/) by Forrest Brazeal. The project demonstrates cloud engineering skills by building a serverless resume website on AWS with CI/CD pipelines.

## 🏆 Challenge Completion

This project completes all 16 steps of the Cloud Resume Challenge:

✅ **1. Certification** - AWS Certified Solutions Architect Associate & Developer Associate  
✅ **2. HTML** - Semantic HTML5 resume  
✅ **3. CSS** - Modern, responsive styling  
✅ **4. Static Website** - Hosted on Amazon S3  
✅ **5. HTTPS** - Secured with CloudFront  
✅ **6. DNS** - Custom domain with Route 53  
✅ **7. JavaScript** - Visitor counter functionality  
✅ **8. Database** - DynamoDB for counter storage  
✅ **9. API** - API Gateway REST API  
✅ **10. Python** - Lambda function with boto3  
✅ **11. Tests** - Pytest unit tests with >90% coverage  
✅ **12. Infrastructure as Code** - AWS SAM & Terraform  
✅ **13. Source Control** - Git & GitHub  
✅ **14. CI/CD (Backend)** - GitHub Actions for Lambda deployment  
✅ **15. CI/CD (Frontend)** - GitHub Actions for S3/CloudFront updates  
✅ **16. Blog Post** - [Link to blog post]  

## 🏗️ Architecture

```
┌─────────────┐
│   Route 53  │
└──────┬──────┘
       │
┌──────▼────────┐
│  CloudFront   │ (HTTPS, CDN)
└──────┬────────┘
       │
┌──────▼────────┐
│   S3 Bucket   │ (Static Website)
└───────────────┘

┌─────────────────────────────────────┐
│           Visitor Counter           │
├─────────────────────────────────────┤
│ JavaScript → API Gateway → Lambda   │
│                    ↓                │
│                DynamoDB              │
└─────────────────────────────────────┘
```

## 🚀 Live Demo

- **Website**: [https://bennymaliti.co.uk](https://bennymaliti.co.uk)
- **API Endpoint**: [API Gateway URL]

## 📁 Project Structure

```
cloud-resume-challenge/
├── frontend/
│   ├── index.html          # Resume HTML
│   ├── styles.css          # Styling
│   ├── script.js           # Visitor counter JS
│   └── .github/
│       └── workflows/
│           └── frontend-cicd.yml
├── backend/
│   ├── lambda_function.py         # Python Lambda handler
│   ├── test_lambda_function.py    # Pytest tests
│   ├── template.yaml              # AWS SAM template
│   ├── requirements.txt           # Python dependencies
│   └── .github/
│       └── workflows/
│           └── backend-cicd.yml
├── terraform/                     # Alternative IaC
│   ├── main.tf
│   ├── variables.tf
│   ├── dynamodb.tf
│   ├── lambda.tf
│   ├── api_gateway.tf
│   ├── s3_cloudfront.tf
│   └── outputs.tf
└── README.md
```

## 🛠️ Technologies Used

### Frontend
- HTML5, CSS3, JavaScript (ES6+)
- Amazon S3 (Static Website Hosting)
- Amazon CloudFront (CDN, HTTPS)
- Route 53 (DNS)

### Backend
- Python 3.11
- AWS Lambda
- Amazon API Gateway
- Amazon DynamoDB
- boto3 (AWS SDK for Python)

### Infrastructure as Code
- AWS SAM (Serverless Application Model)
- Terraform (Alternative)

### CI/CD & DevOps
- GitHub Actions
- AWS CLI
- Pytest (Testing)
- Git Version Control

## 📋 Prerequisites

To deploy this project, you need:

1. **AWS Account** with appropriate permissions
2. **AWS CLI** configured with credentials
3. **SAM CLI** installed
4. **Python 3.11+** installed
5. **Git** installed
6. **GitHub Account** for CI/CD

### AWS Certifications (recommended)
- AWS Certified Cloud Practitioner
- AWS Certified Solutions Architect - Associate
- AWS Certified Developer - Associate

## 🚀 Deployment Instructions

### Option 1: Using AWS SAM (Recommended)

#### Backend Deployment

1. **Install dependencies**:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Run tests**:
   ```bash
   pytest test_lambda_function.py -v --cov=lambda_function
   ```

3. **Build SAM application**:
   ```bash
   sam build
   ```

4. **Deploy to AWS**:
   ```bash
   sam deploy --guided
   ```

5. **Note the API Gateway URL** from the outputs

#### Frontend Deployment

1. **Update API endpoint** in `frontend/script.js`:
   ```javascript
   const config = {
       apiEndpoint: 'YOUR_API_GATEWAY_URL'
   };
   ```

2. **Create S3 bucket** (if not exists):
   ```bash
   aws s3 mb s3://your-resume-bucket-name
   ```

3. **Upload files to S3**:
   ```bash
   cd frontend
   aws s3 sync . s3://your-resume-bucket-name/ --exclude ".git/*"
   ```

4. **Create CloudFront distribution** (see AWS Console)

5. **Configure Route 53** for custom domain

### Option 2: Using Terraform

1. **Initialize Terraform**:
   ```bash
   cd terraform
   terraform init
   ```

2. **Create `terraform.tfvars`**:
   ```hcl
   s3_bucket_name = "your-unique-bucket-name"
   domain_name    = "your-domain.com"  # Optional
   ```

3. **Plan deployment**:
   ```bash
   terraform plan
   ```

4. **Apply configuration**:
   ```bash
   terraform apply
   ```

5. **Note outputs**:
   ```bash
   terraform output
   ```

## ⚙️ CI/CD Setup

### GitHub Secrets Configuration

Add these secrets to your GitHub repository:

#### For OpenID Connect (Recommended)
- `AWS_ROLE_ARN`: IAM role ARN for GitHub Actions

#### For IAM User (Alternative)
- `AWS_ACCESS_KEY_ID`: Your AWS access key
- `AWS_SECRET_ACCESS_KEY`: Your AWS secret key

### GitHub Actions Workflows

1. **Backend CI/CD** (`.github/workflows/backend-cicd.yml`):
   - Runs tests on push/PR
   - Deploys to AWS on merge to main
   - Includes security scanning

2. **Frontend CI/CD** (`.github/workflows/frontend-cicd.yml`):
   - Validates HTML/CSS
   - Syncs to S3
   - Invalidates CloudFront cache
   - Runs Lighthouse performance audit

## 🧪 Testing

### Backend Tests

Run unit tests:
```bash
cd backend
pytest test_lambda_function.py -v
```

Run with coverage:
```bash
pytest test_lambda_function.py -v --cov=lambda_function --cov-report=html
```

### Frontend Tests

Validate HTML:
```bash
npm install -g html-validator-cli
html-validator --file=frontend/index.html
```

## 📊 Monitoring

### CloudWatch Metrics
- Lambda invocations and errors
- API Gateway 4xx/5xx errors
- DynamoDB read/write metrics

### CloudWatch Alarms
- Lambda error rate > 5 in 5 minutes
- API Gateway 5xx errors

### CloudWatch Logs
- Lambda function logs: `/aws/lambda/prod-VisitorCounterFunction`

## 💰 Cost Optimization

This project uses AWS Free Tier eligible services:

- **S3**: First 5GB free
- **CloudFront**: 1TB data transfer/month
- **Lambda**: 1M requests/month, 400K GB-seconds
- **DynamoDB**: 25GB storage, 25 RCU/WCU
- **API Gateway**: 1M API calls/month

Expected monthly cost: **$0-5** (within Free Tier)

## 🔒 Security Best Practices

- ✅ S3 bucket with public access blocked
- ✅ CloudFront Origin Access Identity
- ✅ HTTPS enforced via CloudFront
- ✅ IAM roles with least privilege
- ✅ DynamoDB encryption at rest
- ✅ API Gateway throttling enabled
- ✅ No hardcoded credentials
- ✅ CloudWatch logging enabled

## 📝 API Documentation

### Visitor Counter Endpoint

**Endpoint**: `POST /visitor-count`

**Request**:
```bash
curl -X POST https://your-api-gateway-url/prod/visitor-count
```

**Response**:
```json
{
  "count": 42,
  "message": "Visitor count updated successfully"
}
```

**Error Response**:
```json
{
  "error": "Failed to update visitor count",
  "message": "Error details"
}
```

## 🐛 Troubleshooting

### Common Issues

1. **CORS Errors**:
   - Ensure API Gateway has CORS enabled
   - Check Lambda response headers

2. **CloudFront not serving latest content**:
   - Create cache invalidation
   - Check S3 bucket policy

3. **Lambda timeout**:
   - Increase timeout in SAM template
   - Check DynamoDB connection

4. **CI/CD failures**:
   - Verify AWS credentials
   - Check IAM permissions

## 🎯 Future Enhancements

- [ ] Add contact form with SES
- [ ] Implement dark mode toggle
- [ ] Add blog section with S3 + CloudFront
- [ ] Multi-region deployment
- [ ] Add WAF for security
- [ ] Implement custom metrics
- [ ] Add internationalization (i18n)

## 📚 Resources

- [Cloud Resume Challenge](https://cloudresumechallenge.dev)
- [AWS SAM Documentation](https://docs.aws.amazon.com/serverless-application-model/)
- [Terraform AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [GitHub Actions AWS](https://github.com/aws-actions)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Benny Maliti**
- LinkedIn: [bennymaliti](https://www.linkedin.com/in/bennymaliti)
- GitHub: [@bennymaliti](https://github.com/bennymaliti)
- Website: [bennymaliti.co.uk](https://bennymaliti.co.uk)

## 🙏 Acknowledgments

- Forrest Brazeal for creating the Cloud Resume Challenge
- The AWS community for excellent documentation
- All the cloud engineers who shared their implementations

---

⭐ If you found this helpful, please star the repository!
# Test CI/CD
