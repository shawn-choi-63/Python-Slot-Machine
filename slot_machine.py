#TODO: Add functionality for users to add symbols
#TODO: Add functionality for users to edit reels
#TODO: Add functionality for users to edit pay table
#TODO: Add functionality for users to edit amount of reels
#TODO: Add functionality for users to simulate games and compare deltas to PAR Sheet
#TODO: Refactor print_par_sheet function to be scalable for more reels

SYMBOLS_REGISTRY = {
    "bell":      {"name": "Bell", "icon": "🔔"},
    "heart":     {"name": "Heart", "icon": "💖"},
    "diamond":   {"name": "Diamond", "icon": "💎"},
    "spade":     {"name": "Spade", "icon": "🖤"},
    "horseshoe": {"name": "Horseshoe", "icon": "🐴"},
    "star":      {"name": "Star", "icon": "⭐"}
}

REELS = [
    ['bell', 'horseshoe', 'spade', 'horseshoe', 'diamond', 'horseshoe', 'spade', 'horseshoe', 'heart', 'horseshoe'],
    ['bell', 'horseshoe', 'spade', 'horseshoe', 'diamond', 'horseshoe', 'spade', 'horseshoe', 'heart', 'horseshoe'],
    ['bell', 'diamond', 'star', 'spade', 'bell', 'diamond', 'heart', 'star', 'spade', 'diamond']
]

PAY_TABLE = [
    {"line": ['bell', 'bell', 'bell'], "pays": 20},
    {"line": ['heart', 'heart', 'heart'], "pays": 16},
    {"line": ['diamond', 'diamond', 'diamond'], "pays": 12},
    {"line": ['spade', 'spade', 'spade'], "pays": 8},
    {"line": ['horseshoe', 'horseshoe', 'star'], "pays": 4},
    {"line": ['horseshoe', 'horseshoe', 'any-star'], "pays": 2},
]


def calculate_ways_to_win():
    ret = []
    for entry in PAY_TABLE:
        winning_line = entry["line"]
        line_count = 1
        for i in range(len(winning_line)):
            count = 0
            for stop in REELS[i]:
                if "any-" in winning_line[i]:
                    ignore = winning_line[i].split("any-")[1]
                    if ignore != stop:
                        count += 1
                
                elif winning_line[i] == stop:
                    count += 1
            line_count *= count
        ret.append(line_count)
    return ret

def calculate_total_payouts(wins):
    ret = []
    for i in range(len(wins)):
        ret.append(PAY_TABLE[i]["pays"] * wins[i])
    return ret

def get_symbol_distribution():
    keys = list(SYMBOLS_REGISTRY.keys())
    ret = [[] for _ in range(len(keys))]

    for i in range(len(keys)):
        for reel in REELS:
            ret[i].append(reel.count(keys[i]))
    
    size = [len(reel) for reel in REELS]
    total_ways = 1
    for reel in size:
        total_ways *= reel
    ret.append([size, total_ways])
    return ret
            


def print_par_sheet():
    distribution = get_symbol_distribution()
    total_ways = distribution[-1][1]
    reel_lengths = distribution[-1][0]
    
    wins = calculate_ways_to_win()
    total_ways_to_win = sum(wins)

    payouts = calculate_total_payouts(wins)
    total_payout = sum(payouts)

    #just using these for the print so type casting them now so it's easier to truncate the strings

    hit_frequency = total_ways_to_win / total_ways
    rtp = str(total_payout / total_ways * 100)
    avg_spins_to_win = str(1 / hit_frequency)
    hit_frequency = str(hit_frequency * 100)


    print("=" * 40)
    print(" SLOT MACHINE PAR SHEET ")
    print("=" * 40)
    print(" Reel 1 | Reel 2 | Reel 3 ")

    transposed = [list(row) for row in zip(*REELS)]
    for row in transposed:
        row_display = ""
        for item in row:
            icon = SYMBOLS_REGISTRY.get(item, {}).get("icon", "❓")
            
            row_display +="   " + icon + "   " 
        print (row_display)
    print("=" * 40)

    print(" SYMBOL DISTRIBUTION ")
    print(" Symbol | Reel 1 | Reel 2 | Reel 3 ")
    for symbol_id, symbol_data in SYMBOLS_REGISTRY.items():
        #this is not a good way to do this -- it's not scalable if I want to add more reels. Come back and fix later
        print("   " + symbol_data["icon"] + "        " + str(REELS[0].count(symbol_id)) + "        " + str(REELS[1].count(symbol_id)) + "        " + str(REELS[2].count(symbol_id)))
    print(" Totals      " + str(len(REELS[0])) + "       " + str(len(REELS[1])) + "       " + str(len(REELS[2])))
    print(" Total Ways: " + str(total_ways))

    print(f"{'Winning Line':<10} | {'Pays':<6} | {'Ways To Win'} | {'Total Payout'}")
    print("-" * 40)
    for i in range(len(PAY_TABLE)):
        emojis = "".join([SYMBOLS_REGISTRY.get(sid, {}).get("icon", "❓") for sid in PAY_TABLE[i]["line"]])
        print(f"{emojis:<9} | {PAY_TABLE[i]['pays']:<6} | {wins[i]:<11} | {payouts[i]}")
    print("Total Ways To Win: " + str(total_ways_to_win))
    print("Total Payout: " + str(total_payout))
    print("Hit Frequency: "  + hit_frequency[:4] + "%")
    print("RTP: " + rtp + "%")
    print("Average Spins Until Win: " + avg_spins_to_win[:4])
    print("=" * 40)

print_par_sheet()