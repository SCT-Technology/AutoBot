# coding: utf8
import json
import os
import shutil
import pathlib

# Only tested on Win10!
# Carpet Mod needed and function CommandPlayer must be on!
# Author: MercyNaima

# function: Kick bot with incorrect botPrefix default:[False]
AutoKickUnPrefixBot = False
# A whitelist for necessary bot
unPrefixNameWhiteList = ['Alex', 'Steve']
botPrefix = ['bot', 'farm', 'peace', 'p']
AutoBotFolder = './AutoBot'
AutoBotGroupFolder = AutoBotFolder + '\\group'
PluginPrefix = '§d[AutoBot]§r'


helpmsg = '''§d------MCDR [AutoBot]插件------§r
命令帮助如下:
§d!!bot§r -§e显示帮助消息
§d!!bot§r §aadd§r §8<BOT名字> <X坐标> <Y坐标> <Z坐标> <世界> <备注> -§e添加BOT到BOT列表§r
注：名字必须为{}{}, 开头, 坐标为整数，世界为overworld, nether, end, 三者之一
§d!!bot§r §adel§r §8<BOT名字>§r -§e从BOT列表删除BOT§r
§d!!bot§r §arename§r §8<BOT名字/BOT组名字> <目标名字>§r -§e重命名BOT/BOT组§r
§d!!bot§r §aaddgroup§r §8<BOT组名字>§r -§e添加BOT组§r
§d!!bot§r §adelgroup§r §8<BOT组名字>§r -§e移除BOT组§r
§d!!bot§r §agadd§r §8<BOT名字> <BOT组名字>§r -§e添加BOT至BOT组§r
§d!!bot§r §agdel§r §8<BOT名字> <BOT组名字>§r -§e从BOT组移除BOT§r
§d!!bot§r §alist§r §8<组名字> (可选变量)§r -§e查看可部署的BOT列表/查看组内BOT列表§r
§d!!bot§r §aglist§r -§e查看可部署的BOT组列表§r
§d!!bot§r §ainfo§r §8<BOT名字>/<BOT组名字> <BOT名字>§r -§e查看BOT/BOT组信息§r
§d!!bot§r §8<BOT名字/BOT组名字>§r -§e部署BOT/BOT组§r
§d!!bot§r §akill§r §8<BOT名字/BOT组名字>§r -§e下线BOT/BOT组§r
§d--------------------------------§r'''.format(botPrefix, '加下划线')


# get BotList with .json
def getBotListJson():
    botListJson = os.listdir(AutoBotFolder)
    # remove group folder
    botListJson.remove('group')
    return botListJson


# get BotList without .json
def getBotList():
    botList = []
    list = os.listdir(AutoBotFolder)
    # remove group folder
    list.remove('group')
    for var in list:
        botName = var.split('.', 1)[0]
        botList.append(botName)
    return botList


# get GroupList
def getGroupList():
    return os.listdir(AutoBotGroupFolder)


# get BotList in group without .json
def getBotListInGroup(groupName):
    botList = []
    list = os.listdir('{}\\{}'.format(AutoBotGroupFolder, groupName))
    for var in list:
        if var == 'info.json':
            pass
        else:
            botName = var.split('.', 1)[0]
            botList.append(botName)
    return botList


# get BotList in group with .json
def getBotListInGroupJson(groupName):
    botListJson = os.listdir('{}\\{}'.format(AutoBotGroupFolder, groupName))
    return botListJson


# print botList in game
def printBotList(server, info):
    server.reply(info, '{}BOT列表如下:'.format(PluginPrefix))
    server.reply(info, '{}§d-------------------------§r'.format(PluginPrefix))
    for var in getBotList():
        server.reply(info, '{}{}'.format(PluginPrefix, var))
    server.reply(info, '{}§d-------------------------§r'.format(PluginPrefix))


# print groupList in game
def printGroupList(server, info):
    server.reply(info, '{}BOT组列表如下:'.format(PluginPrefix))
    server.reply(info, '{}§d-------------------------§r'.format(PluginPrefix))
    for var in getGroupList():
        server.reply(info, '{}§a{}§r'.format(PluginPrefix, var))
    server.reply(info, '{}§d-------------------------§r'.format(PluginPrefix))


# print botList in game
def printBotListInGroup(groupName, server, info):
    server.reply(info, '{}BOT组:{}中BOT列表如下:'.format(PluginPrefix, groupName))
    server.reply(info, '{}§d-------------------------§r'.format(PluginPrefix))
    for var in getBotListInGroup(groupName):
        server.reply(info, '{}§a{}§r'.format(PluginPrefix, var))
    server.reply(info, '{}§d-------------------------§r'.format(PluginPrefix))


# print botInfo in game
def printBotInfo(botName, server, info):
    botInfo = getBotInfo(botName)
    server.reply(info, '{}BOT信息如下:'.format(PluginPrefix))
    server.reply(info, '{}§d-------------------------§r'.format(PluginPrefix))
    server.reply(info, '{}{}'.format(PluginPrefix, str(botInfo)))
    server.reply(info, '{}§d-------------------------§r'.format(PluginPrefix))


# print botInfo in game (bot is in group)
def printGroupBotInfo(groupName, botName, server, info):
    botInfo = getGroupBotInfo(groupName, botName)
    server.reply(info, '{}BOT信息如下:'.format(PluginPrefix))
    server.reply(info, '{}§d-------------------------§r'.format(PluginPrefix))
    server.reply(info, '{}{}'.format(PluginPrefix, str(botInfo)))
    server.reply(info, '{}§d-------------------------§r'.format(PluginPrefix))


# bot name check
def botNameCheck(botName, server, info):
    namePrefix = botName.split('_', 1)[0]
    if botName.find('_') == -1 or botName.find('.') != -1:
        server.reply(info, '{}BOT名字格式错误'.format(PluginPrefix))
        return False
    if namePrefix not in botPrefix:
        server.reply(info, '{}BOT名字格式错误'.format(PluginPrefix))
        return False
    return True


# bot pos check
def botPosCheck(posX, posY, posZ, server, info):
    if posX.find('+') != -1 or posY.find('+') != -1 or posZ.find('+') != -1:
        server.reply(info, '{}BOT坐标格式错误'.format(PluginPrefix))
        return False
    try:
        int(posX)
        int(posY)
        int(posZ)
    except ValueError:
        server.reply(info, '{}BOT坐标格式错误'.format(PluginPrefix))
        return False
    return True


# bot world check
def botWorldCheck(world, server, info):
    if world != 'overworld' and world != 'nether' and world != 'end':
        server.reply(info, '{}BOT世界格式错误'.format(PluginPrefix))
        return False
    return True


# bot format check
def addBotCheck(botName, posX, posY, posZ, world, server, info):
    # name check
    if botNameCheck(botName, server, info):
        # pos check
        if botPosCheck(posX, posY, posZ, server, info):
            # world check
            if botWorldCheck(world, server, info):
                return True
            else:
                return False
        else:
            return False
    else:
        return False


# add bot to AutoBotFolder and return a dict with botInfo
def addBot(botName, pos, world, detail, server, info):
    if botName in getBotList():
        server.reply(info, '{}已存在该BOT'.format(PluginPrefix))
        return
    # change world name to full world name
    if world == 'overworld':
        world = 'minecraft:' + world
    elif world == 'nether' or 'end':
        world = 'minecraft:the_' + world
    # create botName.json to store bots
    dict = {'name': botName, 'pos': pos, 'world': world, 'detail': detail}
    with pathlib.Path('{}\\{}.json'.format(AutoBotFolder, botName)).open('w') as f:
        f.write(json.dumps(dict))
    server.reply(info, '{}BOT:{}添加成功'.format(PluginPrefix, botName))
    return dict


# add a group to AutoBotGroupFolder
def addGroup(groupName, server, info):
    try:
        pathlib.Path('{}\\{}'.format(AutoBotGroupFolder, groupName)).mkdir()
        server.reply(info, '{}BOT组:§a{}§r创建成功'.format(PluginPrefix, groupName))
    except FileExistsError:
        server.reply(info, '{}已存在BOT组:§a{}§r'.format(PluginPrefix, groupName))
        return


# add a bot to group
def addBotToGroup(botName, groupName, server, info):
    if botName not in getBotList():
        server.reply(info, '{}未找到该BOT'.format(PluginPrefix))
        return
    if groupName not in getGroupList():
        server.reply(info, '{}未找到该BOT组'.format(PluginPrefix))
        return
    shutil.move('{}\\{}.json'.format(AutoBotFolder, botName), '{}\\{}\\'.format(AutoBotGroupFolder, groupName))
    server.reply(info, '{}已将BOT:§a{}§r移动至组:§a{}§r'.format(PluginPrefix, botName, groupName))


# del bot from AutoBotFolder
def delBot(botName, server, info):
    try:
        pathlib.Path('{}\\{}.json'.format(AutoBotFolder, botName)).unlink()
        server.reply(info, '{}BOT:§a{}§r删除成功'.format(PluginPrefix, botName))
    except FileNotFoundError:
        server.reply(info, '{}未找到该BOT'.format(PluginPrefix))
        return


# del group from AutoBotGroupFolder
def delGroup(groupName, server, info):
    try:
        shutil.rmtree('{}\\{}'.format(AutoBotGroupFolder, groupName))
        server.reply(info, '{}BOT组:§a{}§r删除成功'.format(PluginPrefix, groupName))
    except FileNotFoundError:
        server.reply(info, '{}未找到BOT组:§a{}§r'.format(PluginPrefix, groupName))


# del bot from group
def delBotFromGroup(botName, groupName, server, info):
    if groupName not in getGroupList():
        server.reply(info, '{}未找到该BOT组'.format(PluginPrefix))
        return
    if botName not in getBotListInGroup(groupName):
        server.reply(info, '{}未找到该BOT'.format(PluginPrefix))
        return
    shutil.move('{}\\{}\\{}.json'.format(AutoBotGroupFolder, groupName, botName), '{}\\'.format(AutoBotFolder))
    server.reply(info, '{}已将BOT:§a{}§r从组:§a{}§r移除'.format(PluginPrefix, botName, groupName))


# rename a group which in AutoBotGroupFolder
def renameGroup(originGroupName, targetGroupName, server, info):
    if targetGroupName in getGroupList():
        server.reply(info, '{}该BOT组名字已经存在'.format(PluginPrefix))
        return
    try:
        os.rename('{}\\{}'.format(AutoBotGroupFolder, originGroupName),
                  '{}\\{}'.format(AutoBotGroupFolder, targetGroupName))
        server.reply(info, '{}已将BOT组:§a{}§r重命名为:§a{}§r'.format(PluginPrefix, originGroupName, targetGroupName))
    except OSError:
        server.reply(info, '{}该BOT组不存在'.format(PluginPrefix))


# rename a bot which in AutoBotFolder
def renameBot(originBotName, targetBotName, server, info):
    if targetBotName in getBotList():
        server.reply(info, '{}该BOT名字已经存在'.format(PluginPrefix))
        return
    if not botNameCheck(targetBotName, server, info):
        return
    newBot = getBotInfo(originBotName)
    newBot['name'] = targetBotName
    with pathlib.Path('{}\\{}.json'.format(AutoBotFolder, targetBotName)).open('w') as f:
        f.write(json.dumps(newBot))
    pathlib.Path('{}\\{}.json'.format(AutoBotFolder, originBotName)).unlink()
    server.reply(info, '{}已将BOT:§a{}§r重命名为:§a{}§r'.format(PluginPrefix, originBotName, targetBotName))


# return a dict with botInfo
def getBotInfo(botName):
    with pathlib.Path('{}\\{}.json'.format(AutoBotFolder, botName)).open('r') as f:
        botInfo = json.loads(f.read())
        return botInfo


# return a dict with botInfo (bot is in group)
def getGroupBotInfo(groupName, botName):
    with pathlib.Path('{}\\{}\\{}.json'.format(AutoBotGroupFolder, groupName, botName)).open('r') as f:
        botInfo = json.loads(f.read())
        return botInfo


# return a list with dict of all bot info (bot is in group)
def getGroupAllBotInfo(groupName):
    allBotInfo = []
    for var in getBotListInGroup(groupName):
        allBotInfo.append(getGroupBotInfo(groupName, var))
    return allBotInfo


# spawn a bot in game
def spawnBot(botName, server):
    botInfo = getBotInfo(botName)
    server.execute('player {} spawn at {} facing ~ ~ in {}'.format(botInfo['name'], botInfo['pos'], botInfo['world']))
    server.say('{}BOT:§a{}§r已经部署'.format(PluginPrefix, botName))


# spawn a group of bot in game
def spawnGroupBot(groupName, server):
    if len(getBotListInGroup(groupName)) == 0:
        server.say('{}BOT组:§a{}§r内无BOT'.format(PluginPrefix, groupName))
        return
    for var in getGroupAllBotInfo(groupName):
        server.execute('player {} spawn at {} facing ~ ~ in {}'.format(var['name'], var['pos'], var['world']))
        server.say('{}BOT:§a{}§r已经部署'.format(PluginPrefix, var['name']))
    server.say('{}BOT组:§a{}§r已经部署'.format(PluginPrefix, groupName))


# kill a bot in game
def killBot(botName, server):
    server.execute('player {} kill'.format(botName))
    server.say('{}BOT:§a{}§r已经下线'.format(PluginPrefix, botName))


# kill a group of bot in game
def killGroupBot(groupName, server):
    if len(getBotListInGroup(groupName)) == 0:
        server.say('{}BOT组:§a{}§r内无BOT'.format(PluginPrefix, groupName))
        return
    for var in getGroupAllBotInfo(groupName):
        server.execute('player {} kill'.format(var['name']))
        server.say('{}BOT:§a{}§r已经下线'.format(PluginPrefix, var['name']))
    server.say('{}BOT组:§a{}§r已经下线'.format(PluginPrefix, groupName))


def kickBot(botName, server):
    server.execute('kill {}'.format(botName))
    server.say('{}BOT:§a{}§r不符合命名规则，强制踢出'.format(PluginPrefix, botName))


# spawn bot group peace when game on
def on_server_startup(server):
    if 'peace' in getGroupList():
        spawnGroupBot('peace', server)


# check AutoBotFolders and create folders when load/reload the plugin
def on_load(server, old):
    # help message register
    server.add_help_message('!!bot', '查看自动放置BOT的帮助')
    if not pathlib.Path(AutoBotFolder).exists():
        pathlib.Path(AutoBotFolder).mkdir()
    if not pathlib.Path(AutoBotGroupFolder).exists():
        pathlib.Path(AutoBotGroupFolder).mkdir()


def on_info(server, info):
    # change a bot`s gamemode to survival
    if not info.is_player and info.content.find('[local] logged in') != -1:
        botName = info.content.split('[')[0]
        # function: Kick bot
        if AutoKickUnPrefixBot:
            if botName.find('_') == -1 and botName not in unPrefixNameWhiteList:
                kickBot(botName, server)
            else:
                if botName.split('_')[0] not in botPrefix and botName not in unPrefixNameWhiteList:
                    kickBot(botName, server)
        server.execute('gamemode survival {}'.format(botName))

    # command register
    if info.is_player:
        if info.content.startswith('!!bot'):
            cmdList = info.content.split(' ')
            cmdLen = len(cmdList)
            if cmdLen == 1:
                for line in helpmsg.splitlines():
                    server.reply(info, line)
            # !!bot add
            if (cmdLen == 7 or cmdLen == 8) and cmdList[1] == 'add':
                if addBotCheck(cmdList[2], cmdList[3], cmdList[4], cmdList[5], cmdList[6], server, info):
                    if cmdLen == 7:
                        addBot(cmdList[2], '{} {} {}'.format(cmdList[3], cmdList[4], cmdList[5]), cmdList[6], '空',
                               server, info)
                    if cmdLen == 8:
                        addBot(cmdList[2], '{} {} {}'.format(cmdList[3], cmdList[4], cmdList[5]), cmdList[6],
                               cmdList[7], server, info)
            # !!bot del <bot>
            if cmdLen == 3 and cmdList[1] == 'del':
                delBot(cmdList[2], server, info)
            # !!bot rename <bot/group>
            if cmdLen == 4 and cmdList[1] == 'rename':
                if cmdList[2] in getBotList():
                    renameBot(cmdList[2], cmdList[3], server, info)
                elif cmdList[2] in getGroupList():
                    renameGroup(cmdList[2], cmdList[3], server, info)
                else:
                    server.reply(info, '{}未找到该BOT/BOT组'.format(PluginPrefix))
            # !!bot info <bot/group bot>
            if (cmdLen == 3 or cmdLen == 4) and cmdList[1] == 'info':
                if cmdLen == 3 and cmdList[2] in getBotList():
                    printBotInfo(cmdList[2], server, info)
                elif cmdLen == 4 and cmdList[2] in getGroupList() and cmdList[3] in getBotListInGroup(cmdList[2]):
                    printGroupBotInfo(cmdList[2], cmdList[3], server, info)
                else:
                    server.reply(info, '{}未找到该BOT'.format(PluginPrefix))
            # !!bot list
            if (cmdLen == 2 or cmdLen == 3) and cmdList[1] == 'list':
                if cmdLen == 2:
                    printBotList(server, info)
                elif cmdLen == 3 and cmdList[2] in getGroupList():
                    printBotListInGroup(cmdList[2], server, info)
                else:
                    server.reply(info, '{}未找到该BOT组'.format(PluginPrefix))
            # !!bot glist
            if cmdLen == 2 and cmdList[1] == 'glist':
                printGroupList(server, info)
            # !!bot gadd
            if cmdLen == 4 and cmdList[1] == 'gadd':
                addBotToGroup(cmdList[2], cmdList[3], server, info)
            # !!bot gdel
            if cmdLen == 4 and cmdList[1] == 'gdel':
                delBotFromGroup(cmdList[2], cmdList[3], server, info)
            # !!bot addgroup <group>
            if cmdLen == 3 and cmdList[1] == 'addgroup':
                addGroup(cmdList[2], server, info)
            # !!bot delgroup <group>
            if cmdLen == 3 and cmdList[1] == 'delgroup':
                delGroup(cmdList[2], server, info)
            # !!bot <bot/group>
            if cmdLen == 2:
                if cmdList[1] in getBotList():
                    spawnBot(cmdList[1], server)
                elif cmdList[1] in getGroupList():
                    spawnGroupBot(cmdList[1], server)
                # else:
                #     server.reply(info, '{}未找到该BOT/BOT组'.format(PluginPrefix))
            # !!bot kill <bot/group>
            if cmdLen == 3 and cmdList[1] == 'kill':
                if cmdList[2] in getBotList():
                    killBot(cmdList[2], server)
                elif cmdList[2] in getGroupList():
                    killGroupBot(cmdList[2], server)
                else:
                    server.reply(info, '{}未找到该BOT/BOT组'.format(PluginPrefix))
