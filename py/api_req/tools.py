#!/bin/python3

import json
import csv
import urllib.request as urllib2
from graphqlclient import GraphQLClient

def multi_split(p):
    if len(p) == 1:
        return p[0]["gamerTag"]
    else:
        LIST = []
        for item in p:
            LIST.append(item["gamerTag"])
        return ', '.join(LIST)
    return


with open("token.txt", "r") as r:
    authToken = r.read().replace("\n" , "")
try:
    slug = sys.argv[1]
except IndexError:
    slug = "hlm"

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
streamedGames = dict()
streamedTitles = []

for event in tournament['events']:
    for phaseGroup in event['phaseGroups']:
        for node in phaseGroup['sets']['nodes']:
            if node['stream'] != None:
                streamName = node['stream']['streamName']
                if streamName in streamedGames:
                    streamedGames[streamName].append(node)
                else:
                    streamedGames[streamName] = [node]
            if node['fullRoundText'] == 'Grand Final Reset':
                streamedGames.pop()

totalGames = 0
games = 0

# {tournament} - {P1} VS {P2} - {round}
for streamName in streamedGames:
    print(streamName + ":")
    games = 0
    for node in streamedGames[streamName]:
        title = "{P1} VS {P2} - {_round} | {name}"
        title = title.format(
            name=tournament['name'],
            P1=multi_split(node['slots'][0]['entrant']['participants']),
            P2=multi_split(node['slots'][1]['entrant']['participants']),
            _round=node['fullRoundText']
        )
        streamedTitles.append(title)
        print(title)
        games += 1
        totalGames += 1
    print("Recorded Games: {games}\n".format(games=games))

print("Total Recorded Games: " + str(totalGames))
