import boto3

def lambda_handler(event, context):
    stopCount = 0
    keepaliveCount = 0
    totalCount = 0

    client = boto3.client('sagemaker')
    notebooks = client.list_notebook_instances(MaxResults=100)['NotebookInstances']
    totalCount = len(notebooks)
    print('Found %s Notebook Instances' % totalCount)

    for notebook in notebooks:
        tags = client.list_tags(ResourceArn=notebook['NotebookInstanceArn'])['Tags']
        if notebook['NotebookInstanceStatus'] != 'Stopped':
            keepalive = has_keepalive(tags)
            if keepalive:
                keepaliveCount += 1
                print('Keeping notebook %s alive' % notebook['NotebookInstanceName'])
            else:
                print('Stopping a notebook %s' % notebook['NotebookInstanceName'])
                stopCount += 1
                client.stop_notebook_instance(NotebookInstanceName=notebook['NotebookInstanceName'])

    return { 'stopped': stopCount, 'kept': keepaliveCount, 'total': totalCount }

def has_keepalive(tags):
    for tag in tags:
        if tag['Key'] == 'keepalive' and tag['Value'] == 'true':
            return True
    return False