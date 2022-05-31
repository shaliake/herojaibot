import urllib.request
import requests
import re
import time
import random
from threading import Thread

baseUrl = "https://herojai.net/server1"
questionsAndAnswersSource = "https://herojai.net/server1/viktorinos_klausimai.txt"
questionsAndAnswers = {}
questionAnswerDelay = 20.1
users = {"waha": "Xgh7YkmrOHmlBvSVjMGD",
         "crazy": "u6FcsNVRZd0jyYXR6imt",
         "paparacas": "uuYaLIBcxr593efGyYXK",
         "fanatikas": "AabhuoJyg7pbiOmR8BiK"}
user_agents = {
    "SGS9": "Mozilla/5.0 (Linux; Android 8.0.0; SM-G960F Build/R16NW) Chrome/62.0.3202.84 Mobile Safari/537.36",
    "macOS": "Chrome/96.0.4664.93 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko)",
    "X11": "(X11; Linux x86_64; rv:95.0) Gecko/20100101 Firefox/95.0",
    "iPhone": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_8_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1"
}
tasks = [
    {'name': 'waha',
     'resources': {
         'XP': 0,
         'Kovų': 0,
         'Misijų': 0
     },
     'agent': "X11",
     'imin': 6,
     'imax': 6,
     'target': {
         'i': "tamsybiu_salis",
         'j': "ismires_miestas",
         'k': "miesto_pakrastys",
         'cooldown': 0
     },
     'mission': {
         'i': "tamsybiu_salis",
         'j': "ismires_miestas",
         'k': "miesto_sodai",
         'taskGiver': "ylthana"
     }},
    {'name': 'paparacas',
     'resources': {
         'XP': 0,
         'Kovų': 0,
         'Misijų': 0
     },
     'agent': "SG9",
     'imin': 6,
     'imax': 6,
     'target': {
         'i': "tamsybiu_salis",
         'j': "ismires_miestas",
         'k': "miesto_sodai",
         'cooldown': 0
     },
     'mission': {
         'i': "tamsybiu_salis",
         'j': "ismires_miestas",
         'k': "miesto_pakrastys",
         'taskGiver': "nebirosas"
     }},
    {'name': 'fanatikas',
     'resources': {
         'XP': 0,
         'Kovų': 0,
         'Misijų': 0
     },
     'agent': "iPhone",
     'imin': 6,
     'imax': 6,
     'target': {
         'i': "tamsybiu_salis",
         'j': "legendiniu_kovotju_slenis",
         'k': "riteriu_rumai",
         'cooldown': 0
     },
     'mission': {
         'i': "tamsybiu_salis",
         'j': "legendiniu_kovotju_slenis",
         'k': "valdovu_slenis",
         'taskGiver': "brandas"
     }},
    {'name': 'crazy',
     'resources': {
         'XP': 0,
         'Kovų': 0,
         'Misijų': 0
     },
     'agent': "macOS",
     'imin': 6,
     'imax': 6,
     'target': {
         'i': "siaubunu_zeme",
         'j': "pavoju_krastas",
         'k': "drakonu_buveine",
         'cooldown': 0
     },
     'mission': {
         'i': "siaubunu_zeme",
         'j': "pavoju_krastas",
         'k': "numireliu_miestas",
         'taskGiver': "kasparas"
     }}
]


def fight(character: str, gathered_resources, agent: str, imin: int, imax: int, i: str, j: str, k: str, cooldown: float,
          mi: str, mj: str, mk: str, mm: str):
    headers = {"User-Agent": agent}
    m = random.randint(imin, imax)
    location_url = f'{baseUrl}/index.php?action=map&id={character}&i={i}&j={j}&k={k}'
    battle_url = f'{baseUrl}/index.php?action=nbattle&id={character}&i={i}&j={j}&k={k}'
    event_url = f'{baseUrl}/index.php?action=event&id={character}&i={i}&j={j}&k={k}&m={m}'
    mission_url = f'{baseUrl}/index.php?action=object&id={character}&i={mi}&j={mj}&k={mk}&m={mm}'
    fakeLog_url = f'{baseUrl}/index.php?id={character}'
    barakai_pickup_url = f'{baseUrl}/index.php?action=barakai&n=take&id={character}&server='
    requests.get(location_url, headers=headers)
    event = requests.get(event_url, headers=headers).text
    npc = re.findall('event\=(.*?)\"', event)
    resource = re.findall('J&#363;s radote (.*?)<\/b>', event)
    # Jei kova prasidėjo
    if len(npc) == 1:
        event_id = npc[0]
        npc_attack_url = f'{battle_url}&event={event_id}'
        event_response = requests.get(npc_attack_url, headers=headers).text
        battle = re.findall('event=(.*?)\"', event_response)
        battle_completed = re.findall('Gavote patirties: (.*?)<\/b>', event_response)
        on_cooldown = re.findall('<small>Gal&#279;site kovoti po: <span id=\"cnt\" style=\"color:red;\">(.*?)<\/span>',
                                 event_response)
        # Kovojimas
        while True:
            # Kovos eiga
            if len(battle) > 0:
                # Paimam 1 skeleta ant mesos
                requests.post(barakai_pickup_url, data={'unit': 'skeletonas', 'quan': 1}, headers=headers)
                requests.post(barakai_pickup_url, data={'unit': 'skeletonu_lankininkas', 'quan': 1}, headers=headers)
                requests.post(barakai_pickup_url, data={'unit': 'inirses_valstietis', 'quan': 1}, headers=headers)
                battle_details = re.findall('\d+', battle[0])
                event = battle_details[0]
                timeStamp = battle_details[1]
                npc_event_url = f'{battle_url}&event={event}&time={timeStamp}'
                event_response = requests.get(npc_event_url, headers=headers).text
                battle = re.findall('event=(.*?)\"', event_response)
                battle_completed = re.findall('Gavote patirties: (.*?)<\/b>', event_response)
            # Kovos pabaiga
            if len(battle_completed) == 1:
                # Paimam 1 skeleta ant mesos
                requests.post(barakai_pickup_url, data={'unit': 'skeletonas', 'quan': 1}, headers=headers)
                requests.post(barakai_pickup_url, data={'unit': 'skeletonu_lankininkas', 'quan': 1}, headers=headers)
                requests.post(barakai_pickup_url, data={'unit': 'valstietis', 'quan': 1}, headers=headers)
                gathered_resources['XP'] += float(battle_completed[0])
                gathered_resources['Kovų'] += 1
                battle_resource = re.findall('Gavote (.*?)<\/b>', event_response)
                if len(battle_resource) > 1:
                    battle_resource_values = battle_resource[1].split(' ')
                    battle_resource_amount = float(battle_resource_values[0])
                    battle_resource_name = battle_resource_values[1][:-1]
                    if gathered_resources.get(battle_resource_name) is None:
                        gathered_resources[battle_resource_name] = battle_resource_amount
                    else:
                        gathered_resources[battle_resource_name] = gathered_resources.get(
                            battle_resource_name) + battle_resource_amount
                print(f'Herojus: {character}\nSurinkta: {gathered_resources},'
                      f' XP vidutiniškai:{gathered_resources["XP"] / gathered_resources["Kovų"]:.2f}')
                # Misijos vykdymas, reikia prideti resursu
                missionStatusResponse = requests.get(mission_url, headers=headers).text
                # Fake log
                requests.get(fakeLog_url, headers=headers)
                if len(re.findall('J&#363;s &#303;vykd&#279;te u&#382;duot&#303;', missionStatusResponse)) > 0:
                    gold_reward = re.findall('Gavote (d+) aukso', missionStatusResponse)
                    xp_reward = re.findall('Gavote patirties: (d+)', missionStatusResponse)
                    if len(gold_reward) > 0:
                        if gathered_resources.get('aukso') is None:
                            gathered_resources['aukso'] = gold_reward[0]
                        else:
                            gathered_resources['aukso'] += gold_reward[0]
                        print(f'Misija davė:{gold_reward[0]} aukso')
                    if len(xp_reward) > 0:
                        if gathered_resources.get('XP') is None:
                            gathered_resources['XP'] = xp_reward[0]
                        else:
                            gathered_resources['XP'] += xp_reward[0]
                        print(f'Misija davė:{xp_reward[0]} XP')
                    gathered_resources['Misijų'] += 1
                else:
                    target = float(re.findall('Nu&#382;udyti (.*?) ', missionStatusResponse)[0])
                    current = float(
                        re.findall('<small>Esate nu&#382;ud&#281;: <b>(.*?)<\/b>', missionStatusResponse)[0])
                    print(f'Misijos atlikta: {(current / target) * 100:.2f} %')
                time.sleep(cooldown)
                break
            # Jei negali kovoti
            if len(on_cooldown) == 1:
                fightCooldown = float(on_cooldown[0]) + 0.1
                requests.get(fakeLog_url, headers=headers)
                # print(f'Herojus pavargęs {fightCooldown} s')
                time.sleep(fightCooldown)
                break
    # Zemelapio resursai
    if len(resource) == 1:
        resource_values = resource[0].split(' ')
        amount = float(resource_values[0])
        # Monstru tekstas gan prastas
        name = resource_values[1][:-1]
        if gathered_resources.get(name) is None:
            gathered_resources[name] = amount
        else:
            gathered_resources[name] = gathered_resources.get(name) + amount


def single_auto_fight(acc):
    while True:
        fight(users.get(acc['name']),
              acc['resources'],
              user_agents.get(acc['agent']),
              acc['imin'], acc['imax'],
              acc['target']['i'],
              acc['target']['j'],
              acc['target']['k'],
              acc['target']['cooldown'],
              acc['mission']['i'],
              acc['mission']['j'],
              acc['mission']['k'],
              acc['mission']['taskGiver'])


def parallel_auto_fight():
    for account in tasks:
        Thread(target=single_auto_fight, args=[account]).start()


def init_qa():
    for fileLine in urllib.request.urlopen(questionsAndAnswersSource):
        line = fileLine.decode('utf-8')
        lineValues = line.split('|')
        if len(lineValues) == 3:
            key = lineValues[0]
            value = lineValues[1]
            questionsAndAnswers[key] = value
    print(f'Paruošta klausimų:{len(questionsAndAnswers)}')


def answer_question(char):
    getQuestion = requests.get(f'{baseUrl}/viktorina.php?id={char}&nv=')
    questionMatch = re.findall('<div class="center"><small>(.*?)<br\/>', getQuestion.text)
    if len(questionMatch) >= 1:
        if "Ruo&#353;iamas kitas klausimas" not in questionMatch[0]:
            question = questionMatch[0]
            print(f'Gautas klausimas:{question}')
            answer = questionsAndAnswers.get(question).capitalize()
            print(f'Atsakymas:{answer}')
            if answer is not None:
                formdata = {"zinute": answer, "submit": "Ra%C5%A1yti+%3E"}
                submissionResult = re.findall('<b>(.*?)<\/b>',
                                              requests.post(f'{baseUrl}/viktorina.php?id={char}&nv=rasau',
                                                            formdata).text)
                if len(submissionResult) == 2:
                    spamDelay = float(submissionResult[1]) + 0.1
                    print(f'Spam apsauga:{spamDelay} s')
                    time.sleep(spamDelay)
                    return 0
                if submissionResult[0] == "&#381;inut&#279; &#303;ra&#353;yta":
                    print(f'Atsakymas įrašytas')
                    time.sleep(questionAnswerDelay)
                    return 1
                return 0
            else:
                sleepDuration = float(re.findall('<b>(.*?)<\/b>', questionMatch[0])[0]) + 0.1
                print(f'Ruosiamas klausimas:{sleepDuration} s')
                time.sleep(sleepDuration)
                return 0


def single_auto_answer(char):
    counter = 0
    while True:
        print(f'Atsakyta klausimų:{counter}')
        counter += answer_question(char)
