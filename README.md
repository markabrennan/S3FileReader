# S3FileReader
This simple class encapsulates the boto3 library calls needed to obtain a S3 resource
and be able to stream the contents of a file.

This class was developed primarily as a way to demonstrate the utility of generator
functions and the interation interface, motivated by a real-world example.  Most
discussions of generators involve trivial and contrived loops yielding values, which
I always found confusing, as such examples failed (at least for me) to crystallize the 
primary use of generators, which is to provide lazy production of data, thereby saving
memory and compute resources.

Previously I had only worked with the boto3 "download" API call, which, though useful, 
downloads the entire contents of a file to the working directory of the running script.
This is all well and good if you run your script in a Docker container on an EC2 instance,
but I wanted the flexibility to be able to interact with S3 data on my MacBook Air, without
needing to download files.

boto3 allows clients to obtain a file object, and then get a handle to the "body" of the object - 
essentially a stream.  Streams should be iterable, so I wrap the iteration of the s3 file
stream in a generator function.  This functionality is in turn wrapped in the S3FileReader
class, which provides an __iter__ method for clients to iterate over a concrete S3FileReader
object they have instantiated.

## TO DO

Add an optional filter predicate to the constructor, to be used when iterating
over the stream, allowing clients to filter the stream up-front, before handling the data.
