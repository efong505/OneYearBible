import boto3

def invalidate_cloudfront():
    """Invalidate CloudFront cache for updated files"""
    try:
        cloudfront = boto3.client('cloudfront')
        
        # Replace with your CloudFront distribution ID
        distribution_id = 'E1234567890123'  # You'll need to replace this with your actual distribution ID
        
        response = cloudfront.create_invalidation(
            DistributionId=distribution_id,
            InvalidationBatch={
                'Paths': {
                    'Quantity': 2,
                    'Items': [
                        '/index.html',
                        '/assets/js/calendar.js'
                    ]
                },
                'CallerReference': str(hash('invalidation-' + str(boto3.Session().region_name)))
            }
        )
        
        print(f"Invalidation created: {response['Invalidation']['Id']}")
        return True
        
    except Exception as e:
        print(f"Error creating invalidation: {e}")
        print("You may need to manually invalidate the CloudFront cache for:")
        print("- /index.html")
        print("- /assets/js/calendar.js")
        return False

if __name__ == "__main__":
    invalidate_cloudfront()