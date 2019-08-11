import boto3


class S3FileReader:
    """
    class S3FileReader:
    Class to encapsulate boto3 calls to access an S3 resource
    and allow clients to stream the contents of the file iteratively,
    via a generator function: __iter__()
    """

    def __init__(self, cfg, resource_key, bucket=None):
        """
        __init__(self, cfg, bucket, resource_name):
        S3FileReader constructor initializes the S3 Session,
        gets the resource for a given bucket and key,
        obtains the resource's object, and obtains a handle to the object.
        Params:
            cfg: config.py file containing S3 crexentials
            bucket: name of the S3 bucket to access
            resource_key: key of the S3 resource (file name)
        """

        try:
            if not bucket:
                bucket = cfg.bucket

            self._session = boto3.Session(
                aws_access_key_id=cfg.aws_access_key_id,
                aws_secret_access_key=cfg.aws_secret_access_key)

            self._resource = self._session.resource('s3')
            self._object = self._resource.Object(bucket, resource_key)
            self._handle = self._object.get()

        except Exception:
            raise S3FileReaderException('Failed to initialize S3 resources!')

    def __iter__(self):
        """
        __iter__(self):
        Provide iteration interface to clients. Get the stream of our
        S3 object handle and produce results lazily for our clients
        from a generator function.

        yield statement yields a single line from the file.

        Returns:  nothing.  A StopIteration exception is implicitly
        raised following the completion of the for loop.
        """

        if not self._handle:
            raise S3FileReaderException('No S3 object handle!')

        stream = self._handle['Body']
        for line in stream:
            yield line

    def __enter__(self):
        """
        __enter__(self):
        Implement Python's context management protocol
        so this class can be used in a "with"  statement.
        """

        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        """
        __exit__(self, exc_type, exc)_value, exc_tb):
        Implement Python's context management protocol
        so this class can be used in a "with" statement.
        If exc_type is not None, then we are handling an
        exception and for safety should delete our resources
        """

        if exc_type is not None:
            del self._session
            del self._resource
            del self._object
            del self._handle

            return False

        else:  # normal exit flow
            return True


class S3FileReaderException(Exception):
    """
    class S3FileReaderException(Exception):
    Simple exception class to use if we can't get an S3
    File handle, or otherwise have an exception when
    dealing with S3.
    """

    def __init(self, msg):
        self.msg = msg
