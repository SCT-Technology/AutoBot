# AutoBot
A plugin for MCDR to spawn BOT/BOTS
用来生成BOT或批量生成BOT的插件
!!Carpet模组需要并且打开commandPlayer!!
-----------------------------------------------------------------------------------------
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
-----------------------------------------------------------------------------------------
注:删除BOT组会将组内所有BOT删除。
# 文件架构：
	./AutoBot//:
		group//:
			eachgroup//
		eachbots.json
