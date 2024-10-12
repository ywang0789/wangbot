from secret.keys import DISCORD_TOKEN
from wangbot import WangBot


def main():
    bot = WangBot()
    bot.run(DISCORD_TOKEN)


if __name__ == "__main__":
    main()
