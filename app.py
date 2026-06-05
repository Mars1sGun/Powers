import os
import re
import yaml
import subprocess
from pathlib import Path

import discord
from discord import app_commands
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN", "YOUR_TOKEN_HERE")
BASE = Path("C:\\Users\\pc\\Desktop\\Tech\\PowersRepo")

NAME_MAP = {
    "Almight": "almighty", "Timeweaver": "timestop", "BlowingGuy": "blowingguys",
    "GravitySucker": "sucker", "Flashbang": "flashbang", "SkeletonKing": "skeletonking",
    "Atrain": "atrain", "BigBetha": "bigbetha", "MtLady": "mtlady",
    "ExtraHeartMan": "extraheartman", "SpiderMan": "spiderman", "KingMidas": "kingmidas",
    "Dragon2": "dragon2", "IronGolem": "irongolem", "IronMan": "ironman",
    "LavaWalker": "lavawalker", "IronBlaster": "ironblaster", "GravityGuy": "gravityguy",
    "Aerosurfer": "aerosurfer", "Tinkerbell": "tinkerbell", "Speleologist": "speleologist",
    "Pickpocket": "pickpocket", "Terrorist": "Terrorist",
    "Benson": "benson",
}
MANUAL_DESC = {
    "Timeweaver": "Stop time and teleport through space.", "Tank": "Reinforce yourself and repair all your gear.",
    "Homelander": "Fly through the skies and blast foes with laser vision and fireballs!",
    "Goku": "You are an Adult Saiyan.", "Atrain": "Super speedster.",
    "Eraserhead": "Erase other people's powers by sneaking.", "Sorcerer": "Create magical spell books using redstone.",
    "Terrorist": "Explosive power.", "Heatwave": "Engulf your surroundings in scorching flames!",
    "Archer": "Shoot arrows and repel everyone!", "Almight": "Sneak to become stronger.",
    "IronBlaster": "Fly and unleash rapid ghast fireballs!", "Doomfist": "You are Doomfist.",
    "Starlight": "No power file found.", "IronMan": "Genius, billionaire, playboy, philanthropist.",
    "BigBetha": "You are GiantGertrude!", "MtLady": "You are a giant!", "Strongman": "Pickup and throw entities!",
    "Superhuman": "A more powerful human.", "ExtraHeartMan": "Extra hearts and give absorption.",
    "Speedster": "Permanent speed IV.", "Flashbang": "Blind nearby players.", "Lazer": "Fire a deadly laser beam.",
    "Gun": "You have a gun.", "Robot": "You're a robot.", "Phase": "Phase through the ground.",
    "Repulsion": "Repel entities when sneaking.", "BlackHole": "Attract entities when sneaking.",
    "GravitySucker": "Control gravity.", "Sucker": "You suck everything.", "Bubble": "You have a bubble.",
    "Stormborn": "No power file found.", "Frozone": "Walk on water, slow others.",
    "Nebular": "Controls the void world.", "Dracula": "Absorb life force.", "Zeus": "Strike lightning.",
    "Midoriya": "The Ninth Holder of One For All.", "Disguise": "Trick players with disguise.",
    "DrCloak": "Not attacked while disguised.", "GravityGuy": "Sneak to rise, let go to fall.",
    "Aerosurfer": "Create platforms.", "Floral": "Create and consume flowers.", "Aquaman": "Walk underwater.",
    "LavaWalker": "Walk on lava.", "Pyromaniac": "Create fire trails.", "Chicken": "You're a chicken.",
    "Pig": "You're a pig.", "Dolphin": "Swim at great speeds!", "Tinkerbell": "You are Tinkerbell!",
    "Spartan": "Unbreakable shield + arrows.", "SpiderMan": "Climb blocks!", "KingMidas": "Turn items to gold.",
    "Scavenger": "Extra crafting recipes.", "Mole": "Instant break certain blocks.",
    "Speleologist": "Double and smelt ores!", "Pickpocket": "Steal from players!", "BlowingGuy": "Rise and blow away.",
    "Revealer": "Reveal nearby enemies.", "Creeper": "You're a creeper.", "Enderman": "Teleport by punching.",
    "SkeletonKing": "Lead an army of skeletons!", "Zombie": "You are a zombie!", "Dragon": "Throw fireballs.",
    "Dragon2": "Suck and blow everyone!", "Slime": "Bounce along the floor.", "IronGolem": "You're an iron golem.",
    "Guardian": "No power file found.", "Snowman": "Create snow trails!", "Powerless": "You have no power.",
    "Benson": "Fly like Tinkerbell! Disabled for 5s on hit or when you hit someone.",
    "Swiper": "Shift-click a player to steal their power for 60s! S++ tier.",
    "Mirror": "Shift-click a player to copy their power for 60s! S tier.",
    "TheCrippler": "Sneak to disable all powers within 15 blocks for 60s! A tier.",
    "Gambler": "Sneak to get a random power for 60s! Secret power.",
    "Shuffler": "Sneak to get a random S/S++ tier power for 60s! Secret power.",
    "Reflector": "Sneak to reflect all damage for 30s! Secret power.",
    "Enhancer": "Sneak to boost potion effects +1 for everyone in 15 blocks for 60s! Secret power.",
    "TempU": "Temporary power potion. Gives a random hero for a duration, or boosts your current hero's potion effects + cooldown reduction if you already have one. Configurable duration and cooldown.",
    "CompoundU": "High-risk volatile potion. Gives a random hero from a specific tier with a chance of death. Higher tiers = higher death chance but better heroes.",
    "UltraExtras": "Plugin that adds: Tentacle ability (Butcher), TempU/CompoundU potions, Lazer Eyes (REDSTONE_BLOCK + TempU), Wandering Trader potion trades, chest loot injection, crying obsidian chest gen, and power abilities (Swiper, Mirror, TheCrippler, and secret powers). All configurable and reloadable via /heroextras reload.",
}
MANUAL_HOWTO = {
    "Tank": "Sneak (120s cd)", "Timeweaver": "Left-click (5s cd) / Sneak (60s cd)",
    "Homelander": "Jetpack (hold jump) + Right-click Redstone Block", "Goku": "Right-click Breeze Rod (10s cd)",
    "Atrain": "Eat Sugar / Sneak (30s cd)", "Eraserhead": "Sneak near target (30 range)",
    "Sorcerer": "Craft books with redstone", "Terrorist": "Right-click to detonate", "Heatwave": "Sneak (40s cd)",
    "Archer": "Right-click Feather (2s cd)", "Almight": "Sneak (65s cd)",
    "IronBlaster": "Jetpack + Right-click Blaze Powder", "Doomfist": "Punch air (10s cd)", "Starlight": "N/A",
    "IronMan": "Jetpack (hold jump)", "BigBetha": "Passive", "MtLady": "Passive", "Strongman": "Right-click entity",
    "Superhuman": "Passive", "ExtraHeartMan": "Right-click player", "Speedster": "Passive", "Flashbang": "Sneak (60s cd)",
    "Lazer": "Right-click Echo Shard", "Gun": "Right-click Stone Hoe", "Robot": "Passive", "Phase": "Sneak to phase",
    "Repulsion": "Sneak", "BlackHole": "Sneak", "GravitySucker": "Passive sneaking", "Sucker": "Sneak", "Bubble": "Sneak",
    "Stormborn": "N/A", "Frozone": "Passive", "Nebular": "Sneak (10s cd)", "Dracula": "Attack enemies",
    "Zeus": "Left-click (10s cd)", "Midoriya": "Sneak-jump to toggle", "Disguise": "Sneak for invisibility",
    "DrCloak": "Sneak (30s cd)", "GravityGuy": "Sneak to rise", "Aerosurfer": "Sneak to create platforms",
    "Floral": "Look at ground / Right-click", "Aquaman": "Passive", "LavaWalker": "Passive", "Pyromaniac": "Walk",
    "Chicken": "Passive", "Pig": "Passive", "Dolphin": "Passive / Eat Ink Sac", "Tinkerbell": "Passive",
    "Spartan": "Right-click Arrow", "SpiderMan": "Walk near walls", "KingMidas": "Passive / Right-click",
    "Scavenger": "Craft at table", "Mole": "Break dirt/stone", "Speleologist": "Mine ores",
    "Pickpocket": "Sneak + right-click", "BlowingGuy": "Sneak", "Revealer": "Sneak (60s cd)",
    "Creeper": "Right-click to explode", "Enderman": "Left-click (10s cd)", "SkeletonKing": "Passive", "Zombie": "Passive",
    "Dragon": "Right-click (30s cd)", "Dragon2": "Right-click (2s cd)", "Slime": "Passive", "IronGolem": "Passive",
    "Guardian": "N/A", "Snowman": "Walk / Throw snowballs", "Powerless": "N/A",
    "Benson": "Passive",
    "Swiper": "Sneak + right-click target player (180s cd, 120s with TempU)",
    "Mirror": "Sneak + right-click target player (180s cd, 120s with TempU)",
    "TheCrippler": "Sneak to trigger (180s cd, 120s with TempU)",
    "Gambler": "Sneak (100s cd, 70s with TempU)",
    "Shuffler": "Sneak (100s cd, 70s with TempU)",
    "Reflector": "Sneak (90s cd, 60s with TempU)",
    "Enhancer": "Sneak (100s cd, 70s with TempU)",
    "TempU": "Drink the potion. If you have a hero: boosts your potion effects and reduces cooldowns for 60s. If powerless: gives a random hero for 120s. Found in structure chests (25% chance) or bought from Wandering Trader.",
    "CompoundU": "Drink the potion. Random hero from a tier with death chance. Higher tier = better hero but more likely to die. Found in structure chests (25% chance).",
    "UltraExtras": "/heroextras grab|release|reload | /mars give|locate|gen|reload | Lazer Eyes: hold REDSTONE_BLOCK + have TempU active + left-click for continuous beam.",
}
MANUAL_EFFECTS = {
    "Tank": "Resistance III, Absorption III, full repair", "Timeweaver": "Teleport 30 blocks, Time Stop 15s",
    "Homelander": "Flight, Speed II, Strength II, Resistance II, Laser (6 dmg), Fireballs, X-ray",
    "Goku": "Ki Blast (5 dmg, 100 range), Speed VI, Jump Boost IV, Strength II, +20% HP",
    "Atrain": "Speed VI, burst Speed XI, AoE slowness", "Eraserhead": "Power erasure on target",
    "Sorcerer": "12+ spells: Fireball, Lightning, Explosion, etc.", "Terrorist": "Creeper explosion (power 10), Remote detonation",
    "Heatwave": "AoE fire (10 dmg), Ignite, Nausea", "Archer": "Levitation, Repulsion, Infinite arrows",
    "Almight": "Strength VI, Resistance VI, Regen VI, Absorption VI", "IronBlaster": "Flight, Speed VI, Fireball barrage",
    "Doomfist": "Slam (8 dmg, 5 radius)", "Starlight": "N/A", "IronMan": "Flight with gliding",
    "BigBetha": "1.5x scale, Flight, Damage modifier", "MtLady": "3x scale, 2x HP, Step height 3",
    "Strongman": "Throw (velocity 2.5)", "Superhuman": "Resistance II, Speed II, Jump Boost III",
    "ExtraHeartMan": "+4 HP, Absorption II (60s) to others", "Speedster": "Speed V", "Flashbang": "AoE Blindness (20 blocks)",
    "Lazer": "Laser (6 dmg, 30 range)", "Gun": "Gun (5 dmg, 64 range)", "Robot": "No hunger, Resistance, Night vision",
    "Phase": "Phase 5 blocks deep", "Repulsion": "Repulse (1.5x, 10 radius)", "BlackHole": "Attract (-0.35x, 10 radius)",
    "GravitySucker": "Levitation, Slow falling, Repulse", "Sucker": "Attract (-0.8x, 3.4 radius)", "Bubble": "Repulse (2x, 3.4 radius)",
    "Stormborn": "N/A", "Frozone": "Water walk, Slowness aura", "Nebular": "AoE 5 dmg + Blindness + Wither",
    "Dracula": "5% lifesteal, +2 max hearts per kill", "Zeus": "Lightning (30 range), Lightning immunity",
    "Midoriya": "Full Cowling, Detroit Smash (8 dmg)", "Disguise": "Invisibility, speed, decoy spawn",
    "DrCloak": "10s invisibility, mobs lose target", "GravityGuy": "Levitation II, Slow falling",
    "Aerosurfer": "Glass platforms, Speed II", "Floral": "11 flower types with buffs", "Aquaman": "Water breathing, water walking",
    "LavaWalker": "Lava walk, fire heals, fire immunity", "Pyromaniac": "Fire trail, fire/lava immunity",
    "Chicken": "Lay eggs, Speed III, Slow falling", "Pig": "Pig beast control (32 range)",
    "Dolphin": "Dolphins Grace V, Water breathing", "Tinkerbell": "Flight, Tiny (0.25x)",
    "Spartan": "Unbreakable shield, infinite arrows (3 dmg)", "SpiderMan": "Wall climb, 90% fall reduction, web traps",
    "KingMidas": "Golden Apple craft, blocks to gold", "Scavenger": "Cheap diamond tools/armor",
    "Mole": "Instant break, Night vision", "Speleologist": "Auto-smelt & double all ores",
    "Pickpocket": "Pickpocket (3 range)", "BlowingGuy": "Levitation, Repulse (0.8x)",
    "Revealer": "Glowing on all enemies (20 blocks)", "Creeper": "Explosion (power 1), Remote detonation",
    "Enderman": "Teleport 30 blocks, OHKO Endermen", "SkeletonKing": "Skeleton control, spawn skeletons",
    "Zombie": "Resistance II, knockback, burns in sun", "Dragon": "Dragon fireballs",
    "Dragon2": "Levitation X, Repulse, Wind Charges", "Slime": "Bouncy, No fall damage",
    "IronGolem": "Iron ingots, Resistance II, Slowness II", "Guardian": "N/A", "Snowman": "Snow trail, infinite snowballs",
    "Powerless": "Nothing. Normal player.",
    "Benson": "Flight, disabled by Slowness II + Weakness V + Blindness for 5s on PvP.",
    "Swiper": "Steal target's hero (60s), target becomes Powerless. Reverts after expiry.",
    "Mirror": "Copy target's hero (60s), target keeps theirs. Reverts after expiry.",
    "TheCrippler": "AoE 15 blocks: all players set to Powerless (60s). Reverts after expiry.",
    "Gambler": "Random hero for 60s. Reverts to Gambler after expiry.",
    "Shuffler": "Random S/S++ hero for 60s. Reverts to Shuffler after expiry.",
    "Reflector": "All damage ignored and reflected to attacker for 30s.",
    "Enhancer": "All players in 15 blocks: each active potion effect gets amplifier +1 for 60s. Reverts after expiry.",
    "TempU": "No hero: random hero for duration. Has hero: power boost — potion effect amplifier x2, cooldowns reduced 50% for 60s. Duration/boost configurable per hero via specificPowers.",
    "CompoundU": "9 tiers (S++ to F). Each has a death chance and hero pool. Random hero from tier on success, death on fail. Cooldown applies regardless.",
    "UltraExtras": "Tentacle: Butcher with BLACK_CONCRETE_POWDER (right-click hold grab, left-click damage/chuck, TempU boosts range/max hits, life steal 1:1 in damage mode). Lazer Eyes: REDSTONE_BLOCK + TempU + left-click for continuous orange beam (6 dmg, fire, block break after sustained hits). Potion abilities: Swiper (steal), Mirror (copy), TheCrippler (AOE disable), Gambler (random), Shuffler (S/S++), Reflector (reflect), Enhancer (boost effects). All 60s duration, cooldowns reduced with TempU. Reload: /heroextras reload or /shootstar reload.",
}
TIER_CFG = {
    "s_plus_plus": ("S++", 0xffd700), "legendary": ("S", 0xff6b6b), "heroes": ("A", 0xf093fb),
    "tech": ("B", 0x4facfe), "magic": ("C", 0x43e97b), "nature": ("D", 0xfa709a),
    "utility": ("E", 0xa8edea), "monsters": ("F", 0xd8d8d8), "f_tier": ("F-", 0x555555),
}
ORDER = ["s_plus_plus", "legendary", "heroes", "tech", "magic", "nature", "utility", "monsters", "f_tier"]

def build_tiers():
    with open(BASE / "reroll.yml", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    groups = data.get("reroll_groups", {})
    tiers = []
    for key in ORDER:
        group = groups.get(key)
        if not group:
            continue
        label, color = TIER_CFG[key]
        item = (group.get("item", {}).get("types") or ["Unknown"])[0]
        heroes_raw = group.get("heroes", [])
        total = sum(h.get("weight", 1) for h in heroes_raw)
        heroes = []
        for h in heroes_raw:
            name = h["hero"]
            w = h.get("weight", 1)
            chance = f"{(w / total) * 100:.1f}%"
            desc = MANUAL_DESC.get(name)
            if not desc:
                desc = load_yaml_desc(name) or "No power file found."
            tiers.append({
                "label": label, "color": color, "item": item,
                "name": name, "desc": desc,
                "howto": MANUAL_HOWTO.get(name, "N/A"),
                "effects": MANUAL_EFFECTS.get(name, "N/A"),
                "chance": chance,
            })
        tiers.append({"__tier_end": label, "color": color, "item": item})
    result, cur = [], {}
    for t in tiers:
        if "__tier_end" in t:
            cur["heroes"] = cur.get("heroes", [])
            result.append(cur)
            cur = {}
        else:
            cur.setdefault("label", t["label"])
            cur["color"] = t["color"]
            cur["item"] = t["item"]
            cur.setdefault("heroes", []).append(t)
    return result

def load_yaml_desc(name):
    mapped = NAME_MAP.get(name, name)
    for f in (BASE / "powers").iterdir():
        if f.suffix.lower() not in (".yml", ".yaml"):
            continue
        if f.stem == mapped or f.stem.lower() == name.lower():
            with open(f, encoding="utf-8") as fh:
                d = yaml.safe_load(fh)
            if d and isinstance(d, dict) and d.get("description"):
                return d["description"]
    return None

TIERS = build_tiers()

def gen_index_html():
    lines = []
    lines.append("""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Superheroes Tierlist</title>
<meta property="og:title" content="Superheroes Tierlist">
<meta property="og:description" content="All powers ranked across 9 tiers with drop chances, controls, and effects.">
<meta property="og:image" content="https://mars1sgun.github.io/Powers/og-image.png">
<meta property="og:url" content="https://mars1sgun.github.io/Powers/">
<meta property="og:type" content="website">
<meta name="theme-color" content="#e94560">
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap');
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Inter',sans-serif;background:#0a0a0f;color:#e0e0e0;min-height:100vh}
header{background:linear-gradient(135deg,#1a1a2e,#16213e,#0f3460);padding:2rem;text-align:center;border-bottom:3px solid #e94560}
header h1{font-size:2.5rem;font-weight:900;background:linear-gradient(90deg,#e94560,#0f3460,#e94560);background-size:200%;-webkit-background-clip:text;-webkit-text-fill-color:transparent;animation:shimmer 4s ease-in-out infinite}
header p{color:#a0a0b0;margin-top:.5rem;font-size:1.1rem}
@keyframes shimmer{0%,100%{background-position:0 50%}50%{background-position:100% 50%}}
.container{max-width:1400px;margin:0 auto;padding:1rem}
.tier{background:rgba(255,255,255,.03);border-radius:12px;margin:1rem 0;overflow:hidden;border:1px solid rgba(255,255,255,.06);transition:box-shadow .3s}
.tier:hover{box-shadow:0 0 30px rgba(233,69,96,.1)}
.tier-header{display:flex;align-items:center;padding:.75rem 1.25rem;gap:.75rem;cursor:pointer;user-select:none}
.tier-rank{font-weight:900;font-size:1.3rem;min-width:50px;text-align:center;padding:.25rem .75rem;border-radius:8px}
.tier-name{font-weight:700;font-size:1.1rem;flex:1}
.tier-item{font-size:.8rem;color:#888;background:rgba(255,255,255,.05);padding:.2rem .6rem;border-radius:4px}
.tier-rarity{font-size:.8rem;color:#888}
.tier-toggle{font-size:1.2rem;color:#666;transition:transform .3s}
.tier.collapsed .tier-toggle{transform:rotate(-90deg)}
.tier-content{display:flex;flex-wrap:wrap;gap:.75rem;padding:0 1.25rem 1.25rem}
.tier.collapsed .tier-content{display:none}
.hero-card{background:rgba(255,255,255,.04);border-radius:10px;padding:.75rem;width:calc(33.333% - .5rem);border:1px solid rgba(255,255,255,.06);transition:all .3s;position:relative;overflow:hidden}
.hero-card:hover{transform:translateY(-3px);box-shadow:0 8px 25px rgba(0,0,0,.3);border-color:rgba(255,255,255,.15)}
.hero-card h3{font-size:1rem;font-weight:700;margin-bottom:.25rem}
.hero-desc{font-size:.8rem;color:#999;line-height:1.4;margin-bottom:.5rem}
.hero-meta{display:flex;gap:.5rem;flex-wrap:wrap;font-size:.7rem;align-items:center}
.meta-tag{background:rgba(255,255,255,.06);padding:.15rem .5rem;border-radius:4px;color:#aaa}
.meta-tag.howto{background:rgba(233,69,96,.15);color:#e94560}
.meta-tag.chance{background:rgba(255,215,0,.12);color:#ffd700;font-weight:700}
.spp-tier .tier-rank{background:linear-gradient(135deg,#ffd700,#ff8c00,#ffd700);color:#111}
.spp-tier{border-color:#ffd700!important}.spp-tier .tier-header{background:linear-gradient(90deg,rgba(255,215,0,.08),transparent)}
.s-tier .tier-rank{background:linear-gradient(135deg,#ff6b6b,#ee5a24);color:#fff}
.a-tier .tier-rank{background:linear-gradient(135deg,#f093fb,#f5576c);color:#fff}
.b-tier .tier-rank{background:linear-gradient(135deg,#4facfe,#00f2fe);color:#fff}
.c-tier .tier-rank{background:linear-gradient(135deg,#43e97b,#38f9d7);color:#111}
.d-tier .tier-rank{background:linear-gradient(135deg,#fa709a,#fee140);color:#111}
.e-tier .tier-rank{background:linear-gradient(135deg,#a8edea,#fed6e3);color:#111}
.f-tier .tier-rank{background:linear-gradient(135deg,#d8d8d8,#999);color:#111}
.f_minus-tier .tier-rank{background:linear-gradient(135deg,#555,#333);color:#888}
.hero-card.powerless{opacity:.4;filter:grayscale(1)}
.hero-card.powerless:hover{opacity:.8;filter:grayscale(.5)}
@media(max-width:900px){.hero-card{width:calc(50% - .5rem)}}
@media(max-width:600px){.hero-card{width:100%}header h1{font-size:1.8rem}}
footer{text-align:center;padding:2rem;color:#b388ff;font-size:.8rem}
footer a{color:#b388ff;text-decoration:underline}
</style>
</head>
<body>
<header>
<h1>SUPERHEROES TIERLIST</h1>
<p>All powers ranked — click a tier to expand/collapse</p>
<p style="margin-top:.5rem;font-size:.9rem;color:#4fc3f7">Bedrock: <b>138.201.255.236</b> port <b>5183</b> &nbsp;|&nbsp; Java: <b>138.201.255.236:5106</b></p>
</header>
<div class="container" id="app"></div>
<footer>Built by 1sGun &middot; join the discord <a href="https://discord.gg/srqWWpAAYW" target="_blank">https://discord.gg/srqWWpAAYW</a></footer>
<script>
""")
    lines.append("const TIERS = [")
    for t in TIERS:
        rank = {"S++": "spp", "S": "s", "A": "a", "B": "b", "C": "c", "D": "d", "E": "e", "F": "f", "F-": "f_minus"}[t["label"]]
        lines.append(f'  {{ id: "{rank}", label: "{t["label"]}", item: "{t["item"]}", heroes: [')
        for h in t["heroes"]:
            d = h["desc"].replace("'", "\\'")
            lines.append(f'    {{ name: "{h["name"]}", desc: "{d}", howto: "{h["howto"]}", effects: "{h["effects"]}", chance: "{h["chance"]}" }},')
        lines.append('  ]},')
    lines.append("""];
const C = {"spp":"spp-tier","s":"s-tier","a":"a-tier","b":"b-tier","c":"c-tier","d":"d-tier","e":"e-tier","f":"f-tier","f_minus":"f_minus-tier"};
function render(){const e=document.getElementById("app");e.innerHTML=TIERS.map((t,i)=>{const r=t.id!="spp"?"collapsed":"";return`<div class="tier ${C[t.id]} ${r}" onclick="this.classList.toggle('collapsed')"><div class="tier-header"><span class="tier-rank">${t.label}</span><span class="tier-item">${t.item}</span><span class="tier-rarity">${t.heroes.length} powers</span><span class="tier-toggle">▼</span></div><div class="tier-content">${t.heroes.map(h=>`<div class="hero-card${h.name==='Powerless'?' powerless':''}"><h3>${h.name}</h3><div class="hero-desc">${h.desc}</div><div class="hero-meta"><span class="meta-tag howto">${h.howto}</span><span class="meta-tag">${h.effects}</span><span class="meta-tag chance">${h.chance}</span></div></div>`).join("")}</div></div>`}).join("")}render();
</script>
</body>
</html>""")
    return "\n".join(lines)

class HeroBot(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()

client = HeroBot()

@client.tree.command(name="powers", description="List all power tiers or get info on a specific hero")
@app_commands.describe(hero="Optional: hero name for details")
async def powers(interaction: discord.Interaction, hero: str = None):
    if hero:
        hl = hero.lower()
        for tier in TIERS:
            for h in tier["heroes"]:
                if h["name"].lower() == hl:
                    em = discord.Embed(title=f"{h['name']}  [{tier['label']} Tier]", description=h["desc"], color=tier["color"])
                    em.add_field(name="How to use", value=h["howto"], inline=False)
                    em.add_field(name="Effects", value=h["effects"], inline=False)
                    em.add_field(name="Drop Chance", value=h["chance"], inline=True)
                    em.add_field(name="Reroll Item", value=tier["item"], inline=True)
                    em.set_footer(text="mars1sgun.github.io/Powers")
                    await interaction.response.send_message(embed=em)
                    return
        await interaction.response.send_message(f"Hero '{hero}' not found.", ephemeral=True)
        return
    em = discord.Embed(title="Superheroes Tierlist", description="All powers ranked across 9 tiers.", color=0xe94560)
    for tier in TIERS:
        names = ", ".join(h["name"] for h in tier["heroes"])
        em.add_field(name=f"**{tier['label']}** ({tier['item']})", value=names, inline=False)
    em.add_field(name="\u200b", value="**Bedrock:** 138.201.255.236 **port** 5183\n**Java:** 138.201.255.236:5106\n[Open full tierlist](https://mars1sgun.github.io/Powers/)", inline=False)
    em.set_footer(text="Use /powers <hero name> for details")
    await interaction.response.send_message(embed=em)

@client.tree.command(name="refresh", description="Reload tiers from reroll.yml and push updated site")
async def refresh(interaction: discord.Interaction):
    global TIERS
    try:
        TIERS = build_tiers()
        html = gen_index_html()
        (BASE / "index.html").write_text(html, encoding="utf-8")
        subprocess.run(["git", "add", "-A"], cwd=BASE)
        subprocess.run(["git", "commit", "-m", "Auto-update from bot"], cwd=BASE)
        subprocess.run(["git", "push"], cwd=BASE)
        await interaction.response.send_message("Tiers reloaded, index.html regenerated, pushed to GitHub.", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"Error: {e}", ephemeral=True)

client.run(TOKEN)
