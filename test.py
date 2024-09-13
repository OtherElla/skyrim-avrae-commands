<drac2>
args = "&*&".strip().lower().split()
if not args:
    return f'-title "Test" -desc "Usage: `!shout [words of power]`"'

# Get character stats
proficiency_bonus = proficiencyBonus
charisma_mod = charismaMod

# Define the shouts with their properties
shouts = {
    "fus": {
        "name": "Unrelenting Force",
        "words": ["fus", "roh", "dah"],
        "levels": {
            "1": {
                "name": "Fus (Force)",
                "range": "15-foot cone",
                "damage_dice": "2d6",
                "push_distance": 10,
                "prone": False,
                "dc": 8 + proficiency_bonus + charisma_mod,
                "image": "https://media1.tenor.com/m/O8zaeaYI8NkAAAAd/fus-roh-dah-skyrim.gif"
            },
            "2": {
                "name": "Fus Roh (Force Balance)",
                "range": "30-foot cone",
                "damage_dice": "4d6",
                "push_distance": 20,
                "prone": True,
                "dc": 10 + proficiency_bonus + charisma_mod,
                "image": "https://media1.tenor.com/m/O8zaeaYI8NkAAAAd/fus-roh-dah-skyrim.gif"
            },
            "3": {
                "name": "Fus Roh Dah (Unrelenting Force)",
                "range": "60-foot cone",
                "damage_dice": "6d6",
                "push_distance": 30,
                "prone": True,
                "dc": 12 + proficiency_bonus + charisma_mod,
                "image": "https://media1.tenor.com/m/O8zaeaYI8NkAAAAd/fus-roh-dah-skyrim.gif"
            }
        }
    },
    "wuld": {
        "name": "Whirlwind Sprint",
        "words": ["wuld", "nah", "kest"],
        "levels": {
            "1": {
                "name": "Wuld (Whirlwind)",
                "range": "Self",
                "effect": "You move 15 feet in a straight line without provoking opportunity attacks.",
                "dc": None,
                "image": "https://gifrun.blob.core.windows.net/temp/45aa95edc9154c99a3b7a3da6a6b1425.gif"
            },
            "2": {
                "name": "Wuld Nah (Whirlwind Fury)",
                "range": "Self",
                "effect": "You move 30 feet in a straight line without provoking opportunity attacks. Creatures in your path must make a Strength saving throw or be knocked prone.",
                "dc": 10 + proficiency_bonus + charisma_mod,
                "image": "https://gifrun.blob.core.windows.net/temp/45aa95edc9154c99a3b7a3da6a6b1425.gif"
            },
            "3": {
                "name": "Wuld Nah Kest (Whirlwind Tempest)",
                "range": "Self",
                "effect": "You move 60 feet in a straight line without provoking opportunity attacks. Creatures in your path must make a Strength saving throw or take 2d6 thunder damage and be knocked prone.",
                "dc": 12 + proficiency_bonus + charisma_mod,
                "damage_dice": "2d6",
                "damage_type": "thunder",
                "image": "https://gifrun.blob.core.windows.net/temp/45aa95edc9154c99a3b7a3da6a6b1425.gif"
            }
        }
    },
    "fo": {
        "name": "Frost Breath",
        "words": ["fo", "krah", "diin"],
        "levels": {
            "1": {
                "name": "Fo (Frost)",
                "range": "30-foot cone",
                "damage_dice": "3d6",
                "damage_type": "cold",
                "dc": 8 + proficiency_bonus + charisma_mod,
                "effect": "Each creature in the area must make a Constitution saving throw or be **restrained**",
                "image": "https://media1.tenor.com/m/mCF-wFOSlfsAAAAC/game-of-thrones-white-walker.gif"
            },
            "2": {
                "name": "Fo Krah (Frost Cold)",
                "range": "30-foot cone",
                "damage_dice": "5d6",
                "damage_type": "cold",
                "dc": 10 + proficiency_bonus + charisma_mod,
                "effect": "On a failed save, creatures are **paralyzed** until the end of their next turn.",
                "image": "https://media1.tenor.com/m/mCF-wFOSlfsAAAAC/game-of-thrones-white-walker.gif"
            },
            "3": {
                "name": "Fo Krah Diin (Frost Cold Freeze)",
                "range": "60-foot cone",
                "damage_dice": "7d6",
                "damage_type": "cold",
                "dc": 12 + proficiency_bonus + charisma_mod,
                "effect": "On a failed save, creatures are **slowed** (as per the Slow spell) until the end of their next turn.",
                "image": "https://media1.tenor.com/m/mCF-wFOSlfsAAAAC/game-of-thrones-white-walker.gif"
            }
        }
    }
}
# Match the input words to a shout
input_words = args
matched_shout = None
level = 0

for key, shout in shouts.items():
    shout_words = shout["words"]
    if shout_words[:len(input_words)] == input_words:
        matched_shout = shout
        level = len(input_words)
        break

if not matched_shout:
    return f"Shout not recognized. Available shouts are: {', '.join([s['name'] for s in shouts.values()])}."

# Get the shout level details
levels = matched_shout["levels"]
level_key = str(level) if str(level) in levels else max(levels.keys(), key=int)
shout_level = levels[level_key]
title = shout_level["name"]
range_area = shout_level.get("range", "Self")
damage_dice = shout_level.get("damage_dice")
damage_type = shout_level.get("damage_type", "damage")
push_distance = shout_level.get("push_distance")
prone = shout_level.get("prone", False)
dc = shout_level.get("dc")
effect = shout_level.get("effect")
image_url = shout_level.get("image")

# Recharge mechanic
recharge_roll = vroll('1d6')
if recharge_roll.total >= 5:
    recharge_text = "Your shout **recharges** and can be used again."
else:
    recharge_text = "Your shout does **not recharge** yet."

# Build the description
description = f"**{title}**\n\n"

if range_area != "Self":
    description += f"You unleash a powerful shout in a {range_area}.\n\n"
else:
    description += "You unleash a powerful shout.\n\n"

if dc:
    description += f"Each affected creature must make a **saving throw** (DC {dc}). "
    if damage_dice:
        damage_roll = vroll(damage_dice)
        description += f"On a failed save, a creature takes **{damage_roll}** {damage_type}."
    else:
        damage_roll = None
    if push_distance:
        description += f" They are pushed {push_distance} feet away from you."
    if prone:
        description += " They are also **knocked prone**."
    if effect:
        description += f" {effect}"
    description += " On a successful save, they take half damage and are not affected."
else:
    # For shouts without a saving throw
    if effect:
        description += effect

# Show the recharge result
description += f"\n\n**Recharge:** {recharge_text} (Recharge roll: {recharge_roll})"

# Return the embed
return f'embed -title "{matched_shout["name"]}" -desc "{description}" -image "{image_url}" -color #0000FF'
</drac2>

