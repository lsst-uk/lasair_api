## Alert Streams

```eval_rst
.. todo::

    - Flesh out how to use the alert streams ... text below is from old pages
```

By providing Kafka streams, Lasair provides a machine-readable packet of data that can cause action at your site. See the FAQ article on how to create a stream using the Lasair web environment. This page is about how to read it on your side. There is a [blog post](https://roywilliams.github.io/writing/streaming_data.html) about why Kafka is a good way to deal with streaming data.

*   We recommend [Confluent Kafka](https://pypi.org/project/confluent-kafka/), the python install being "pip install confluent\_kafka".
*   You will be connecting to kafka.lsst.ac.uk on port 9092
*   For coding details, please see the [accompanying notebook](https://colab.research.google.com/drive/1sV-JGzzVdZrP86P1tGu-naUQcMSSXAi7?usp=sharing).

You will need to understand two concepts: Topic and GroupID. The Topic is a string to identify which stream of alerts you want, which derives from the name of a Lasair streaming query. For example, the query defined [here](https://lasair-ztf.lsst.ac.uk/query/2/) is named "SN-like candidates", and its output collected [here](https://lasair-ztf.lsst.ac.uk/streams/lasair_2SN-likecandidates/). Its Kafka topic is "lasair\_2SN-likecandidates". The GroupID tells Kafka where to start delivery to you. It is just a string that you can make up, for example "Susan3456". The Kafka server remembers which GroupIds it has seen before, and which was the last alert it delivered. When you start your code again with the same GroupID, you only get alerts that arrived since last time you used that GroupId. If you use a new GroupID, you get the alerts from the start of the Kafka cache, which is about 7 days.


