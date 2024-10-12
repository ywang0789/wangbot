import secret.keys as keys
from wangbot import WangBot


def main():
    bot = WangBot()
    bot.run(keys.DISCORD_TOKEN)


if __name__ == "__main__":
    main()
