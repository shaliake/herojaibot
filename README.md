# WAP žaidimo Herojai.net veiksmų automatas
Herojai.net žaidime veikiantis robotas, atliekantis tam tikrus veiksmus automatiškai.

Ši biblioteka veikia žaidime herojai.net, tačiau jeigu analogiškas žaidimo skriptas paleistas kitur, jį galima konfigūruoti.

Norint pakeisti kur veikia automatas, importuojame roboto modulį ir pakeičiame šiuos kintamuosius
```python
import herojaibot
herojaibot.baseUrl = "https://herojai.net/server1"
herojaibot.questionsAndAnswersSource = "https://herojai.net/server1/viktorinos_klausimai.txt"
```

Robotui veikti, reikia privačių prisijungimo duomenų, užtenka tik md5 šifruotos teksto eilutės
```python
herojaibot.users = {"veikejas1": "veikejoPrisijungimoPaslaptis",
         "veikejas2": "veikejoPrisijungimoPaslaptis",
         "veikejas3": "veikejoPrisijungimoPaslaptis",
         "veikejas4": "veikejoPrisijungimoPaslaptis"}
```
Ši robotą pravartu naudoti kelioms paskyroms iš karto, tad kad nesusietų kiti žaidėjai per viešai prieinamą informaciją Jūsų paskyrų
ir nepraneštų - galima naudoti skirtingus naršyklės agentus. Šių agentų gali būti kiek naudosite paskyrų ar mažiau. Jų naudojimasis pasimatys tolimesniame konfigūracijos etape
```python
herojaibot.user_agents = {
    "SGS9": "Mozilla/5.0 (Linux; Android 8.0.0; SM-G960F Build/R16NW) Chrome/62.0.3202.84 Mobile Safari/537.36",
    "macOS": "Chrome/96.0.4664.93 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko)",
    "X11": "(X11; Linux x86_64; rv:95.0) Gecko/20100101 Firefox/95.0",
    "iPhone": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_8_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1"
}
```

Šis automatas turi dvi funkcijas - auto kovojimą ir viktorinos klausimų įveikimą. Norint vykdyti kovas jums reikia užpildyti veikėjų konfigūracijos masyvą
```python
herojaibot.tasks = [
    {'name': 'veikejas1',
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
     }}]
```

| Kintamasis        | Reikšmė           | Paaiškinimas  |
| ------------- |:-------------:| -----:|
|name      | string | Veikėjo vardas, pagal kurį bus paimta md5 prisijungimo paslaptis iš herojaibot.users žodyno |
|resources     | dict      |   Žodynas,kuriame fiksuojami kovų metu surinkti resursai ir įveiktos misijos. Šis žodynas privalo turėti XP, Kovų, Misijų žodyno reikšmes, vėliau dinamiškai papildomos randant kažką nestandartiško kovų metu |
|agent | string    |    Privaloma reikšmė, pagal ją bus paimtas narškyklės agentas iš herojaibot.agents |
|imin | int    |    Kovų metu gali būti priešų nuo 1 iki 6. Ši reikšmė nusako, kurį priešą pasirinkti puolimo metu atsitikinai (nuo) (minimali vertė 1) |
|imax | int    |    Kovų metu gali būti priešų nuo 1 iki 6. Ši reikšmė nusako, kurį priešą pasirinkti puolimo metu atsitikinai (iki) (minimali vertė 6) |
|target | dict    |   Žodynas apibrėžiantis: i,j,k koordinatės kovų vietovės, cooldown kiek laiko laukti po kovos |
|mission | dict    |   Žodynas apibrėžiantis: i,j,k koordinatės misijos vykdymo vietovės, taskGiver koks npc duoda misiją |


Norint kovoti tik kartą ar integruoti kovos veiksmą pačiam galime kviesti metodą fight:


```python
herojai.botfight(character: 'veikejoPaslaptis', resources: {
         'XP': 0,
         'Kovų': 0,
         'Misijų': 0
     }, agent: "Mozilla/5.0 (Linux; Android 8.0.0; SM-G960F Build/R16NW) Chrome/62.0.3202.84 Mobile Safari/537.36",
     imin: 1, imax: 6, i: "vietovei", j: "vietovej", k: "vietovek", cooldown: 0,
          mi: "vietovemi, mj: "vietovemj", mk: "vietovemk", mm: "uzduoties npc")
```
Šio metodo reikšmių aprašymas atitinka aukščiau pateiktą reikšmių lentelę


Norint, kad veikėjas kovotų neribotą laiką galima kviesti:
```python
herojaibot.single_auto_fight(herojaibot.tasks[0])
```


Norint, kad veikėjai kovotų neribotą laiką galima kviesti(herojaibot.tasks privalo būti sukonfigūruotas prieš tai):
```python
herojaibot.parallel_auto_fight()
```


Norint, kad robotas atsakytų į viktorinos klausimą svarbu prieš tai užpildyti "žinių" bazę:
```python
herojaibot.init_qa()
```
Šis kvietinys parsiųs klausimus ir atsakymus iš sukonfigūruoto šaltinio ir atsakinės pagal jį.

Atsakyti į vieną klausimą:
```python
herojaibot.answer_question('veikejopaslaptis')
```

Atsakinėti į klausimus iki proceso sustabdymo:
```python
herojaibot.single_auto_answer('veikejopaslaptis')
```


**Visos užduotys, kurios vyksta be pabaigos vykdomos iki proceso pabaigos, o užduočių vykdymo progreso ataskaita spausdinima terminal output.
 Norint perkeltį ataskaitas kitur, reikia nukreipti output.**




