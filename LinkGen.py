import json, os, platform, time, discord

client = discord.Bot()

# Check if correctly setup

if os.path.exists("accounts"): pass
else: os.mkdir("accounts")
if platform.system() == "Windows": os.system("cls")
else: os.system("clear")
try: json.loads(open("config.json", "r").read())
except Exception: print("[ERROR] Config File missing")
try:json.loads(open("config.json", "r").read())["token"]
except Exception: print("[ERROR] Discord Token not set")
try:json.loads(open("config.json", "r").read())["guild_id"]
except Exception: print("[ERROR] Guild ID not set")
try:json.loads(open("config.json", "r").read())["log_channel"]
except Exception: print("[ERROR] Log Channel not set")

# When bot is logged in

@client.event
async def on_ready():
    print(f"Logged in as: {client.user.name}")
    print(f"Using guild: {client.guilds[0].name}")
    print("CRGEN Ready", "\n")
    await client.change_presence(activity=discord.Game(name="CRGEN V2.0"))
    try: client.guilds[0].get_role(int(json.loads(open("config.json", "r").read())["gen_role"]))
    except Exception: print("[ERROR] Gen Role not set")
    try: client.guilds[0].get_channel(int(json.loads(open("config.json", "r").read())["gen_channel"]))
    except Exception: print("[ERROR] Gen Channel not set")
    services = [ "valorant", "hulu", "fortnite", "Steam", "spotify", "netflix", "disney", "minecraft" ]
    for service in services:
        if os.path.exists(f"accounts/{service}.txt"): pass
        else:
            open(f"accounts/{service}.txt", "a").write(f"Paste {service} accounts here")
            print(f"[WARNING] No Accounts found for {service} - Creating file...")

# Generate Command

@client.slash_command(name="pgenerate", guild_ids=[json.loads(open("config.json", "r").read())["guild_id"]])
async def generate(ctx, service_name):
    if str(ctx.channel.id) != json.loads(open("config.json", "r").read())["gen_channel"]:
        await ctx.respond(f"You can only gen in: <#{json.loads(open('config.json', 'r').read())['gen_channel']}>", ephemeral=True)
    else:
        services = [ "valorant", "hulu", "fortnite", "Steam", "spotify", "netflix", "disney", "minecraft" ]
        for service in services:
            if service_name.lower() == service.lower():
                if str(json.loads(open("config.json", "r").read())["gen_role"]) in str(ctx.author.roles):
                    if os.path.exists(f"accounts/{service.lower()}.txt"):
                        with open(f"accounts/{service.lower()}.txt", "r+") as accounts:
                            data = accounts.readlines()
                            accounts.seek(0)
                            accounts.truncate()
                            accounts.writelines(data[1:])
                            try:
                                embed = discord.Embed(title=f"{service} Account Generated", description="CRGEN Account Generator", color=0x46a9f0)
                                embed.add_field(name="Login Credentials", value=f"```{data[0]}```", inline=True)
                                embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/773133136929226763/797204521997828106/777514274829893683.gif")
                                user = await client.fetch_user(int(ctx.author.id))
                                await user.send(embed=embed)
                                log = client.guilds[0].get_channel(int(json.loads(open("config.json", "r").read())["log_channel"]))
                                embed = discord.Embed(title=f"{ctx.author.name} has genned 1 {service}", description=f"**Account**\n```{data[0]}```", color=0x46a9f0)
                                await log.send(embed=embed)
                                await ctx.respond("Account Generated, check your DM")
                            except Exception:
                                await ctx.respond(f"We are currently out of {service}!", ephemeral=True)
                    else:
                        await ctx.respond(f"We are currently out of {service}!", ephemeral=True)
                else:
                    await ctx.respond(f"You cannot gen {service}!", ephemeral=True)

# Help Command

@client.slash_command(name="phelp", guild_ids=[json.loads(open("config.json", "r").read())["guild_id"]])
async def help(ctx):
    embed = discord.Embed(title="CRGEN help command", description="Usage: /generate <service name>, /stock", color=0x46a9f0)
    embed.add_field(name="All Services", value="``steam``, ``spotify``, ``netflix``, ``disney``, ``valorant``, ``minecraft``, ``hulu``, ``fortnite`` ")
    embed.set_footer(text="Made by Cridi.mp4#9730")
    await ctx.respond(embed=embed)

# Stock Command

@client.slash_command(name="pstock", guild_ids=[json.loads(open("config.json", "r").read())["guild_id"]])
async def stock(ctx):
    services = [ "valorant", "hulu", "fortnite", "Steam", "spotify", "netflix", "disney", "minecraft" ]
    stocklist = []
    for service in services:
        if os.path.exists(f"accounts/{service.lower()}.txt"):
            stocklist.append(f"{service} stock: {len(open(f'accounts/{service}.txt', 'r').readlines())} accounts")
    embed = discord.Embed(title="CRGEN Stock", description="Display's stock of all services", color=0x46a9f0)
    embed.add_field(name="Stock", value="\n".join(stocklist))
    embed.set_footer(text="Made by Cridi.mp4#9730")
    await ctx.respond(embed=embed)

client.run(json.loads(open("config.json", "r").read())["token"])