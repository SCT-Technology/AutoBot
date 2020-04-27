# -*- coding: utf-8 -*-
import json
import os
import shutil

helpmsg = '''------MCDR AutoBot插件------
命令帮助如下:
!!bot -显示帮助消息
!!bot add <BOT名字> <X坐标> <Y坐标> <Z坐标> <世界> <备注> -添加BOT到BOT列表
注：名字必须为bot_, farm_, p_, 开头, 坐标为整数，世界为overworld, nether, end, 三者之一
!!bot del <BOT名字>
!!bot radd -覆盖已有BOT 参数需完全覆盖
!!bot addgroup <组名字> <备注>-添加BOT组
!!bot delgroup <组名字> -移除BOT组
!!bot gadd <BOT名字> <组名字> -添加BOT至BOT组
!!bot gdel <BOT名字> <组名字> -从BOT组移除BOT
!!bot list -查看可部署的BOT列表
!!bot glist -查看可部署的BOT组列表
!!bot info <BOT名字/BOT组名字> -查看BOT/BOT组信息
!!bot <BOT名字/BOT组名字> -部署BOT/BOT组
!!bot kill <BOT名字/BOT组名字> -下线BOT/BOT组
--------------------------------'''


AutoBotFolder = './AutoBot'
AutoBotGroupFolder = AutoBotFolder + '\\group'


def on_info(server, info):
    if info.is_player:
        if info.content.startswith('!!bot'):
            cmdList = info.content.split(' ')
            cmdLen = len(cmdList)
            if cmdLen == 1:
                for line in helpmsg.splitlines():
                    server.tell(info.player, line)
            if cmdLen == 2 and cmdList[1] == 'list':
                list = getBotList()
                for bot in list:
                    server.reply(info, bot)
            if cmdLen == 2 and cmdList[1] == 'glist':
                list = getGroupList()
                for group in list:
                    server.reply(info, group)
            if cmdLen == 3 and cmdList[1] == 'info':
                name = cmdList[2]
                if name in getBotList():
                    botInfo = getBotInfo(name)
                    server.reply(info, 'BOT名字:' + botInfo['name'] + '\nBOT坐标:' + botInfo['pos'] + '\nBOT世界:' + botInfo[
                        'world'] + '\nBOT备注:' + botInfo['detail'])
                elif name in getGroupList():
                    groupInfo = getGroupInfo(name)
                    groupBotList = getGroupBotList(name)
                    server.reply(info, '组名字:' + name + '\n组备注:' + groupInfo['detail'])
                    server.reply(info, '组BOT列表:')
                    for bot in groupBotList:
                        server.reply(info, bot.split('.', 1)[0])
                else:
                    server.reply(info, '该BOT不存在，获取信息失败')
            if (cmdLen == 7 or cmdLen == 8) and (cmdList[1] == 'add' or cmdList[1] == 'radd'):
                # BOT名字, 坐标， 世界名字检测
                name = cmdList[2]
                posX = cmdList[3]
                posY = cmdList[4]
                posZ = cmdList[5]
                world = cmdList[6]
                if cmdLen == 8:
                    detail = cmdList[7]
                if not botNameCheck(name):
                    server.reply(info, 'BOT名字不符合规范，添加失败。请使用bot_, farm_, p_前缀, 长度保持在16以下')
                elif (name in getBotList()) and (cmdList[1] == 'add'):
                    server.reply(info, '该BOT已存在，添加失败。请使用!!bot radd覆盖原有BOT')
                elif (name not in getBotList()) or cmdList[1] == 'radd':
                    if posCheck(posX, posY, posZ):
                        pos = posX + ' ' + posY + ' ' + posZ
                        if worldCheck(world):
                            if cmdLen == 8:
                                addFullBot(name, pos, world, detail)
                            else:
                                addBot(name, pos, world)
                            server.reply(info, 'BOT:' + name + '添加成功')
                        else:
                            server.reply(info, '世界名字不符合规范，添加失败。请使用overworld， nether， end作为世界名字')
                    else:
                        server.reply(info, '坐标不符合规范，添加失败。请添加整数坐标')
            if cmdLen == 3 and cmdList[1] == 'del':
                name = cmdList[2]
                if botNameCheck(name):
                    if name in getBotList():
                        delBot(name)
                        server.reply(info, 'BOT:' + name + '删除成功')
                    else:
                        server.reply(info, '未找到该BOT，请检查BOT名字')
                else:
                    server.reply(info, 'BOT名字不符合规范，删除失败。请使用bot_, farm_, p_前缀, 长度保持在16以下')
            if (cmdLen == 3 or cmdLen == 4) and cmdList[1] == 'addgroup':
                name = cmdList[2]
                if cmdLen == 4:
                    detail = cmdList[3]
                if cmdLen == 3 and name not in getGroupList():
                    addGroup(name)
                    server.reply(info, 'BOT组:' + name + '建立成功')
                if cmdLen == 4 and name not in getGroupList():
                    addFullGroup(name, detail)
                    server.reply(info, 'BOT组:' + name + '建立成功')
                if name in getGroupList():
                    server.reply(info, '已存在该组， 添加失败')
            if cmdLen == 3 and cmdList[1] == 'delgroup':
                name = cmdList[2]
                if name in getGroupList():
                    delGroup(name)
                    server.reply(info, 'BOT组:' + name + '删除成功')
                else:
                    server.reply(info, '未找到该BOT组，删除失败')
            if cmdLen == 4 and cmdList[1] == 'gadd':
                botName = cmdList[2]
                groupName = cmdList[3]
                if botName in getBotList():
                    if groupName in getGroupList():
                        addBotToGroup(botName, groupName)
                        server.reply(info, '已将BOT:' + botName + '添加至组:' + groupName)
                    else:
                        server.reply(info, '未找到该BOT组，添加失败')
                else:
                    server.reply(info, '未找到该BOT，添加失败')
            if cmdLen == 4 and cmdList[1] == 'gdel':
                botName = cmdList[2] + '.json'
                groupName = cmdList[3]
                if botName in getGroupBotList(groupName):
                    if groupName in getGroupList():
                        delBotFromGroup(botName, groupName)
                        server.reply(info, '已将BOT:' + cmdList[2] + '从组:' + groupName + '移除')
                    else:
                        server.reply(info, '未找到该BOT组，删除失败')
                else:
                    server.reply(info, '未找到该BOT，删除失败')
            if cmdLen == 2:
                name = cmdList[1]
                if name in getBotList():
                    if botNameCheck(name):
                        spawnBot(name, server)
                    else:
                        pass
                if name in getGroupList():
                    spawnGroupBot(name, server)
                else:
                    pass
                # if name not in getBotList() and name not in getGroupList():
                #     server.reply(info, '未找到BOT/BOT组，部署失败')
            if cmdLen == 3 and cmdList[1] == 'kill':
                name = cmdList[2]
                if name in getBotList():
                    if botNameCheck(name):
                        killBot(name, server)
                    else:
                        pass
                if name in getGroupList():
                    killGroupBot(name, server)
                if name not in getBotList() and name not in getGroupList():
                    server.reply(info, '未找到BOT/BOT组，下线失败')


def on_load(server, old_module):
    server.add_help_message('!!bot', '显示自动放置BOT插件的帮助信息')
    if not os.path.exists(AutoBotFolder):
        os.mkdir(AutoBotFolder)
    if not os.path.exists(AutoBotGroupFolder):
        os.mkdir(AutoBotGroupFolder)


def spawnBot(name, server):
    botInfo = getBotInfo(name)
    name = botInfo['name']
    pos = botInfo['pos']
    world = botInfo['world']
    cmdSpawnBot = 'player ' + name + ' spawn at ' + pos + ' facing ~ ~ in ' + world
    server.execute(cmdSpawnBot)
    server.say('BOT:' + name + '已经部署')


def spawnGroupBot(name, server):
    botList = getGroupBotList(name)
    groupName = name
    for bot in botList:
        botInfo = getGroupBotInfo(groupName, bot)
        name = botInfo['name']
        pos = botInfo['pos']
        world = botInfo['world']
        cmdSpawnBot = 'player ' + name + ' spawn at ' + pos + ' facing ~ ~ in ' + world
        server.execute(cmdSpawnBot)
        server.say('BOT:' + name + '已经部署')


def killBot(name, server):
    botInfo = getBotInfo(name)
    name = botInfo['name']
    cmdKillBot = 'player ' + name + ' kill'
    server.execute(cmdKillBot)
    server.say('BOT:' + name + '已经下线')


def killGroupBot(name, server):
    botList = getGroupBotList(name)
    groupName = name
    for bot in botList:
        botInfo = getGroupBotInfo(groupName, bot)
        name = botInfo['name']
        cmdKillBot = 'player ' + name + ' kill'
        server.execute(cmdKillBot)
        server.say('BOT:' + name + '已经下线')


def addBot(name, pos, world):
    if world == 'overworld' or world == 'nether' or world == 'end':
        if world == 'overworld':
            world = 'minecraft:' + world
        else:
            world = 'minecraft:the_' + world
    dict = {'name': name, 'pos': pos, 'world': world, 'detail': '空'}
    with open(AutoBotFolder + '\\' + name + '.json', 'w') as f:
        f.write(json.dumps(dict))


def addFullBot(name, pos, world, detail):
    dict = {'name': name, 'pos': pos, 'world': world, 'detail': detail}
    with open(AutoBotFolder + '\\' + name + '.json', 'w') as f:
        f.write(json.dumps(dict))


def delBot(name):
    if name in getBotList():
        os.remove(AutoBotFolder + '\\' + name + '.json')


def getBotList():
    botList = []
    dirs = os.listdir(AutoBotFolder)
    for bot in dirs:
        if bot == 'group':
            pass
        else:
            botList.append(bot.split('.', 1)[0])
    return botList


def getGroupBotList(name):
    groupBotList = []
    dirs = os.listdir(AutoBotGroupFolder + '\\' + name + '\\')
    for bot in dirs:
        if bot == 'info.json':
            pass
        else:
            groupBotList.append(bot)
    return groupBotList


def addGroup(name):
    thisGroupFolder = AutoBotGroupFolder + '\\' + name
    if not os.path.exists(thisGroupFolder):
        os.mkdir(thisGroupFolder)
        dict = {'detail': '空'}
        with open(thisGroupFolder + '\\' + 'info.json', 'w') as f:
            f.write(json.dumps(dict))


def addFullGroup(name, detail):
    thisGroupFolder = AutoBotGroupFolder + '\\' + name
    if not os.path.exists(thisGroupFolder):
        os.mkdir(thisGroupFolder)
        dict = {'detail': detail}
        with open(thisGroupFolder + '\\' + 'info.json', 'w') as f:
            f.write(json.dumps(dict))


def delGroup(name):
    shutil.rmtree(AutoBotGroupFolder + '\\' + name)


def addBotToGroup(botName, groupName):
    shutil.move(AutoBotFolder + '\\' + botName + '.json', AutoBotGroupFolder + '\\' + groupName + '\\')


def delBotFromGroup(botName, groupName):
    shutil.move(AutoBotGroupFolder + '\\' + groupName + '\\' + botName, AutoBotFolder + '\\')


def getGroupList():
    groupList = []
    dirs = os.listdir(AutoBotGroupFolder)
    for file in dirs:
        groupList.append(file)
    return groupList


def getBotInfo(name):
    with open(AutoBotFolder + '\\' + name + '.json', 'r') as f:
        botInfo = json.loads(f.read())
        return botInfo


def getGroupBotInfo(groupName, botName):
    with open(AutoBotGroupFolder + '\\' + groupName + '\\' + botName, 'r') as f:
        groupBotInfo = json.loads(f.read())
        return groupBotInfo


def getGroupInfo(name):
    with open(AutoBotGroupFolder + '\\' + name + '\\' + 'info.json', 'r') as f:
        groupInfo = json.loads(f.read())
        return groupInfo


def botNameCheck(name):
    if name.find('_') == -1 or name.find('.') != -1:
        return False
    else:
        botNameWhiteList = ['bot', 'farm', 'p', 'peace']
        if len(name) <= 16:
            return name.split('_', 1)[0] in botNameWhiteList
        else:
            return False


def posCheck(posX, posY, posZ):
    try:
        a = int(posX)
        a = int(posY)
        a = int(posZ)
        return True
    except ValueError:
        return False


def worldCheck(world):
    if world == 'overworld' or world == 'nether' or world == 'end':
        return True
    else:
        return False
