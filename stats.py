import json
seasons = json.load(open("seasons.json"))
print(seasons)
players = {}

canonical = {
    "Terell, Neal" : "Terrell, Neal",
    "Longbhen, Michael" : "Longbehn, Michael",
    "Chango, Juno" : "Chang, Juno",
    "Grespie, Jason" : "Gruspe, Jason",
    "Mesa, Matt" : "Mesa, Matthew",
    "Braulio, V" : "Velazquez, Braulio",
    "Velasquez, Braulio" : "Velazquez, Braulio"
}

columns = [None, None, "AB", "H", "AVG", "R", "RBI", "2B", "3B", "HR", "SLG", "OBP", "RSP", "SAF", "K", "BB", "PO", "A", "E", "FAVE", "IP", "H", "K", "BB", "R", "ER", "ERA"]
dontadd = set([4, 10, 11, 12, 19, 26])
convert = [None, None, int, int, float, int, int, int, int, int, float, float, float, int, int, int, int, int, int, float, float, int, int, int, int, int, float]
def addint(stat1, stat2):
    stat1 = int(stat1)
    stat2 = int(stat2)
    return stat1 + stat2

def addfloat(stat1, stat2):
    stat1 = float(stat1)
    stat2 = float(stat2)
    return stat1 + stat2

for s in seasons:
    for p in s["players"]:
        stats = {"season": s["season"], "stats": p}
        name = p[1] if p[1] not in canonical else canonical[p[1]]
        if name not in players:
            players[name ] = [stats]
        else:
            players[name].append(stats)


for name, stats in players.items():
    totals = [0] * len(columns)
    
    if "Player" not in name:
        with open(f"{name}.md", "w") as file:
            # header
            file.write(f"# {name}\n\n")

            file.write("| Season      ")
            for c in columns:
                if c is not None:
                    file.write(f"| {c.ljust(11, ' ')} ")
            file.write("\n")
            file.write(("| ----------- " * (len(columns)-1)) + "\n")
                
            for season in stats:
                file.write(f"| {season['season'].ljust(11)} ")
                for i, stat in enumerate(season['stats']):
                    if columns[i] is not None:
                        file.write(f"| {stat.ljust(11, ' ')} ")
                        if i not in dontadd:
                            totals[i] += convert[i](stat)
                file.write("\n")
            file.write("| **Totals**  ")
            totals[4] = f"{totals[3] / totals[2]:.3f}"[1:]
            singles = totals[3] - totals[7] - totals[8] - totals[9]

            def stripzero(s):
                if s.startswith('0'):
                    return s[1:]
                return s
            
            if totals[2] != 0:
                totals[10] = stripzero(f"{(singles + totals[7] * 2 + totals[8] * 3 + totals[9] * 4) / totals[2]:.3f}")
            if totals[16] + totals[17] + totals[18] != 0:
                totals[19] = stripzero(f"{(totals[16] + totals[17]) / (totals[16] + totals[17] + totals[18]):.3f}")
            if totals[20] != 0:
                totals[26] = stripzero(f"{(totals[25] / totals[20] * 7):.3f}")
            for i, t in enumerate(totals):
                if columns[i] is not None:
                    file.write(f"| {str(t).ljust(11, ' ')} ")
            file.write("\n")