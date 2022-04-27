# Chibibot Script

import random
import asyncio
import nextcord
from nextcord.ext.commands.errors import BotMissingPermissions
from nextcord.ext import commands
from nextcord import ButtonStyle
from nextcord.ui import Button, View
import webbrowser



# site variables
youtube = 'https://www.youtube.com'
discord_url = 'https://discord.com'
twitter = 'https://twitter.com'
github = 'https://github.com'
stackoverflow = 'https://stackoverflow.com'
bot = commands.Bot(command_prefix="c!", case_insensitive=True)
bot.remove_command('help')


@bot.event
async def on_ready():
    await bot.change_presence(activity=nextcord.Game(name=f'c!help https://discord.gg/8xJJVKZjEN'))
    print('I\'m logged in. Beep Bop Bop Beep Bop.')


@bot.event
async def on_member_join(member: nextcord.Member):
    welcoming_msg = [
        "Welcome to the server!",
        "Great to see you here!",
        "Enjoy your stay here!",
        "Cool that you are here!"
    ]
    join_channel = member.guild.get_channel(860864110047264768)
    await join_channel.send(f'Hey {member.mention}, {random.choice(welcoming_msg)}')


#Message is raised when you made an error while using one of the commands
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('Beeeep boop...')
        await asyncio.sleep(0.5)
        await ctx.send('Error in file bot.py, line 53')
        await asyncio.sleep(0.5)
        await ctx.send('```await do_nothing(nothing=discord.Tasks.do_nothing())```')
        await ctx.send('Command_Error: command not found')
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send('You do not have the permissions to use this command.')
    elif isinstance(error, BotMissingPermissions):
        msg = await ctx.send("Hey, GIVE ME THE DAMN PERMISSIONS TO DO MY JOB!")
        await msg.add_reaction(":face_with_symbols_over_mouth:")


@bot.command()
async def botinfo(ctx):
    botinfo_embed = nextcord.Embed(
        color=nextcord.Colour.blue()
    )
    botinfo_embed.set_author(name="-----Bot Info-----")
    botinfo_embed.add_field(name='About this Bot:',
                            value='Chibibot is a Fully Open-Source Discord Bot  with Source Code on GitHub. ')
    botinfo_embed.add_field(name="Prefix:", value="c!, If you want to change it, edit the Source Code.")
    botinfo_embed.add_field(name='Source Code:', value='Bot Source Code on GitHub:'
                                                       ' https://github.com/atomfrog/Chibibot/blob/main/bot.py')
    botinfo_embed.add_field(name='Developed by thatonedumbdev', value='-------------------------------',
                            inline=False)
    await ctx.send(embed=botinfo_embed)


# moderation commands

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, user: nextcord.Member, *, reason=None):
    if reason is None:
        return await ctx.send('Please specify a reason to kick this user!')
    await user.kick(reason=reason)
    await user.send(f'You have been kicked for reason {reason} !')
    await ctx.send(f"\u2705 User {user.mention} has been kicked for reason {reason}!")


@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("Sorry, You aren\'t allowed to kick Users! ")
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("You have to specify a User to kick!")
    if isinstance(error, commands.MemberNotFound):
        await ctx.send(f'BOOOOP ... FATAL ERROR {random.randint(1, 50)} ... MEMBER_NOT_FOUND')


@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, user: nextcord.Member, *, reason=None):
    if reason is None:
        await ctx.send('PLease specify a reason to ban this user!')
    await user.ban(reason=reason)
    await user.send(f'You have been banned for reason {reason} !')
    await ctx.send(f"\u2705 User {user.mention} has been banned successfully!")


@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("Sorry, You aren\'t allowed to ban Users! Please make sure you have the permissions. ")
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please Specify a User to ban!")
    if isinstance(error, commands.MemberNotFound):
        await ctx.send("BEEP ... ERROR: MEMBER_NOT_FOUND BEEP BOP BOP")


@bot.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'\u2705 Unbanned {user.mention} !')
            return


@unban.error
async def unban_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("Sorry, You aren\'t allowed to unban Users! ")
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("You have to specify a User to unban!")
    if isinstance(error, commands.MemberNotFound):
        await ctx.send("Hey, I could not find that user.")


@bot.command()
@commands.has_permissions(kick_members=True)
async def warn(ctx, user: nextcord.Member, *, reason=None):
    embed = nextcord.Embed(
        color=nextcord.Colour.red()
    )
    embed.set_author(name='---You have been warned---')
    embed.add_field(name=f'You have been warned by {ctx.author} for reason {reason} .',
                    value='This message is automatically '
                          'sent. It will be deleted after an '
                          'hour.', inline=False)
    embed2 = nextcord.Embed(
        color=nextcord.Colour.green()
    )
    embed2.set_author(name=f'\u2705 Member {user} has been warned')
    embed2.add_field(name=f'You warned {user} for reason {reason} .', value=f'I sent a direct Message to {user} !')
    if user == ctx.author:
        return await ctx.send("You cannot warn yourself!")
    if reason is None:
        return await ctx.send("Please specify a reason to warn this user.")
    await user.send(embed=embed, delete_after=60 * 60)
    await ctx.send(embed=embed2)


@warn.error
async def warn_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("Sorry, You aren\'t allowed to warn Users. ")
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("You have to specify a User!")
    if isinstance(error, commands.MemberNotFound):
        await ctx.send("Hey, i did not find that user. Make sure it\'s the right name.")

#Please don't use this right now
@bot.command()
@commands.has_permissions(kick_members=True)
async def set_watchlist(ctx, user: nextcord.Member):
    watchlist = []
    embed = nextcord.Embed(
        color=nextcord.Colour.random()
    )
    embed.set_author(name="--User Watchlist--")
    embed.add_field(name=f"{user} is now on the Watchlist.", value=f"{user} is already informed.", inline=False)
    watchlist.append(f'{user}')
    await ctx.send(embed=embed)
    await user.send("You are now on the Moderator Watchlist! Be Careful, now you can get kicked easily!")
    await ctx.send(f'Current members on the watchlist: {watchlist}')


@bot.command(name='create_thread', aliases=['thread'])
@commands.has_permissions(create_public_threads=True)
async def thread(ctx, *, arg):
    await ctx.channel.create_thread(name=f'{arg}', message=None, auto_archive_duration=60, type=nextcord.ChannelType.public_thread, reason=None)
    await ctx.send(f'Successfully created thread {arg}!')


@bot.command(name='create_channel')
@commands.has_permissions(manage_channels=True)
async def addchannel(ctx, *, arg):
    await ctx.guild.create_text_channel(f'{arg}')
    await ctx.send(f"I've successfully created the text channel {arg}!")


@bot.command(name='delete_channel', aliases=['remove_channel'])
@commands.has_permissions(manage_channels=True)
async def remove_channel(ctx, *, arg):
    removed_channel = nextcord.utils.get(ctx.guild.text_channels, name=arg.lower())
    if removed_channel is None:
        return await ctx.reply("I did not find that channel!")
    await removed_channel.delete()
    await ctx.send("I've Successfully deleted the channel!")


@bot.command()
async def ticket(ctx):
    author = ctx.author.name
    embed = nextcord.Embed(
        title='Create a Ticket',
        description='React with 📩 to create a ticket',
        color=nextcord.Colour.green()
    )
    embed.set_footer(text="Ticket System")
    msg = await ctx.send(embed=embed)
    await msg.add_reaction("📩")

    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) == '📩'
    try:
        reaction, user = await bot.wait_for('reaction_add', timeout=10, check=check)
    except asyncio.TimeoutError:
        await ctx.send("Not fast enough buddy! You timed out!")
        return
    channel = await ctx.guild.create_text_channel(f'ticket-support {author}')
    ticket_embed = nextcord.Embed(
        title='This is your ticket channel!',
        description='A supporter will help you as quickly as possible!',
        color=nextcord.Colour.blurple()
    )
    ticket_embed.set_footer(text="Support System")
    ticket_msg = await channel.send(embed=ticket_embed)
    await ticket_msg.add_reaction('✅')


@bot.command()
async def close_ticket(ctx, *, arg):
    user = arg.lower()
    support_channel = nextcord.utils.get(ctx.guild.text_channels, name=f'ticket-support-{user}')
    if support_channel is None:
        return await ctx.send(f"Ticket Channel {arg} was not found! \n Create on with the **c!ticket** command.")
    await support_channel.delete(reason="TICKET_CLOSED")
    closed_embed = nextcord.Embed(
        title='Ticket succesfully closed!',
        description='I deleted the Ticket Channel!',
        color=nextcord.Colour.dark_blue()
        )
    closed_embed.set_footer(text='Ticket System')
    closed_msg = await ctx.send(embed=closed_embed)
    await closed_msg.add_reaction('\u2705')


@close_ticket.error
async def close_ticket_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please type the name of the ticket channel after the c!close_ticket!")
        await ctx.send("e.g. c!close_ticket justarandomuser")


# some random stuff idk why we added this
@bot.command()
async def rickroll(ctx):
    rickroll_button = Button(label='get rickrolled', url='https://www.youtube.com/watch?v=dQw4w9WgXcQ')

    rickroll_view = View(timeout=None)
    rickroll_view.add_item(rickroll_button)
    await ctx.send("So you really want to get rickrolled?", view=rickroll_view)


@bot.command()
async def lotto(ctx, amount: int):
    lottonumber = random.randint(1, 50)
    if amount == lottonumber:
        await ctx.send("Congratulations! You\'re right!")
    elif amount < 1 or amount > 50:
        await ctx.send("Only Numbers between 1 and 50 are valid!")
    else:
        await ctx.send(f"Noo... Sorry, {amount} isn\'t right... The Solution was {lottonumber}. Better Luck next Time!")


@lotto.error
async def lotto_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please enter a number between 1 and 50 after the c!lotto command.")


@bot.command()
async def play(ctx):
    valid_choices = ["🪨", "📰", "✂"]
    ai_choices = ["Rock", "Paper", "Scissors"]
    ai_choice = random.choice(ai_choices)
    embed = nextcord.Embed(
        title='Rock Paper Scissors',
        description='React with the emojis to play',
        color=nextcord.Colour.random()
    )
    embed.set_footer(text="Rock Paper Scissors Game")
    msg = await ctx.send(embed=embed)
    await msg.add_reaction("🪨")
    await msg.add_reaction("📰")
    await msg.add_reaction("✂")

    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in valid_choices
    try:
        reaction, user = await bot.wait_for('reaction_add', timeout=30.0, check=check)
    except asyncio.TimeoutError:
        return await ctx.send("Not fast enough my guy!")
    if str(reaction.emoji) == "✂":
        if ai_choice == "Rock":
            await ctx.send("HAHAHAHA! I SMASHED YOU WITH MY ROCK!")
        elif ai_choice == "Scissors":
            await ctx.send("Tie! No one wins! We both chose this red thing right here: ✂")
        else:
            await ctx.send("Nooooooooo... You got me with your scissors")
    if str(reaction.emoji) == "🪨":
        if ai_choice == "Paper":
            await ctx.send("Yes! I packed your rock into paper!")
        elif ai_choice == "Rock":
            await ctx.send("Tie! No one wins! But why did we try to fight ourselves with the same thing?")
        else:
            await ctx.send("WHAT? HOW DID YOU JUST SMASH ME?")
            await asyncio.sleep(0.1)
            await ctx.send("*aimbot*")
            await asyncio.sleep(0.1)
            await ctx.send("*hacker*")
    if str(reaction.emoji) == "📰":
        if ai_choice == "Scissors":
            await ctx.send("Sometimes paper isn't strong enough against scissors... anyways, **I won**")
        elif ai_choice == "Paper":
            await ctx.send("Tie! We both chose 📰")
        else:
            await ctx.send("You got me again...")


# help command
@bot.command(pass_context=True)
async def help(ctx):
    embed1 = nextcord.Embed(
        color=nextcord.Colour.blue()
    )
    embed1.set_author(name='--Help for the Commands--')
    embed1.add_field(name='c!botinfo', value='Shows a Botinfo')
    embed1.add_field(name='c!ban', value='Bans a Member', inline=True)
    embed1.add_field(name='c!kick', value='Kicks a Member', inline=True)
    embed1.add_field(name='c!unban', value='Unbans Member', inline=True)
    embed1.add_field(name='c!warn', value='warns a Member, this Command is still in development', inline=True)
    embed1.add_field(name='c!clear (amount of messages)', value='deletes Messages', inline=True)
    embed1.add_field(name='c!rickroll', value='rickrolls yourself, so don\'t try it', inline=True)
    embed1.add_field(name='c!lotto {any number between 1 and 50}', value='starts a small lottery', inline=True)
    embed1.add_field(name='c!battle {any user}', value='Attacks the user', inline=True)
    embed1.add_field(name='c!set_watchlist', value='Command still in development', inline=True)
    embed1.add_field(name='c!ticket', value='Creates a support ticket')
    embed1.add_field(name='c!close_ticket', value='Deletes the ticket channel, use \n this only if there is already a ticket channel.')
    embed1.add_field(name='c!play', value='Starts a rock-paper-scissors round.')
    embed1.add_field(name='c!create_channel <name of the channel>', value='Creates a channel.')
    embed1.add_field(name='c!delete_channel <name of the channel>',value='Deletes the channel')
    embed1.add_field(name='If you need help:', value='https://discord.gg/2WRXSjEkzY', inline=False)
    embed1.add_field(
        name='Bot made and Developed by atomfrog and FreerideFriendsYT, Source Code: '
             'https://github.com/atomfrog/Chibibot/blob/main/bot.py',
        value='-----------------------------------', inline=False)
    msg = await ctx.send(embed=embed1)
    await msg.add_reaction('\u2705')


# clear command

@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    await asyncio.sleep(0.5)
    if amount > 100:
        return await ctx.send("You can\'t delete 100 or more messages!")
    elif amount < 1:
        return await ctx.send("You can\'t clear less than 1 message!")
    else:
        await ctx.channel.purge(limit=amount + 1)


@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please specify an amount of messages to delete!')


# new battle command
@bot.command()
async def battle(ctx, user: nextcord.Member):
    if user == ctx.author:
        await ctx.send("What? You are literally trying to battle yourself?")
        await asyncio.sleep(0.5)
        return await ctx.send("You are a bit weird...")

    class Army:
        player1 = ctx.author

        def __init__(self):
            self.Force = random.randint(10, 100)

        @staticmethod
        async def initiate_attack():
            await ctx.send("Recruiting the Troops...")
            await asyncio.sleep(0.5)
            await ctx.send(f"Army is ready to battle against {user} !")

    class Enemy(Army):
        enemy_player = user

        @staticmethod
        async def initiate_attack():
            await user.send(f'Quick! You are getting  attacked by {ctx.author}!')
        pass

    a = Army()
    e = Enemy()
    await a.initiate_attack()
    await e.initiate_attack()
    await asyncio.sleep(2.5)
    if a.Force > e.Force:
        await ctx.send(f'{a.player1} won against {e.enemy_player} !')
        await user.send(f'{a.player1} defeated you...')
    elif a.Force == e.Force:
        await ctx.send('No one won!')
        await user.send("You were lucky... no one won!")
    else:
        await ctx.send(f'{e.enemy_player} won the battle.')
        await user.send(f"Congrats! You won against {a.player1}")


@battle.error
async def battle_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Umm... \n So you have to specify a user to battle... otherwise it won't work.")

    elif isinstance(error, commands.MemberNotFound):
        await ctx.send("Hey, it looks like this user is not on the server.")
                                            
bot.run('Your token here')
