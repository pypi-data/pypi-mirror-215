import boto3

from pipebuilder.core import core as pbcore


def bucket_key_from_docpath(docpath):
    full_path = docpath.split('//')[-1]
    bucket_name = full_path.split('/')[0]
    key = '/'.join(full_path.split('/')[1:])
    return bucket_name, key


def get_s3_client():
    return boto3.client('s3')

def get_objects_from_s3(s3, bucket_name, prefix=None):
    kwargs = {'Bucket': bucket_name}
    if prefix:
        kwargs['Prefix'] = prefix
    kwargs['MaxKeys'] = 1000  # maximum number of objects to retrieve in one API call
    return s3.list_objects_v2(**kwargs)

def filter_and_format_files(result, bucket_name, start=None, end=None, s3_client=None, prefix=None):
    files_list=[]
    s3 = s3_client() if s3_client else get_s3_client()
    kwargs = {'Bucket': bucket_name, 'MaxKeys': 1000}
    if prefix:
        kwargs['Prefix'] = prefix
    while True:
        for content in result.get("Contents"):
            last_modified = content.get("LastModified")
            if start and last_modified < start:
                continue
            if end and last_modified > end:
                continue
            if content.get("Key")[-1] != '/':
                files_list.append("s3://{}/{}".format(bucket_name, content.get("Key")))
        if not result.get("IsTruncated"):
            break
        kwargs['ContinuationToken'] = result.get("NextContinuationToken")
        result = s3.list_objects_v2(**kwargs)
    return files_list

def list_docs(docpath, prefix=None, start=None, end=None, 
              s3_client=get_s3_client, 
              get_date_func=pbcore.get_date,
              filter_func=filter_and_format_files):
    s3 = s3_client()  
    bucket_name, prefix = bucket_key_from_docpath(docpath)
    if start:
        start = get_date_func(start, output='datetime')
    if end:
        end = get_date_func(end, output='datetime')

    result = get_objects_from_s3(s3, bucket_name, prefix)
    # Done by Doug for temporary fix. Must return empty list if no files.
    if not result.get("Contents"):
        return []
    return filter_func(result, bucket_name, start, end, s3, prefix)