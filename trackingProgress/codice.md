# Private Dashboard

## Struttura Del Progetto
```sh
privateDashboard
├── dashboardWeb
│   ├── static
│   │   ├── css
│   │   │   └── custom.css
│   │   └── js
│   │       ├── charts_allenamento.js
│   │       ├── charts_dieta.js
│   │       ├── charts_home.js
│   │       ├── charts_misure.js
│   │       ├── charts_palestra.js
│   │       ├── charts_smartwatch.js
│   │       ├── db.js
│   │       └── nav.js
│   ├── allenamento.html
│   ├── dieta.html
│   ├── home.html
│   ├── misure.html
│   ├── nav.html
│   ├── palestra.html
│   └── smartwatch.html
└── trackingProgress
    ├── openGymData
    │   ├── downloadCatalog.py
    │   └── exercisesCatalog.json
    ├── dashboardSync.py
    ├── diet.py
    ├── measures.py
    ├── personal.py
    ├── smartwatch.py
    ├── testSetup.py
    ├── updateTracking.py
    ├── utility.py
    └── workout.py

7 directories, 27 files
```

## dashboardWeb/static/css/custom.css
```css

```

## dashboardWeb/static/js/charts_allenamento.js
```js

```

## dashboardWeb/static/js/charts_dieta.js
```js

```

## dashboardWeb/static/js/charts_home.js
```js

```

## dashboardWeb/static/js/charts_misure.js
```js

```

## dashboardWeb/static/js/charts_palestra.js
```js

```

## dashboardWeb/static/js/charts_smartwatch.js
```js

```

## dashboardWeb/static/js/db.js
```js

```

## dashboardWeb/static/js/nav.js
```js

```

## dashboardWeb/allenamento.html
```html

```

## dashboardWeb/dieta.html
```html

```

## dashboardWeb/home.html
```html

```

## dashboardWeb/misure.html
```html

```

## dashboardWeb/nav.html
```html

```

## dashboardWeb/palestra.html
```html

```

## dashboardWeb/smartwatch.html
```html

```

## trackingProgress/openGymData/downloadCatalog.py
```py
import json
import os
import urllib.request

print("Scaricamento Catalogo openGym In Corso...")

# 1. URL del database ufficiale degli esercizi
url = "https://raw.githubusercontent.com/hasaneyldrm/exercises-dataset/main/data/exercises.json"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})

# 2. Richiesta HTTP e decodifica dei dati JSON
with urllib.request.urlopen(req, timeout=15) as response:
    raw_exercises = json.loads(response.read().decode('utf-8'))

# 3. Creazione immediata del dizionario ID -> Nome (con iniziale maiuscola)
catalog = {item['id']: item['name'].title() for item in raw_exercises}

# 4. Percorso della cartella dove si trova questo script
current_dir = os.path.dirname(os.path.abspath(__file__))
output_path = os.path.join(current_dir, "exercisesCatalog.json")

# 5. Salvataggio su file JSON locale
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(catalog, f, ensure_ascii=False, indent=2)

print("Catalogo Salvato Con Successo!")
print(f"Totale Esercizi: {len(catalog)}")
print(f"File Salvato In: {output_path}")
```

## trackingProgress/openGymData/exercisesCatalog.json
```json
{
  "0001": "3/4 Sit-Up",
  "0002": "45° Side Bend",
  "0003": "Air Bike",
  "1512": "All Fours Squad Stretch",
  "0006": "Alternate Heel Touchers",
  "0007": "Alternate Lateral Pulldown",
  "1368": "Ankle Circles",
  "3293": "Archer Pull Up",
  "3294": "Archer Push Up",
  "2355": "Arm Slingers Hanging Bent Knee Legs",
  "2333": "Arm Slingers Hanging Straight Legs",
  "3214": "Arms Apart Circular Toe Touch (Male)",
  "3204": "Arms Overhead Full Sit-Up (Male)",
  "0009": "Assisted Chest Dip (Kneeling)",
  "0011": "Assisted Hanging Knee Raise",
  "0010": "Assisted Hanging Knee Raise With Throw Down",
  "1708": "Assisted Lying Calves Stretch",
  "1709": "Assisted Lying Glutes Stretch",
  "1710": "Assisted Lying Gluteus And Piriformis Stretch",
  "0012": "Assisted Lying Leg Raise With Lateral Throw Down",
  "0013": "Assisted Lying Leg Raise With Throw Down",
  "0014": "Assisted Motion Russian Twist",
  "0015": "Assisted Parallel Close Grip Pull-Up",
  "0016": "Assisted Prone Hamstring",
  "1713": "Assisted Prone Lying Quads Stretch",
  "1714": "Assisted Prone Rectus Femoris Stretch",
  "0017": "Assisted Pull-Up",
  "1716": "Assisted Seated Pectoralis Major Stretch With Stability Ball",
  "1712": "Assisted Side Lying Adductor Stretch",
  "1758": "Assisted Sit-Up",
  "1431": "Assisted Standing Chin-Up",
  "1432": "Assisted Standing Pull-Up",
  "0018": "Assisted Standing Triceps Extension (With Towel)",
  "0019": "Assisted Triceps Dip (Kneeling)",
  "2364": "Assisted Wide-Grip Chest Dip (Kneeling)",
  "3220": "Astride Jumps (Male)",
  "3672": "Back And Forth Step",
  "1314": "Back Extension On Exercise Ball",
  "3297": "Back Lever",
  "1405": "Back Pec Stretch",
  "1473": "Backward Jump",
  "0020": "Balance Board",
  "0968": "Band Alternating Biceps Curl",
  "0969": "Band Alternating V-Up",
  "0970": "Band Assisted Pull-Up",
  "0971": "Band Assisted Wheel Rollerout",
  "1254": "Band Bench Press",
  "0980": "Band Bent-Over Hip Extension",
  "0972": "Band Bicycle Crunch",
  "0974": "Band Close-Grip Pulldown",
  "0975": "Band Close-Grip Push-Up",
  "0976": "Band Concentration Curl",
  "3117": "Band Fixed Back Close Grip Pulldown",
  "3116": "Band Fixed Back Underhand Pulldown",
  "0977": "Band Front Lateral Raise",
  "0978": "Band Front Raise",
  "1408": "Band Hip Lift",
  "0979": "Band Horizontal Pallof Press",
  "0981": "Band Jack Knife Sit-Up",
  "0983": "Band Kneeling One Arm Pulldown",
  "0985": "Band Kneeling Twisting Crunch",
  "0984": "Band Lying Hip Internal Rotation",
  "1002": "Band Lying Straight Leg Raise",
  "0986": "Band One Arm Overhead Biceps Curl",
  "0987": "Band One Arm Single Leg Split Squat",
  "0988": "Band One Arm Standing Low Row",
  "0989": "Band One Arm Twisting Chest Press",
  "0990": "Band One Arm Twisting Seated Row",
  "0991": "Band Pull Through",
  "0992": "Band Push Sit-Up",
  "0993": "Band Reverse Fly",
  "0994": "Band Reverse Wrist Curl",
  "0996": "Band Seated Hip Internal Rotation",
  "1011": "Band Seated Twist",
  "0997": "Band Shoulder Press",
  "1018": "Band Shrug",
  "0998": "Band Side Triceps Extension",
  "0999": "Band Single Leg Calf Raise",
  "1000": "Band Single Leg Reverse Calf Raise",
  "1001": "Band Single Leg Split Squat",
  "1004": "Band Squat",
  "1003": "Band Squat Row",
  "1005": "Band Standing Crunch",
  "1022": "Band Standing Rear Delt Row",
  "1007": "Band Standing Twisting Crunch",
  "1008": "Band Step-Up",
  "1009": "Band Stiff Leg Deadlift",
  "1023": "Band Straight Back Stiff Leg Deadlift",
  "1010": "Band Straight Leg Deadlift",
  "1012": "Band Twisting Overhead Press",
  "1369": "Band Two Legs Calf Raise - (Band Under Both Legs) V. 2",
  "1013": "Band Underhand Pulldown",
  "1014": "Band V-Up",
  "1015": "Band Vertical Pallof Press",
  "1016": "Band Wrist Curl",
  "1017": "Band Y-Raise",
  "0023": "Barbell Alternate Biceps Curl",
  "0024": "Barbell Bench Front Squat",
  "0025": "Barbell Bench Press",
  "0026": "Barbell Bench Squat",
  "1316": "Barbell Bent Arm Pullover",
  "0027": "Barbell Bent Over Row",
  "2407": "Barbell Biceps Curl (With Arm Blaster)",
  "0028": "Barbell Clean And Press",
  "0029": "Barbell Clean-Grip Front Squat",
  "0030": "Barbell Close-Grip Bench Press",
  "0031": "Barbell Curl",
  "0032": "Barbell Deadlift",
  "0033": "Barbell Decline Bench Press",
  "0034": "Barbell Decline Bent Arm Pullover",
  "0035": "Barbell Decline Close Grip To Skull Press",
  "1255": "Barbell Decline Pullover",
  "0036": "Barbell Decline Wide-Grip Press",
  "0037": "Barbell Decline Wide-Grip Pullover",
  "0038": "Barbell Drag Curl",
  "1370": "Barbell Floor Calf Raise",
  "0039": "Barbell Front Chest Squat",
  "0041": "Barbell Front Raise",
  "0040": "Barbell Front Raise And Pullover",
  "0042": "Barbell Front Squat",
  "0043": "Barbell Full Squat",
  "1461": "Barbell Full Squat (Back Pov)",
  "1462": "Barbell Full Squat (Side Pov)",
  "1545": "Barbell Full Zercher Squat",
  "1409": "Barbell Glute Bridge",
  "3562": "Barbell Glute Bridge Two Legs On Bench (Male)",
  "0044": "Barbell Good Morning",
  "0045": "Barbell Guillotine Bench Press",
  "0046": "Barbell Hack Squat",
  "1436": "Barbell High Bar Squat",
  "0047": "Barbell Incline Bench Press",
  "1719": "Barbell Incline Close Grip Bench Press",
  "0048": "Barbell Incline Reverse-Grip Press",
  "0049": "Barbell Incline Row",
  "0050": "Barbell Incline Shoulder Raise",
  "0051": "Barbell Jefferson Squat",
  "0052": "Barbell Jm Bench Press",
  "0053": "Barbell Jump Squat",
  "1410": "Barbell Lateral Lunge",
  "1435": "Barbell Low Bar Squat",
  "0054": "Barbell Lunge",
  "1720": "Barbell Lying Back Of The Head Tricep Extension",
  "0055": "Barbell Lying Close-Grip Press",
  "0056": "Barbell Lying Close-Grip Triceps Extension",
  "0057": "Barbell Lying Extension",
  "0058": "Barbell Lying Lifting (On Hip)",
  "0059": "Barbell Lying Preacher Curl",
  "0061": "Barbell Lying Triceps Extension",
  "0060": "Barbell Lying Triceps Extension Skull Crusher",
  "0063": "Barbell Narrow Stance Squat",
  "0064": "Barbell One Arm Bent Over Row",
  "0065": "Barbell One Arm Floor Press",
  "0066": "Barbell One Arm Side Deadlift",
  "0067": "Barbell One Arm Snatch",
  "0068": "Barbell One Leg Squat",
  "0069": "Barbell Overhead Squat",
  "1411": "Barbell Palms Down Wrist Curl Over A Bench",
  "1412": "Barbell Palms Up Wrist Curl Over A Bench",
  "3017": "Barbell Pendlay Row",
  "1751": "Barbell Pin Presses",
  "0070": "Barbell Preacher Curl",
  "0071": "Barbell Press Sit-Up",
  "0072": "Barbell Prone Incline Curl",
  "0073": "Barbell Pullover",
  "0022": "Barbell Pullover To Press",
  "0074": "Barbell Rack Pull",
  "0075": "Barbell Rear Delt Raise",
  "0076": "Barbell Rear Delt Row",
  "0078": "Barbell Rear Lunge",
  "0077": "Barbell Rear Lunge V. 2",
  "0079": "Barbell Revers Wrist Curl V. 2",
  "2187": "Barbell Reverse Close-Grip Bench Press",
  "0080": "Barbell Reverse Curl",
  "0118": "Barbell Reverse Grip Bent Over Row",
  "1256": "Barbell Reverse Grip Decline Bench Press",
  "1257": "Barbell Reverse Grip Incline Bench Press",
  "1317": "Barbell Reverse Grip Incline Bench Row",
  "1721": "Barbell Reverse Grip Skullcrusher",
  "0081": "Barbell Reverse Preacher Curl",
  "0082": "Barbell Reverse Wrist Curl",
  "0084": "Barbell Rollerout",
  "0083": "Barbell Rollerout From Bench",
  "0085": "Barbell Romanian Deadlift",
  "0086": "Barbell Seated Behind Head Military Press",
  "0087": "Barbell Seated Bradford Rocky Press",
  "0088": "Barbell Seated Calf Raise",
  "1371": "Barbell Seated Calf Raise",
  "1718": "Barbell Seated Close Grip Behind Neck Triceps Extension",
  "0089": "Barbell Seated Close-Grip Concentration Curl",
  "0090": "Barbell Seated Good Morning",
  "0091": "Barbell Seated Overhead Press",
  "0092": "Barbell Seated Overhead Triceps Extension",
  "0094": "Barbell Seated Twist",
  "0095": "Barbell Shrug",
  "0096": "Barbell Side Bent V. 2",
  "0098": "Barbell Side Split Squat",
  "0097": "Barbell Side Split Squat V. 2",
  "1756": "Barbell Single Leg Deadlift",
  "0099": "Barbell Single Leg Split Squat",
  "2799": "Barbell Sitted Alternate Leg Raise",
  "2800": "Barbell Sitted Alternate Leg Raise (Female)",
  "0100": "Barbell Skier",
  "0101": "Barbell Speed Squat",
  "2810": "Barbell Split Squat V. 2",
  "0102": "Barbell Squat (On Knees)",
  "2798": "Barbell Squat Jump Step Rear Lunge",
  "0103": "Barbell Standing Ab Rollerout",
  "0104": "Barbell Standing Back Wrist Curl",
  "0105": "Barbell Standing Bradford Press",
  "1372": "Barbell Standing Calf Raise",
  "0106": "Barbell Standing Close Grip Curl",
  "1456": "Barbell Standing Close Grip Military Press",
  "2414": "Barbell Standing Concentration Curl",
  "0107": "Barbell Standing Front Raise Over Head",
  "0108": "Barbell Standing Leg Calf Raise",
  "0109": "Barbell Standing Overhead Triceps Extension",
  "0110": "Barbell Standing Reverse Grip Curl",
  "0111": "Barbell Standing Rocking Leg Calf Raise",
  "0112": "Barbell Standing Twist",
  "1629": "Barbell Standing Wide Grip Biceps Curl",
  "1457": "Barbell Standing Wide Military Press",
  "0113": "Barbell Standing Wide-Grip Curl",
  "0114": "Barbell Step-Up",
  "0115": "Barbell Stiff Leg Good Morning",
  "0116": "Barbell Straight Leg Deadlift",
  "0117": "Barbell Sumo Deadlift",
  "3305": "Barbell Thruster",
  "0120": "Barbell Upright Row",
  "0119": "Barbell Upright Row V. 2",
  "0121": "Barbell Upright Row V. 3",
  "0122": "Barbell Wide Bench Press",
  "1258": "Barbell Wide Reverse Grip Bench Press",
  "0124": "Barbell Wide Squat",
  "0123": "Barbell Wide-Grip Upright Row",
  "0126": "Barbell Wrist Curl",
  "0125": "Barbell Wrist Curl V. 2",
  "0127": "Barbell Zercher Squat",
  "3212": "Basic Toe Touch (Male)",
  "0128": "Battling Ropes",
  "3360": "Bear Crawl",
  "1259": "Behind Head Chest Stretch",
  "0129": "Bench Dip (Knees Bent)",
  "1399": "Bench Dip On Floor",
  "0130": "Bench Hip Extension",
  "3019": "Bench Pull-Ups",
  "3639": "Bent Knee Lying Twist (Male)",
  "1770": "Biceps Leg Concentration Curl",
  "0139": "Biceps Narrow Pull-Ups",
  "0140": "Biceps Pull-Up",
  "0137": "Body-Up",
  "3543": "Bodyweight Drop Jump Squat",
  "3544": "Bodyweight Incline Side Plank",
  "1771": "Bodyweight Kneeling Triceps Extension",
  "1769": "Bodyweight Side Lying Biceps Curl",
  "3168": "Bodyweight Squatting Row",
  "3167": "Bodyweight Squatting Row (With Towel)",
  "1373": "Bodyweight Standing Calf Raise",
  "3156": "Bodyweight Standing Close-Grip One Arm Row",
  "3158": "Bodyweight Standing Close-Grip Row",
  "3162": "Bodyweight Standing One Arm Row",
  "3161": "Bodyweight Standing One Arm Row (With Towel)",
  "3166": "Bodyweight Standing Row",
  "3165": "Bodyweight Standing Row (With Towel)",
  "0138": "Bottoms-Up",
  "1374": "Box Jump Down With One Leg Stabilization",
  "2466": "Bridge - Mountain Climber (Cross Body)",
  "1160": "Burpee",
  "0870": "Butt-Ups",
  "1494": "Butterfly Yoga Pose",
  "0148": "Cable Alternate Shoulder Press",
  "0149": "Cable Alternate Triceps Extension",
  "3235": "Cable Assisted Inverse Leg Curl",
  "0150": "Cable Bar Lateral Pulldown",
  "0151": "Cable Bench Press",
  "1630": "Cable Close Grip Curl",
  "1631": "Cable Concentration Curl",
  "0152": "Cable Concentration Extension (On Knee)",
  "0153": "Cable Cross-Over Lateral Pulldown",
  "0154": "Cable Cross-Over Revers Fly",
  "0155": "Cable Cross-Over Variation",
  "0868": "Cable Curl",
  "0157": "Cable Deadlift",
  "0158": "Cable Decline Fly",
  "1260": "Cable Decline One Arm Press",
  "1261": "Cable Decline Press",
  "0159": "Cable Decline Seated Wide-Grip Row",
  "1632": "Cable Drag Curl",
  "0160": "Cable Floor Seated Wide-Grip Row",
  "0161": "Cable Forward Raise",
  "0162": "Cable Front Raise",
  "0164": "Cable Front Shoulder Raise",
  "0165": "Cable Hammer Curl (With Rope)",
  "1722": "Cable High Pulley Overhead Tricep Extension",
  "0167": "Cable High Row (Kneeling)",
  "0168": "Cable Hip Adduction",
  "0169": "Cable Incline Bench Press",
  "1318": "Cable Incline Bench Row",
  "0171": "Cable Incline Fly",
  "0170": "Cable Incline Fly (On Stability Ball)",
  "0172": "Cable Incline Pushdown",
  "0173": "Cable Incline Triceps Extension",
  "0174": "Cable Judo Flip",
  "0860": "Cable Kickback",
  "0175": "Cable Kneeling Crunch",
  "3697": "Cable Kneeling Rear Delt Row (With Rope) (Male)",
  "0176": "Cable Kneeling Triceps Extension",
  "2330": "Cable Lat Pulldown Full Range Of Motion",
  "0177": "Cable Lateral Pulldown (With Rope Attachment)",
  "2616": "Cable Lateral Pulldown With V-Bar",
  "0178": "Cable Lateral Raise",
  "0179": "Cable Low Fly",
  "0180": "Cable Low Seated Row",
  "1634": "Cable Lying Bicep Curl",
  "0182": "Cable Lying Close-Grip Curl",
  "0184": "Cable Lying Extension Pullover (With Rope Attachment)",
  "0185": "Cable Lying Fly",
  "0186": "Cable Lying Triceps Extension V. 2",
  "0188": "Cable Middle Fly",
  "0189": "Cable One Arm Bent Over Row",
  "0190": "Cable One Arm Curl",
  "1262": "Cable One Arm Decline Chest Fly",
  "1263": "Cable One Arm Fly On Exercise Ball",
  "1264": "Cable One Arm Incline Fly On Exercise Ball",
  "1265": "Cable One Arm Incline Press",
  "1266": "Cable One Arm Incline Press On Exercise Ball",
  "0191": "Cable One Arm Lateral Bent-Over",
  "0192": "Cable One Arm Lateral Raise",
  "1633": "Cable One Arm Preacher Curl",
  "1267": "Cable One Arm Press On Exercise Ball",
  "3563": "Cable One Arm Pulldown",
  "1635": "Cable One Arm Reverse Preacher Curl",
  "0193": "Cable One Arm Straight Back High Row (Kneeling)",
  "1723": "Cable One Arm Tricep Pushdown",
  "1636": "Cable Overhead Curl",
  "1637": "Cable Overhead Curl On Exercise Ball",
  "0194": "Cable Overhead Triceps Extension (Rope Attachment)",
  "1319": "Cable Palm Rotational Row",
  "0195": "Cable Preacher Curl",
  "1268": "Cable Press On Exercise Ball",
  "0196": "Cable Pull Through (With Rope)",
  "0198": "Cable Pulldown",
  "0197": "Cable Pulldown (Pro Lat Bar)",
  "1638": "Cable Pulldown Bicep Curl",
  "0201": "Cable Pushdown",
  "0199": "Cable Pushdown (Straight Arm) V. 2",
  "0200": "Cable Pushdown (With Rope Attachment)",
  "0202": "Cable Rear Delt Row (Stirrups)",
  "0203": "Cable Rear Delt Row (With Rope)",
  "0204": "Cable Rear Drive",
  "0205": "Cable Rear Pulldown",
  "0873": "Cable Reverse Crunch",
  "0206": "Cable Reverse Curl",
  "2406": "Cable Reverse Grip Triceps Pushdown (Sz-Bar) (With Arm Blaster)",
  "1413": "Cable Reverse One Arm Curl",
  "0209": "Cable Reverse Preacher Curl",
  "0210": "Cable Reverse Wrist Curl",
  "0207": "Cable Reverse-Grip Pushdown",
  "0208": "Cable Reverse-Grip Straight Back Seated High Row",
  "1320": "Cable Rope Crossover Seated Row",
  "1321": "Cable Rope Elevated Seated Row",
  "1322": "Cable Rope Extension Incline Bench Row",
  "1639": "Cable Rope Hammer Preacher Curl",
  "1724": "Cable Rope High Pulley Overhead Tricep Extension",
  "1725": "Cable Rope Incline Tricep Extension",
  "1726": "Cable Rope Lying On Floor Tricep Extension",
  "1640": "Cable Rope One Arm Hammer Preacher Curl",
  "1323": "Cable Rope Seated Row",
  "0211": "Cable Russian Twists (On Stability Ball)",
  "2144": "Cable Seated Chest Press",
  "0212": "Cable Seated Crunch",
  "1641": "Cable Seated Curl",
  "0213": "Cable Seated High Row (V-Bar)",
  "0214": "Cable Seated One Arm Alternate Row",
  "1642": "Cable Seated One Arm Concentration Curl",
  "1643": "Cable Seated Overhead Curl",
  "0215": "Cable Seated Rear Lateral Raise",
  "0861": "Cable Seated Row",
  "0216": "Cable Seated Shoulder Internal Rotation",
  "2399": "Cable Seated Twist",
  "0218": "Cable Seated Wide-Grip Row",
  "0219": "Cable Shoulder Press",
  "0220": "Cable Shrug",
  "0222": "Cable Side Bend",
  "0221": "Cable Side Bend Crunch (Bosu Ball)",
  "0223": "Cable Side Crunch",
  "1717": "Cable Squat Row (With Rope Attachment)",
  "1644": "Cable Squatting Curl",
  "0224": "Cable Standing Back Wrist Curl",
  "1375": "Cable Standing Calf Raise",
  "0225": "Cable Standing Cross-Over High Reverse Fly",
  "0226": "Cable Standing Crunch",
  "0874": "Cable Standing Crunch (With Rope Attachment)",
  "0227": "Cable Standing Fly",
  "0228": "Cable Standing Hip Extension",
  "0229": "Cable Standing Inner Curl",
  "0230": "Cable Standing Lift",
  "0231": "Cable Standing One Arm Triceps Extension",
  "1376": "Cable Standing One Leg Calf Raise",
  "0232": "Cable Standing Pulldown (With Rope)",
  "0233": "Cable Standing Rear Delt Row (With Rope)",
  "1727": "Cable Standing Reverse Grip One Arm Overhead Tricep Extension",
  "0234": "Cable Standing Row (V-Bar)",
  "0235": "Cable Standing Shoulder External Rotation",
  "0236": "Cable Standing Twist Row (V-Bar)",
  "1269": "Cable Standing Up Straight Crossovers",
  "0238": "Cable Straight Arm Pulldown",
  "0237": "Cable Straight Arm Pulldown (With Rope)",
  "0239": "Cable Straight Back Seated Row",
  "0240": "Cable Supine Reverse Fly",
  "2464": "Cable Thibaudeau Kayak Row",
  "0241": "Cable Triceps Pushdown (V-Bar)",
  "2405": "Cable Triceps Pushdown (V-Bar) (With Arm Blaster)",
  "0242": "Cable Tuck Reverse Crunch",
  "0243": "Cable Twist",
  "0862": "Cable Twist (Up-Down)",
  "0244": "Cable Twisting Pull",
  "1645": "Cable Two Arm Curl On Incline Bench",
  "1728": "Cable Two Arm Tricep Kickback",
  "0245": "Cable Underhand Pulldown",
  "1270": "Cable Upper Chest Crossovers",
  "1324": "Cable Upper Row",
  "0246": "Cable Upright Row",
  "1325": "Cable Wide Grip Rear Pulldown Behind Neck",
  "0247": "Cable Wrist Curl",
  "1407": "Calf Push Stretch With Hands Against Wall",
  "1377": "Calf Stretch With Hands Against Wall",
  "1378": "Calf Stretch With Rope",
  "0248": "Cambered Bar Lying Row",
  "2963": "Captains Chair Straight Leg Raise",
  "1548": "Chair Leg Extended Stretch",
  "1271": "Chest And Front Of Shoulder Stretch",
  "0251": "Chest Dip",
  "1430": "Chest Dip (On Dip-Pull-Up Cage)",
  "2462": "Chest Dip On Straight Bar",
  "1272": "Chest Stretch With Exercise Ball",
  "3216": "Chest Tap Push-Up (Male)",
  "1326": "Chin-Up",
  "0253": "Chin-Ups (Narrow Parallel Grip)",
  "0257": "Circles Knee Stretch",
  "1273": "Clap Push Up",
  "0258": "Clock Push-Up",
  "1327": "Close Grip Chin-Up",
  "0259": "Close-Grip Push-Up",
  "2398": "Close-Grip Push-Up (On Knees)",
  "0260": "Cocoons",
  "1468": "Crab Twist Toe Touch",
  "0262": "Cross Body Crunch",
  "0267": "Crunch (Hands Overhead)",
  "0271": "Crunch (On Stability Ball)",
  "0272": "Crunch (On Stability Ball, Arms Straight)",
  "0274": "Crunch Floor",
  "3016": "Curl-Up",
  "3769": "Curtsey Squat",
  "2331": "Cycle Cross Trainer",
  "0276": "Dead Bug",
  "0277": "Decline Crunch",
  "0279": "Decline Push-Up",
  "0282": "Decline Sit-Up",
  "1274": "Deep Push Up",
  "0283": "Diamond Push-Up",
  "0284": "Donkey Calf Raise",
  "1275": "Drop Push Up",
  "0285": "Dumbbell Alternate Biceps Curl",
  "2403": "Dumbbell Alternate Biceps Curl (With Arm Blaster)",
  "1646": "Dumbbell Alternate Hammer Preacher Curl",
  "1647": "Dumbbell Alternate Preacher Curl",
  "1648": "Dumbbell Alternate Seated Hammer Curl",
  "0286": "Dumbbell Alternate Side Press",
  "1649": "Dumbbell Alternating Bicep Curl With Leg Raised On Exercise Ball",
  "1650": "Dumbbell Alternating Seated Bicep Curl On Exercise Ball",
  "2137": "Dumbbell Arnold Press",
  "0287": "Dumbbell Arnold Press V. 2",
  "0288": "Dumbbell Around Pullover",
  "0289": "Dumbbell Bench Press",
  "0290": "Dumbbell Bench Seated Press",
  "0291": "Dumbbell Bench Squat",
  "0293": "Dumbbell Bent Over Row",
  "1651": "Dumbbell Bicep Curl Lunge With Bowling Motion",
  "1652": "Dumbbell Bicep Curl On Exercise Ball With Leg Raised",
  "1653": "Dumbbell Bicep Curl With Stork Stance",
  "0294": "Dumbbell Biceps Curl",
  "2401": "Dumbbell Biceps Curl (With Arm Blaster)",
  "1654": "Dumbbell Biceps Curl Reverse",
  "1655": "Dumbbell Biceps Curl Squat",
  "1656": "Dumbbell Biceps Curl V Sit On Bosu Ball",
  "1201": "Dumbbell Burpee",
  "0295": "Dumbbell Clean",
  "1731": "Dumbbell Close Grip Press",
  "0296": "Dumbbell Close-Grip Press",
  "0297": "Dumbbell Concentration Curl",
  "3635": "Dumbbell Contralateral Forward Lunge",
  "0298": "Dumbbell Cross Body Hammer Curl",
  "1657": "Dumbbell Cross Body Hammer Curl V. 2",
  "0299": "Dumbbell Cuban Press",
  "2136": "Dumbbell Cuban Press V. 2",
  "0300": "Dumbbell Deadlift",
  "0301": "Dumbbell Decline Bench Press",
  "0302": "Dumbbell Decline Fly",
  "0303": "Dumbbell Decline Hammer Press",
  "1276": "Dumbbell Decline One Arm Fly",
  "1617": "Dumbbell Decline One Arm Hammer Press",
  "0305": "Dumbbell Decline Shrug",
  "0304": "Dumbbell Decline Shrug V. 2",
  "0306": "Dumbbell Decline Triceps Extension",
  "0307": "Dumbbell Decline Twist Fly",
  "1437": "Dumbbell Finger Curls",
  "0308": "Dumbbell Fly",
  "1277": "Dumbbell Fly On Exercise Ball",
  "1732": "Dumbbell Forward Lunge Triceps Extension",
  "0310": "Dumbbell Front Raise",
  "0309": "Dumbbell Front Raise V. 2",
  "0311": "Dumbbell Full Can Lateral Raise",
  "1760": "Dumbbell Goblet Squat",
  "0313": "Dumbbell Hammer Curl",
  "1659": "Dumbbell Hammer Curl On Exercise Ball",
  "0312": "Dumbbell Hammer Curl V. 2",
  "2402": "Dumbbell Hammer Curls (With Arm Blaster)",
  "1664": "Dumbbell High Curl",
  "3545": "Dumbbell Incline Alternate Press",
  "0314": "Dumbbell Incline Bench Press",
  "0315": "Dumbbell Incline Biceps Curl",
  "0316": "Dumbbell Incline Breeding",
  "0318": "Dumbbell Incline Curl",
  "0317": "Dumbbell Incline Curl V. 2",
  "0319": "Dumbbell Incline Fly",
  "1278": "Dumbbell Incline Fly On Exercise Ball",
  "0320": "Dumbbell Incline Hammer Curl",
  "0321": "Dumbbell Incline Hammer Press",
  "1618": "Dumbbell Incline Hammer Press On Exercise Ball",
  "0322": "Dumbbell Incline Inner Biceps Curl",
  "1279": "Dumbbell Incline One Arm Fly",
  "1280": "Dumbbell Incline One Arm Fly On Exercise Ball",
  "1619": "Dumbbell Incline One Arm Hammer Press",
  "1620": "Dumbbell Incline One Arm Hammer Press On Exercise Ball",
  "0323": "Dumbbell Incline One Arm Lateral Raise",
  "1281": "Dumbbell Incline One Arm Press",
  "1282": "Dumbbell Incline One Arm Press On Exercise Ball",
  "0324": "Dumbbell Incline Palm-In Press",
  "1283": "Dumbbell Incline Press On Exercise Ball",
  "0325": "Dumbbell Incline Raise",
  "0326": "Dumbbell Incline Rear Lateral Raise",
  "0327": "Dumbbell Incline Row",
  "0328": "Dumbbell Incline Shoulder Raise",
  "0329": "Dumbbell Incline Shrug",
  "3542": "Dumbbell Incline T-Raise",
  "0330": "Dumbbell Incline Triceps Extension",
  "0331": "Dumbbell Incline Twisted Flyes",
  "1733": "Dumbbell Incline Two Arm Extension",
  "3541": "Dumbbell Incline Y-Raise",
  "0332": "Dumbbell Iron Cross",
  "0333": "Dumbbell Kickback",
  "1734": "Dumbbell Kickbacks On Exercise Ball",
  "1660": "Dumbbell Kneeling Bicep Curl Exercise Ball",
  "0334": "Dumbbell Lateral Raise",
  "0335": "Dumbbell Lateral To Front Raise",
  "0336": "Dumbbell Lunge",
  "1658": "Dumbbell Lunge With Bicep Curl",
  "0337": "Dumbbell Lying Extension (Across Face)",
  "1729": "Dumbbell Lying Alternate Extension",
  "0338": "Dumbbell Lying Elbow Press",
  "0863": "Dumbbell Lying External Shoulder Rotation",
  "0339": "Dumbbell Lying Femoral",
  "0340": "Dumbbell Lying Hammer Press",
  "2470": "Dumbbell Lying On Floor Rear Delt Raise",
  "0341": "Dumbbell Lying One Arm Deltoid Rear",
  "0343": "Dumbbell Lying One Arm Press",
  "0342": "Dumbbell Lying One Arm Press V. 2",
  "0344": "Dumbbell Lying One Arm Pronated Triceps Extension",
  "0345": "Dumbbell Lying One Arm Rear Lateral Raise",
  "0346": "Dumbbell Lying One Arm Supinated Triceps Extension",
  "0347": "Dumbbell Lying Pronation",
  "2705": "Dumbbell Lying Pronation On Floor",
  "1284": "Dumbbell Lying Pullover On Exercise Ball",
  "1328": "Dumbbell Lying Rear Delt Row",
  "0348": "Dumbbell Lying Rear Lateral Raise",
  "1735": "Dumbbell Lying Single Extension",
  "0349": "Dumbbell Lying Supination",
  "2706": "Dumbbell Lying Supination On Floor",
  "1661": "Dumbbell Lying Supine Biceps Curl",
  "0350": "Dumbbell Lying Supine Curl",
  "0351": "Dumbbell Lying Triceps Extension",
  "1662": "Dumbbell Lying Wide Curl",
  "0352": "Dumbbell Neutral Grip Bench Press",
  "1285": "Dumbbell One Arm Bench Fly",
  "0292": "Dumbbell One Arm Bent-Over Row",
  "1286": "Dumbbell One Arm Chest Fly On Exercise Ball",
  "0353": "Dumbbell One Arm Concentration Curl (On Stability Ball)",
  "1287": "Dumbbell One Arm Decline Chest Press",
  "1288": "Dumbbell One Arm Fly On Exercise Ball",
  "1736": "Dumbbell One Arm French Press On Exercise Ball",
  "1663": "Dumbbell One Arm Hammer Preacher Curl",
  "1621": "Dumbbell One Arm Hammer Press On Exercise Ball",
  "1289": "Dumbbell One Arm Incline Chest Press",
  "0354": "Dumbbell One Arm Kickback",
  "0355": "Dumbbell One Arm Lateral Raise",
  "0356": "Dumbbell One Arm Lateral Raise With Support",
  "1290": "Dumbbell One Arm Press On Exercise Ball",
  "1665": "Dumbbell One Arm Prone Curl",
  "1666": "Dumbbell One Arm Prone Hammer Curl",
  "1291": "Dumbbell One Arm Pullover On Exercise Ball",
  "0358": "Dumbbell One Arm Reverse Wrist Curl",
  "0359": "Dumbbell One Arm Reverse Fly (With Support)",
  "1622": "Dumbbell One Arm Reverse Grip Press",
  "1414": "Dumbbell One Arm Reverse Preacher Curl",
  "1667": "Dumbbell One Arm Reverse Spider Curl",
  "1668": "Dumbbell One Arm Seated Bicep Curl On Exercise Ball",
  "1669": "Dumbbell One Arm Seated Hammer Curl",
  "1415": "Dumbbell One Arm Seated Neutral Wrist Curl",
  "0361": "Dumbbell One Arm Shoulder Press",
  "0360": "Dumbbell One Arm Shoulder Press V. 2",
  "3888": "Dumbbell One Arm Snatch",
  "1670": "Dumbbell One Arm Standing Curl",
  "1671": "Dumbbell One Arm Standing Hammer Curl",
  "0362": "Dumbbell One Arm Triceps Extension (On Bench)",
  "0363": "Dumbbell One Arm Upright Row",
  "0364": "Dumbbell One Arm Wrist Curl",
  "1672": "Dumbbell One Arm Zottman Preacher Curl",
  "1292": "Dumbbell One Leg Fly On Exercise Ball",
  "0365": "Dumbbell Over Bench Neutral Wrist Curl",
  "0366": "Dumbbell Over Bench One Arm Neutral Wrist Curl",
  "1441": "Dumbbell Over Bench One Arm Reverse Wrist Curl",
  "0367": "Dumbbell Over Bench One Arm Wrist Curl",
  "0368": "Dumbbell Over Bench Revers Wrist Curl",
  "0369": "Dumbbell Over Bench Wrist Curl",
  "1329": "Dumbbell Palm Rotational Bent Over Row",
  "1623": "Dumbbell Palms In Incline Bench Press",
  "0370": "Dumbbell Peacher Hammer Curl",
  "0371": "Dumbbell Plyo Squat",
  "0372": "Dumbbell Preacher Curl",
  "1673": "Dumbbell Preacher Curl Over Exercise Ball",
  "1293": "Dumbbell Press On Exercise Ball",
  "0373": "Dumbbell Pronate-Grip Triceps Extension",
  "0374": "Dumbbell Prone Incline Curl",
  "1674": "Dumbbell Prone Incline Hammer Curl",
  "0375": "Dumbbell Pullover",
  "1294": "Dumbbell Pullover Hip Extension On Exercise Ball",
  "1295": "Dumbbell Pullover On Exercise Ball",
  "1700": "Dumbbell Push Press",
  "0376": "Dumbbell Raise",
  "2292": "Dumbbell Rear Delt Raise",
  "0377": "Dumbbell Rear Delt Row_Shoulder",
  "0378": "Dumbbell Rear Fly",
  "0380": "Dumbbell Rear Lateral Raise",
  "0379": "Dumbbell Rear Lateral Raise (Support Head)",
  "0381": "Dumbbell Rear Lunge",
  "0382": "Dumbbell Revers Grip Biceps Curl",
  "1624": "Dumbbell Reverse Bench Press",
  "0383": "Dumbbell Reverse Fly",
  "1330": "Dumbbell Reverse Grip Incline Bench One Arm Row",
  "1331": "Dumbbell Reverse Grip Incline Bench Two Arm Row",
  "2327": "Dumbbell Reverse Grip Row (Female)",
  "0384": "Dumbbell Reverse Preacher Curl",
  "1675": "Dumbbell Reverse Spider Curl",
  "0385": "Dumbbell Reverse Wrist Curl",
  "1459": "Dumbbell Romanian Deadlift",
  "0386": "Dumbbell Rotation Reverse Fly",
  "2397": "Dumbbell Scott Press",
  "0387": "Dumbbell Seated Alternate Front Raise",
  "1676": "Dumbbell Seated Alternate Hammer Curl On Exercise Ball",
  "0388": "Dumbbell Seated Alternate Press",
  "3546": "Dumbbell Seated Alternate Shoulder",
  "0389": "Dumbbell Seated Bench Extension",
  "2317": "Dumbbell Seated Bent Arm Lateral Raise",
  "1730": "Dumbbell Seated Bent Over Alternate Kickback",
  "1737": "Dumbbell Seated Bent Over Triceps Extension",
  "1677": "Dumbbell Seated Bicep Curl",
  "0390": "Dumbbell Seated Biceps Curl (On Stability Ball)",
  "3547": "Dumbbell Seated Biceps Curl To Shoulder Press",
  "1379": "Dumbbell Seated Calf Raise",
  "0391": "Dumbbell Seated Curl",
  "0392": "Dumbbell Seated Front Raise",
  "1678": "Dumbbell Seated Hammer Curl",
  "0393": "Dumbbell Seated Inner Biceps Curl",
  "0394": "Dumbbell Seated Kickback",
  "0396": "Dumbbell Seated Lateral Raise",
  "0395": "Dumbbell Seated Lateral Raise V. 2",
  "0397": "Dumbbell Seated Neutral Wrist Curl",
  "1679": "Dumbbell Seated One Arm Bicep Curl On Exercise Ball With Leg Raised",
  "0398": "Dumbbell Seated One Arm Kickback",
  "0399": "Dumbbell Seated One Arm Rotate",
  "0400": "Dumbbell Seated One Leg Calf Raise",
  "1380": "Dumbbell Seated One Leg Calf Raise - Hammer Grip",
  "1381": "Dumbbell Seated One Leg Calf Raise - Palm Up",
  "0401": "Dumbbell Seated Palms Up Wrist Curl",
  "0402": "Dumbbell Seated Preacher Curl",
  "0403": "Dumbbell Seated Revers Grip Concentration Curl",
  "1738": "Dumbbell Seated Reverse Grip One Arm Overhead Tricep Extension",
  "0405": "Dumbbell Seated Shoulder Press",
  "0404": "Dumbbell Seated Shoulder Press (Parallel Grip)",
  "2188": "Dumbbell Seated Triceps Extension",
  "0406": "Dumbbell Shrug",
  "0407": "Dumbbell Side Bend",
  "0408": "Dumbbell Side Lying One Hand Raise",
  "3664": "Dumbbell Side Plank With Rear Fly",
  "3548": "Dumbbell Single Arm Overhead Carry",
  "0409": "Dumbbell Single Leg Calf Raise",
  "1757": "Dumbbell Single Leg Deadlift",
  "2805": "Dumbbell Single Leg Deadlift With Stepbox Support",
  "0410": "Dumbbell Single Leg Split Squat",
  "0411": "Dumbbell Single Leg Squat",
  "0413": "Dumbbell Squat",
  "3560": "Dumbbell Standing Alternate Hammer Curl And Press",
  "0414": "Dumbbell Standing Alternate Overhead Press",
  "0415": "Dumbbell Standing Alternate Raise",
  "1739": "Dumbbell Standing Alternating Tricep Kickback",
  "2143": "Dumbbell Standing Around World",
  "1740": "Dumbbell Standing Bent Over One Arm Triceps Extension",
  "1741": "Dumbbell Standing Bent Over Two Arm Triceps Extension",
  "0416": "Dumbbell Standing Biceps Curl",
  "0417": "Dumbbell Standing Calf Raise",
  "0418": "Dumbbell Standing Concentration Curl",
  "0419": "Dumbbell Standing Front Raise Above Head",
  "2321": "Dumbbell Standing Inner Biceps Curl V. 2",
  "0420": "Dumbbell Standing Kickback",
  "0421": "Dumbbell Standing One Arm Concentration Curl",
  "0422": "Dumbbell Standing One Arm Curl (Over Incline Bench)",
  "1680": "Dumbbell Standing One Arm Curl Over Incline Bench",
  "0423": "Dumbbell Standing One Arm Extension",
  "0424": "Dumbbell Standing One Arm Palm In Press",
  "0425": "Dumbbell Standing One Arm Reverse Curl",
  "0426": "Dumbbell Standing Overhead Press",
  "0427": "Dumbbell Standing Palms In Press",
  "0428": "Dumbbell Standing Preacher Curl",
  "0429": "Dumbbell Standing Reverse Curl",
  "0430": "Dumbbell Standing Triceps Extension",
  "2293": "Dumbbell Standing Zottman Preacher Curl",
  "1684": "Dumbbell Step Up Single Leg Balance With Bicep Curl",
  "0431": "Dumbbell Step-Up",
  "2796": "Dumbbell Step-Up Lunge",
  "2812": "Dumbbell Step-Up Split Squat",
  "0432": "Dumbbell Stiff Leg Deadlift",
  "0433": "Dumbbell Straight Arm Pullover",
  "0434": "Dumbbell Straight Leg Deadlift",
  "2808": "Dumbbell Sumo Pull Through",
  "2803": "Dumbbell Supported Squat",
  "0436": "Dumbbell Tate Press",
  "1742": "Dumbbell Tricep Kickback With Stork Stance",
  "1743": "Dumbbell Twisting Bench Press",
  "0437": "Dumbbell Upright Row",
  "1765": "Dumbbell Upright Row (Back Pov)",
  "0864": "Dumbbell Upright Shoulder External Rotation",
  "5201": "Dumbbell Waiter Biceps Curl",
  "0438": "Dumbbell W-Press",
  "0439": "Dumbbell Zottman Curl",
  "2294": "Dumbbell Zottman Preacher Curl",
  "2189": "Dumbbells Seated Triceps Extension",
  "1167": "Dynamic Chest Stretch (Male)",
  "3287": "Elbow Dips",
  "1772": "Elbow Lift - Reverse Push-Up",
  "0443": "Elbow-To-Knee",
  "3292": "Elevator",
  "1332": "Exercise Ball Alternating Arm Ups",
  "1333": "Exercise Ball Back Extension With Arms Extended",
  "1334": "Exercise Ball Back Extension With Hands Behind Head",
  "1335": "Exercise Ball Back Extension With Knees Off Ground",
  "1336": "Exercise Ball Back Extension With Rotation",
  "1744": "Exercise Ball Dip",
  "1559": "Exercise Ball Hip Flexor Stretch",
  "1338": "Exercise Ball Hug",
  "1339": "Exercise Ball Lat Stretch",
  "1341": "Exercise Ball Lower Back Stretch (Pyramid)",
  "1342": "Exercise Ball Lying Side Lat Stretch",
  "1382": "Exercise Ball On The Wall Calf Raise",
  "3241": "Exercise Ball On The Wall Calf Raise (Tennis Ball Between Ankles)",
  "3240": "Exercise Ball On The Wall Calf Raise (Tennis Ball Between Knees)",
  "1416": "Exercise Ball One Leg Prone Lower Body Rotation",
  "1417": "Exercise Ball One Legged Diagonal Kick Hamstring Curl",
  "1296": "Exercise Ball Pike Push Up",
  "1343": "Exercise Ball Prone Leg Raise",
  "1560": "Exercise Ball Seated Hamstring Stretch",
  "1745": "Exercise Ball Seated Triceps Stretch",
  "1746": "Exercise Ball Supine Triceps Extension",
  "1747": "Ez Bar French Press On Exercise Ball",
  "3010": "Ez Bar Lying Bent Arms Pullover",
  "1748": "Ez Bar Lying Close Grip Triceps Extension Behind Head",
  "1344": "Ez Bar Reverse Grip Bent Over Row",
  "1682": "Ez Bar Seated Close Grip Concentration Curl",
  "1749": "Ez Bar Standing French Press",
  "0445": "Ez Barbell Anti Gravity Press",
  "1627": "Ez Barbell Close Grip Preacher Curl",
  "0446": "Ez Barbell Close-Grip Curl",
  "0447": "Ez Barbell Curl",
  "0448": "Ez Barbell Decline Close Grip Face Press",
  "2186": "Ez Barbell Decline Triceps Extension",
  "0449": "Ez Barbell Incline Triceps Extension",
  "0450": "Ez Barbell Jm Bench Press",
  "0451": "Ez Barbell Reverse Grip Curl",
  "0452": "Ez Barbell Reverse Grip Preacher Curl",
  "1458": "Ez Barbell Seated Curls",
  "0453": "Ez Barbell Seated Triceps Extension",
  "0454": "Ez Barbell Spider Curl",
  "1628": "Ez Barbell Spider Curl",
  "2404": "Ez-Bar Biceps Curl (With Arm Blaster)",
  "2432": "Ez-Bar Close-Grip Bench Press",
  "2741": "Ez-Barbell Standing Wide Grip Biceps Curl",
  "2133": "Farmers Walk",
  "0455": "Finger Curls",
  "3303": "Flag",
  "0456": "Flexion Leg Sit Up (Bent Knee)",
  "0457": "Flexion Leg Sit Up (Straight Arm)",
  "0458": "Floor Fly (With Barbell)",
  "0459": "Flutter Kicks",
  "1472": "Forward Jump",
  "3470": "Forward Lunge (Male)",
  "3194": "Frankenstein Squat",
  "2429": "Frog Crunch",
  "3301": "Frog Planche",
  "3296": "Front Lever",
  "3295": "Front Lever Reps",
  "0464": "Front Plank With Twist",
  "3315": "Full Maltese",
  "3299": "Full Planche",
  "3327": "Full Planche Push-Up",
  "0466": "Gironda Sternum Chin",
  "3561": "Glute Bridge March",
  "3523": "Glute Bridge Two Legs On Bench (Male)",
  "3193": "Glute-Ham Raise",
  "0467": "Gorilla Chin",
  "0469": "Groin Crunch",
  "1383": "Hack Calf Raise",
  "1384": "Hack One Leg Calf Raise",
  "3221": "Half Knee Bends (Male)",
  "3202": "Half Sit-Up (Male)",
  "1511": "Hamstring Stretch",
  "2139": "Hands Bike",
  "3218": "Hands Clasped Circular Toe Touch (Male)",
  "3215": "Hands Reversed Clasped Circular Toe Touch (Male)",
  "3302": "Handstand",
  "0471": "Handstand Push-Up",
  "1764": "Hanging Leg Hip Raise",
  "0472": "Hanging Leg Raise",
  "1761": "Hanging Oblique Knee Raise",
  "0473": "Hanging Pike",
  "0474": "Hanging Straight Leg Hip Raise",
  "0475": "Hanging Straight Leg Raise",
  "0476": "Hanging Straight Twisting Leg Hip Raise",
  "3636": "High Knee Against Wall",
  "0484": "Hip Raise (Bent Knee)",
  "1418": "Hug Keens To Chest",
  "3234": "Hyght Dumbbell Fly",
  "0489": "Hyperextension",
  "0488": "Hyperextension (On Bench)",
  "3289": "Impossible Dips",
  "1471": "Inchworm",
  "3698": "Inchworm V. 2",
  "0490": "Incline Close-Grip Push-Up",
  "0491": "Incline Leg Hip Raise (Leg Straight)",
  "0492": "Incline Push Up Depth Jump",
  "0493": "Incline Push-Up",
  "3785": "Incline Push-Up (On Box)",
  "0494": "Incline Reverse Grip Push-Up",
  "3011": "Incline Scapula Push Up",
  "0495": "Incline Twisting Sit-Up",
  "1564": "Intermediate Hip Flexor And Quad Stretch",
  "0496": "Inverse Leg Curl (Bench Support)",
  "2400": "Inverse Leg Curl (On Pull-Up Cable Machine)",
  "0499": "Inverted Row",
  "2300": "Inverted Row Bent Knees",
  "2298": "Inverted Row On Bench",
  "0497": "Inverted Row V. 2",
  "0498": "Inverted Row With Straps",
  "1419": "Iron Cross Stretch",
  "1297": "Isometric Chest Squeeze",
  "0500": "Isometric Wipers",
  "0501": "Jack Burpee",
  "3224": "Jack Jump (Male)",
  "0507": "Jackknife Sit-Up",
  "0508": "Janda Sit-Up",
  "2612": "Jump Rope",
  "0514": "Jump Squat",
  "0513": "Jump Squat V. 2",
  "0517": "Kettlebell Advanced Windmill",
  "0518": "Kettlebell Alternating Hang Clean",
  "0520": "Kettlebell Alternating Press",
  "0519": "Kettlebell Alternating Press On Floor",
  "0521": "Kettlebell Alternating Renegade Row",
  "0522": "Kettlebell Alternating Row",
  "0523": "Kettlebell Arnold Press",
  "0524": "Kettlebell Bent Press",
  "0525": "Kettlebell Bottoms Up Clean From The Hang Position",
  "0526": "Kettlebell Double Alternating Hang Clean",
  "0527": "Kettlebell Double Jerk",
  "0528": "Kettlebell Double Push Press",
  "0529": "Kettlebell Double Snatch",
  "0530": "Kettlebell Double Windmill",
  "0531": "Kettlebell Extended Range One Arm Press On Floor",
  "0532": "Kettlebell Figure 8",
  "0533": "Kettlebell Front Squat",
  "0534": "Kettlebell Goblet Squat",
  "0535": "Kettlebell Hang Clean",
  "0536": "Kettlebell Lunge Pass Through",
  "0537": "Kettlebell One Arm Clean And Jerk",
  "1298": "Kettlebell One Arm Floor Press",
  "0538": "Kettlebell One Arm Jerk",
  "0539": "Kettlebell One Arm Military Press To The Side",
  "0540": "Kettlebell One Arm Push Press",
  "0541": "Kettlebell One Arm Row",
  "0542": "Kettlebell One Arm Snatch",
  "0543": "Kettlebell Pirate Supper Legs",
  "0544": "Kettlebell Pistol Squat",
  "0545": "Kettlebell Plyo Push-Up",
  "0546": "Kettlebell Seated Press",
  "1438": "Kettlebell Seated Two Arm Military Press",
  "0547": "Kettlebell Seesaw Press",
  "0548": "Kettlebell Sumo High Pull",
  "0549": "Kettlebell Swing",
  "0550": "Kettlebell Thruster",
  "0551": "Kettlebell Turkish Get Up (Squat Style)",
  "0552": "Kettlebell Two Arm Clean",
  "0553": "Kettlebell Two Arm Military Press",
  "1345": "Kettlebell Two Arm Row",
  "0554": "Kettlebell Windmill",
  "0555": "Kick Out Sit",
  "0558": "Kipping Muscle Up",
  "3640": "Knee Touch Crunch",
  "1420": "Kneeling Jump Squat",
  "1346": "Kneeling Lat Stretch",
  "3239": "Kneeling Plank Tap Shoulder (Male)",
  "3211": "Kneeling Push-Up (Male)",
  "3288": "Korean Dips",
  "3418": "L-Pull-Up",
  "3419": "L-Sit On Floor",
  "0562": "Landmine 180",
  "3237": "Landmine Lateral Raise",
  "3300": "Lean Planche",
  "2271": "Left Hook. Boxing",
  "0570": "Leg Pull In Flat Bench",
  "1576": "Leg Up Hamstring Stretch",
  "2287": "Lever Alternate Leg Press",
  "0571": "Lever Alternating Narrow Grip Seated Row",
  "0572": "Lever Assisted Chin-Up",
  "0573": "Lever Back Extension",
  "0574": "Lever Bent Over Row",
  "3200": "Lever Bent-Over Row With V-Bar",
  "0575": "Lever Bicep Curl",
  "2289": "Lever Calf Press",
  "0577": "Lever Chest Press",
  "0576": "Lever Chest Press",
  "0578": "Lever Deadlift",
  "1300": "Lever Decline Chest Press",
  "1253": "Lever Donkey Calf Raise",
  "0579": "Lever Front Pulldown",
  "0580": "Lever Gripless Shrug",
  "1439": "Lever Gripless Shrug V. 2",
  "2288": "Lever Gripper Hands",
  "1615": "Lever Hammer Grip Preacher Curl",
  "0581": "Lever High Row",
  "2286": "Lever Hip Extension V. 2",
  "2611": "Lever Horizontal One Leg Press",
  "1299": "Lever Incline Chest Press",
  "1479": "Lever Incline Chest Press V. 2",
  "0582": "Lever Kneeling Leg Curl",
  "0583": "Lever Kneeling Twist",
  "0584": "Lever Lateral Raise",
  "0585": "Lever Leg Extension",
  "0586": "Lever Lying Leg Curl",
  "3195": "Lever Lying Two-One Leg Curl",
  "0587": "Lever Military Press",
  "0588": "Lever Narrow Grip Seated Row",
  "0589": "Lever One Arm Bent Over Row",
  "1356": "Lever One Arm Lateral High Row",
  "1347": "Lever One Arm Lateral Wide Pulldown",
  "0590": "Lever One Arm Shoulder Press",
  "0591": "Lever Overhand Triceps Dip",
  "0592": "Lever Preacher Curl",
  "1614": "Lever Preacher Curl V. 2",
  "2285": "Lever Pullover",
  "2736": "Lever Reverse Grip Lateral Pulldown",
  "1616": "Lever Reverse Grip Preacher Curl",
  "1348": "Lever Reverse Grip Vertical Row",
  "0593": "Lever Reverse Hyperextension",
  "1349": "Lever Reverse T-Bar Row",
  "2315": "Lever Rotary Calf",
  "2335": "Lever Seated Calf Press",
  "0594": "Lever Seated Calf Raise",
  "1452": "Lever Seated Crunch",
  "0595": "Lever Seated Crunch (Chest Pad)",
  "3760": "Lever Seated Crunch V. 2",
  "1451": "Lever Seated Dip",
  "0596": "Lever Seated Fly",
  "3759": "Lever Seated Good Morning",
  "0597": "Lever Seated Hip Abduction",
  "0598": "Lever Seated Hip Adduction",
  "0599": "Lever Seated Leg Curl",
  "0600": "Lever Seated Leg Raise Crunch",
  "0602": "Lever Seated Reverse Fly",
  "0601": "Lever Seated Reverse Fly (Parallel Grip)",
  "1350": "Lever Seated Row",
  "1385": "Lever Seated Squat Calf Raise On Leg Press Machine",
  "0603": "Lever Shoulder Press",
  "0869": "Lever Shoulder Press V. 2",
  "2318": "Lever Shoulder Press V. 3",
  "0604": "Lever Shrug",
  "0605": "Lever Standing Calf Raise",
  "3758": "Lever Standing Chest Press",
  "0606": "Lever T Bar Row",
  "1351": "Lever T-Bar Reverse Grip Row",
  "0607": "Lever Triceps Extension",
  "1313": "Lever Unilateral Row",
  "0609": "London Bridge",
  "3013": "Low Glute Bridge On Floor",
  "1352": "Lower Back Curl",
  "3582": "Lunge With Jump",
  "1688": "Lunge With Twist",
  "0613": "Lying (Side) Quads Stretch",
  "2312": "Lying Elbow To Knee",
  "0620": "Lying Leg Raise Flat Bench",
  "0865": "Lying Leg-Hip Raise",
  "1301": "Machine Inner Chest Press",
  "0624": "March Sit (Wall)",
  "1353": "Medicine Ball Catch And Overhead Throw",
  "1302": "Medicine Ball Chest Pass",
  "1303": "Medicine Ball Chest Push From 3 Point Stance",
  "1304": "Medicine Ball Chest Push Multiple Response",
  "1305": "Medicine Ball Chest Push Single Response",
  "1312": "Medicine Ball Chest Push With Run Release",
  "1701": "Medicine Ball Close Grip Push Up",
  "1354": "Medicine Ball Overhead Slam",
  "1750": "Medicine Ball Supine Chest Throw",
  "0627": "Mixed Grip Chin-Up",
  "3217": "Modified Hindu Push-Up (Male)",
  "1421": "Modified Push Up To Lower Arms",
  "0628": "Monster Walk",
  "0630": "Mountain Climber",
  "0631": "Muscle Up",
  "1401": "Muscle-Up (On Vertical Bar)",
  "2328": "Narrow Push-Up On Exercise Ball",
  "1403": "Neck Side Stretch",
  "0634": "Negative Crunch",
  "1495": "Oblique Crunch V. 2",
  "0635": "Oblique Crunches Floor",
  "0636": "Olympic Barbell Hammer Curl",
  "0637": "Olympic Barbell Triceps Extension",
  "1355": "One Arm Against Wall",
  "0638": "One Arm Chin-Up",
  "0639": "One Arm Dip",
  "0640": "One Arm Slam (With Medicine Ball)",
  "1773": "One Arm Towel Row",
  "1386": "One Leg Donkey Calf Raise",
  "1387": "One Leg Floor Calf Raise",
  "1476": "One Leg Squat",
  "0641": "Otis Up",
  "0642": "Outside Leg Kick Push-Up",
  "0643": "Overhead Triceps Stretch",
  "3147": "Pelvic Tilt",
  "1422": "Pelvic Tilt Into Bridge",
  "1388": "Peroneals Stretch",
  "3662": "Pike-To-Cobra Push-Up",
  "1306": "Plyo Push Up",
  "1687": "Posterior Step To Overhead Reach",
  "1389": "Posterior Tibialis Stretch",
  "3119": "Potty Squat",
  "3132": "Potty Squat With Support",
  "0648": "Power Clean",
  "3665": "Power Point Plank",
  "3203": "Prisoner Half Sit-Up (Male)",
  "1707": "Prone Twist On Stability Ball",
  "0651": "Pull Up (Neutral Grip)",
  "0650": "Pull-In (On Stability Ball)",
  "0652": "Pull-Up",
  "1689": "Push And Pull Bodyweight",
  "3638": "Push To Run",
  "1307": "Push Up On Bosu Ball",
  "0662": "Push-Up",
  "0653": "Push-Up (Bosu Ball)",
  "0655": "Push-Up (On Stability Ball)",
  "0656": "Push-Up (On Stability Ball)",
  "0659": "Push-Up (Wall)",
  "0658": "Push-Up (Wall) V. 2",
  "0660": "Push-Up Close-Grip Off Dumbbell",
  "0661": "Push-Up Inside Leg Kick",
  "0663": "Push-Up Medicine Ball",
  "1467": "Push-Up On Lower Arms",
  "3145": "Push-Up Plus",
  "0664": "Push-Up To Side Plank",
  "3533": "Quads",
  "3201": "Quarter Sit-Up",
  "3552": "Quick Feet V. 2",
  "0666": "Raise Single Arm Push-Up",
  "0668": "Rear Decline Bridge",
  "0669": "Rear Deltoid Stretch",
  "0670": "Rear Pull-Up",
  "1582": "Reclining Big Toe Pose With Rope",
  "3236": "Resistance Band Hip Thrusts On Knees (Female)",
  "3007": "Resistance Band Leg Extension",
  "3123": "Resistance Band Seated Biceps Curl",
  "3124": "Resistance Band Seated Chest Press",
  "3006": "Resistance Band Seated Hip Abduction",
  "3122": "Resistance Band Seated Shoulder Press",
  "3144": "Resistance Band Seated Straight Back Row",
  "0872": "Reverse Crunch",
  "0672": "Reverse Dip",
  "0673": "Reverse Grip Machine Lat Pulldown",
  "0674": "Reverse Grip Pull-Up",
  "0675": "Reverse Hyper Extension (On Stability Ball)",
  "1423": "Reverse Hyper On Flat Bench",
  "3663": "Reverse Plank With Leg Lift",
  "0677": "Ring Dips",
  "2571": "Rocking Frog Stretch",
  "0678": "Rocky Pull-Up Pulldown",
  "2208": "Roller Back Stretch",
  "2204": "Roller Body Saw",
  "2205": "Roller Hip Lat Stretch",
  "2202": "Roller Hip Stretch",
  "2206": "Roller Reverse Crunch",
  "2203": "Roller Seated Shoulder Flexor Depresor Retractor",
  "2209": "Roller Seated Single Leg Shoulder Flexor Depresor Retractor",
  "2207": "Roller Side Lat Stretch",
  "0680": "Rope Climb",
  "0685": "Run",
  "0684": "Run (Equipment)",
  "1585": "Runners Stretch",
  "0687": "Russian Twist",
  "3012": "Scapula Dips",
  "3021": "Scapula Push-Up",
  "0688": "Scapular Pull-Up",
  "3219": "Scissor Jumps (Male)",
  "1390": "Seated Calf Stretch (Male)",
  "1424": "Seated Glute Stretch",
  "0689": "Seated Leg Raise",
  "0690": "Seated Lower Back Stretch",
  "2567": "Seated Piriformis Stretch",
  "0691": "Seated Side Crunch (Wall)",
  "1587": "Seated Wide Angle Pose Sequence",
  "0697": "Self Assisted Inverse Leg Curl",
  "1766": "Self Assisted Inverse Leg Curl",
  "0696": "Self Assisted Inverse Leg Curl (On Floor)",
  "3222": "Semi Squat Jump (Male)",
  "3656": "Short Stride Run",
  "1763": "Shoulder Grip Pull-Up",
  "3699": "Shoulder Tap",
  "0699": "Shoulder Tap Push-Up",
  "1774": "Side Bridge Hip Abduction",
  "0705": "Side Bridge V. 2",
  "0709": "Side Hip (On Parallel Bars)",
  "0710": "Side Hip Abduction",
  "1358": "Side Lying Floor Stretch",
  "3667": "Side Lying Hip Adduction (Male)",
  "1775": "Side Plank Hip Adduction",
  "0716": "Side Push Neck Stretch",
  "0717": "Side Push-Up",
  "0721": "Side Wrist Pull Stretch",
  "0720": "Side-To-Side Chin",
  "3213": "Side-To-Side Toe Touch (Male)",
  "0725": "Single Arm Push-Up",
  "3645": "Single Leg Bridge With Outstretched Leg",
  "0727": "Single Leg Calf Raise (On A Dumbbell)",
  "0730": "Single Leg Platform Slide",
  "1759": "Single Leg Squat (Pistol) Male",
  "1489": "Sissy Squat",
  "0735": "Sit-Up V. 2",
  "3679": "Sit-Up With Arms On Chest",
  "3361": "Skater Hops",
  "2142": "Ski Ergometer",
  "3671": "Ski Step",
  "3304": "Skin The Cat",
  "1425": "Sled 45 Degrees One Leg Press",
  "0738": "Sled 45В° Calf Press",
  "0739": "Sled 45В° Leg Press",
  "1464": "Sled 45В° Leg Press (Back Pov)",
  "1463": "Sled 45° Leg Press (Side Pov)",
  "0740": "Sled 45В° Leg Wide Press",
  "1391": "Sled Calf Press On Leg Press",
  "0741": "Sled Closer Hack Squat",
  "0742": "Sled Forward Angled Calf Raise",
  "0743": "Sled Hack Squat",
  "2334": "Sled Lying Calf Press",
  "0744": "Sled Lying Squat",
  "1392": "Sled One Leg Calf Press On Leg Press",
  "1496": "Sledge Hammer",
  "0746": "Smith Back Shrug",
  "0747": "Smith Behind Neck Press",
  "0748": "Smith Bench Press",
  "0749": "Smith Bent Knee Good Morning",
  "1359": "Smith Bent Over Row",
  "0750": "Smith Chair Squat",
  "0751": "Smith Close-Grip Bench Press",
  "0752": "Smith Deadlift",
  "0753": "Smith Decline Bench Press",
  "0754": "Smith Decline Reverse-Grip Press",
  "1433": "Smith Front Squat (Clean Grip)",
  "3281": "Smith Full Squat",
  "0755": "Smith Hack Squat",
  "0756": "Smith Hip Raise",
  "0757": "Smith Incline Bench Press",
  "0758": "Smith Incline Reverse-Grip Press",
  "0759": "Smith Incline Shoulder Raises",
  "0760": "Smith Leg Press",
  "1434": "Smith Low Bar Squat",
  "1683": "Smith Machine Bicep Curl",
  "1625": "Smith Machine Decline Close Grip Bench Press",
  "1752": "Smith Machine Incline Tricep Extension",
  "1626": "Smith Machine Reverse Decline Close Grip Bench Press",
  "0761": "Smith Narrow Row",
  "1360": "Smith One Arm Row",
  "1393": "Smith One Leg Floor Calf Raise",
  "0762": "Smith Rear Delt Row",
  "0763": "Smith Reverse Calf Raises",
  "1394": "Smith Reverse Calf Raises",
  "1361": "Smith Reverse Grip Bent Over Row",
  "0764": "Smith Reverse-Grip Press",
  "1395": "Smith Seated One Leg Calf Raise",
  "0765": "Smith Seated Shoulder Press",
  "1426": "Smith Seated Wrist Curl",
  "0766": "Smith Shoulder Press",
  "0767": "Smith Shrug",
  "0768": "Smith Single Leg Split Squat",
  "0769": "Smith Sprint Lunge",
  "0770": "Smith Squat",
  "0771": "Smith Standing Back Wrist Curl",
  "0772": "Smith Standing Behind Head Military Press",
  "0773": "Smith Standing Leg Calf Raise",
  "0774": "Smith Standing Military Press",
  "3142": "Smith Sumo Squat",
  "1396": "Smith Toe Raise",
  "0775": "Smith Upright Row",
  "1308": "Smith Wide Grip Bench Press",
  "1309": "Smith Wide Grip Decline Bench Press",
  "0776": "Snatch Pull",
  "0777": "Spell Caster",
  "1362": "Sphinx",
  "0778": "Spider Crawl Push Up",
  "1363": "Spine Stretch",
  "2329": "Spine Twist",
  "2368": "Split Squats",
  "0786": "Squat Jerk",
  "1705": "Squat On Bosu Ball",
  "1685": "Squat To Overhead Reach",
  "1686": "Squat To Overhead Reach With Twist",
  "2297": "Stability Ball Crunch (Full Range Hands Behind Head)",
  "3291": "Stalder Press",
  "3669": "Standing Archer",
  "0788": "Standing Behind Neck Press",
  "1490": "Standing Calf Raise (On A Staircase)",
  "1397": "Standing Calves",
  "1398": "Standing Calves Calf Stretch",
  "1599": "Standing Hamstring And Calf Stretch With Strap",
  "0794": "Standing Lateral Stretch",
  "1364": "Standing Pelvic Tilt",
  "0795": "Standing Single Leg Curl",
  "0796": "Standing Wheel Rollerout",
  "3223": "Star Jump (Male)",
  "2138": "Stationary Bike Run V. 3",
  "0798": "Stationary Bike Walk",
  "3314": "Straddle Maltese",
  "3298": "Straddle Planche",
  "1427": "Straight Leg Outer Hip Abductor",
  "0803": "Superman Push-Up",
  "0805": "Suspended Abdominal Fallout",
  "0806": "Suspended Push-Up",
  "0807": "Suspended Reverse Crunch",
  "0808": "Suspended Row",
  "0809": "Suspended Split Squat",
  "3433": "Swimmer Kicks V. 2 (Male)",
  "3318": "Swing 360",
  "1753": "Three Bench Dip",
  "2459": "Tire Flip",
  "0811": "Trap Bar Deadlift",
  "0814": "Triceps Dip",
  "0812": "Triceps Dip (Bench Leg)",
  "0813": "Triceps Dip (Between Benches)",
  "0815": "Triceps Dips Floor",
  "0816": "Triceps Press",
  "0817": "Triceps Stretch",
  "0871": "Tuck Crunch",
  "0818": "Twin Handle Parallel Grip Lat Pulldown",
  "1466": "Twist Hip Lift",
  "2802": "Twisted Leg Raise",
  "2801": "Twisted Leg Raise (Female)",
  "3231": "Two Toe Touch (Male)",
  "1365": "Upper Back Stretch",
  "1366": "Upward Facing Dog",
  "3420": "V-Sit On Floor",
  "0826": "Vertical Leg Raise (On Parallel Bars)",
  "2141": "Walk Elliptical Cross Trainer",
  "3655": "Walking High Knees Lunge",
  "1460": "Walking Lunge",
  "3666": "Walking On Incline Treadmill",
  "2311": "Walking On Stepmill",
  "0830": "Weighted Bench Dip",
  "2987": "Weighted Close Grip Chin-Up On Dip Cage",
  "3643": "Weighted Cossack Squats (Male)",
  "0832": "Weighted Crunch",
  "3670": "Weighted Decline Sit-Up",
  "0833": "Weighted Donkey Calf Raise",
  "1310": "Weighted Drop Push Up",
  "2135": "Weighted Front Plank",
  "0834": "Weighted Front Raise",
  "0866": "Weighted Hanging Leg-Hip Raise",
  "0835": "Weighted Hyperextension (On Stability Ball)",
  "3641": "Weighted Kneeling Step With Swing",
  "3644": "Weighted Lunge With Swing",
  "3286": "Weighted Muscle Up",
  "3312": "Weighted Muscle Up (On Bar)",
  "3290": "Weighted One Hand Pull Up",
  "0840": "Weighted Overhead Crunch (On Stability Ball)",
  "0841": "Weighted Pull-Up",
  "0844": "Weighted Round Arm",
  "0846": "Weighted Russian Twist",
  "0845": "Weighted Russian Twist (Legs Up)",
  "2371": "Weighted Russian Twist V. 2",
  "0847": "Weighted Seated Bicep Curl (On Stability Ball)",
  "0849": "Weighted Seated Twist (On Stability Ball)",
  "0850": "Weighted Side Bend (On Stability Ball)",
  "0851": "Weighted Sissy Squat",
  "0852": "Weighted Squat",
  "0853": "Weighted Standing Curl",
  "0854": "Weighted Standing Hand Squeeze",
  "3313": "Weighted Straight Bar Dip",
  "3642": "Weighted Stretch Lunge",
  "0856": "Weighted Svend Press",
  "1754": "Weighted Three Bench Dips",
  "1755": "Weighted Tricep Dips",
  "1767": "Weighted Triceps Dip On High Parallel Bars",
  "0857": "Wheel Rollerout",
  "3637": "Wheel Run",
  "1429": "Wide Grip Pull-Up",
  "1367": "Wide Grip Rear Pull-Up",
  "1311": "Wide Hand Push Up",
  "2363": "Wide-Grip Chest Dip On High Parallel Bars",
  "0858": "Wind Sprints",
  "1604": "World Greatest Stretch",
  "1428": "Wrist Circles",
  "0859": "Wrist Rollerer"
}
```

## trackingProgress/dashboardSync.py
```py
import sqlite3

import pandas as pd
import smartwatch
import utility

# AA Soglia Di Affidabilita Per Le Misurazioni Corporee
# BB Le Misurazioni Precedenti A Questa Data Sono State Rilevate Con Minore Rigore
SOGLIA_AFFIDABILITA_MISURE = "2026-06-01"


# AA Creazione Delle Tabelle Del Database Dashboard, Se Non Esistono Ancora
def initializeDashboardDB(DASHBOARD_DB_PATH):
    conn = sqlite3.connect(DASHBOARD_DB_PATH)
    cursor = conn.cursor()

    # BB Dominio Smartwatch (Dati Ad Alta Frequenza Da Gadgetbridge)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS smartwatch_activity_raw (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data TEXT NOT NULL,
            ora TEXT NOT NULL,
            data_ora TEXT NOT NULL,
            passi INTEGER,
            frequenza_cardiaca INTEGER,
            spo2 REAL,
            livello_stress INTEGER,
            calorie_attive REAL,
            distanza_m REAL,
            tipo_attivita INTEGER
        );
    """)
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_activity_raw_data ON smartwatch_activity_raw(data);")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS smartwatch_daily_summary (
            data TEXT PRIMARY KEY,
            passi_totali INTEGER,
            calorie_totali REAL,
            calorie_attive REAL,
            frequenza_riposo INTEGER,
            frequenza_media INTEGER,
            frequenza_minima INTEGER,
            ora_battito_min TEXT,
            frequenza_massima INTEGER,
            ora_battito_max TEXT,
            stress_medio INTEGER,
            stress_massimo INTEGER,
            stress_minimo INTEGER,
            spo2_medio REAL,
            ore_in_piedi REAL,
            indice_vitalita INTEGER
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS smartwatch_sleep_sessions (
            data TEXT PRIMARY KEY,
            inizio_sonno TEXT,
            fine_sonno TEXT,
            durata_totale_min INTEGER,
            sonno_profondo_min INTEGER,
            sonno_leggero_min INTEGER,
            sonno_rem_min INTEGER,
            tempo_sveglio_min INTEGER
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS smartwatch_sleep_stages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data TEXT NOT NULL,
            inizio_fase TEXT NOT NULL,
            fase TEXT,
            durata_min REAL
        );
    """)
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_sleep_stages_data ON smartwatch_sleep_stages(data);")

    # BB Dominio Tracking (Specchio Dei Fogli Excel)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS misure (
            data_misurazione TEXT PRIMARY KEY,
            peso_kg REAL,
            circ_collo_cm REAL,
            circ_vita_cm REAL,
            circ_fianchi_cm REAL,
            circ_braccio_cm REAL,
            circ_coscia_cm REAL,
            massa_grassa_pct REAL,
            massa_magra_kg REAL,
            metabolismo_basale REAL,
            fabbisogno_giornaliero REAL,
            affidabile INTEGER NOT NULL DEFAULT 1
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS dieta (
            data_inizio TEXT PRIMARY KEY,
            data_fine TEXT,
            durata INTEGER,
            kcal INTEGER,
            deficit_teorico INTEGER,
            carbo_g INTEGER,
            grassi_g INTEGER,
            proteine_g INTEGER,
            proteine_g_kg REAL,
            pct_carbo REAL,
            pct_grassi REAL,
            pct_proteine REAL,
            note TEXT
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS personale (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            sesso TEXT,
            altezza_cm REAL,
            data_nascita TEXT,
            eta INTEGER,
            peso_corrente_kg REAL,
            massa_magra_corrente_kg REAL,
            bmr_mifflin REAL,
            bmr_katch REAL,
            tdee_corrente REAL,
            deficit_corrente REAL,
            ultimo_aggiornamento TEXT
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS allenamento (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data TEXT NOT NULL,
            durata_allenamento REAL,
            nome_scheda TEXT,
            nome_esercizio TEXT,
            indice_serie INTEGER,
            ripetizioni_serie INTEGER,
            peso_serie REAL,
            volume_serie INTEGER,
            massimale_stimato_serie INTEGER,
            note TEXT
        );
    """)
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_allenamento_data ON allenamento(data);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_allenamento_esercizio ON allenamento(nome_esercizio);")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS palestra (
            nome_esercizio TEXT PRIMARY KEY,
            schema TEXT,
            volume_totale_kg INTEGER,
            data TEXT,
            numero_serie INTEGER,
            ripetizioni_medie INTEGER,
            peso_medio REAL,
            massimale_stimato_1rm INTEGER,
            note TEXT
        );
    """)

    # BB Tabella Derivata (Calcolata Durante La Sync A Partire Da Misure, Dieta E Personale)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS profilo_storico (
            data TEXT PRIMARY KEY,
            eta INTEGER,
            bmr_mifflin REAL,
            bmr_katch REAL,
            tdee REAL,
            deficit_teorico INTEGER,
            affidabile INTEGER NOT NULL DEFAULT 1
        );
    """)

    conn.commit()
    conn.close()


# AA Sincronizzazione Dei Dati Smartwatch (Attivita, Riepilogo Giornaliero, Sonno) Verso Il Database Dashboard
def syncSmartwatchData(DASHBOARD_DB_PATH, activityData, dailySummary, sleepSessions, sleepStages):
    tagDashboard = f"{utility.CLR_DASHBOARD}[DASHBOARD]{utility.CLR_RESET}"

    conn = sqlite3.connect(DASHBOARD_DB_PATH)

    # BB Specchio Dell'Attivita Al Minuto
    if not activityData.empty:
        activityDf = activityData.copy()
        activityDf["Data"] = pd.to_datetime(activityDf["Data"]).dt.strftime("%Y-%m-%d")
        activityDf["Data Ora"] = pd.to_datetime(activityDf["Data Ora"]).dt.strftime("%Y-%m-%d %H:%M:%S")

        renameMapActivity = {
            "Data": "data",
            "Ora": "ora",
            "Data Ora": "data_ora",
            "Passi": "passi",
            "Frequenza Cardiaca (bpm)": "frequenza_cardiaca",
            "SpO2 (%)": "spo2",
            "Livello Stress": "livello_stress",
            "Calorie Attive (kcal)": "calorie_attive",
            "Distanza (m)": "distanza_m",
            "Tipo Attivita": "tipo_attivita",
        }
        activityDf = activityDf.rename(columns=renameMapActivity)

        conn.execute("DELETE FROM smartwatch_activity_raw;")
        activityDf.to_sql("smartwatch_activity_raw", conn, if_exists="append", index=False)
        print(f"{tagDashboard} Attivita Specchiata: {utility.CLR_BOLD}{len(activityDf)}{utility.CLR_RESET} Righe.")

    # BB Specchio Del Riepilogo Giornaliero
    if not dailySummary.empty:
        summaryDf = dailySummary.copy()
        summaryDf["Data"] = pd.to_datetime(summaryDf["Data"]).dt.strftime("%Y-%m-%d")

        renameMapSummary = {
            "Data": "data",
            "Passi Totali": "passi_totali",
            "Calorie Totali (kcal)": "calorie_totali",
            "Calorie Attive (kcal)": "calorie_attive",
            "Frequenza Riposo (bpm)": "frequenza_riposo",
            "Frequenza Media (bpm)": "frequenza_media",
            "Frequenza Minima (bpm)": "frequenza_minima",
            "Ora Battito Min": "ora_battito_min",
            "Frequenza Massima (bpm)": "frequenza_massima",
            "Ora Battito Max": "ora_battito_max",
            "Stress Medio": "stress_medio",
            "Stress Massimo": "stress_massimo",
            "Stress Minimo": "stress_minimo",
            "SpO2 Medio (%)": "spo2_medio",
            "Ore In Piedi": "ore_in_piedi",
            "Indice Vitalita": "indice_vitalita",
        }
        summaryDf = summaryDf.rename(columns=renameMapSummary)

        conn.execute("DELETE FROM smartwatch_daily_summary;")
        summaryDf.to_sql("smartwatch_daily_summary", conn, if_exists="append", index=False)
        print(f"{tagDashboard} Riepilogo Giornaliero Specchiato: {utility.CLR_BOLD}{len(summaryDf)}{utility.CLR_RESET} Righe.")

    # BB Specchio Delle Sessioni Di Sonno
    if not sleepSessions.empty:
        sessionsDf = sleepSessions.copy()
        sessionsDf["Data"] = pd.to_datetime(sessionsDf["Data"]).dt.strftime("%Y-%m-%d")
        sessionsDf["Inizio Sonno"] = pd.to_datetime(sessionsDf["Inizio Sonno"]).dt.strftime("%Y-%m-%d %H:%M:%S")
        sessionsDf["Fine Sonno"] = pd.to_datetime(sessionsDf["Fine Sonno"]).dt.strftime("%Y-%m-%d %H:%M:%S")

        renameMapSessions = {
            "Data": "data",
            "Inizio Sonno": "inizio_sonno",
            "Fine Sonno": "fine_sonno",
            "Durata Totale (min)": "durata_totale_min",
            "Sonno Profondo (min)": "sonno_profondo_min",
            "Sonno Leggero (min)": "sonno_leggero_min",
            "Sonno REM (min)": "sonno_rem_min",
            "Tempo Sveglio (min)": "tempo_sveglio_min",
        }
        sessionsDf = sessionsDf.rename(columns=renameMapSessions)

        conn.execute("DELETE FROM smartwatch_sleep_sessions;")
        sessionsDf.to_sql("smartwatch_sleep_sessions", conn, if_exists="append", index=False)
        print(f"{tagDashboard} Sessioni Sonno Specchiate: {utility.CLR_BOLD}{len(sessionsDf)}{utility.CLR_RESET} Notti.")

    # BB Specchio Della Timeline Delle Fasi Di Sonno
    if not sleepStages.empty:
        stagesDf = sleepStages.copy()
        stagesDf["Data"] = pd.to_datetime(stagesDf["Data"]).dt.strftime("%Y-%m-%d")
        stagesDf["Inizio Fase"] = pd.to_datetime(stagesDf["Inizio Fase"]).dt.strftime("%Y-%m-%d %H:%M:%S")

        renameMapStages = {
            "Data": "data",
            "Inizio Fase": "inizio_fase",
            "Fase": "fase",
            "Durata (min)": "durata_min",
        }
        stagesDf = stagesDf.rename(columns=renameMapStages)

        conn.execute("DELETE FROM smartwatch_sleep_stages;")
        stagesDf.to_sql("smartwatch_sleep_stages", conn, if_exists="append", index=False)
        print(f"{tagDashboard} Fasi Sonno Specchiate: {utility.CLR_BOLD}{len(stagesDf)}{utility.CLR_RESET} Righe.")

    conn.commit()
    conn.close()

    print(f"\n{tagDashboard} {utility.CLR_BOLD}Sincronizzazione Smartwatch Completata!{utility.CLR_RESET}\n")


# AA Sincronizzazione Dei Dati Excel (Misure, Dieta, Personale, Allenamento, Palestra) Verso Il Database Dashboard
def syncTrackingMirror(DASHBOARD_DB_PATH, excelData):
    tagDashboard = f"{utility.CLR_DASHBOARD}[DASHBOARD]{utility.CLR_RESET}"

    conn = sqlite3.connect(DASHBOARD_DB_PATH)

    # BB Specchio Della Scheda Dati Misure
    misureDf = excelData["Dati Misure"].copy()
    if not misureDf.empty:
        misureDf["Data Misurazione"] = pd.to_datetime(misureDf["Data Misurazione"]).dt.strftime("%Y-%m-%d")
        misureDf["affidabile"] = (misureDf["Data Misurazione"] >= SOGLIA_AFFIDABILITA_MISURE).astype(int)

        renameMapMisure = {
            "Data Misurazione": "data_misurazione",
            "Peso (Kg)": "peso_kg",
            "Circonferenza Collo (cm)": "circ_collo_cm",
            "Circonferenza Vita (cm)": "circ_vita_cm",
            "Circonferenza Fianchi (cm)": "circ_fianchi_cm",
            "Circonferenza Braccio (cm)": "circ_braccio_cm",
            "Circonferenza Coscia (cm)": "circ_coscia_cm",
            "Massa Grassa (%)": "massa_grassa_pct",
            "Massa Magra (Kg)": "massa_magra_kg",
            "Metabolismo Basale": "metabolismo_basale",
            "Fabbisogno Giornaliero": "fabbisogno_giornaliero",
        }
        misureDf = misureDf.rename(columns=renameMapMisure)

        colonneMisure = [
            "data_misurazione", "peso_kg", "circ_collo_cm", "circ_vita_cm", "circ_fianchi_cm",
            "circ_braccio_cm", "circ_coscia_cm", "massa_grassa_pct", "massa_magra_kg",
            "metabolismo_basale", "fabbisogno_giornaliero", "affidabile"
        ]
        misureDf = misureDf[colonneMisure]

        conn.execute("DELETE FROM misure;")
        misureDf.to_sql("misure", conn, if_exists="append", index=False)
        print(f"{tagDashboard} Misure Specchiate: {utility.CLR_BOLD}{len(misureDf)}{utility.CLR_RESET} Righe.")

    # BB Specchio Della Scheda Dati Dieta
    dietaDf = excelData["Dati Dieta"].copy()
    if not dietaDf.empty:
        dietaDf["Data Inizio"] = pd.to_datetime(dietaDf["Data Inizio"]).dt.strftime("%Y-%m-%d")

        # CC La Fase Ancora Aperta Non Ha Data Fine: Deve Restare Nulla, Non Diventare La Stringa "NaT"
        dataFineOBJ = pd.to_datetime(dietaDf["Data Fine"])
        dietaDf["Data Fine"] = dataFineOBJ.dt.strftime("%Y-%m-%d")
        dietaDf.loc[dataFineOBJ.isna(), "Data Fine"] = None

        renameMapDieta = {
            "Data Inizio": "data_inizio",
            "Data Fine": "data_fine",
            "Durata": "durata",
            "Kcal": "kcal",
            "Deficit Teorico": "deficit_teorico",
            "Carbo (g)": "carbo_g",
            "Grassi (g)": "grassi_g",
            "Proteine (g)": "proteine_g",
            "Proteine (g/Kg)": "proteine_g_kg",
            "% Carbo": "pct_carbo",
            "% Grassi": "pct_grassi",
            "% Proteine": "pct_proteine",
            "Note": "note",
        }
        dietaDf = dietaDf.rename(columns=renameMapDieta)

        conn.execute("DELETE FROM dieta;")
        dietaDf.to_sql("dieta", conn, if_exists="append", index=False)
        print(f"{tagDashboard} Dieta Specchiata: {utility.CLR_BOLD}{len(dietaDf)}{utility.CLR_RESET} Fasi.")

    # BB Specchio Della Scheda Dati Personali (Riga Singola, Layout Verticale Parametro/Valore)
    personalDf = excelData["Dati Personali"]

    # CC Piccola Funzione Di Appoggio Per Leggere Un Valore Dato Il Nome Del Parametro
    def getParam(nome):
        match = personalDf.loc[personalDf["Parametro"] == nome, "Valore"]
        if match.empty:
            return None
        return match.iloc[0]

    sesso = getParam("Sesso")
    altezza = getParam("Altezza (cm)")
    dataNascita = getParam("Data Di Nascita")
    eta = getParam("Età")
    pesoCorrente = getParam("Peso Corrente (Kg)")
    massaMagraCorrente = getParam("Massa Magra Corrente (Kg)")
    bmrMifflinCorrente = getParam("BMR Mifflin-St Jeor (Kcal)")
    bmrKatchCorrente = getParam("BMR Katch-McArdle (Kcal)")
    tdeeCorrente = getParam("TDEE Corrente Pesato (Kcal)")
    deficitCorrente = getParam("Deficit Corrente (Kcal)")
    ultimoAggiornamento = getParam("Ultimo Aggiornamento")

    if dataNascita is not None:
        dataNascita = pd.to_datetime(dataNascita).strftime("%Y-%m-%d")
    if ultimoAggiornamento is not None:
        ultimoAggiornamento = str(ultimoAggiornamento)

    conn.execute("DELETE FROM personale;")
    conn.execute("""
        INSERT INTO personale (
            id, sesso, altezza_cm, data_nascita, eta, peso_corrente_kg,
            massa_magra_corrente_kg, bmr_mifflin, bmr_katch, tdee_corrente,
            deficit_corrente, ultimo_aggiornamento
        ) VALUES (1, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, (
        sesso, altezza, dataNascita, eta, pesoCorrente,
        massaMagraCorrente, bmrMifflinCorrente, bmrKatchCorrente, tdeeCorrente,
        deficitCorrente, ultimoAggiornamento
    ))
    print(f"{tagDashboard} Profilo Personale Specchiato.")

    # BB Specchio Della Scheda Dati Allenamento
    allenamentoDf = excelData["Dati Allenamento"].copy()
    if not allenamentoDf.empty:
        allenamentoDf["Data"] = pd.to_datetime(allenamentoDf["Data"]).dt.strftime("%Y-%m-%d")

        renameMapAllenamento = {
            "Data": "data",
            "Durata Allenamento": "durata_allenamento",
            "Nome Scheda": "nome_scheda",
            "Nome Esercizio": "nome_esercizio",
            "Indice Serie": "indice_serie",
            "Ripetizioni Serie": "ripetizioni_serie",
            "Peso Serie": "peso_serie",
            "Volume Serie": "volume_serie",
            "Massimale Stimato Serie": "massimale_stimato_serie",
            "Note Post Allenamento": "note",
        }
        allenamentoDf = allenamentoDf.rename(columns=renameMapAllenamento)

        conn.execute("DELETE FROM allenamento;")
        allenamentoDf.to_sql("allenamento", conn, if_exists="append", index=False)
        print(f"{tagDashboard} Allenamenti Specchiati: {utility.CLR_BOLD}{len(allenamentoDf)}{utility.CLR_RESET} Serie.")

    # BB Specchio Della Scheda Dati Palestra
    palestraDf = excelData["Dati Palestra"].copy()
    if not palestraDf.empty:
        palestraDf["Data"] = pd.to_datetime(palestraDf["Data"]).dt.strftime("%Y-%m-%d")

        renameMapPalestra = {
            "Nome Esercizio": "nome_esercizio",
            "Schema": "schema",
            "Volume Totale (Kg)": "volume_totale_kg",
            "Data": "data",
            "Numero Serie": "numero_serie",
            "Ripetizioni Medie": "ripetizioni_medie",
            "Peso Medio": "peso_medio",
            "Massimale Stimato (1RM)": "massimale_stimato_1rm",
            "Note Post Allenamento": "note",
        }
        palestraDf = palestraDf.rename(columns=renameMapPalestra)

        conn.execute("DELETE FROM palestra;")
        palestraDf.to_sql("palestra", conn, if_exists="append", index=False)
        print(f"{tagDashboard} Bacheca Record Specchiata: {utility.CLR_BOLD}{len(palestraDf)}{utility.CLR_RESET} Esercizi.")

    # BB Calcolo Della Tabella Derivata Profilo Storico (Eta, BMR Mifflin E Deficit Per Ogni Misurazione)
    # CC Serve Sesso, Altezza E Data Di Nascita Dal Profilo Personale, Gia Estratti Sopra
    if not misureDf.empty and dataNascita is not None and altezza is not None and sesso is not None:
        dobOBJ = pd.to_datetime(dataNascita)
        altezzaFloat = float(altezza)

        profiloRows = []
        for _, riga in misureDf.iterrows():
            dataMisurazioneOBJ = pd.to_datetime(riga["data_misurazione"])
            pesoRiga = riga["peso_kg"]

            # DD Calcolo Dell'Eta Alla Data Della Misurazione (Stessa Logica Di personal.py)
            etaRiga = dataMisurazioneOBJ.year - dobOBJ.year - (
                (dataMisurazioneOBJ.month, dataMisurazioneOBJ.day) < (dobOBJ.month, dobOBJ.day)
            )

            # DD Calcolo Del BMR Mifflin-St Jeor Alla Data Della Misurazione
            if sesso == "M":
                bmrMifflinRiga = (10 * pesoRiga) + (6.25 * altezzaFloat) - (5 * etaRiga) + 5
            else:
                bmrMifflinRiga = (10 * pesoRiga) + (6.25 * altezzaFloat) - (5 * etaRiga) - 161

            # DD Ricerca Della Fase Dieta Attiva Alla Data Della Misurazione, Se Presente
            deficitRiga = None
            if not dietaDf.empty:
                faseAttiva = dietaDf[
                    (dietaDf["data_inizio"] <= riga["data_misurazione"]) &
                    ((dietaDf["data_fine"].isna()) | (dietaDf["data_fine"] >= riga["data_misurazione"]))
                ]
                if not faseAttiva.empty:
                    deficitRiga = int(faseAttiva.iloc[-1]["deficit_teorico"])

            profiloRows.append({
                "data": riga["data_misurazione"],
                "eta": int(etaRiga),
                "bmr_mifflin": round(bmrMifflinRiga, 0),
                "bmr_katch": riga["metabolismo_basale"],
                "tdee": riga["fabbisogno_giornaliero"],
                "deficit_teorico": deficitRiga,
                "affidabile": riga["affidabile"],
            })

        profiloDf = pd.DataFrame(profiloRows)

        conn.execute("DELETE FROM profilo_storico;")
        profiloDf.to_sql("profilo_storico", conn, if_exists="append", index=False)
        print(f"{tagDashboard} Profilo Storico Calcolato: {utility.CLR_BOLD}{len(profiloDf)}{utility.CLR_RESET} Righe.")

    conn.commit()
    conn.close()

    print(f"\n{tagDashboard} {utility.CLR_BOLD}Sincronizzazione Dati Tracking Completata!{utility.CLR_RESET}\n")


# AA Blocco Di Test Diretto Dello Script
if __name__ == "__main__":
    EXCEL_PATH = "/mnt/c/Users/cicci/Documents/Appunti_E_Personale/trackingProgressi/trackingProgressi.xlsx"
    SMARTWATCH_DB = "/mnt/c/Users/cicci/Documents/Appunti_E_Personale/trackingProgressi/gadgetBridgeSync/Gadgetbridge.db"
    DASHBOARD_DB_PATH = "/home/lag/## dashboardData.db"

    excelData = {
        "Dati Personali": pd.read_excel(EXCEL_PATH, sheet_name="Dati Personali"),
        "Dati Misure": pd.read_excel(EXCEL_PATH, sheet_name="Dati Misure"),
        "Dati Dieta": pd.read_excel(EXCEL_PATH, sheet_name="Dati Dieta"),
        "Dati Allenamento": pd.read_excel(EXCEL_PATH, sheet_name="Dati Allenamento"),
        "Dati Palestra": pd.read_excel(EXCEL_PATH, sheet_name="Dati Palestra"),
    }

    initializeDashboardDB(DASHBOARD_DB_PATH)

    activityData, dailySummary, sleepSessions, sleepStages = smartwatch.processSmartwatchData(SMARTWATCH_DB)
    syncSmartwatchData(DASHBOARD_DB_PATH, activityData, dailySummary, sleepSessions, sleepStages)

    syncTrackingMirror(DASHBOARD_DB_PATH, excelData)
```

## trackingProgress/diet.py
```py
from copy import copy

import numpy as np
import openpyxl
import pandas as pd
import utility


def updateDietData(excelData, EXCEL_PATH):
    # AA Definizione Dei Tag Colorati Per La Visualizzazione
    tagDieta = f"{utility.CLR_DIETA}[DIETA]{utility.CLR_RESET}"
    tagErrore = f"{utility.CLR_ERRORE}[ERRORE]{utility.CLR_RESET}"

    # AA Caricamento E Inizializzazione Dei Dati Da Excel
    dietData = excelData['Dati Dieta']
    measureData = excelData['Dati Misure']

    # BB Controllo Di Sicurezza Sulla Presenza Di Misurazioni Corporee Precedenti
    # CC Impedisce L'Inserimento Se Non Abbiamo Peso E TDEE Di Riferimento
    if len(measureData) == 0:
        print(f"\n{tagErrore} Nessuna Misurazione Rilevata Nella Scheda 'Dati Misure'.")
        print(f"{tagErrore} Inserisci Almeno Una Misurazione Corporea Prima Di Configurare La Dieta.\n")
        return

    # BB Controllo Se La Scheda Dati Dieta È Vuota Per Evitare Errori Di Indice
    if len(dietData) == 0:
        print(f"{tagDieta} Nessun Record Dieta Precedente Rilevato.\n")
    else:
        # BB Recupero E Stampa Dell'Ultimo Record Dieta Registrato
        # CC Lettura Dei Valori Dell'Ultima Riga Nel Foglio Excel
        lastRow = dietData.iloc[-1]
        dataInizioLastOBJ = pd.to_datetime(lastRow['Data Inizio'])

        # CC Controllo Se La Data Fine Dell'Ultimo Record È Vuota (Piano Ancora Attivo)
        if pd.isna(lastRow['Data Fine']):
            print(f"\n{tagDieta} Rilevato Un Piano Alimentare Precedente Ancora Attivo (Senza Data Fine).")
            print(f"{tagDieta} Data Inizio Del Piano Attivo: {utility.CLR_BOLD}{dataInizioLastOBJ.strftime('%d-%m-%Y')}{utility.CLR_RESET}")
            
            # DD Richiesta Obbligatoria Della Data Fine Per Chiudere Il Piano Precedente
            while True:
                dataFineLastStr = input(f"{tagDieta} Inserisci La Data Fine Per Chiudere Questo Piano (GG-MM-AAAA): ")
                try:
                    dataFineLastOBJ = pd.to_datetime(dataFineLastStr, format='%d-%m-%Y')
                    if dataFineLastOBJ.date() < dataInizioLastOBJ.date():
                        print(f"{tagErrore} La Data Fine Deve Essere Successiva O Uguale Alla Data Inizio ({dataInizioLastOBJ.strftime('%d-%m-%Y')}).")
                        continue
                    break
                except ValueError:
                    print(f"{tagErrore} Formato Data Non Valido. Riprova.")
            
            # DD Calcolo Della Durata Per Il Piano Precedente
            durataLast = (dataFineLastOBJ.date() - dataInizioLastOBJ.date()).days + 1
            
            # EE Scrittura Della Chiusura Nel File Excel Fisico Con Openpyxl
            excelFile = openpyxl.load_workbook(EXCEL_PATH)
            dietSheet = excelFile['Dati Dieta']
            lastRowIdx = dietSheet.max_row
            
            # EE Colonna 2 Per Data Fine E Colonna 3 Per Durata
            dietSheet.cell(row=lastRowIdx, column=2).value = dataFineLastOBJ.date() # type: ignore
            dietSheet.cell(row=lastRowIdx, column=3).value = int(durataLast)        # type: ignore
            
            excelFile.save(EXCEL_PATH)
            excelFile.close()
            
            # EE Sincronizzazione Del DataFrame In Memoria
            dietData.loc[dietData.index[-1], 'Data Fine'] = dataFineLastOBJ
            dietData.loc[dietData.index[-1], 'Durata'] = int(durataLast)
            excelData['Dati Dieta'] = dietData
            
            print(f"{tagDieta} {utility.CLR_BOLD}Piano Precedente Chiuso Con Successo!{utility.CLR_RESET}\n")
            
            # EE Ricarica Della Riga Aggiornata Per La Stampa Successiva
            lastRow = dietData.iloc[-1]

        # CC Recupero E Stampa Dell'Ultimo Record Dieta Registrato (Ora Sicuramente Chiuso)
        dataInizioOBJ = pd.to_datetime(lastRow['Data Inizio'])
        dataFineOBJ = pd.to_datetime(lastRow['Data Fine'])
        
        # DD Formattazione Protetta Delle Date In Stringhe Per La Stampa A Video
        dataInizio = dataInizioOBJ.strftime("%d-%m-%Y") if not pd.isna(dataInizioOBJ) else "Non Specificata"
        dataFine = dataFineOBJ.strftime("%d-%m-%Y") if not pd.isna(dataFineOBJ) else "In Corso"
        
        kcal = lastRow['Kcal']
        carbo = lastRow['Carbo (g)']
        grassi = lastRow['Grassi (g)']
        proteine = lastRow['Proteine (g)']

        print(f"{tagDieta} Ultima Entry: {utility.CLR_BOLD}{dataInizio} - {dataFine}{utility.CLR_RESET} | "
              f"Kcal: {utility.CLR_BOLD}{kcal}{utility.CLR_RESET} | "
              f"C: {utility.CLR_BOLD}{carbo}g{utility.CLR_RESET} | "
              f"G: {utility.CLR_BOLD}{grassi}g{utility.CLR_RESET} | "
              f"P: {utility.CLR_BOLD}{proteine}g{utility.CLR_RESET}\n")
    
    print(f"{tagDieta} Inserisci I Nuovi Dati Dieta:")

    # BB Richiesta Input All Utente Per I Nuovi Record Alimentari
    # CC Parsing Delle Date Con Formato Giorno Primo E Ciclo Di Validazione
    while True:
        inizioNewStr = input(f"{tagDieta} Inserisci Data Inizio (DD-MM-YYYY): ")
        try:
            inizioNew = pd.to_datetime(inizioNewStr, format='%d-%m-%Y')
            break
        except ValueError:
            print(f"{tagErrore} Formato Data Non Valido. Riprova.")

    # CC Richiesta Data Fine Opzionale Con Ciclo Di Validazione
    while True:
        dataFineNewStr = input(f"{tagDieta} Inserisci Data Fine (DD-MM-YYYY) [Opzionale, premi Invio per lasciare aperto]: ")
        if dataFineNewStr.strip() == "":
            dataFineNew = None
            break
        try:
            dataFineNew = pd.to_datetime(dataFineNewStr, format='%d-%m-%Y')
            if dataFineNew.date() < inizioNew.date():
                print(f"{tagErrore} La Data Fine Deve Essere Successiva O Uguale Alla Data Inizio.")
                continue
            break
        except ValueError:
            print(f"{tagErrore} Formato Data Non Valido. Riprova.")

    # BB Richiesta Input All'Utente Per I Nuovi Record Alimentari
    # CC Parsing Delle Date Con Formato Giorno Primo Per Evitare Errori Di Conversione
    kcalNew = int(input(f"{tagDieta} Inserisci Kcal:                     "))
    carboNew = int(input(f"{tagDieta} Inserisci Carboidrati (g):           "))
    grassiNew = int(input(f"{tagDieta} Inserisci Grassi (g):                 "))
    proteineNew = int(input(f"{tagDieta} Inserisci Proteine (g):               "))
    noteNew = input(f"{tagDieta} Inserisci Note (Opzionale):          ")

    # BB Calcolo Dei Parametri Temporali E Confronto Con La Scheda Misure
    # CC Calcolo Della Durata Complessiva Della Nuova Fase Dieta (Solo Se Presente)
    if dataFineNew is not None:
        durataNew = (dataFineNew - inizioNew).days + 1
        dataFineValueExcel = dataFineNew.date()
        durataValueExcel = int(durataNew)
    else:
        durataNew = None
        dataFineValueExcel = None
        durataValueExcel = None

    # CC Recupero Dei Dati Antropometrici Più Recenti Dalla Scheda Misure
    pesoMeasure = measureData['Peso (Kg)'].iloc[-1]

    # DD Calcolo Delle Proteine Giornaliere Rapportate Al Peso Corporeo Dell'Atleta
    proteinePerPeso = proteineNew / pesoMeasure

    # DD Recupero Del Fabbisogno Corretto Dalla Colonna Esistente In Excel
    fabbisognoMeasure = measureData['Fabbisogno Giornaliero'].iloc[-1]

    # DD Calcolo Del Deficit Energetico Rispetto Al Fabbisogno Stimato
    deficitTeorico = fabbisognoMeasure - kcalNew

    # BB Calcolo Delle Percentuali Dei Macronutrienti Rispetto Alle Calorie Totali
    # DD Calcolo Dei Rapporti Decimali Per La Gestione Delle Celle Percentuali In Excel
    percentualeCarbo = (carboNew * 4) / kcalNew
    percentualeGrassi = (grassiNew * 9) / kcalNew
    percentualeProteine = (proteineNew * 4) / kcalNew

    # BB Controllo Di Coerenza Energetica Tra Calorie Inserite E Calcolate
    # DD Calcolo Energetico Tramite Moltiplicatori Standard Dei Macronutrienti
    kcalCalcolate = (carboNew * 4) + (grassiNew * 9) + (proteineNew * 4)

    # CC Verifica Di Corrispondenza E Gestione Dello Script In Caso Di Errore
    if kcalCalcolate != kcalNew:
        # EE Errore Di Inserimento Con Arresto Di Sicurezza Dello Script
        print(f"\n{tagErrore} Le Kcal Calcolate ({kcalCalcolate}) Non Corrispondono A Quelle Inserite ({kcalNew}).\n")
        return
    else:
        # EE Messaggio Di Conferma Se Il Bilancio Energetico Risulta Corretto
        print(f"\n{tagDieta} Kcal Calcolate: {utility.CLR_BOLD}{kcalCalcolate}{utility.CLR_RESET} | "
          f"Kcal Inserite: {utility.CLR_BOLD}{kcalNew}{utility.CLR_RESET} | "
          f"{utility.CLR_BOLD}OK{utility.CLR_RESET}\n")

    # AA Inserimento Dei Valori Calcolati Nella Scheda "Dati Dieta"

    # BB Creazione Della Lista Ordinata Dei Nuovi Valori
    # CC Conversione Delle Date Di Pandas Nel Formato Data Nativo Per Excel
    if dataFineNew is not None:
        dataFineNew = dataFineNew.date()
    else:
        dataFineNew = None
    
    if durataNew is not None:
        durataNew = int(durataNew)
    else:
        durataNew = None
    newValue = [
        inizioNew.date(),               # Data Inizio (Colonna 1)
        dataFineNew,                    # Data Fine (Colonna 2)
        durataNew,                      # Durata (Colonna 3)
        int(kcalNew),                   # Kcal (Colonna 4)
        int(round(deficitTeorico, 0)),  # Deficit Teorico (Colonna 5)
        int(carboNew),                  # Carbo (g) (Colonna 6)
        int(grassiNew),                 # Grassi (g) (Colonna 7)
        int(proteineNew),               # Proteine (g) (Colonna 8)
        round(proteinePerPeso, 2),      # Proteine (g/Kg) (Colonna 9)
        round(percentualeCarbo, 4),     # % Carbo (Colonna 10)
        round(percentualeGrassi, 4),    # % Grassi (Colonna 11)
        round(percentualeProteine, 4),  # % Proteine (Colonna 12)
        noteNew                         # Note (Colonna 13)
    ]

    # BB Caricamento Del File Excel Con Openpyxl Per Preservare Stili, Colori E Larghezze Delle Celle E Aggiunta Nuova Riga
    excelFile = openpyxl.load_workbook(EXCEL_PATH)
    dietSheet = excelFile['Dati Dieta']

    dietSheet.append(newValue)

    # CC Copia Della Formattazione Dalla Riga Precedente (Incluso Formato Data E Percentuale)
    # CC Copia Della Formattazione Dalla Riga Precedente (Incluso Formato Data E Percentuale)
    lastRowIdx = dietSheet.max_row

    if lastRowIdx > 2: # Riga 1 = Intestazioni, Riga 2 = Primo Dato (Se Esiste, Copiamo Da Lì)
        for col_idx in range(1, len(newValue) + 1):
            sourceCell = dietSheet.cell(row=lastRowIdx - 1, column=col_idx)
            targetCell = dietSheet.cell(row=lastRowIdx, column=col_idx)
            
            # Copiamo Gli Stili E Il Formato Numerico Se Presenti (Silenziando I Falsi Positivi Di Pylance)
            if sourceCell.has_style:
                targetCell.font = copy(sourceCell.font)  # type: ignore
                targetCell.border = copy(sourceCell.border)  # type: ignore
                targetCell.fill = copy(sourceCell.fill)  # type: ignore
                targetCell.alignment = copy(sourceCell.alignment)  # type: ignore
                targetCell.number_format = sourceCell.number_format
    else:
        # DD Formattazione Manuale Solo Se È La Prima Riga Di Dati In Assoluto
        # Formato Decimale Per La Colonna 9 (Proteine (g/Kg))
        dietSheet.cell(row=lastRowIdx, column=9).number_format = '0.0'
        # Formato Percentuale Per La Colonna 10 (% Carbo)
        dietSheet.cell(row=lastRowIdx, column=10).number_format = '0.0%'
        # Formato Percentuale Per La Colonna 11 (% Grassi)
        dietSheet.cell(row=lastRowIdx, column=11).number_format = '0.0%'
        # Formato Percentuale Per La Colonna 12 (% Proteine)
        dietSheet.cell(row=lastRowIdx, column=12).number_format = '0.0%'

    # EE Forza Esplicitamente Il Formato GG-MM-AAAA Sulle Colonne Delle Date
    # EE Questo Evita Che Openpyxl Ripristini Il Formato ISO Default AAAA-MM-GG
    dietSheet.cell(row=lastRowIdx, column=1).number_format = 'dd/mm/yy;@'
    dietSheet.cell(row=lastRowIdx, column=2).number_format = 'dd/mm/yy;@'

    # BB Salvataggio Del File Excel Per Applicare Le Modifiche Senza Ricreare I Fogli
    excelFile.save(EXCEL_PATH)
    excelFile.close()

    # CC Sincronizzazione Del DataFrame In Memoria Per Coerenza Della Sessione
    # CC Sincronizzazione Del DataFrame In Memoria Per Coerenza Della Sessione
    dfToAppend = pd.DataFrame([{
        'Data Inizio': pd.to_datetime(inizioNew),
        'Data Fine': pd.to_datetime(dataFineNew) if dataFineNew is not None else pd.NaT,
        'Durata': int(durataNew) if durataNew is not None else np.nan,
        'Kcal': int(kcalNew),
        'Deficit Teorico': int(round(deficitTeorico, 0)),
        'Carbo (g)': int(carboNew),
        'Grassi (g)': int(grassiNew),
        'Proteine (g)': int(proteineNew),
        'Proteine (g/Kg)': round(proteinePerPeso, 2),
        '% Carbo': round(percentualeCarbo, 4),
        '% Grassi': round(percentualeGrassi, 4),
        '% Proteine': round(percentualeProteine, 4),
        'Note': noteNew
    }])

    excelData['Dati Dieta'] = pd.concat([excelData['Dati Dieta'], dfToAppend], ignore_index=True)

    print(f"\n{tagDieta} {utility.CLR_BOLD}Piano Alimentare E Calcoli Salvati Con Successo Nel File Excel!{utility.CLR_RESET}\n")
```

## trackingProgress/measures.py
```py
from copy import copy
from datetime import datetime, timezone

import numpy as np
import openpyxl
import pandas as pd
import utility


def updateMeasuresData(excelData, EXCEL_PATH):
    # AA Definizione Dei Tag Colorati Per La Visualizzazione
    tagMisure = f"{utility.CLR_MISURE}[MISURE]{utility.CLR_RESET}"
    tagErrore = f"{utility.CLR_ERRORE}[ERRORE]{utility.CLR_RESET}"

    # AA Recupero Delle Misurazioni Più Recenti
    personalData = excelData['Dati Personali']
    
    # BB Estrazione Dei Valori Dal Layout Verticale Usando .loc
    gender = personalData.loc[personalData['Parametro'] == 'Sesso', 'Valore'].iloc[0]
    heightRaw = personalData.loc[personalData['Parametro'] == 'Altezza (cm)', 'Valore'].iloc[0]
    
    # CC Conversione Protetta Dell'Altezza In Valore Numerico Decimale
    height = float(heightRaw)
    
    # BB Accesso Alla Scheda "Dati Misure"
    measureData = excelData['Dati Misure']

    # AA Inserimento Misurazioni Data Odierna O Specifica
    # BB Controllo Se La Scheda Dati Misure È Vuota Per Evitare Errori Di Indice
    if len(measureData) == 0:
        print(f"{tagMisure} Nessuna Misurazione Precedente Rilevata.\n")
        ultimaDataOBJ = None
        ultimaData = "Nessuna"
    else:
        # BB Stampa Data Ultima Misurazione
        ultimaDataOBJ = pd.to_datetime(measureData['Data Misurazione'].iloc[-1])
        ultimaData = ultimaDataOBJ.strftime("%d-%m-%Y")
        print(f"\n{tagMisure} Ultima Misurazione Registrata: {utility.CLR_BOLD}{ultimaData}{utility.CLR_RESET}\n")

    # BB Chiedi Se Vuoi Aggiungere Misurazioni Oggi O In Data Specifica
    print(f"{tagMisure} Seleziona Cosa Vuoi Fare:")
    print(f"{tagMisure}   1. Inserimento Misurazioni Oggi")
    if ultimaDataOBJ is not None:
        print(f"{tagMisure}   2. Inserimento Data Specifica (Successiva A {ultimaData})\n")
    else:
        print(f"{tagMisure}   2. Inserimento Data Specifica\n")
        
    scelta = input(f"{tagMisure} Inserisci Numero Corrispondente: ")

    if scelta == "1":
        dataOBJ = datetime.now(timezone.utc).date()
        data = dataOBJ.strftime("%d-%m-%Y")
        print(f"\n{tagMisure} Inserimento Misurazioni Data: {utility.CLR_BOLD}{data}{utility.CLR_RESET}\n")

    elif scelta == "2":
        dataInput = input(f"\n{tagMisure} Inserisci Data Specifica (GG-MM-AAAA): ")
        dataOBJ = pd.to_datetime(dataInput, format='%d-%m-%Y').date()
        if ultimaDataOBJ is not None and dataOBJ <= ultimaDataOBJ.date():
            print(f"\n{tagErrore} La Data Inserita Deve Essere Successiva A {ultimaData}\n")
            return
        data = dataOBJ.strftime("%d-%m-%Y")
        print(f"{tagMisure} Inserimento Misurazioni Data: {utility.CLR_BOLD}{data}{utility.CLR_RESET}\n")

    pesoNew = float(input(f"{tagMisure} Inserisci Peso (Kg):                  "))
    colloNew = float(input(f"{tagMisure} Inserisci Circonferenza Collo (cm):   "))
    vitaNew = float(input(f"{tagMisure} Inserisci Circonferenza Vita (cm):    "))
    fianchiNew = float(input(f"{tagMisure} Inserisci Circonferenza Fianchi (cm): "))
    braccioNew = utility.optionalInput(f"{tagMisure} Inserisci Circonferenza Braccio (cm) [Opzionale]: ")
    cosciaNew = utility.optionalInput(f"{tagMisure} Inserisci Circonferenza Coscia (cm)  [Opzionale]: ")
    
    # AA Calcolo Valori Scheda Con Dati Aggiornati

    # BB Massa Grassa, Massa Magra E Metabolismo Basale (BMR)
    # CC Massa Grassa E Massa Magra Tramite Formula US Navy Dinamica Per Sesso
    if gender == "M":
        usNavyBF = ( 495 / (1.0324 - 0.19077 * np.log10(vitaNew - colloNew) + 0.15456 * np.log10(height)) ) - 450
    else:
        usNavyBF = ( 495 / (1.29579 - 0.35004 * np.log10(vitaNew + fianchiNew - colloNew) + 0.22100 * np.log10(height)) ) - 450

    massaGrassa = pesoNew * (usNavyBF / 100)
    massaMagra = pesoNew - massaGrassa

    # CC Metabolismo Basale (BMR) - Formula Katch-McArdle
    metabolismoBasale = 370 + (21.6 * massaMagra)

    # DD Fabbisogno Energetico Giornaliero (TDEE)
    tdeeAllenamento = metabolismoBasale * 1.55  # Moderato
    tdeeRiposo = metabolismoBasale * 1.2        # Sedentario
    tdeeMedio = (tdeeAllenamento * 3 + tdeeRiposo * 4) / 7

    # AA Inserimento Dei Valori Calcolati Nella Scheda "Dati Misure"
    # BB Creazione Della Lista Ordinata Dei Nuovi Valori
    # Se In Excel Hai Impostato La Cella Come "Percentuale" Si Deve Dividere Per 100, Perché Excel Gestisce Le Percentuali Come Decimali.
    newValue = [
        dataOBJ,                        # Data Misurazione
        round(pesoNew, 2),              # Peso (Kg)
        round(colloNew, 2),             # Circonferenza Collo (cm)
        round(vitaNew, 2),              # Circonferenza Vita (cm)
        round(fianchiNew, 2),           # Circonferenza Fianchi (cm)
        braccioNew,                     # Circonferenza Braccio (cm)
        cosciaNew,                      # Circonferenza Coscia (cm)
        round(usNavyBF / 100, 4),       # Massa Grassa (%)
        round(massaMagra, 2),           # Massa Magra (Kg)
        round(metabolismoBasale, 0),    # Metabolismo Basale
        round(tdeeMedio, 0)             # Fabbisogno Giornaliero
    ]

    # BB Caricamento Del File Excel Con Openpyxl Per Preservare Stili, Colori E Larghezze Delle Celle E Aggiunta Nuova Riga
    excelFile = openpyxl.load_workbook(EXCEL_PATH)
    measureSheet = excelFile['Dati Misure']

    measureSheet.append(newValue)

    # CC Copia Della Formattazione Dalla Riga Precedente (Incluso Formato Data E Percentuale)
    lastRowIdx = measureSheet.max_row

    if lastRowIdx > 2: # Riga 1 = Intestazioni, Riga 2 = Primo Dato (Se Esiste, Copiamo Da Lì)
        for col_idx in range(1, len(newValue) + 1):
            sourceCell = measureSheet.cell(row=lastRowIdx - 1, column=col_idx)
            targetCell = measureSheet.cell(row=lastRowIdx, column=col_idx)
            
            # Copiamo Gli Stili E Il Formato Numerico Se Presenti (Silenziando I Falsi Positivi Di Pylance)
            if sourceCell.has_style:
                targetCell.font = copy(sourceCell.font)  # type: ignore
                targetCell.border = copy(sourceCell.border)  # type: ignore
                targetCell.fill = copy(sourceCell.fill)  # type: ignore
                targetCell.alignment = copy(sourceCell.alignment)  # type: ignore
                targetCell.number_format = sourceCell.number_format
    else:
        # DD Formattazione Manuale Solo Se È La Prima Riga Di Dati In Assoluto
        # Formato Data Per La Colonna 1 (Data Misurazione)
        measureSheet.cell(row=lastRowIdx, column=1).number_format = 'DD-MM-YYYY'
        # Formato Percentuale Per La Colonna 8 (Massa Grassa (%))
        measureSheet.cell(row=lastRowIdx, column=8).number_format = '0.0%'

    # BB Salvataggio Del File Excel Per Applicare Le Modifiche Senza Ricreare I Fogli
    excelFile.save(EXCEL_PATH)
    excelFile.close()

    # CC Sincronizzazione Del DataFrame In Memoria Per Coerenza Della Sessione
    dfToAppend = pd.DataFrame([{
        'Data Misurazione': pd.to_datetime(dataOBJ),
        'Peso (Kg)': round(pesoNew, 2),
        'Circonferenza Collo (cm)': round(colloNew, 2),
        'Circonferenza Vita (cm)': round(vitaNew, 2),
        'Circonferenza Fianchi (cm)': round(fianchiNew, 2),
        'Circonferenza Braccio (cm)': braccioNew,
        'Circonferenza Coscia (cm)': cosciaNew,
        'Massa Grassa (%)': round(usNavyBF / 100, 4),
        'Massa Magra (Kg)': round(massaMagra, 2),
        'Metabolismo Basale': round(metabolismoBasale, 0),
        'Fabbisogno Giornaliero': round(tdeeMedio, 0)
    }])
    
    excelData['Dati Misure'] = pd.concat([excelData['Dati Misure'], dfToAppend], ignore_index=True)

    print(f"\n{tagMisure} {utility.CLR_BOLD}Misurazioni E Calcoli Salvati Con Successo Nel File Excel!{utility.CLR_RESET}\n")
```

## trackingProgress/personal.py
```py
from copy import copy
from datetime import datetime, time, timezone

import openpyxl
import pandas as pd
import utility
from openpyxl.cell.cell import MergedCell


def updatePersonalData(excelData, EXCEL_PATH):
    # AA Definizione Dei Tag Colorati Per La Visualizzazione
    tagProfilo = f"{utility.CLR_PROFILO}[PROFILO]{utility.CLR_RESET}"
    tagErrore = f"{utility.CLR_ERRORE}[ERRORE]{utility.CLR_RESET}"

    # BB Verifica Presenza Dei Dati Di Misurazione Essenziali
    measureData = excelData['Dati Misure']
    
    # CC Controllo Se La Scheda Dati Misure È Vuota
    if len(measureData) == 0:
        print(f"\n{tagErrore} Nessuna Misurazione Trovata Nella Scheda Dati Misure.")
        print(f"{tagErrore} Inserisci Almeno Una Misurazione Prima Di Aggiornare Il Profilo.\n")
        return

    print(f"\n{tagProfilo} Avvio Sincronizzazione Dei Dati Personali...")

    # DD Accesso Alla Scheda Dati Personali
    personalDf = excelData['Dati Personali']
    
    # EE Pulizia Spazi Bianchi Nelle Etichette Per Evitare Errori Di Corrispondenza
    personalDf['Parametro'] = personalDf['Parametro'].astype(str).str.strip()

    # AA Estrazione Dei Dati Statici Inseriti Dall'Utente
    gender = personalDf.loc[personalDf['Parametro'] == 'Sesso', 'Valore'].values[0]
    heightValue = personalDf.loc[personalDf['Parametro'] == 'Altezza (cm)', 'Valore'].values[0]
    height = float(heightValue)
    dobValue = personalDf.loc[personalDf['Parametro'] == 'Data Di Nascita', 'Valore'].values[0]
    dobDate = pd.to_datetime(dobValue)

    # BB Recupero Delle Informazioni Fisiche Più Recenti Dallo Storico Misure
    latestMeasure = measureData.iloc[-1]
    currentWeight = float(latestMeasure['Peso (Kg)'])
    currentLbm = float(latestMeasure['Massa Magra (Kg)'])
    currentTdee = float(latestMeasure['Fabbisogno Giornaliero'])

    # CC Recupero Del Deficit Energetico Corrente Dalla Scheda Dieta
    dietData = excelData['Dati Dieta']
    
    # DD Gestione Caso Scheda Dieta Vuota O Assenza Di Fasi Attive
    if len(dietData) > 0:
        latestDiet = dietData.iloc[-1]
        currentDeficit = float(latestDiet['Deficit Teorico'])
    else:
        currentDeficit = 0.0

    # EE Calcolo Della Età Attuale Dell'Utente
    currentDate = datetime.now(timezone.utc)
    calculatedAge = currentDate.year - dobDate.year - ((currentDate.month, currentDate.day) < (dobDate.month, dobDate.day))

    # AA Calcolo Del Metabolismo Basale Con Formula Mifflin St Jeor
    if gender == "M":
        bmrMifflin = (10 * currentWeight) + (6.25 * height) - (5 * calculatedAge) + 5
    else:
        bmrMifflin = (10 * currentWeight) + (6.25 * height) - (5 * calculatedAge) - 161

    # BB Calcolo Del Metabolismo Basale Con Formula Katch McArdle
    bmrKatch = 370 + (21.6 * currentLbm)

    # CC Visualizzazione Dei Dati Estratti E Dei Calcoli Nel Terminale
    print(f"{tagProfilo}   - Età Rilevata:                 {utility.CLR_BOLD}{calculatedAge} Anni{utility.CLR_RESET}")
    print(f"{tagProfilo}   - Peso Corrente Rilevato:       {utility.CLR_BOLD}{currentWeight:.2f} Kg{utility.CLR_RESET}")
    print(f"{tagProfilo}   - Massa Magra Rilevata:         {utility.CLR_BOLD}{currentLbm:.2f} Kg{utility.CLR_RESET}")
    print(f"{tagProfilo}   - TDEE Corrente Rilevato:       {utility.CLR_BOLD}{int(currentTdee)} Kcal{utility.CLR_RESET}")
    print(f"{tagProfilo}   - Deficit Attivo Rilevato:      {utility.CLR_BOLD}{int(currentDeficit)} Kcal{utility.CLR_RESET}")
    print(f"{tagProfilo}   - BMR Mifflin-St Jeor:          {utility.CLR_BOLD}{int(bmrMifflin)} Kcal{utility.CLR_RESET}")
    print(f"{tagProfilo}   - BMR Katch-McArdle:            {utility.CLR_BOLD}{int(bmrKatch)} Kcal{utility.CLR_RESET}")

    # DD Aggiornamento Del File Excel Fisico Tramite Openpyxl
    excelFile = openpyxl.load_workbook(EXCEL_PATH)
    personalSheet = excelFile['Dati Personali']

    # EE Scrittura Valori Nella Colonna B Per Il Profilo Verticale
    personalSheet['B6'].value = int(calculatedAge)
    personalSheet['B7'].value = round(currentWeight, 2)
    personalSheet['B8'].value = round(currentLbm, 2)
    personalSheet['B9'].value = round(bmrMifflin, 0)
    personalSheet['B10'].value = round(bmrKatch, 0)
    personalSheet['B11'].value = round(currentTdee, 0)
    personalSheet['B12'].value = round(currentDeficit, 0)
    
    # AA Inserimento Timestamp Di Esecuzione Nella Nuova Cella B13
    executionTime = datetime.now(timezone.utc)
    personalSheet['B13'].value = executionTime
    personalSheet['B13'].number_format = 'YYYY-MM-DD HH:MM:SS'

    # BB Bonifica Difensiva: Rimozione Di Eventuali Timezone Residue Da Qualsiasi Cella Del Workbook
    # CC Necessaria Perche' Excel Non Supporta Datetime Con Timezone E Openpyxl Si Blocca In Fase Di Salvataggio
    for sheet in excelFile.worksheets:
        for row in sheet.iter_rows():
            for cell in row:
                # DD Le MergedCell Non Permettono La Scrittura Diretta Del Valore (Solo La Cella In Alto A Sinistra Lo Ha)
                if isinstance(cell, MergedCell):
                    continue
                if isinstance(cell.value, (datetime, time)) and getattr(cell.value, 'tzinfo', None) is not None:
                    cell.value = cell.value.replace(tzinfo=None)

    # BB Salvataggio Delle Modifiche Nel File Excel
    excelFile.save(EXCEL_PATH)
    excelFile.close()

    # CC Sincronizzazione Del DataFrame In Memoria Per Coerenza Sessione
    personalDf.loc[personalDf['Parametro'] == 'Età', 'Valore'] = int(calculatedAge)
    personalDf.loc[personalDf['Parametro'] == 'Peso Corrente (Kg)', 'Valore'] = round(currentWeight, 2)
    personalDf.loc[personalDf['Parametro'] == 'Massa Magra Corrente (Kg)', 'Valore'] = round(currentLbm, 2)
    personalDf.loc[personalDf['Parametro'] == 'BMR Mifflin-St Jeor (Kcal)', 'Valore'] = round(bmrMifflin, 0)
    personalDf.loc[personalDf['Parametro'] == 'BMR Katch-McArdle (Kcal)', 'Valore'] = round(bmrKatch, 0)
    personalDf.loc[personalDf['Parametro'] == 'TDEE Corrente Pesato (Kcal)', 'Valore'] = round(currentTdee, 0)
    personalDf.loc[personalDf['Parametro'] == 'Deficit Corrente (Kcal)', 'Valore'] = round(currentDeficit, 0)
    personalDf.loc[personalDf['Parametro'] == 'Ultimo Aggiornamento', 'Valore'] = executionTime

    excelData['Dati Personali'] = personalDf

    print(f"\n{tagProfilo} {utility.CLR_BOLD}Scheda Dati Personali Aggiornata Con Successo!{utility.CLR_RESET}\n")
```

## trackingProgress/smartwatch.py
```py
import os
import sqlite3

import pandas as pd
import utility


# AA Funzione Helper Per Rilevare I Dispositivi Associati Nel Database Gadgetbridge
def getAvailableDevices(conn):
    # BB Estrazione Della Lista Dispositivi Dalla Tabella DEVICE
    queryDevices = """
        SELECT _id, NAME, MANUFACTURER, TYPE_NAME 
        FROM DEVICE 
        ORDER BY _id ASC;
    """
    try:
        return pd.read_sql_query(queryDevices, conn)
    except (pd.errors.DatabaseError, sqlite3.Error):
        return pd.DataFrame()


# AA Mappa Dei Codici Fase Sonno Specifici Per Xiaomi
# BB Corrispondenza Verificata Confrontando Le Durate Calcolate Con I Totali Ufficiali Di XIAOMI_SLEEP_TIME_SAMPLE
XIAOMI_SLEEP_STAGE_MAP = {
    2: "Sonno Profondo",
    3: "Sonno Leggero",
    4: "Sonno REM",
    5: "Sveglio",
}


# AA Parser Per I Dati Del Sonno Della Famiglia Xiaomi
def parseXiaomiSleep(conn, deviceId):
    # BB Estrazione Delle Sessioni Di Sonno Aggregate (Una Riga Per Notte)
    querySessions = f"""
        SELECT
            TIMESTAMP,
            WAKEUP_TIME,
            TOTAL_DURATION,
            DEEP_SLEEP_DURATION,
            LIGHT_SLEEP_DURATION,
            REM_SLEEP_DURATION,
            AWAKE_DURATION
        FROM XIAOMI_SLEEP_TIME_SAMPLE
        WHERE DEVICE_ID = {deviceId}
        ORDER BY TIMESTAMP ASC;
    """
    sleepSessions = pd.read_sql_query(querySessions, conn)

    # BB Estrazione Della Timeline Dettagliata Delle Fasi (Per Il Drill-Down Giornaliero)
    queryStages = f"""
        SELECT
            TIMESTAMP,
            STAGE
        FROM XIAOMI_SLEEP_STAGE_SAMPLE
        WHERE DEVICE_ID = {deviceId}
        ORDER BY TIMESTAMP ASC;
    """
    stageRows = pd.read_sql_query(queryStages, conn)

    sleepStages = pd.DataFrame()

    if not sleepSessions.empty:
        # CC Associazione Di Ogni Fase Alla Sessione Di Appartenenza
        # DD Necessario Perche' XIAOMI_SLEEP_STAGE_SAMPLE Non Ha Un ID Di Sessione Esplicito
        # EE Il Confronto Avviene Sui Millisecondi Grezzi, Prima Di Qualsiasi Conversione Di Fuso Orario
        stageBlocks = []
        for _, session in sleepSessions.iterrows():
            sessionStartMs = session["TIMESTAMP"]
            sessionEndMs = session["WAKEUP_TIME"]

            mask = (stageRows["TIMESTAMP"] >= sessionStartMs) & (stageRows["TIMESTAMP"] < sessionEndMs)
            sessionStages = stageRows[mask].copy()

            if sessionStages.empty:
                continue

            # EE Calcolo Della Durata Di Ogni Fase Come Differenza Con La Fase Successiva
            # EE L'Ultima Fase Della Notte Dura Fino All'Orario Di Sveglia Della Sessione
            sessionStages["NEXT_TIMESTAMP"] = sessionStages["TIMESTAMP"].shift(-1)
            sessionStages.loc[sessionStages.index[-1], "NEXT_TIMESTAMP"] = sessionEndMs
            sessionStages["Durata (min)"] = ((sessionStages["NEXT_TIMESTAMP"] - sessionStages["TIMESTAMP"]) / 1000 / 60).round(1)
            sessionStages["SESSION_WAKEUP_TIME"] = sessionEndMs

            stageBlocks.append(sessionStages)

        if stageBlocks:
            sleepStages = pd.concat(stageBlocks, ignore_index=True)

            sleepStages["Inizio Fase"] = (
                pd.to_datetime(sleepStages["TIMESTAMP"], unit="ms", utc=True)
                .dt.tz_convert("Europe/Rome")
                .dt.tz_localize(None)
            )
            # EE La Fase Viene Attribuita Alla Data Di Sveglia Della Sessione Di Appartenenza
            sleepStages["Data"] = (
                pd.to_datetime(sleepStages["SESSION_WAKEUP_TIME"], unit="ms", utc=True)
                .dt.tz_convert("Europe/Rome")
                .dt.date
            )
            sleepStages["Fase"] = sleepStages["STAGE"].map(XIAOMI_SLEEP_STAGE_MAP)

            # EE Segnalazione Di Eventuali Codici Fase Non Ancora Mappati, Senza Interrompere Lo Script
            unknownStages = sleepStages.loc[sleepStages["Fase"].isna(), "STAGE"].unique()
            if len(unknownStages) > 0:
                print(f"{utility.CLR_ERRORE}[ERRORE]{utility.CLR_RESET} Codici Fase Sonno Non Riconosciuti: {list(unknownStages)}")
                sleepStages["Fase"] = sleepStages["Fase"].fillna("Sconosciuto")

            sleepStages = sleepStages[["Data", "Inizio Fase", "Fase", "Durata (min)"]]

        # CC Conversione Delle Colonne Di Sessione In Orario Locale (Fatta Dopo Aver Usato I Millisecondi Grezzi Sopra)
        sleepSessions["Inizio Sonno"] = (
            pd.to_datetime(sleepSessions["TIMESTAMP"], unit="ms", utc=True)
            .dt.tz_convert("Europe/Rome")
            .dt.tz_localize(None)
        )
        sleepSessions["Fine Sonno"] = (
            pd.to_datetime(sleepSessions["WAKEUP_TIME"], unit="ms", utc=True)
            .dt.tz_convert("Europe/Rome")
            .dt.tz_localize(None)
        )
        # CC La Notte Viene Attribuita Alla Data Della Sveglia (Convenzione Standard Di Sleep-Tracking)
        sleepSessions["Data"] = sleepSessions["Fine Sonno"].dt.date

        renameMapSleep = {
            "TOTAL_DURATION": "Durata Totale (min)",
            "DEEP_SLEEP_DURATION": "Sonno Profondo (min)",
            "LIGHT_SLEEP_DURATION": "Sonno Leggero (min)",
            "REM_SLEEP_DURATION": "Sonno REM (min)",
            "AWAKE_DURATION": "Tempo Sveglio (min)",
        }
        sleepSessions = sleepSessions.rename(columns=renameMapSleep)

        columnsSessions = [
            "Data", "Inizio Sonno", "Fine Sonno", "Durata Totale (min)",
            "Sonno Profondo (min)", "Sonno Leggero (min)", "Sonno REM (min)", "Tempo Sveglio (min)"
        ]
        sleepSessions = sleepSessions[columnsSessions]

    return sleepSessions, sleepStages


# AA Parser Specifico Per La Famiglia Xiaomi / Redmi / Poco (Stesso Protocollo, Stesse Tabelle)
def parseXiaomiFamily(conn, deviceId):
    # BB Estrazione Delle Rilevazioni Al Minuto Filtrate Per DEVICE_ID
    queryActivity = f"""
        SELECT 
            TIMESTAMP,
            STEPS,
            HEART_RATE,
            RAW_KIND,
            SPO2,
            STRESS,
            DISTANCE_CM,
            ACTIVE_CALORIES
        FROM XIAOMI_ACTIVITY_SAMPLE
        WHERE DEVICE_ID = {deviceId}
        ORDER BY TIMESTAMP ASC;
    """
    activityData = pd.read_sql_query(queryActivity, conn)

    if not activityData.empty:
        # CC Conversione Del Timestamp Unix In UTC E Localizzazione Su Fuso Orario Locale
        activityData["Data Ora"] = (
            pd.to_datetime(activityData["TIMESTAMP"], unit="s", utc=True)
            .dt.tz_convert("Europe/Rome")
            .dt.tz_localize(None)
        )
        activityData["Data"] = activityData["Data Ora"].dt.date
        activityData["Ora"] = activityData["Data Ora"].dt.strftime("%H:%M:%S")

        # CC Conversione Della Distanza Da Centimetri A Metri
        activityData["Distanza (m)"] = (activityData["DISTANCE_CM"] / 100).round(1)

        # CC Ridenominazione Delle Metriche Biometriche E Di Movimento
        renameMapActivity = {
            "STEPS": "Passi",
            "HEART_RATE": "Frequenza Cardiaca (bpm)",
            "RAW_KIND": "Tipo Attivita",
            "SPO2": "SpO2 (%)",
            "STRESS": "Livello Stress",
            "ACTIVE_CALORIES": "Calorie Attive (kcal)",
        }
        activityData = activityData.rename(columns=renameMapActivity)
        activityData["SpO2 (%)"] = activityData["SpO2 (%)"].replace(0, pd.NA)

        columnsActivity = [
            "Data", "Ora", "Data Ora", "Passi", "Frequenza Cardiaca (bpm)",
            "SpO2 (%)", "Livello Stress", "Calorie Attive (kcal)", "Distanza (m)", "Tipo Attivita"
        ]
        activityData = activityData[columnsActivity]

    # BB Estrazione Delle Metriche Aggregate Giornaliere Filtrate Per DEVICE_ID
    querySummary = f"""
        SELECT 
            TIMESTAMP,
            STEPS,
            CALORIES,
            ACTIVE_CALORIES,
            HR_RESTING,
            HR_AVG,
            HR_MIN,
            HR_MIN_TS,
            HR_MAX,
            HR_MAX_TS,
            STRESS_AVG,
            STRESS_MAX,
            STRESS_MIN,
            SPO2_AVG,
            STANDING,
            VITALITY_CURRENT
        FROM XIAOMI_DAILY_SUMMARY_SAMPLE
        WHERE DEVICE_ID = {deviceId}
        ORDER BY TIMESTAMP ASC;
    """
    dailySummary = pd.read_sql_query(querySummary, conn)

    if not dailySummary.empty:
        dailySummary["Data"] = (
            pd.to_datetime(dailySummary["TIMESTAMP"], unit="ms", utc=True)
            .dt.tz_convert("Europe/Rome")
            .dt.date
        )

        hrMinValid = dailySummary["HR_MIN_TS"].replace(0, pd.NA)
        hrMaxValid = dailySummary["HR_MAX_TS"].replace(0, pd.NA)
        dailySummary["Ora Battito Min"] = (
            pd.to_datetime(hrMinValid, unit="s", utc=True)
            .dt.tz_convert("Europe/Rome")
            .dt.strftime("%H:%M:%S")
        )
        dailySummary["Ora Battito Max"] = (
            pd.to_datetime(hrMaxValid, unit="s", utc=True)
            .dt.tz_convert("Europe/Rome")
            .dt.strftime("%H:%M:%S")
        )

        renameMapSummary = {
            "STEPS": "Passi Totali",
            "CALORIES": "Calorie Totali (kcal)",
            "ACTIVE_CALORIES": "Calorie Attive (kcal)",
            "HR_RESTING": "Frequenza Riposo (bpm)",
            "HR_AVG": "Frequenza Media (bpm)",
            "HR_MIN": "Frequenza Minima (bpm)",
            "HR_MAX": "Frequenza Massima (bpm)",
            "STRESS_AVG": "Stress Medio",
            "STRESS_MAX": "Stress Massimo",
            "STRESS_MIN": "Stress Minimo",
            "SPO2_AVG": "SpO2 Medio (%)",
            "STANDING": "Secondi In Piedi",
            "VITALITY_CURRENT": "Indice Vitalita",
        }
        dailySummary = dailySummary.rename(columns=renameMapSummary)
        dailySummary["Ore In Piedi"] = (dailySummary["Secondi In Piedi"] / 3600).round(1)

        columnsDaily = [
            "Data", "Passi Totali", "Calorie Totali (kcal)", "Calorie Attive (kcal)",
            "Frequenza Riposo (bpm)", "Frequenza Media (bpm)", "Frequenza Minima (bpm)", "Ora Battito Min",
            "Frequenza Massima (bpm)", "Ora Battito Max", "Stress Medio", "Stress Massimo",
            "Stress Minimo", "SpO2 Medio (%)", "Ore In Piedi", "Indice Vitalita"
        ]
        dailySummary = dailySummary[columnsDaily]

    # BB Estrazione Dei Dati Del Sonno
    sleepSessions, sleepStages = parseXiaomiSleep(conn, deviceId)

    return activityData, dailySummary, sleepSessions, sleepStages


# AA Funzione Master Per Elaborare I Dati Smartwatch
# BB Supporta Solo Dispositivi Xiaomi / Redmi / Poco (Stesso Protocollo Xiaomi Wear)
# CC Per Aggiungere Altre Marche: Fork Del Progetto, Il Codice E Pubblico Su GitHub
def processSmartwatchData(DB_PATH, targetDevice=None):
    # AA Definizione Dei Tag Colorati Per La Visualizzazione
    tagSmartwatch = f"{utility.CLR_SMARTWATCH}[SMARTWATCH]{utility.CLR_RESET}"
    tagErrore = f"{utility.CLR_ERRORE}[ERRORE]{utility.CLR_RESET}"

    # AA Verifica Esistenza Del Database Gadgetbridge
    if not os.path.exists(DB_PATH):
        print(f"\n{tagSmartwatch} File Database Non Trovato Nel Percorso Specificato: {DB_PATH}\n")
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

    # BB Apertura Connessione Verso Il Database SQLite
    conn = sqlite3.connect(DB_PATH)

    # AA Rilevamento Dei Dispositivi Registrati Nel Database
    devicesDf = getAvailableDevices(conn)
    if devicesDf.empty:
        print(f"\n{tagErrore} Nessun Dispositivo Rilevato Nella Tabella DEVICE Di Gadgetbridge.\n")
        conn.close()
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

    # BB Selezione Del Dispositivo Target (Automatica O Tramite Input Utente)
    selectedDevice = None
    if targetDevice is None:
        # Selezione Automatica Del Primo Dispositivo Disponibile
        selectedDevice = devicesDf.iloc[0]
    else:
        # Ricerca Tramite Nome O Produttore
        matched = devicesDf[
            devicesDf["NAME"].astype(str).str.contains(str(targetDevice), case=False, na=False) |
            devicesDf["MANUFACTURER"].astype(str).str.contains(str(targetDevice), case=False, na=False) |
            devicesDf["TYPE_NAME"].astype(str).str.contains(str(targetDevice), case=False, na=False)
        ]
        if not matched.empty:
            selectedDevice = matched.iloc[0]
        else:
            print(f"\n{tagErrore} Dispositivo '{targetDevice}' Non Trovato. Verrà Utilizzato: {devicesDf.iloc[0]['NAME']}\n")
            selectedDevice = devicesDf.iloc[0]

    deviceId = int(selectedDevice["_id"])
    deviceName = selectedDevice["NAME"]
    manufacturer = str(selectedDevice["MANUFACTURER"]).upper()
    typeName = str(selectedDevice["TYPE_NAME"]).upper()

    print(f"\n{tagSmartwatch} Dispositivo Selezionato: {utility.CLR_BOLD}{deviceName}{utility.CLR_RESET} (ID: {deviceId}, Produttore: {manufacturer})")

    # AA Solo Famiglia Xiaomi / Redmi / Poco E Supportata
    activityData = pd.DataFrame()
    dailySummary = pd.DataFrame()
    sleepSessions = pd.DataFrame()
    sleepStages = pd.DataFrame()

    if manufacturer in ["XIAOMI", "REDMI", "POCO"] or "XIAOMI" in typeName or "REDMI" in typeName:
        activityData, dailySummary, sleepSessions, sleepStages = parseXiaomiFamily(conn, deviceId)
    else:
        print(f"{tagErrore} Produttore '{manufacturer}' Non Supportato. Questo Script Gestisce Solo Dispositivi Xiaomi/Redmi/Poco.")

    # BB Chiusura Connessione Database
    conn.close()

    # AA Notifica Di Completamento Estrazione Dati
    if not activityData.empty or not dailySummary.empty:
        print(
            f"{tagSmartwatch} Dati Smartwatch Estratti Con Successo: "
            f"{utility.CLR_BOLD}{len(activityData)}{utility.CLR_RESET} Rilevazioni, "
            f"{utility.CLR_BOLD}{len(dailySummary)}{utility.CLR_RESET} Giorni Di Sintesi, "
            f"{utility.CLR_BOLD}{len(sleepSessions)}{utility.CLR_RESET} Notti Registrate.\n"
        )

    return activityData, dailySummary, sleepSessions, sleepStages


# AA Blocco Di Test Diretto Dello Script
if __name__ == "__main__":
    DB_PATH = "/mnt/c/Users/cicci/Documents/Appunti_E_Personale/trackingProgressi/gadgetBridgeSync/Gadgetbridge.db"

    if not os.path.exists(DB_PATH):
        print(f"File Non Trovato: {DB_PATH}")
    else:
        activityData, dailySummary, sleepSessions, sleepStages = processSmartwatchData(DB_PATH)

        if not activityData.empty:
            print(f"Attivita: {len(activityData)} righe, dal {activityData['Data'].min()} al {activityData['Data'].max()}")
        else:
            print("Nessun Dato Di Attivita Trovato.")

        if not dailySummary.empty:
            print(f"Riepilogo Giornaliero: {len(dailySummary)} righe, dal {dailySummary['Data'].min()} al {dailySummary['Data'].max()}")
        else:
            print("Nessun Riepilogo Giornaliero Trovato.")

        if not sleepSessions.empty:
            print("\n--- Sessioni Di Sonno ---")
            print(sleepSessions.to_string(index=False))

        if not sleepStages.empty:
            print("\n--- Timeline Fasi Sonno ---")
            print(sleepStages.to_string(index=False))
```

## trackingProgress/testSetup.py
```py
import logging
import os
import sqlite3

import pandas as pd
import smartwatch
import utility

# AA Percorsi Assoluti, Identici A Quelli Di updateTracking.py
EXCEL_PATH = "/mnt/c/Users/cicci/Documents/Appunti_E_Personale/trackingProgressi/trackingProgressi.xlsx"
SMARTWATCH_DB = "/mnt/c/Users/cicci/Documents/Appunti_E_Personale/trackingProgressi/gadgetBridgeSync/Gadgetbridge.db"
DASHBOARD_DB_PATH = "/home/lag/## dashboardData.db"

SOGLIA_AFFIDABILITA_MISURE = "2026-06-01"

# AA Elenco Globale Dei Risultati Dei Controlli, Popolato Man Mano Dallo Script
risultati = []


# AA Funzione Di Appoggio Per Registrare E Stampare Un Singolo Esito Di Controllo
def segnaRisultato(nome, esito, dettaglio=""):
    risultati.append((nome, esito, dettaglio))
    tag = f"{utility.CLR_MISURE}[OK]{utility.CLR_RESET}" if esito else f"{utility.CLR_ERRORE}[FALLITO]{utility.CLR_RESET}"
    print(f"{tag} {nome}" + (f" — {dettaglio}" if dettaglio else ""))


# AA Verifica Che I Tre File/Database Principali Esistano Fisicamente Sul Disco
def verificaPercorsi():
    print(f"\n{utility.CLR_TEST}=== Verifica Percorsi ==={utility.CLR_RESET}")
    for nome, percorso in [
        ("File Excel", EXCEL_PATH),
        ("Database Gadgetbridge", SMARTWATCH_DB),
        ("Database Dashboard", DASHBOARD_DB_PATH),
    ]:
        esiste = os.path.exists(percorso)
        dettaglio = f"{os.path.getsize(percorso) / 1024 / 1024:.2f} MB" if esiste else percorso
        segnaRisultato(f"Percorso Trovato: {nome}", esiste, dettaglio)


# AA Verifica Che Il File Excel Sia Leggibile E Che Tutti I Fogli Attesi Siano Presenti
def verificaExcel():
    print(f"\n{utility.CLR_TEST}=== Verifica File Excel ==={utility.CLR_RESET}")
    if not os.path.exists(EXCEL_PATH):
        segnaRisultato("Lettura Fogli Excel", False, "File Non Trovato, Salto Il Controllo")
        return {}

    fogliAttesi = ['Dati Personali', 'Dati Misure', 'Dati Dieta', 'Dati Allenamento', 'Dati Palestra']
    excelData = {}
    try:
        for foglio in fogliAttesi:
            excelData[foglio] = pd.read_excel(EXCEL_PATH, sheet_name=foglio)
        segnaRisultato("Lettura Fogli Excel", True, f"{len(fogliAttesi)} Fogli Letti Correttamente")
        for foglio, df in excelData.items():
            print(f"    {foglio}: {len(df)} Righe")
    except Exception as e:
        segnaRisultato("Lettura Fogli Excel", False, str(e))

    return excelData


# AA Verifica Diretta Del Parser Smartwatch (Conferma Anche Che Il Percorso SMARTWATCH_DB Sia Corretto)
def verificaParserSmartwatch():
    print(f"\n{utility.CLR_TEST}=== Verifica Parser Smartwatch (Esecuzione Diretta) ==={utility.CLR_RESET}")
    if not os.path.exists(SMARTWATCH_DB):
        segnaRisultato("Esecuzione Parser Smartwatch", False, "File Gadgetbridge.db Non Trovato, Salto Il Controllo")
        return

    try:
        activityData, dailySummary, sleepSessions, sleepStages = smartwatch.processSmartwatchData(SMARTWATCH_DB)
        segnaRisultato("Esecuzione Parser Smartwatch Senza Errori", True)
        segnaRisultato("Attivita Estratta", not activityData.empty, f"{len(activityData)} Righe")
        segnaRisultato("Riepilogo Giornaliero Estratto", not dailySummary.empty, f"{len(dailySummary)} Righe")
        segnaRisultato("Sessioni Sonno Estratte", not sleepSessions.empty, f"{len(sleepSessions)} Notti")
    except Exception as e:
        segnaRisultato("Esecuzione Parser Smartwatch Senza Errori", False, str(e))


# AA Verifica Del Database Gadgetbridge: Presenza Dispositivi E Tabelle Smartwatch Attese
def verificaGadgetbridge():
    print(f"\n{utility.CLR_TEST}=== Verifica Database Gadgetbridge ==={utility.CLR_RESET}")
    if not os.path.exists(SMARTWATCH_DB):
        segnaRisultato("Connessione Database Gadgetbridge", False, "File Non Trovato, Salto Il Controllo")
        return

    try:
        conn = sqlite3.connect(SMARTWATCH_DB)
        devices = pd.read_sql_query("SELECT _id, NAME, MANUFACTURER FROM DEVICE;", conn)
        segnaRisultato("Connessione Database Gadgetbridge", True, f"{len(devices)} Dispositivi Trovati")

        tabelleAttese = [
            "XIAOMI_ACTIVITY_SAMPLE", "XIAOMI_DAILY_SUMMARY_SAMPLE",
            "XIAOMI_SLEEP_TIME_SAMPLE", "XIAOMI_SLEEP_STAGE_SAMPLE"
        ]
        for tabella in tabelleAttese:
            try:
                conteggio = pd.read_sql_query(f"SELECT COUNT(*) as n FROM {tabella};", conn).iloc[0]['n']
                segnaRisultato(f"Tabella Presente: {tabella}", True, f"{conteggio} Righe")
            except Exception:
                segnaRisultato(f"Tabella Presente: {tabella}", False, "Tabella Non Trovata")

        conn.close()
    except Exception as e:
        segnaRisultato("Connessione Database Gadgetbridge", False, str(e))


# AA Verifica Completa Del Database Dashboard: Tabelle, Coerenza Specchio, Regressioni Note
def verificaDashboardDB(excelData):
    print(f"\n{utility.CLR_TEST}=== Verifica Database Dashboard ==={utility.CLR_RESET}")
    if not os.path.exists(DASHBOARD_DB_PATH):
        segnaRisultato("Connessione Database Dashboard", False, "File Non Trovato, Salto Il Controllo")
        return

    conn = sqlite3.connect(DASHBOARD_DB_PATH)

    tabelleAttese = [
        "smartwatch_activity_raw", "smartwatch_daily_summary",
        "smartwatch_sleep_sessions", "smartwatch_sleep_stages",
        "misure", "dieta", "personale", "allenamento", "palestra", "profilo_storico"
    ]

    # BB Presenza Tabelle E Conteggio Righe
    conteggi = {}
    for tabella in tabelleAttese:
        try:
            conteggio = pd.read_sql_query(f"SELECT COUNT(*) as n FROM {tabella};", conn).iloc[0]['n']
            conteggi[tabella] = conteggio
            segnaRisultato(f"Tabella Presente: {tabella}", True, f"{conteggio} Righe")
        except Exception:
            segnaRisultato(f"Tabella Presente: {tabella}", False, "Tabella Non Trovata")

    # BB Regressione: Nessuna Stringa "NaT" Residua (Il Bug Che Abbiamo Gia' Corretto Una Volta)
    print(f"\n{utility.CLR_TEST}--- Controllo Valori 'NaT' Residui ---{utility.CLR_RESET}")
    natTrovati = []
    for tabella in tabelleAttese:
        try:
            df = pd.read_sql_query(f"SELECT * FROM {tabella};", conn)
        except (sqlite3.Error, pd.errors.DatabaseError):
            logging.getLogger(__name__).exception(
                "Errore nel controllo della tabella dashboard %s", tabella
            )
            continue
        for colonna in df.select_dtypes(include=['object', 'str']).columns:
            match = df[df[colonna].astype(str) == "NaT"]
            if not match.empty:
                natTrovati.append(f"{tabella}.{colonna} ({len(match)} Righe)")
    segnaRisultato("Nessuna Stringa 'NaT' Residua", len(natTrovati) == 0, "; ".join(natTrovati))

    # BB Coerenza Specchio: Conteggio Righe Dashboard Deve Combaciare Con L'Excel Di Origine
    if excelData:
        print(f"\n{utility.CLR_TEST}--- Controllo Coerenza Specchio Excel <-> Dashboard ---{utility.CLR_RESET}")
        mappaSpecchio = {
            "Dati Misure": "misure",
            "Dati Dieta": "dieta",
            "Dati Allenamento": "allenamento",
            "Dati Palestra": "palestra",
        }
        for foglioExcel, tabellaDashboard in mappaSpecchio.items():
            righeExcel = len(excelData.get(foglioExcel, []))
            righeDashboard = conteggi.get(tabellaDashboard)
            segnaRisultato(
                f"Coerenza Righe: {foglioExcel} <-> {tabellaDashboard}",
                righeDashboard == righeExcel,
                f"Excel: {righeExcel}, Dashboard: {righeDashboard}"
            )

    # BB La Tabella Personale Deve Contenere Sempre Esattamente Una Riga (Vincolo id = 1)
    segnaRisultato("Tabella 'personale' Ha Esattamente 1 Riga", conteggi.get("personale") == 1, f"Trovate: {conteggi.get('personale')}")

    # BB Coerenza Del Flag Affidabile Rispetto Alla Soglia Dell'1 Giugno 2026
    print(f"\n{utility.CLR_TEST}--- Controllo Flag Affidabilita Misure ---{utility.CLR_RESET}")
    try:
        misureDf = pd.read_sql_query("SELECT data_misurazione, affidabile FROM misure;", conn)
        errori = misureDf[
            ((misureDf["data_misurazione"] < SOGLIA_AFFIDABILITA_MISURE) & (misureDf["affidabile"] != 0)) |
            ((misureDf["data_misurazione"] >= SOGLIA_AFFIDABILITA_MISURE) & (misureDf["affidabile"] != 1))
        ]
        segnaRisultato("Flag Affidabile Coerente Con La Soglia", errori.empty, f"{len(errori)} Righe Incoerenti")
    except Exception as e:
        segnaRisultato("Flag Affidabile Coerente Con La Soglia", False, str(e))

    # BB Tutti I Codici Fase Sonno Devono Essere Tra Quelli Verificati E Mappati
    print(f"\n{utility.CLR_TEST}--- Controllo Codici Fase Sonno ---{utility.CLR_RESET}")
    try:
        fasiDf = pd.read_sql_query("SELECT DISTINCT fase FROM smartwatch_sleep_stages;", conn)
        fasiConosciute = {"Sonno Profondo", "Sonno Leggero", "Sonno REM", "Sveglio"}
        fasiSconosciute = set(fasiDf["fase"]) - fasiConosciute
        segnaRisultato("Tutte Le Fasi Sonno Sono Codici Riconosciuti", len(fasiSconosciute) == 0, f"Sconosciute: {fasiSconosciute}" if fasiSconosciute else "")
    except Exception as e:
        segnaRisultato("Tutte Le Fasi Sonno Sono Codici Riconosciuti", False, str(e))

    # BB La Durata Totale Della Sessione Deve Coincidere Con Profondo + Leggero + REM (Verificato Manualmente In Precedenza)
    print(f"\n{utility.CLR_TEST}--- Controllo Coerenza Durata Sonno ---{utility.CLR_RESET}")
    try:
        sessioni = pd.read_sql_query("SELECT * FROM smartwatch_sleep_sessions;", conn)
        incoerenti = []
        for _, sessione in sessioni.iterrows():
            sommaFasi = sessione["sonno_profondo_min"] + sessione["sonno_leggero_min"] + sessione["sonno_rem_min"]
            if sommaFasi != sessione["durata_totale_min"]:
                incoerenti.append(sessione["data"])
        segnaRisultato(
            "Durata Totale Sonno = Profondo + Leggero + REM",
            len(incoerenti) == 0,
            f"Notti Incoerenti: {incoerenti}" if incoerenti else ""
        )
    except Exception as e:
        segnaRisultato("Durata Totale Sonno = Profondo + Leggero + REM", False, str(e))

    # BB Controllo Incrociato: Somma Della Timeline Fasi Deve Combaciare Con I Totali Ufficiali Della Sessione
    print(f"\n{utility.CLR_TEST}--- Controllo Incrociato Timeline Fasi Vs Sessioni Sonno ---{utility.CLR_RESET}")
    try:
        sessioni = pd.read_sql_query("SELECT * FROM smartwatch_sleep_sessions;", conn)
        fasiTimeline = pd.read_sql_query("SELECT * FROM smartwatch_sleep_stages;", conn)

        mappaFaseColonna = {
            "Sonno Profondo": "sonno_profondo_min",
            "Sonno Leggero": "sonno_leggero_min",
            "Sonno REM": "sonno_rem_min",
        }
        TOLLERANZA_MINUTI = 2
        discrepanze = []

        for _, sessione in sessioni.iterrows():
            fasiNotte = fasiTimeline[fasiTimeline["data"] == sessione["data"]]
            for fase, colonna in mappaFaseColonna.items():
                sommaTimeline = fasiNotte.loc[fasiNotte["fase"] == fase, "durata_min"].sum()
                valoreUfficiale = sessione[colonna]
                if abs(sommaTimeline - valoreUfficiale) > TOLLERANZA_MINUTI:
                    discrepanze.append(f"{sessione['data']}/{fase}: Timeline={sommaTimeline}, Ufficiale={valoreUfficiale}")

        segnaRisultato(
            "Timeline Fasi Coerente Con I Totali Ufficiali Della Sessione",
            len(discrepanze) == 0,
            "; ".join(discrepanze) if discrepanze else ""
        )
    except Exception as e:
        segnaRisultato("Timeline Fasi Coerente Con I Totali Ufficiali Della Sessione", False, str(e))

    conn.close()


# AA Stampa Il Riepilogo Finale Di Tutti I Controlli Eseguiti
def stampaRiepilogoFinale():
    print(f"\n{utility.CLR_TEST}{utility.CLR_BOLD}=========================================================={utility.CLR_RESET}")
    print(f"{utility.CLR_TEST}{utility.CLR_BOLD} RIEPILOGO VERIFICA SISTEMA{utility.CLR_RESET}")
    print(f"{utility.CLR_TEST}{utility.CLR_BOLD}=========================================================={utility.CLR_RESET}")

    totali = len(risultati)
    falliti = [r for r in risultati if not r[1]]

    print(f"Controlli Eseguiti: {utility.CLR_BOLD}{totali}{utility.CLR_RESET}")
    print(f"Superati: {utility.CLR_MISURE}{totali - len(falliti)}{utility.CLR_RESET}")
    print(f"Falliti: {utility.CLR_ERRORE}{len(falliti)}{utility.CLR_RESET}")

    if falliti:
        print(f"\n{utility.CLR_ERRORE}Controlli Falliti:{utility.CLR_RESET}")
        for nome, _, dettaglio in falliti:
            print(f"  - {nome}" + (f" ({dettaglio})" if dettaglio else ""))
    else:
        print(f"\n{utility.CLR_MISURE}{utility.CLR_BOLD}Tutti I Controlli Sono Passati! Sistema Pronto Per La Dashboard.{utility.CLR_RESET}")

    print(f"{utility.CLR_TEST}{utility.CLR_BOLD}=========================================================={utility.CLR_RESET}\n")


# AA Blocco Di Esecuzione Diretta Dello Script
if __name__ == "__main__":
    os.system('clear')
    print(f"{utility.CLR_TEST}{utility.CLR_BOLD}Avvio Verifica Completa Del Sistema...{utility.CLR_RESET}")

    verificaPercorsi()
    excelData = verificaExcel()
    verificaParserSmartwatch()
    verificaGadgetbridge()
    verificaDashboardDB(excelData)

    stampaRiepilogoFinale()
```

## trackingProgress/updateTracking.py
```py
import logging
import os
import sys
from datetime import datetime, timezone

# AA Importazione Dei Moduli Del Sistema
import dashboardSync
import diet
import measures
import pandas as pd
import personal
import smartwatch
import utility
import workout

logger = logging.getLogger(__name__)

# AA Percorsi Assoluti Per Il File System Di Windows Tramite WSL
EXCEL_PATH = "/mnt/c/Users/cicci/Documents/Appunti_E_Personale/trackingProgressi/trackingProgressi.xlsx"
OPENGYM_DATA = "/mnt/c/Users/cicci/Documents/Appunti_E_Personale/trackingProgressi/workoutData.json"
SMARTWATCH_DB = "/mnt/c/Users/cicci/Documents/Appunti_E_Personale/trackingProgressi/gadgetBridgeSync/Gadgetbridge.db"
DASHBOARD_DB_PATH = "/home/lag/## dashboardData.db"

# BB Inizializzazione E Sincronizzazione All Avvio Del Programma Lineare
os.system('clear')

# CC Definizione Dei Tag Colorati Per La Visualizzazione
tagSistema = "\033[97m[SISTEMA]\033[0m"
tagErrore = f"{utility.CLR_ERRORE}[ERRORE]{utility.CLR_RESET}"

print(f"{tagSistema} {utility.CLR_BOLD}Avvio Del Sistema Di Tracciamento Progressi...{utility.CLR_RESET}")
print(f"{tagSistema} Caricamento Dei Fogli Excel In Memoria...")

# DD Caricamento Dei Fogli Di Lavoro In Un Dizionario Di DataFrame Pandas
# EE Gestione Degli Errori In Caso Di File Excel Mancante O Aperto
try:
    excelData = {
        'Dati Personali': pd.read_excel(EXCEL_PATH, sheet_name='Dati Personali'),
        'Dati Misure': pd.read_excel(EXCEL_PATH, sheet_name='Dati Misure'),
        'Dati Dieta': pd.read_excel(EXCEL_PATH, sheet_name='Dati Dieta'),
        'Dati Allenamento': pd.read_excel(EXCEL_PATH, sheet_name='Dati Allenamento'),
        'Dati Palestra': pd.read_excel(EXCEL_PATH, sheet_name='Dati Palestra')
    }
except (OSError, ValueError) as e:
    print(f"\n{tagErrore} Impossibile Caricare Il File Excel. Verifica Che Non Sia Aperto O Che Il Percorso Sia Corretto.")
    print(f"{tagErrore} Errore Rilevato: {e}\n")
    sys.exit()

# AA Inizializzazione Del Database Dashboard (Crea Le Tabelle Se Non Esistono Ancora)
dashboardSync.initializeDashboardDB(DASHBOARD_DB_PATH)

# AA Sincronizzazione Silenziosa Iniziale Del Profilo
# DD Esecuzione Della Sincronizzazione Silenziosa Iniziale Senza Output
# EE Soppressione Temporanea Dei Print Per Avviare Direttamente Il Menu
oldStdout = sys.stdout
with open(os.devnull, 'w') as suppressedStdout:
    try:
        sys.stdout = suppressedStdout
        personal.updatePersonalData(excelData, EXCEL_PATH)
    finally:
        sys.stdout = oldStdout

# AA Ciclo Principale Dell Interfaccia Utente A Livello Root
while True:
    os.system('clear')
    
    # CC Stampa Del Menu Principale Con I Colori Identificativi
    print("==========================================================")
    print(f" {utility.CLR_BOLD}SISTEMA DI TRACCIAMENTO PROGRESSI - MENU PRINCIPALE{utility.CLR_RESET}")
    print("==========================================================")
    print(f" {utility.CLR_MISURE}1. Inserisci Nuova Misura Corporea{utility.CLR_RESET}")
    print(f" {utility.CLR_DIETA}2. Registra Nuova Fase Alimentare{utility.CLR_RESET}")
    print(f" {utility.CLR_ALLENAMENTO}3. Sincronizza Allenamenti{utility.CLR_RESET}")
    print(f" {utility.CLR_SMARTWATCH}4. Sincronizza Dashboard{utility.CLR_RESET}")
    print(f" {utility.CLR_PROFILO}5. Mostra Riepilogo Profilo Corrente{utility.CLR_RESET}")
    print(" 6. Esci Dal Programma")
    print("==========================================================")
    
    scelta = input(f"{tagSistema} Inserisci Il Numero Della Scelta: ").strip()
    
    if scelta == "1":
        os.system('clear')
        # DD Esecuzione Inserimento Misure
        measures.updateMeasuresData(excelData, EXCEL_PATH)
        # EE Sincronizzazione Automatica Del Profilo A Cascata
        personal.updatePersonalData(excelData, EXCEL_PATH)
        input(f"\n{tagSistema} Operazione Completata. Premi Invio Per Tornare Al Menu...")
        
    elif scelta == "2":
        os.system('clear')
        
        # DD Controllo Fuori Soglia Mensile Per Misurazioni Corporee (Overdue Check)
        measureData = excelData['Dati Misure']
        if len(measureData) > 0:
            latestDate = pd.to_datetime(measureData['Data Misurazione'].iloc[-1]).date()
            daysElapsed = (datetime.now(timezone.utc).date() - latestDate).days
            
            if daysElapsed > 40:
                print(f"{utility.CLR_ERRORE}[ATTENZIONE]{utility.CLR_RESET} L'Ultima Misura Corporea Risale A {utility.CLR_BOLD}{daysElapsed} Giorni Fa{utility.CLR_RESET} (Soglia: 40).")
                sceltaMisure = input(f"{utility.CLR_MISURE}[MISURE]{utility.CLR_RESET} Vuoi Inserire Una Nuova Misura Adesso Prima Della Dieta? (S/N): ").strip().upper()
                
                if sceltaMisure == 'S':
                    os.system('clear')
                    # EE Avvio Esecuzione Misure In Caso Di Risposta Affermativa
                    measures.updateMeasuresData(excelData, EXCEL_PATH)
                    # AA Sincronizzazione Del Profilo Post Misure
                    personal.updatePersonalData(excelData, EXCEL_PATH)
                    input(f"\n{tagSistema} Misurazioni Salvate. Premi Invio Per Continuare Con L Inserimento Della Dieta...")
                    os.system('clear')
                    
        # EE Esecuzione Inserimento Dieta
        diet.updateDietData(excelData, EXCEL_PATH)
        # AA Sincronizzazione Automatica Del Profilo A Cascata
        personal.updatePersonalData(excelData, EXCEL_PATH)
        input(f"\n{tagSistema} Operazione Completata. Premi Invio Per Tornare Al Menu...")
        
    elif scelta == "3":
        os.system('clear')
        # DD Avvio Processamento Dei Dati Allenamento Da JSON
        try:
            workoutData, gymSummary = workout.processWorkoutData(OPENGYM_DATA, excelData)
            # EE Aggiornamento Delle Due Schede Allenamento E Palestra
            workout.updateTrainData(workoutData, excelData, EXCEL_PATH)
            workout.updateGymData(gymSummary, excelData, EXCEL_PATH)
        except (OSError, ValueError, KeyError, TypeError) as e:
            print(f"\n{tagErrore} Si È Verificato Un Errore Durante L'Importazione.")
            print(f"{tagErrore} Dettaglio Errore: {e}")
        input(f"\n{tagSistema} Operazione Completata. Premi Invio Per Tornare Al Menu...")

    elif scelta == "4":
        os.system('clear')
        # DD Estrazione Dei Dati Smartwatch (Attivita, Riepilogo Giornaliero, Sonno)
        activityData, dailySummary, sleepSessions, sleepStages = smartwatch.processSmartwatchData(SMARTWATCH_DB)
        # EE Sincronizzazione Dello Smartwatch E Specchio Dei Dati Excel Verso Il Database Dashboard
        dashboardSync.syncSmartwatchData(DASHBOARD_DB_PATH, activityData, dailySummary, sleepSessions, sleepStages)
        dashboardSync.syncTrackingMirror(DASHBOARD_DB_PATH, excelData)
        input(f"\n{tagSistema} Operazione Completata. Premi Invio Per Tornare Al Menu...")

    elif scelta == "5":
        os.system('clear')
        # DD Visualizzazione Dei Dati Personali
        print("==========================================================")
        print(f" {utility.CLR_PROFILO}{utility.CLR_BOLD}RIEPILOGO PROFILO UTENTE{utility.CLR_RESET}")
        print("==========================================================")
        personalDf = excelData['Dati Personali']
        for idx, row in personalDf.iterrows():
            param = row['Parametro']
            val = row['Valore']
            
            # EE Formattazione Delle Date Nel Formato Lineare GG-MM-AAAA HH-MM
            valFormatted = val
            if isinstance(val, (pd.Timestamp, datetime)):
                valFormatted = val.strftime("%d-%m-%Y %H:%M")
            elif param in ['Data Di Nascita', 'Ultimo Aggiornamento']:
                try:
                    valFormatted = pd.to_datetime(val).strftime("%d-%m-%Y %H:%M")
                except (ValueError, TypeError) as exc:
                    logger.debug("Impossibile Formattare Il Valore Di %s: %r", param, val, exc_info=exc)
            
            # EE Formattazione Allineata Per Le Righe Del Cruscotto
            print(f" {utility.CLR_PROFILO}{param:<30}{utility.CLR_RESET} : {utility.CLR_BOLD}{valFormatted}{utility.CLR_RESET}")
        print("==========================================================")
        input(f"\n{tagSistema} Premi Invio Per Tornare Al Menu...")

    elif scelta == "6":
        os.system('clear')
        print(f"\n{tagSistema} {utility.CLR_BOLD}Chiusura Del Programma Di Tracciamento Progressi. Alla Prossima!{utility.CLR_RESET}\n")
        break
        
    else:
        input(f"\n{tagErrore} Scelta Non Valida. Premi Invio Per Riprovare...")
```

## trackingProgress/utility.py
```py

# AA Codici Di Formattazione ANSI Per Il Terminale
# BB Colori Associati Ai Vari Moduli Del Sistema
CLR_MISURE = "\033[92m"         # Verde Chiaro Per Il Modulo Misure
CLR_ERRORE = "\033[91m"         # Rosso Chiaro Per Errori E Blocchi
CLR_RESET = "\033[0m"           # Ripristina Il Colore Di Default Del Terminale
CLR_BOLD = "\033[1m"            # Applica Il Grassetto Al Testo
CLR_PROFILO = "\033[96m"        # Azzurro/Ciano Chiaro Per Il Modulo Profilo
CLR_ALLENAMENTO = "\033[95m"    # Magenta Chiaro Per Il Modulo Allenamento
CLR_PALESTRA = "\033[35m"       # Viola Per Il Modulo Della Bacheca Record Palestra
CLR_DIETA = "\033[93m"          # Giallo Chiaro Per Il Modulo Dieta
CLR_SMARTWATCH = "\033[94m"     # Blu Chiaro Per Il Modulo Smartwatch
CLR_DASHBOARD = "\033[36m"      # Ciano Per Il Modulo Dashboard
CLR_TEST = "\033[97m"           # Bianco Brillante Per Il Modulo Di Verifica Sistema

# AA Funzione Per Gestire Input Opzionali
def optionalInput(prompt):
    value = input(prompt)
    if value.strip() == "":
        return None
    else:
        # CC Conversione Diretta In Numero Se Presente
        return round(float(value), 2)

# AA Funzione Per Convertire Stringhe Di Data In Formato Standard
monthMap = {
    'gen': '01', 'feb': '02', 'mar': '03', 'apr': '04',
    'mag': '05', 'giu': '06', 'lug': '07', 'ago': '08',
    'set': '09', 'ott': '10', 'nov': '11', 'dic': '12'
}

def parseHeavyData(dateStr):
    for month, number in monthMap.items():
        dateStr = dateStr.replace(month, number)
    return dateStr
```

## trackingProgress/workout.py
```py
import json
import os
from copy import copy

import openpyxl
import pandas as pd
import utility


# AA Funzione Per Elaborare I Dati Allenamento E Generare Due DataFrame: workoutData E gymSummary
def processWorkoutData(OPENGYM_DATA, excelData):
    # AA Definizione Dei Tag Colorati Per La Visualizzazione
    tagAllenamento = f"{utility.CLR_ALLENAMENTO}[ALLENAMENTO]{utility.CLR_RESET}"
    
    # AA Caricamento E Parsing Dati Iniziali
    # BB Caricamento Del Catalogo Esercizi Da File Locale (exercisesCatalog.json)
    baseDir = os.path.dirname(os.path.abspath(__file__))
    catalogPath = os.path.join(baseDir, "openGymData", "exercisesCatalog.json")

    exerciseCatalog = {}
    if os.path.exists(catalogPath):
        with open(catalogPath, 'r', encoding='utf-8') as f:
            exerciseCatalog = json.load(f)

    # BB Caricamento File JSON Di openGym
    with open(OPENGYM_DATA, 'r', encoding='utf-8') as f:
        openGymData = json.load(f)

    # CC Integrazione Degli Esercizi Personalizzati Presenti Nel Backup (customEx)
    for cEx in openGymData.get('customEx', []):
        exerciseCatalog[cEx['id']] = cEx.get('n', cEx['id']).title()

    # CC Estrazione Delle Sessioni E Appiattimento Dei Dati Delle Serie
    parsedRows = []
    for w in openGymData.get('workouts', []):
        wDate = w.get('d')
        wName = w.get('name', 'Allenamento')
        wNote = w.get('note', w.get('description', ''))
        startMs = w.get('start')
        endMs = w.get('end')

        for entry in w.get('entries', []):
            exId = entry.get('id')
            exTitle = exerciseCatalog.get(exId, f"Esercizio ({exId})")

            for s in entry.get('sets', []):
                # Escludiamo Eventuali Serie Non Concluse
                if not s.get('done', True):
                    continue

                parsedRows.append({
                    'start_ms': startMs,
                    'end_ms': endMs,
                    'data_str': wDate,
                    'Nome Scheda': wName,
                    'Nome Esercizio': exTitle,
                    'set_type': s.get('phase', 'normal'),
                    'Peso Serie': float(s.get('w', 0)),
                    'Ripetizioni Serie': int(s.get('r', 0)),
                    'Note Post Allenamento': wNote
                })

    workoutData = pd.DataFrame(parsedRows)

    if workoutData.empty:
        return pd.DataFrame(), pd.DataFrame()

    # BB Conversione Date E Calcolo Durata Sessione
    workoutData["Inizio Allenamento"] = pd.to_datetime(workoutData['start_ms'], unit='ms')
    workoutData["Fine Allenamento"] = pd.to_datetime(workoutData["end_ms"], unit='ms')
    workoutData["Data"] = pd.to_datetime(workoutData['data_str']).dt.date
    workoutData["Durata Allenamento"] = (workoutData["Fine Allenamento"] - workoutData["Inizio Allenamento"]).dt.total_seconds() / 60

    # BB Rimozione Colonne Non Necessarie Nel Flusso Iniziale
    columnsToRemove = ['start_ms', 'end_ms', 'data_str', 'Fine Allenamento']
    workoutData = workoutData.drop(columns=columnsToRemove)

    # BB Rimozione Righe Di Riscaldamento E Colonna Tipo Serie
    warmupMask = workoutData['set_type'] == 'warmup'
    rowToRemove = workoutData[warmupMask].index
    workoutData = workoutData.drop(rowToRemove)
    workoutData = workoutData.drop(columns=['set_type'])

    # BB Rimozione Automatica Di Cardio E Attività A Corpo Libero Senza Sovraccarico
    # CC Manteniamo Esclusivamente Le Righe Dove Viene Utilizzato Un Peso Maggiore Di Zero
    # DD Questo Filtro Esclude In Modo Dinamico Corsa, Bici, Plank, Crunch E Corpo Libero Non Zavorrato
    workoutData = workoutData[workoutData['Peso Serie'] > 0]

    # BB Adeguamento Indice Serie In Base 1 Con Ricalcolo Post-Warmup
    # CC Ricalcoliamo La Sequenza Delle Serie Allenanti Usando L'Ora Di Inizio Per Distinguere Le Sessioni Nello Stesso Giorno
    workoutData["Indice Serie"] = workoutData.groupby(['Inizio Allenamento', 'Nome Esercizio']).cumcount() + 1

    # CC Rimozione Della Colonna Di Servizio Temporale Non Più Necessaria Nel DataFrame
    workoutData = workoutData.drop(columns=['Inizio Allenamento'])

    # BB Calcolo Volume E Massimale Per Singola Serie (Espansione Dati Allenamento)
    # CC Calcolo Volume Della Singola Serie (Peso * Reps)
    workoutData["Volume Serie"] = workoutData["Peso Serie"] * workoutData["Ripetizioni Serie"]

    # CC Calcolo Massimale Stimato Di Riga Tramite Formula Epley
    # DD Formula Di Epley: Peso * (1 + Reps / 30)
    workoutData["Massimale Stimato Serie"] = workoutData["Peso Serie"] * (1 + workoutData["Ripetizioni Serie"] / 30)

    # CC Arrotondamento E Conversione In Intero Delle Nuove Metriche Di Riga
    # EE La Conversione In Int Non Genera Errori Poiché Non Vi Sono Più Valori NaN Nel Dataset
    workoutData["Volume Serie"] = workoutData["Volume Serie"].round().astype(int)
    workoutData["Massimale Stimato Serie"] = workoutData["Massimale Stimato Serie"].round().astype(int)


    # AA Setting Colonne DataFrame Per "Dati Palestra" (Bacheca Record Assoluti)
    # BB Copia Del DataFrame Master Espanso
    gymSummary = workoutData.copy()

    # BB Raggruppamento Temporaneo Per Data E Nome Esercizio (85 Sessioni)
    groupedSummary = gymSummary.groupby(['Data', 'Nome Esercizio'])

    gymSummary = groupedSummary.agg({
        'Indice Serie': 'count',
        'Ripetizioni Serie': 'mean',
        'Peso Serie': 'mean',
        'Volume Serie': 'sum',
        'Massimale Stimato Serie': 'max',
        'Note Post Allenamento': 'first'
    }).reset_index()

    # BB Rinomina Delle Metriche Aggregate Di Sessione
    renameMapGym = {
        'Indice Serie': 'Numero Serie',
        'Ripetizioni Serie': 'Ripetizioni Medie',
        'Peso Serie': 'Peso Medio',
        'Volume Serie': 'Volume Totale (Kg)',
        'Massimale Stimato Serie': 'Massimale Stimato (1RM)'
    }
    gymSummary = gymSummary.rename(columns=renameMapGym)

    # BB Approssimazione Medie E Arrotondamenti A Numeri Interi
    gymSummary['Ripetizioni Medie'] = gymSummary['Ripetizioni Medie'].round().astype(int)
    gymSummary['Peso Medio'] = gymSummary['Peso Medio'].round().astype(int)

    # BB Creazione Colonna Schema Riassuntivo Di Sessione
    # CC Utilizzo Di Una Funzione Lambda Per Formattare I Tre Parametri Chiave
    gymSummary['Schema'] = gymSummary.apply(lambda row: f"{row['Numero Serie']}x{row['Ripetizioni Medie']}x{row['Peso Medio']}kg", axis=1)

    # BB Riduzione A Un Record Assoluto Storico Per Ciascun Esercizio 
    # CC Identificazione Della Riga Con Il Massimo 1RM Storico Per Ogni Singolo Gruppo Esercizio
    gymSummary = gymSummary.loc[gymSummary.groupby('Nome Esercizio')['Massimale Stimato (1RM)'].idxmax()].reset_index(drop=True)

    # CC Ordinamento Alfabetico Degli Esercizi Per Una Migliore Resa Estetica Su Excel
    gymSummary = gymSummary.sort_values(by='Nome Esercizio').reset_index(drop=True)
    # DD -----------------------------------------------

    # EE -----------------------------------------------
    # AA Confronto Con Excel E Filtraggio Dati Allenamento Già Presenti
    existingWorkout = excelData['Dati Allenamento']

    # CC Definizione Delle Colonne Per Entrambi I DataFrame Per Garantire Coerenza Di Scrittura
    columnsWorkout = ['Data', 'Durata Allenamento', 'Nome Scheda', 'Nome Esercizio', 
                    'Indice Serie', 'Ripetizioni Serie', 'Peso Serie', 'Volume Serie', 
                    'Massimale Stimato Serie', 'Note Post Allenamento']

    columnsGym = ['Nome Esercizio', 'Schema', 'Volume Totale (Kg)', 'Data', 'Numero Serie', 
                'Ripetizioni Medie', 'Peso Medio', 'Massimale Stimato (1RM)', 'Note Post Allenamento']

    if existingWorkout.empty:
        print(f"\n{tagAllenamento} Nessun Dato Allenamento Precedente Trovato In Excel. Tutti I Dati Saranno Importati.\n")
    else:
        # CC Filtraggio Dati Allenamento Già Presenti In Excel Tramite Calcolo Della Data Massima
        existingWorkoutDate = pd.to_datetime(existingWorkout['Data']).dt.date
        lastExistingDate = existingWorkoutDate.max()
        print(f"\n{tagAllenamento} Ultima Data Allenamento Presente In Excel: {utility.CLR_BOLD}{lastExistingDate}{utility.CLR_RESET}\n")
        lastDateMask = workoutData['Data'] > lastExistingDate
        workoutData = workoutData[lastDateMask]

    # CC Riordino E Selezione Delle Colonne Eseguito In Ogni Caso (Sia Con Excel Vuoto Che Popolato)
    workoutData = workoutData[columnsWorkout]
    gymSummary = gymSummary[columnsGym]
    # EE -----------------------------------------------

    return workoutData, gymSummary

# AA Funzione Per Aggiornare Scheda Dati Allenamento In Excel Con I Nuovi Allenamenti
def updateTrainData(workoutData, excelData, EXCEL_PATH):
    # BB Definizione Dei Tag Colorati Per La Visualizzazione
    tagAllenamento = f"{utility.CLR_ALLENAMENTO}[ALLENAMENTO]{utility.CLR_RESET}"

    # BB Controllo Preliminare Se Ci Sono Nuovi Record Di Allenamento Rilevati
    if workoutData is None or len(workoutData) == 0:
        print(f"{tagAllenamento} Nessun Nuovo Allenamento Rilevato Da Inserire.\n")
        return
    else:
        print(f"{tagAllenamento} Rilevati {utility.CLR_BOLD}{len(workoutData)}{utility.CLR_RESET} Nuovi Record Da Salvare.\n")

    # CC Preparazione Dei Dati E Allineamento Colonne Per La Scheda Dati Allenamento
    dfToAppend = workoutData.copy()
    if 'Data Allenamento' in dfToAppend.columns and 'Data' not in dfToAppend.columns:
        dfToAppend = dfToAppend.rename(columns={'Data Allenamento': 'Data'})

    excelColumns = [
        'Data', 'Durata Allenamento', 'Nome Scheda', 'Nome Esercizio', 
        'Indice Serie', 'Ripetizioni Serie', 'Peso Serie', 'Volume Serie', 
        'Massimale Stimato Serie', 'Note Post Allenamento'
    ]
    dfToAppend = dfToAppend[excelColumns]

    # DD Caricamento Del File Excel Con Openpyxl Per Preservare Stili, Colori E Larghezze Delle Celle E Aggiunta Nuove Righe
    excelFile = openpyxl.load_workbook(EXCEL_PATH)
    workoutSheet = excelFile['Dati Allenamento']

    # DD Scrittura Delle Nuove Righe Nel Foglio Di Lavoro
    for idx, row in dfToAppend.iterrows():
        # EE Creazione Della Lista Ordinata Dei Nuovi Valori Per Ciascuna Riga
        newValue = []
        for colName in excelColumns:
            val = row[colName]
            
            # Gestione Dei Valori Nulli O Incompatibili Con Excel
            if pd.isna(val):
                val = ""
                
            # Conversione Del Formato Data Di Pandas Per Evitare Errori Di Scrittura
            if colName == 'Data' and isinstance(val, pd.Timestamp):
                val = val.date()
                
            newValue.append(val)
            
        workoutSheet.append(newValue)
        lastRowIdx = workoutSheet.max_row
        
        # EE Copia Della Formattazione Dalla Riga Precedente (Incluso Formato Data, Carattere E Allineamenti)
        if lastRowIdx > 2: # Riga 1 = Intestazioni, Riga 2 = Primo Dato (Se Esiste, Copiamo Da Lì)
            for col_idx in range(1, len(newValue) + 1):
                sourceCell = workoutSheet.cell(row=lastRowIdx - 1, column=col_idx)
                targetCell = workoutSheet.cell(row=lastRowIdx, column=col_idx)
                
                # Copiamo Gli Stili E Il Formato Numerico Se Presenti (Silenziando I Falsi Positivi Di Pylance)
                if sourceCell.has_style:
                    targetCell.font = copy(sourceCell.font)  # type: ignore
                    targetCell.border = copy(sourceCell.border)  # type: ignore
                    targetCell.fill = copy(sourceCell.fill)  # type: ignore
                    targetCell.alignment = copy(sourceCell.alignment)  # type: ignore
                    targetCell.number_format = sourceCell.number_format

        else:
            # Formattazione Manuale Solo Se È La Prima Riga Di Dati In Assoluto
            # Formato Data Per La Colonna 1 (Data Allenamento)
            workoutSheet.cell(row=lastRowIdx, column=1).number_format = 'DD-MM-YYYY'
            
    # DD Salvataggio Del File Excel Per Applicare Le Modifiche Senza Ricreare I Fogli
    excelFile.save(EXCEL_PATH)
    excelFile.close()

    # DD Sincronizzazione Del DataFrame In Memoria Per Coerenza Della Sessione
    excelData['Dati Allenamento'] = pd.concat([excelData['Dati Allenamento'], dfToAppend], ignore_index=True)

    print(f"{tagAllenamento} {utility.CLR_BOLD}Dati Di Allenamento E Calcoli Salvati Con Successo Nel File Excel!{utility.CLR_RESET}\n")


# AA Funzione Per Ricreare La Scheda Dati Palestra In Excel Con I Nuovi Record
def updateGymData(gymSummary, excelData, EXCEL_PATH):
    # BB Definizione Dei Tag Colorati Per La Visualizzazione
    tagPalestra = f"{utility.CLR_PALESTRA}[PALESTRA]{utility.CLR_RESET}"

    # BB Controllo Preliminare Se Ci Sono Record Di Palestra Da Aggiornare
    if gymSummary is None or len(gymSummary) == 0:
        print(f"{tagPalestra} Nessun Record Rilevato Da Aggiornare.\n")
        return
    else:
        print(f"{tagPalestra} Aggiornamento Di {utility.CLR_BOLD}{len(gymSummary)}{utility.CLR_RESET} Record Storici In Corso...\n")

    # BB Preparazione Dei Dati E Allineamento Colonne Per La Scheda Dati Palestra
    dfToOverwrite = gymSummary.copy()
    
    excelColumns = [
        'Nome Esercizio', 'Schema', 'Volume Totale (Kg)', 'Data', 
        'Numero Serie', 'Ripetizioni Medie', 'Peso Medio', 
        'Massimale Stimato (1RM)', 'Note Post Allenamento'
    ]
    dfToOverwrite = dfToOverwrite[excelColumns]

    # CC Caricamento Del File Excel Con Openpyxl Per Preservare Stili, Colori E Larghezze Delle Celle E Sovrascrittura
    excelFile = openpyxl.load_workbook(EXCEL_PATH)
    gymSheet = excelFile['Dati Palestra']

    # CC Salvataggio Degli Stili Esistenti Dalla Riga 2 Come Modello Per Il Popolamento
    styleTemplates = {}
    if gymSheet.max_row >= 2:
        for col_idx in range(1, len(excelColumns) + 1):
            cell = gymSheet.cell(row=2, column=col_idx)
            styleTemplates[col_idx] = {
                'font': copy(cell.font),
                'border': copy(cell.border),
                'fill': copy(cell.fill),
                'alignment': copy(cell.alignment),
                'number_format': cell.number_format
            }

    # CC Rimozione Di Tutti I Record Esistenti Dalla Scheda Per Consentire La Sovrascrittura Completa
    if gymSheet.max_row > 1:
        gymSheet.delete_rows(2, amount=gymSheet.max_row)

    # CC Scrittura Dei Nuovi Record Nel Foglio Di Lavoro
    for idx, row in dfToOverwrite.iterrows():
        # CC Creazione Della Lista Ordinata Dei Nuovi Valori Per Ciascuna Riga
        newValue = []
        for colName in excelColumns:
            val = row[colName]
            
            # EE Gestione Dei Valori Nulli O Incompatibili Con Excel
            if pd.isna(val):
                val = ""
                
            # EE Conversione Del Formato Data Di Pandas Per Evitare Errori Di Scrittura
            if colName == 'Data' and isinstance(val, pd.Timestamp):
                val = val.date()
                
            newValue.append(val)
            
        gymSheet.append(newValue)
        lastRowIdx = gymSheet.max_row
        
        # DD Copia Della Formattazione Tramite I Modelli Salvati In Precedenza
        if len(styleTemplates) > 0:
            for col_idx in range(1, len(newValue) + 1):
                targetCell = gymSheet.cell(row=lastRowIdx, column=col_idx)
                tpl = styleTemplates[col_idx]
                
                # Copiamo Gli Stili E Il Formato Numerico (Silenziando I Falsi Positivi Di Pylance)
                targetCell.font = copy(tpl['font'])  # type: ignore
                targetCell.border = copy(tpl['border'])  # type: ignore
                targetCell.fill = copy(tpl['fill'])  # type: ignore
                targetCell.alignment = copy(tpl['alignment'])  # type: ignore
                targetCell.number_format = tpl['number_format']
        else:
            # EE Formattazione Manuale Solo Se La Scheda Era Completamente Vuota
            # Formato Data Per La Colonna 4 (Data)
            gymSheet.cell(row=lastRowIdx, column=4).number_format = 'DD-MM-YYYY'

    # CC Salvataggio Del File Excel Per Applicare Le Modifiche Senza Ricreare I Fogli
    excelFile.save(EXCEL_PATH)
    excelFile.close()

    # CC Sincronizzazione Del DataFrame In Memoria Per Coerenza Della Sessione
    excelData['Dati Palestra'] = dfToOverwrite

    print(f"{tagPalestra} {utility.CLR_BOLD}Record Storici Personali Aggiornati E Salvati Con Successo!{utility.CLR_RESET}\n")
```
