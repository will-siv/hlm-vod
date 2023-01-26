#!/bin/python3

import json
import csv
import urllib.request as urllib2
from graphqlclient import GraphQLClient
import codecs

def multi_split(p):
    if len(p) == 1:
        return p[0]["gamerTag"]
    else:
        LIST = []
        for item in p:
            LIST.append(item["gamerTag"])
        return ', '.join(LIST)
    return


authToken = '8873657796a5e72312e6a87535029012'
slug = 'd-i-those-4'

apiVersion = 'alpha'

client = GraphQLClient("https://api.start.gg/gql/" + apiVersion)
client.inject_token("Bearer " + authToken)

result = client.execute('''
query infoFromSlug($slug: String!) {
  tournament(slug:$slug) {
    name
    events {
      id
      phaseGroups {
        id
        sets(
          perPage: 256,
          page: 1
        ) {
          pageInfo {
            total
          }
          nodes {
            id
            stream {
              streamName
            }
            fullRoundText
            slots{
              id
              entrant {
                participants {
                  gamerTag
                }
              }
            }
          }
        }
      }
    }
  }
}

''',
{
    "slug":slug
}
)

resData = json.loads(result)

tournament = resData['data']['tournament']
streamedGames = []
streamedTitles = []

for event in tournament['events']:
    for phaseGroup in event['phaseGroups']:
        for node in phaseGroup['sets']['nodes']:
            if node['stream'] != None:
                streamedGames.append(node)
            if node['fullRoundText'] == 'Grand Final Reset':
                streamedGames.pop()

# {tournament} - {P1} VS {P2} - {round}
for node in streamedGames:
    title = "{P1} VS {P2} - {_round} | {name}"
    title = title.format(
        name=tournament['name'],
        P1=multi_split(node['slots'][0]['entrant']['participants']),
        P2=multi_split(node['slots'][1]['entrant']['participants']),
        _round=node['fullRoundText']
    )
    streamedTitles.append(title)
    print(title)

print("Recorded Games: " + str(len(streamedGames)))
