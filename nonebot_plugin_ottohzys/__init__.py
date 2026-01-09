import asyncio

from nonebot import get_driver, logger
from nonebot.plugin import PluginMetadata, inherit_supported_adapters, require

require("nonebot_plugin_localstore")
require("nonebot_plugin_alconna")

from . import __main__ as __main__
from .config import DATA_DIR, ConfigModel, config
from .migrate import v0_migrate
from .pack import pack_manager
from .pack.online import download_pack

__version__ = "1.0.2"
__plugin_meta__ = PluginMetadata(
    name="活字印刷",
    description="大家好啊，今天来点大家想看的东西",
    usage="""
🚀 核心指令
• hzys [文本]
  └─ 使用默认语音包生成
  示例：`hzys 大家好啊我是电棍`
• [快捷指令] [文本]
  └─ 使用特定语音包 (取决于配置)
  示例：`ottohzys 欧内的手`

🎛️ 效果微调 (追加在指令后)
• -s [数值]：语速 (默认1.0, ≥0.5)
• --pitch [数值]：音调 (默认1.0, 0~2)
• --pack [名称]：指定语音包
• -r：启用倒放
• -Y：禁用原声大碟 (强制合成)
• -N：禁用音量归一化

📦 资源管理
• -Ll / -Lo：列出 本地/在线 语音包
• -Ly：查看当前包的原声列表
• -D [名称]：下载语音包 (仅超管)
• -R：重载配置 (仅超管)

> 更多用法请发送: hzys -h
""",
    type="application",
    homepage="https://github.com/lgc-NB2Dev/nonebot-plugin-ottohzys",
    config=ConfigModel,
    supported_adapters=inherit_supported_adapters("nonebot_plugin_alconna"),
    extra={"License": "MIT", "Author": "LgCookie"},
)


driver = get_driver()


@driver.on_startup
async def _():
    async def task():
        v0_migrate()
        pack_manager.reload()

        if not pack_manager.get_pack(config.default_pack):
            logger.info(f"Downloading default voice pack (`{config.default_pack}`)")
            try:
                await download_pack(config.default_pack, DATA_DIR / config.default_pack)
            except Exception:
                logger.exception(
                    f"Failed to download voice pack `{config.default_pack}`",
                )
            else:
                logger.success("Downloaded voice pack `{config.default_pack}`")
                pack_manager.reload()

    asyncio.create_task(task())
