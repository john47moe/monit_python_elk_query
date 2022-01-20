import json
import elasticsearch
from elasticsearch import Elasticsearch
domain_name=['raindrop.best', 'www.raindrop.best']

elastic_conn = Elasticsearch(hosts=["http://localhost:9200/"],http_auth=('elastic','!QAZ2wsx#EDC'))
#this will query the last 60 mins data. If you need to increase or decrese the threashold modify "gt": "now-60m" --> "gt": "now-70m", as required 
query_body = {
      "query": {
        "bool": {
          "must": {
            "term":  { "err_severity": "error"  }

          },
          "filter": {
            "range": {
              "@timestamp": {
                "gte": "now-60m"
              }
            }
          }

        }
    },
 "sort": [
   {
     "server.keyword": {
       "order": "asc"
     }
   }
 ]

}
res = elastic_conn.search(index="error-log*", body=query_body,size=999)
if res:
#       print 'error_count | ',res['hits']['total']['value']
        for i in res['hits']['hits']:
                if 'server' in i['_source'] and i['_source']['server'] in domain_name:
                        print i['_source']['server'],i['_source']['client_ip'],i['_source']['err_message'][:45]
