--------------------------------
Step by step installation guide
--------------------------------

Before starting, make sure you have Python 2.7 installed on your system or otherwise install.

1)	Download, install and start Couchbase Server.

At this point you should have Couchbase Server running at your system.
Point your browser at http://localhost:8091 and configure the server.

2)	Install Elasticsearch

3)	Download, install and configure Couchbase transport plugin for Elasticsearch

4)	Create an Elasticsearch index
> curl -XPUT http://localhost:9200/index_name

You can find detailed guides for Elasticsearch in the [official site](http://www.elasticsearch.org/).

5)	Create a   Cross-datacenter Replication  (xdcr) between your Couchbase bucket and your Elasticsearch index. In order to do that you can follow the instructions on the plugin's site [here](https://github.com/couchbaselabs/elasticsearch-transport-couchbase)
You only need to follow the instructions regarding creating xdcr from Couchbase admin interface.

6)	Create a facebook application and get an application access token. You will need this for the facebook data retrieval script. 

7)	Create a twitter application. 

8)	Install the requirements from [here](UIapp/requirements.txt)
> sudo pip install -r requirements.txt

9)	Inside UIapp folder run 
> python manage.py runserver 0.0.0.0:8000 &


Anlzer is ready to be accessed from its web interface at http://localhost:8000

Enjoy!
