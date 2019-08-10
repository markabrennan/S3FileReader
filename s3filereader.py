import boto3


class S3FileReader:
    """
    class S3FileReader:
    Class to encapsulate boto3 calls to access
    an S3 resource and allow clients to stream
    the contents of the file iteratively, via a
    generator function: __iter__()
    """
    def __init__(self, cfg, bucket, resource_key):
        """
        __init__(self, cfg, bucket, resource_name):
        S3FileReader constructor initializes the S3
        Session, gets the resource for a given bucket
        and key, obtains the resource's object,
        and obtains a handle to the object.
        Params:
            cfg: config.py file containing S3 crexentials
            bucket: name of the S3 bucket to access
            resource_key: key of the S3 resource (file name)
        """
        self._session = boto3.Session(
            aws_access_key_id=cfg.aws_access_key_id,
            aws_secret_access_key=cfg.aws_secret_access_key)

        self._resource = self._session.resource('s3')
        self._object = self._resource.Object(bucket, resource_key)
        self._handle = self._object.get()

    def __iter__(self):
        """
        __iter__(self):
        Provide iteration interface to clients. Get the
        stream of our S3 object handle and produce results lazily
        for our clients from a generator function.

        yield statement yields a single line from the file.

        Returns:  nothing.  A StopIteration exception is implicitly
        raised following the completion of the for loop.
        """
        stream = self._handle['Body']
        for line in stream:
            yield line
