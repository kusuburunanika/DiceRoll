# Pycordを読み込む
import discord
import random
from datetime import datetime

# アクセストークンを設定
TOKEN = "MTM4ODY2MTI1OTEzNzcxNjI3NA.GLfZ8W.Eo2l9nL0NTQfBVqlSVRRlMjHHn9cS1rjIX4Ivc"  # 自分のアクセストークンと置換してください

# Botの大元となるオブジェクトを生成する
bot = discord.Bot(
        intents=discord.Intents.all(),  # 全てのインテンツを利用できるようにする
        activity=discord.Game("Shadowverse: Worlds Beyond"),  # "〇〇をプレイ中"の"〇〇"を設定,
)


# 起動時に自動的に動くメソッド
@bot.event
async def on_ready():
    # 起動すると、実行したターミナルに"Hello!"と表示される
    print("Hello!")


# Botが見える場所でメッセージが投稿された時に動くメソッド
@bot.event
async def on_message(message: discord.Message):
    # メッセージ送信者がBot(自分を含む)だった場合は無視する
    if message.author.bot:
        return

    # メッセージが"hello"だった場合、"Hello!"と返信する
    if message.content == 'hello':
        await message.reply("Hello!")

# pingコマンドを実装
@bot.command(name="ping", description="pingを返します")
async def ping(ctx: discord.ApplicationContext):
    await ctx.respond(f"ping to {ctx.author.mention}")

# possition-5コマンドを実装
@bot.command(name="position-5", description="5名のポジションを決める")
async def position5(ctx: discord.ApplicationContext, 
                    user1: discord.Option(discord.User, "対象のユーザー1"), 
                    user2: discord.Option(discord.User, "対象のユーザー2"),
                    user3: discord.Option(discord.User, "対象のユーザー3"),
                    user4: discord.Option(discord.User, "対象のユーザー4"),
                    user5: discord.Option(discord.User, "対象のユーザー5")):
    # 現在時刻を取得してフォーマット
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # ユーザーとそのランダムな値をリストにまとめる
    users = [
        (user1, random.randint(1, 100)),
        (user2, random.randint(1, 100)),
        (user3, random.randint(1, 100)),
        (user4, random.randint(1, 100)),
        (user5, random.randint(1, 100))
    ]
    
    # 値で降順にソート
    users_sorted = sorted(users, key=lambda x: x[1], reverse=True)
    
    # ポジション情報
    position_column = ["TOP", "JUG", "MID", "BOT", "SUP"]
    
    # 出力の初期部分に現在時刻を加える
    response = f"---<{current_time}>-----------------------\n"
    
    # ユーザーとランダム値にポジションを付与
    for i, (user, value) in enumerate(users_sorted):
        response += f"{position_column[i]} - {user.mention}! (Your number is {value}).\n"

    # まとめたレスポンスを1つのメッセージとして送信
    await ctx.respond(response)

@bot.command(name="roll-all", description="オンラインのユーザー全員に1~100のサイコロを振る")
async def greeting(ctx: discord.ApplicationContext):
    # ギルド内の全ユーザーを取得
    # botを含む場合、online_users = [member for member in guild.members if member.status == discord.Status.online]とする。
    guild = ctx.guild
    online_users = [member for member in guild.members if member.status == discord.Status.online and not member.bot]
    
    if online_users:
        # 各ユーザーにランダムな数値を割り振る
        user_numbers = [(user, random.randint(1, 100)) for user in online_users]
        
        # 数値で降順にソート
        sorted_users = sorted(user_numbers, key=lambda x: x[1], reverse=True)
        
        # 挨拶のメッセージを作成
        greetings = [f"Hi, {user.mention}! Your number is {number}." for user, number in sorted_users]
        await ctx.respond("\n".join(greetings))
    else:
        # オンラインユーザーがいない場合のメッセージ
        await ctx.respond("現在オンラインのユーザーは誰もいません。")

# Botを起動
bot.run(TOKEN)

