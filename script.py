import psutil, sys, wx, urllib.request,time, json, appscript
import io
from riotwatcher import RiotWatcher, NORTH_AMERICA

with open('config.json') as config_file:
    config = json.load(config_file)

with open('constants.json') as constants_file:
    constants = json.load(constants_file)

#Summoner name constant
name = config['summoner_name']

#Windows or Mac
osValue = 0

if len(sys.argv) < 2 or sys.argv[1] not in ['0', '1']:
    raise ValueError('Need more arguments in command line')
else:
    osValue = int(sys.argv[1])

#Summoner name from command line, overrides name above
if len(sys.argv) > 2:
    name = sys.argv[2]

#Dev only
timeTaken = 0
processId = ""

#Display constants
leftPadding = constants['left_padding']
wrapWidth = constants['wrap_width']
gap = constants['gap']
championImageSize = constants['champion_image_size']
sumImageSize = championImageSize / 2
keystoneImageSize = sumImageSize

x = wx.GetDisplaySize()[0]
y = wx.GetDisplaySize()[1]
scaleFactor = config['scale_factor']
width = 192 * scaleFactor
height = 108 * scaleFactor
borderSize = 2;
font = wx.Font(15, wx.SWISS, wx.NORMAL, wx.NORMAL)
titleFont = wx.Font(55, wx.ROMAN, wx.ITALIC, wx.BOLD)
miniFont = wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL)
miniBoldFont = wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD)

textColor = constants['colors']['text_color']
titleColor = constants['colors']['title_color']
lighterTextColor = constants['colors']['lighter_text_color']
lighterBlue = constants['colors']['lighter_blue']
lightBlue = constants['colors']['light_blue']
lighterRed = constants['colors']['lighter_red']
lightRed = constants['colors']['light_red']

#Three API keys = thrice the calls before rate limit
order = []
if len(config['api_key_1']) > 0:
    watcher1 = RiotWatcher(config['api_key_1'], default_region=NORTH_AMERICA)
    order.append(watcher1)
if len(config['api_key_2']) > 0:
    watcher2 = RiotWatcher(config['api_key_2'], default_region=NORTH_AMERICA)
    order.append(watcher2)
if len(config['api_key_3']) > 0:
    watcher3 = RiotWatcher(config['api_key_3'], default_region=NORTH_AMERICA)
    order.append(watcher3)

#Finds out which API key is usable
def getWatcher():
    temp = order.pop(0)
    order.append(temp)
    try:
        temp.get_summoner(name)
        return temp
    except:
        time.sleep(1)
        return getWatcher()
#sets to correct version of league
cdnVersion = watcher1.static_get_versions()[0]

#keystones defined
keystones = [
  "Warlord's Bloodlust",
  "Fervor of Battle",
  "Deathfire Touch",
  "Stormraider's Surge",
  "Thunderlord's Decree",
  "Windspeaker's Blessing",
  "Grasp of the Undying",
  "Strength of the Ages",
  "Bond of Stone"
]

#runes defined
runes = {
    "FlatArmorMod": ["+", "armor", 1],
    "FlatAttackSpeedMod": ["+", "attack speed", 1],
    "FlatBlockMod": ["+", "block", 1],
    "FlatCritChanceMod": ["+", "critical strike chance", 1],
    "FlatCritDamageMod": ["+", "criticl strike damage", 1],
    "FlatEXPBonus": ["+", "experience", 1],
    "FlatEnergyPoolMod": ["+", "energy", 1],
    "FlatEnergyRegenMod": ["+", "energy / 5", 1],
    "FlatHPPoolMod": ["+", "health", 1],
    "FlatHPRegenMod": ["+", "health / 5", 1],
    "FlatMPPoolMod": ["+", "mana", 1],
    "FlatMPRegenMod": ["+", "mana / 5", 1],
    "FlatMagicDamageMod": ["+", "ability power", 1],
    "FlatMovementSpeedMod": ["+", "movement speed", 1],
    "FlatPhysicalDamageMod": ["+", "attack damage", 1],
    "FlatSpellBlockMod": ["+", "magic resist", 1],
    "PercentArmorMod": ["+", "%" + " armor", 100],
    "PercentAttackSpeedMod": ["+", "%" + " attack speed", 100],
    "PercentBlockMod": ["+", "%" + " block", 100],
    "PercentCritChanceMod": ["+", "%" + " critical strike chance", 100],
    "PercentCritDamageMod": ["+", "%" + " critical strike damage", 100],
    "PercentDodgeMod": ["+", "%" + " dodge change", 100],
    "PercentEXPBonus": ["+", "%" + " experience", 100],
    "PercentHPPoolMod": ["+", "%" + " health", 100],
    "PercentHPRegenMod": ["+", "%" + " heath / 5", 100],
    "PercentLifeStealMod": ["+", "%" + " lifesteal", 100],
    "PercentMPPoolMod": ["+", "%" + " mana", 100],
    "PercentMPRegenMod": ["+", "%" + " mana / 5", 100],
    "PercentMagicDamageMod": ["+", "%" + " ability power", 100],
    "PercentMovementSpeedMod": ["+", "%" + " movement speed", 100],
    "PercentPhysicalDamageMod": ["+", "%" + " attack damage", 100],
    "PercentSpellBlockMod": ["+", "%" + " magic resist", 100],
    "PercentSpellVampMod": ["+", "%" + " spellvamp", 100],
    "rFlatArmorModPerLevel": ["+", "armor at level 18", 18],
    "rFlatArmorPenetrationMod": ["+", "armor penetration", 1],
    "rFlatArmorPenetrationModPerLevel": ["+", "armor penetration at level 18", 18],
    "rFlatCritChanceModPerLevel": ["+", "critical strike chance at level 18", 18],
    "rFlatCritDamageModPerLevel": ["+", "critical damage at level 18", 18],
    "rFlatDodgeMod": ["+", "dodge", 1],
    "rFlatDodgeModPerLevel": ["+", "dodge at level 18", 18],
    "rFlatEnergyModPerLevel": ["+", "energy at level 18", 18],
    "rFlatEnergyRegenModPerLevel": ["+", "energy / 5 at level 18", 18],
    "rFlatGoldPer10Mod": ["+", "gold / 10", 1],
    "rFlatHPModPerLevel": ["+", "health at level 18", 18],
    "rFlatHPRegenModPerLevel": ["+", "health / 5 at level 18", 18],
    "rFlatMPModPerLevel": ["+", "mana at level 18", 18],
    "rFlatMPRegenModPerLevel": ["+", "mana / 5 at level 18", 18],
    "rFlatMagicDamageModPerLevel": ["+", "ability power at level 18", 18],
    "rFlatMagicPenetrationMod": ["+", "magic penetration", 1],
    "rFlatMagicPenetrationModPerLevel": ["+", "magic penetration at level 18", 18],
    "rFlatMovementSpeedModPerLevel": ["+", "movement speed at level 18", 18],
    "rFlatPhysicalDamageModPerLevel": ["+", "attack damage at level 18", 18],
    "rFlatSpellBlockModPerLevel": ["+", "magic resist at level 18", 18],
    "rFlatTimeDeadMod": ["-", "time spent dead", 1],
    "rFlatTimeDeadModPerLevel": ["-", "time spent dead at level 18", 18],
    "rPercentArmorPenetrationMod": ["+", "%" + " armor penetration", 100],
    "rPercentArmorPenetrationModPerLevel": ["+", "%" + " armor penetration at level 18", 1800],
    "rPercentAttackSpeedModPerLevel": ["+", "%" + " attack speed at level 18", 1800],
    "rPercentCooldownMod": ["+", "%" + " cooldown reduction", 100],
    "rPercentCooldownModPerLevel": ["+", "%" + " cooldown reduction at level 18", 1800],
    "rPercentMagicPenetrationMod": ["+", "%" + " magic penetration", 100],
    "rPercentMagicPenetrationModPerLevel": ["+", "%" + " magic penetration at level 18", 1800],
    "rPercentMovementSpeedModPerLevel": ["+", "%" + " movement speed at level 18", 1800],
    "rPercentTimeDeadMod": ["-", "%" + " time spent dead", 100],
    "rPercentTimeDeadModPerLevel": ["-", "%" + " time spent dead at level 18", 1800]
}


me = watcher1.get_summoner(name=name)
my_id = me['id']

#Returns an array [val, k, d, a, gamesPlayed, winRate] where val is -1 (scrub), 0 (normal), or 1 (one trick)
def isOneTrick(player):
    watcher = getWatcher()
    try:
        stats = watcher.get_ranked_stats(player['summonerId'])['champions']
    except:
        return (-1, 0.0, 0.0, 0.0, 0, 0.0)
    allIndex = -1
    try:
        allIndex = next(index for (index, d) in enumerate(stats) if d['id'] ==  0)
    except:
        pass
    totalRankedGames = 0
    totalChampGames = 0
    championStatistics = []
    if allIndex >= 0:
        totalRankedGames = stats[allIndex]['stats']['totalSessionsPlayed']
    else:
        return (-1, 0.0, 0.0, 0.0, 0, 0.0) #Literally no ranked games played
    champIndex = -1
    try:
        champIndex = next(index for (index, d) in enumerate(stats) if d['id'] ==  player['championId'])
    except:
        pass
    if champIndex >= 0:
        totalChampGames = stats[champIndex]['stats']['totalSessionsPlayed']
        champWinrate = int((stats[champIndex]['stats']['totalSessionsWon'] / (totalChampGames + 0.0) * 100 * 10) + 0.5) / 10.0
        championStatistics = [int(((stats[champIndex]['stats']['totalChampionKills'] + 0.0) / totalChampGames * 10) + 0.5) / 10.0,
         int(((stats[champIndex]['stats']['totalDeathsPerSession'] + 0.0)/ totalChampGames * 10) + 0.5) / 10.0,
         int(((stats[champIndex]['stats']['totalAssists'] + 0.0) / totalChampGames * 10) + 0.5) / 10.0, totalChampGames, champWinrate]
    else:
        return (-1, 0.0, 0.0, 0.0, 0, 0.0) #No ranked games played on this champion
    val = 0
    if totalRankedGames == 0:
        val = -1
    elif totalChampGames / (totalRankedGames + 0.0) >= 0.5:
        val = 1
    elif totalChampGames < totalRankedGames / 40.0:
        val = -1
    championStatistics.insert(0, val)
    return championStatistics

#Returns an array of strings that are the player's ranks
def getRanks(players):
    watcher = getWatcher()
    ids = []
    for i in range(0, len(players)):
        ids.append(players[i]['summonerId'])
    rankList = watcher.get_league(ids)
    values = []
    for i in range(0, len(players)):
        if not str(players[i]['summonerId']) in rankList:
            values.append("UNRANKED")
        else:
            league = rankList[str(players[i]['summonerId'])][0]
            foundIndex = 0
            try:
                foundIndex = next(index for (index, d) in enumerate(league['entries']) if d["playerOrTeamId"] ==  league['participantId'])
            except:
                pass
            division = league['entries'][foundIndex]['division']
            values.append(league['tier'] + " " + division)
    return values

#Returns stats of the rune page of the player
def getRunes(player):
    watcher = getWatcher()
    currentStats = {}
    for i in range(0, len(player['runes'])):
        rune = watcher.static_get_rune(player['runes'][i]['runeId'], rune_data='stats')
        count = player['runes'][i]['count']
        stats = rune['stats']
        for key in stats:
            if stats[key] != 0:
                rune = runes[key]
                number = stats[key] * count * rune[2]
                number = int(abs(number) * 10 + 0.5) / 10.0
                if key in currentStats:
                    currentStats[key] = currentStats[key] + number
                else:
                    currentStats[key] = number
                break
    returnArray = []
    for key in currentStats:
        string = runes[key][0] + str(currentStats[key]) + " " + runes[key][1]
        returnArray.append(string)
    return returnArray

#Returns a tuple of (summonerName, tiltFactor, championImage, summonerSpell1Image, summonerSpell2Image, keystoneImage)
def getPlayer(player):
    watcher = getWatcher()
    games = watcher.get_recent_games(player['summonerId'])['games']
    tiltFactor = 0.0
    wasGame = False
    for i in range(0, len(games)):
        if games[i]['gameType'] == 'MATCHED_GAME':
            wasGame = True
            if not games[i]['stats']['win'] :
                tiltFactor += 10 - i
    tiltFactor *= 10.0 / 55
    tiltFactor = int((tiltFactor * 10) + 0.5) / 10.0
    if not wasGame:
        tiltFactor = "Unknown"
    else:
        tiltFactor = str(tiltFactor)
    champion = watcher.static_get_champion(player['championId'], champ_data='image')
    sum1 = watcher.static_get_summoner_spell(player['spell1Id'], spell_data='image')
    sum2 = watcher.static_get_summoner_spell(player['spell2Id'], spell_data='image')
    keystone = ""
    for i in range(0, len(player['masteries'])):
        temp = watcher.static_get_mastery(player['masteries'][i]['masteryId'], mastery_data='image')
        if temp['name'] in keystones:
            keystone = temp['image']['full']
            break
    return (player['summonerName'], tiltFactor,
    champion['image']['full'], sum1['image']['full'], sum2['image']['full'], keystone)

#Parses url and returns image
def getImage(url):
    buf = urllib.request.urlopen(url).read()
    sbuf = io.BytesIO(buf)
    return wx.Image(sbuf)

#Helper function to get runes and open new frame
def runesHelper(player, x, y):
    def helper(self):
        RuneFrame(getRunes(player), x, y)
    return helper

#Preload images for use
closeButtonImage = getImage("http://oi65.tinypic.com/24qlraf.jpg").ConvertToBitmap()
# closeButtonImageDark = getImage("http://oi64.tinypic.com/xznh4.jpg").ConvertToBitmap()
backgroundImage = getImage("http://oi64.tinypic.com/2v1qkab.jpg").Rescale(width, height).ConvertToBitmap()

#Rune display
class RuneFrame(wx.Frame):
    def __init__(self, runes, x, y):
        style = ( wx.CLIP_CHILDREN | wx.FRAME_NO_TASKBAR |
                  wx.RAISED_BORDER | wx.FRAME_SHAPED  )
        wx.Frame.__init__(self, None, title = 'Runes', style = style)
        self.SetSize( (45 * scaleFactor, 40 + 4 * scaleFactor * len(runes)) )
        self.SetPosition( (x, y) )
        self.SetBackgroundColour(constants['colors']['runepage_color'])
        self.Show(True)
        for i in range(0, len(runes)):
            text = wx.StaticText(self, label=runes[i],
                pos= (5, 40 + i * 4 * scaleFactor))
            text.SetFont(font)
            text.SetForegroundColour('#FFFFFF')
        closeButton = wx.StaticBitmap(self, -1, closeButtonImage, (0, 0), (40, 40))
        closeButton.Bind(wx.EVT_LEFT_DOWN, self.close)
    def close(self, event):
        self.Close()

#The display itself
class MainFrame(wx.Frame):
    def __init__(self):
        game = watcher1.get_current_game(my_id)
        style = ( wx.CLIP_CHILDREN | wx.FRAME_NO_TASKBAR |
                  wx.RAISED_BORDER | wx.FRAME_SHAPED  )
        panelStyle = (wx.SUNKEN_BORDER)
        tempPanelStyle = (wx.NO_BORDER)
        wx.Frame.__init__(self, None, title = 'Fancy', style = style)
        panel = wx.Panel(self, -1, style = panelStyle)
        self.SetSize( (width, height) )
        self.SetPosition( ((x - width) / 2, (y - height) / 2) )
        self.SetBackgroundColour(wx.WHITE)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
        self.Show(True)

        #Get game mode
        gameMode = game['gameMode']
        try:
            if game['gameQueueConfigId'] in [4, 6, 9, 41, 42, 410]:
                gameMode = "RANKED"
        except:
            pass
        title = wx.StaticText(panel, label=gameMode, pos=(width / 2 - 110, height / 14))
        title.SetFont(titleFont)
        title.SetForegroundColour(titleColor)

        #Participants in current game as list
        rankList = getRanks(game['participants'])
        for i in range(0, len(game['participants'])):
            #separate panel for each person
            tempPanel = wx.Panel(panel, -1, size = (width / 2 - wrapWidth, height / 7 + 1),
             pos = ((i // 5) * width / 2 + (1 - i // 5) * wrapWidth, height * (i % 5 + 1.7) / 7 - borderSize), style = tempPanelStyle)
            player, winrate, championImage, sum1Image, sum2Image, keystoneImage = getPlayer(game['participants'][i])

            #Name of summoner and colored based on team
            nameText = wx.StaticText(tempPanel, label=player,
                pos= (leftPadding + championImageSize + sumImageSize + keystoneImageSize + gap * 3, (height / 7 - 20) / 2))
            nameText.SetFont(font)
            color = 'BLUE'
            if game['participants'][i]['teamId'] == 200:
                color = 'RED'
            nameText.SetForegroundColour(color) # set text color

            #Summoner's rank
            rankText = wx.StaticText(tempPanel, label=rankList[i],
                pos= (leftPadding + championImageSize + sumImageSize + keystoneImageSize + gap * 3, (height / 7 + 20) / 2))
            rankText.SetFont(miniFont)
            rankText.SetForegroundColour(textColor)

            #One trick, noob, or normal
            stats = isOneTrick(game['participants'][i])
            description = ""
            if stats[0] == 1:
                description = "ONE TRICK"
            elif stats[0] == -1:
                description = "NOOB"
            descriptionText = wx.StaticText(tempPanel, label=description,
             pos= (leftPadding + championImageSize + sumImageSize + keystoneImageSize + gap * 3, (height / 7 - 45) / 2))
            descriptionText.SetFont(miniBoldFont)

            #Average KDA
            statsText = wx.StaticText(tempPanel, label=str(stats[1]) + " / " + str(stats[2]) + " / " + str(stats[3]),
             pos=(width / 2 - 250, (height / 7 - 20) / 2))
            statsText.SetFont(font)
            statsText.SetForegroundColour(textColor)

            #Number of ranked games on this champion
            gamesPlayedText = wx.StaticText(tempPanel, label="(" + str(stats[5]) + "%" + " Winrate, "+ str(stats[4]) + " games)",
                pos= (width / 2 - 250, (height / 7 + 20) / 2))
            if stats[5] < 60:
                gamesPlayedText.SetFont(miniFont)
            else:
                gamesPlayedText.SetFont(miniBoldFont)
            gamesPlayedText.SetForegroundColour(lighterTextColor)

            #Tilt factor
            winrateText = wx.StaticText(tempPanel, label="Tilt: " + winrate,
                pos= (width / 2 - 90, (height / 7 - 20) / 2))
            winrateText.SetFont(font)
            winrateText.SetForegroundColour(lighterTextColor)

            #Rune button and onClick binding
            runesButton = wx.Button(tempPanel, label="Runes",
                pos= (width / 2 - 310, (height / 7 - 20) / 2), size= (50, 20))
            runesButton.SetFont(miniFont)
            runesButton.Bind(wx.EVT_BUTTON, runesHelper(game['participants'][i],
             (x - width) / 2 + (i // 5) * width / 2 + (1 - i // 5) * wrapWidth + width / 2 - 310,
             (y - height) / 2 + height * (i % 5 + 1.7) / 7 - borderSize + (height / 7 - 20) / 2))

            #Champion icon image
            img = getImage("http://ddragon.leagueoflegends.com/cdn/" + cdnVersion + "/img/champion/" + championImage)
            img.Rescale(championImageSize, championImageSize)
            wx.StaticBitmap(tempPanel, -1, img.ConvertToBitmap(), (leftPadding, (height / 7 - championImageSize) / 2), (championImageSize, championImageSize))

            #First summoner spell image
            sum1Img = getImage("http://ddragon.leagueoflegends.com/cdn/" + cdnVersion + "/img/spell/" + sum1Image)
            sum1Img.Rescale(sumImageSize, sumImageSize)
            wx.StaticBitmap(tempPanel, -1, sum1Img.ConvertToBitmap(), (leftPadding + championImageSize + gap, height / 14 - sumImageSize), (championImageSize, championImageSize))

            #Second summoner spell image
            sum2Img = getImage("http://ddragon.leagueoflegends.com/cdn/" + cdnVersion + "/img/spell/" + sum2Image)
            sum2Img.Rescale(sumImageSize, sumImageSize)
            wx.StaticBitmap(tempPanel, -1, sum2Img.ConvertToBitmap(), (leftPadding + championImageSize + gap, height / 14), (championImageSize, championImageSize))

            #Keystone mastery image
            if keystoneImage != "":
                keystoneImg = getImage("http://ddragon.leagueoflegends.com/cdn/" + cdnVersion + "/img/mastery/" + keystoneImage)
                keystoneImg.Rescale(keystoneImageSize, keystoneImageSize)
                wx.StaticBitmap(tempPanel, -1, keystoneImg.ConvertToBitmap(), (leftPadding + championImageSize + sumImageSize + gap * 2, (height / 7 - keystoneImageSize) / 2), (championImageSize, championImageSize))

            #Panel shading for aesthetics
            if i % 2 == 0:
                if i // 5 == 0:
                    tempPanel.SetBackgroundColour(lightBlue)
                else:
                    tempPanel.SetBackgroundColour(lightRed)
            else:
                if i // 5 == 0:
                    tempPanel.SetBackgroundColour(lighterBlue)
                else:
                    tempPanel.SetBackgroundColour(lighterRed)
        print("Loading took " + str((int(round(time.time() * 1000)) - timeTaken) / 1000.0) + " seconds")

        closeButton = wx.StaticBitmap(panel, -1, closeButtonImage, (0, 0), (40, 40))
        closeButton.Bind(wx.EVT_LEFT_DOWN, self.close)
        if osValue == 1:
            appscript.app(pid=processId).activate()
    def close(self, event):
        self.Close()
    #Draw background image
    def OnEraseBackground(self, evt):
        dc = evt.GetDC()

        if not dc:
            dc = wx.ClientDC(self)
            rect = self.GetUpdateRegion().GetBox()
            dc.SetClippingRect(rect)
        dc.Clear()
        bmp = backgroundImage
        dc.DrawBitmap(bmp, 0, 0)

#Name of process to open the display for
processName = constants['process_name']

exists = False
f = None
app = wx.App()

#Loop logic: scans every 2 seconds if League is running
while True:
    thisCycle = False
    for proc in psutil.process_iter():
        try:
            pinfo = proc.as_dict(attrs=['name'])['name']
            if pinfo == "Python":
                try:
                    processId = proc.as_dict(attrs=['id'])['id']
                except:
                    pass
            if processName == pinfo:
                thisCycle = True
                if not exists:
                    timeTaken = millis = int(round(time.time() * 1000))
                    f = MainFrame()
                    app.MainLoop()
                exists = True
        except psutil.NoSuchProcess:
            pass
    if not thisCycle and exists:
        exists = False

    time.sleep(2)
