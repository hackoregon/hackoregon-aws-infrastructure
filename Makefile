S3BUCKET = "hacko-infrastructure-cfn"

datascience:
	@echo "Packaging and deploying the SageMaker Data Science Environment";
	cd sagemaker && aws cloudformation package \
		--s3-bucket $(S3BUCKET) \
		--s3-prefix sagemaker \
		--template sagemaker.yaml \
		--output-template-file sagemaker.out.yaml;
	cd sagemaker && aws cloudformation deploy \
	  --template-file sagemaker.out.yaml \
		--stack-name DataScienceLab \
		--capabilities CAPABILITY_NAMED_IAM;
