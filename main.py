import discord
import random
import json
import os
import datetime
import asyncio
import pytz
import traceback
import sys

from discord.ext.commands import has_permissions, MissingPermissions
from datetime import datetime
from discord.ext.commands import cooldown, BucketType
from discord.ext import commands
from io import StringIO

intents = discord.Intents.all()

client = commands.Bot(command_prefix='.', intents=intents)
client.remove_command('help')

@client.event
async def on_ready():
	activity = discord.Activity(type=discord.ActivityType.listening, name="v1.0.4")
	await client.change_presence(status=discord.Status.online,
	                             activity=activity)
	print('Signed in as {0.user}'.format(client))

@client.event
async def on_member_join(member):
  guild = client.get_guild(774501063557382155)
  try:
    welcomechannel =  client.get_channel(775658826568957974)
    verifychannel =  client.get_channel(856235691955847168)
    a = discord.utils.get(member.guild.roles, name='Unverified')
    b = discord.utils.get(member.guild.roles, name='-----------------=Roles=-----------------')
    await member.add_roles(a)
    await member.add_roles(b)
    x = "Hey {}, welcome!".format(member.mention)
    embed=discord.Embed(title="Welcome", url="", 
    description="Head on over to <#836708196945100820> to see the rest of the channels. \n \nIP - mc.randomnetwork.xyz".format(member.mention), 
    color=discord.Color.green())
    await welcomechannel.send(content=x, embed=embed)
    embed=discord.Embed(title="Welcome", url="", 
    description=f"Welcome to **{member.guild.name}**! \n \nIP - mc.randomdnetwork.xyz \n Store - http://shop.randomdupes.xyz/ \n \nRegards, \n**RandomNetwork Staff**", 
    color=discord.Color.green())
    await member.send(embed=embed)
    await verifychannel.send("{}".format(member.mention), delete_after=1)


  except Exception:
    welcomechannel =  client.get_channel(858587751268220948)
    a = discord.utils.get(member.guild.roles, name='Unverified')
    b = discord.utils.get(member.guild.roles, name='-----------------=Roles=-----------------')
    await member.add_roles(a)
    await member.add_roles(b)
    x = "Hey {}, welcome!".format(member.mention)
    embed=discord.Embed(title="Welcome", url="", 
    description="Head on over to <#856235691955847168> to see the rest of the channels. \n \nIP - Coming Soon!".format(member.mention), 
    color=discord.Color.green())
    await welcomechannel.send(content=x, embed=embed)
    await verifychannel.send("{}".format(member.mention), delete_after=1)
    
@client.command()
async def enlarge(ctx, emoji: discord.PartialEmoji = None):
    if not emoji:
        await ctx.send("You need to provide an emoji!")
    else:
        await ctx.send(emoji.url)

@client.command()
@commands.has_permissions(administrator=True)
async def rtickets(ctx):
    embed=discord.Embed(title="Tickets", url="", 
    description=f'Please click the reaction to your corresponding problem.', 
    color=discord.Color.purple())
    embed.add_field(name="General", value="📩", inline=True)
    embed.add_field(name="Appeal", value="<:AdminAbooz:862472131446439957>", inline=True)
    embed.add_field(name="Reports", value="<a:BanHammer:862472442785300501>", inline=True)
    embed.add_field(name="Bugs", value="<a:GlitchCat:862472688396140586>", inline=True)
    embed.add_field(name="Donation", value="<:Money:862472891462451201>", inline=True)
    embed.add_field(name="Other", value="<a:Hmmm:862473071679635456>", inline=True)
    msg = await ctx.channel.send(embed=embed)
    await msg.add_reaction('📩')
    await msg.add_reaction('<:AdminAbooz:862472131446439957>')
    await msg.add_reaction('<a:BanHammer:862472442785300501>')
    await msg.add_reaction('<a:GlitchCat:862472688396140586>')
    await msg.add_reaction('<:Money:862472891462451201>')
    await msg.add_reaction('<a:Hmmm:862473071679635456>')
    await ctx.message.delete()

@client.command()
@commands.has_permissions(administrator=True)
async def rrverifys(ctx):
    embed=discord.Embed(title="Verification", url="", 
    description=f'To verify, click the reaction.', 
    color=discord.Color.purple())
    embed.set_footer(text=f"RandomDupes")
    msg = await ctx.channel.send(embed=embed)
    await msg.add_reaction('☑️')
    await ctx.message.delete()
        
@client.event
async def on_raw_reaction_add(payload):
  member = payload.member
  if member.bot:
    return
  guild = client.get_guild(payload.guild_id)
  member = guild.get_member(payload.user_id)

  if str(payload.emoji) == '☑️' and (payload.message_id) == 858589588004274216:
    try:
      unverified = discord.utils.get(guild.roles, name='Unverified')
      verified = discord.utils.get(guild.roles, name='Member')
      await member.send('You have been verified. Thanks!')
      await member.remove_roles(unverified)
      await member.add_roles(verified)

      channel = client.get_channel(payload.channel_id)
      message = await channel.fetch_message(payload.message_id)
      user = client.get_user(payload.user_id)
      emoji = "☑️"
      await message.remove_reaction(emoji, user)
    except Exception:
      unverified = discord.utils.get(guild.roles, name='Unverified')
      verified = discord.utils.get(guild.roles, name='Member')
      await member.remove_roles(unverified)
      await member.add_roles(verified)

      channel = client.get_channel(payload.channel_id)
      message = await channel.fetch_message(payload.message_id)
      user = client.get_user(payload.user_id)
      emoji = "☑️"
      await message.remove_reaction(emoji, user)

  if str(payload.emoji) == '🔒':
    with open('data.json') as f:
      data = json.load(f)

    if payload.channel_id in data["ticket-channel-ids"]:
      channel = client.get_channel(payload.channel_id)
      message = await channel.fetch_message(payload.message_id)
      user = client.get_user(payload.user_id)
      emoji = "🔒"
      await message.remove_reaction(emoji, user)
      def check(message):
        return message.author == payload.member and message.channel == message.channel and message.content.lower(
        ) == "close"

      try:
        em = discord.Embed(
            title="RandomDupes Tickets",
            description=
            "are you sure you want to close this ticket? Reply with `close` if you are sure.",
            color=0x00a8ff)

        await message.channel.send(embed=em)
        await client.wait_for('message', check=check)

        await message.channel.send('Ticket will close in 15 seconds.')

        await asyncio.sleep(15)

        await message.channel.delete()

        index = data["ticket-channel-ids"].index(payload.channel_id)
        del data["ticket-channel-ids"][index]

        with open('data.json', 'w') as f:
          json.dump(data, f)

      except asyncio.TimeoutError:
        await member.send('pp')

  if str(payload.emoji) == '📩' and (payload.message_id) == 862474024470970408:

      await client.wait_until_ready()

      with open("data.json") as f:
        data = json.load(f)
      
      ticket_number = int(data["ticket-counter"])
      ticket_number += 1

      category_channel = guild.get_channel(858587258454147105)
      ticket_channel = await category_channel.create_text_channel(
	    "ticket-{}".format(ticket_number))
      await ticket_channel.set_permissions(guild.get_role(guild.id),
                          send_messages=False,
                          read_messages=False)
     
      for role_id in data["valid-roles"]:
        role = guild.get_role(role_id)

        await ticket_channel.set_permissions(role,
                                            send_messages=True,
                                            read_messages=True,
                                            embed_links=True,
                                            attach_files=True,
                                            read_message_history=True,
                                            external_emojis=True)
                                          
      await ticket_channel.set_permissions(payload.member,
                                          send_messages=True,
                                          read_messages=True,
                                          add_reactions=True,
                                          embed_links=True,
                                          attach_files=True,
                                          read_message_history=True,
                                          external_emojis=True)

      staff_role = discord.utils.get(guild.roles, name="Support")

      pinged_msg_content = ""
      non_mentionable_roles = []

      if data["pinged-roles"] != []:

        for role_id in data["pinged-roles"]:
          role = payload.guild.get_role(role_id)

          pinged_msg_content += role.mention
          pinged_msg_content += " "

          if role.mentionable:
            pass
          else:
            await role.edit(mentionable=True)
            non_mentionable_roles.append(role)
        
        await ticket_channel.send(pinged_msg_content)

        for role in non_mentionable_roles:
          await role.edit(mentionable=False)

      data["ticket-channel-ids"].append(ticket_channel.id)

      data["ticket-counter"] = int(ticket_number)
      with open ("data.json", 'w') as f:
        json.dump(data, f)

      created_em = discord.Embed(
        title="RandomDupes Tickets",
        description="Your ticket has been created at {}".format(
          ticket_channel.mention),
        color=0x00a8ff)

      pp = guild.get_channel(payload.channel_id)

      await pp.send(embed=created_em, delete_after=10)

      await ticket_channel.send(
        f'{payload.member.mention}, please answer the following questions.'
      )

      await ticket_channel.send('-----------------------------------------------')

      channel = client.get_channel(payload.channel_id)
      message = await channel.fetch_message(payload.message_id)
      user = client.get_user(payload.user_id)
      emoji = "📩"
      await message.remove_reaction(emoji, user)


      def check(message):
        return message.channel == ticket_channel and message.author == payload.member

      a = discord.Embed(title="Question 1",
                        description=f"What server is your issue with?",
                        color=0x00a8ff)

      await ticket_channel.send(embed=a)

      question1 = await client.wait_for('message', check=check)

      b = discord.Embed(title="Question 2",
                        description=f"What is your IGN?",
                        color=0x00a8ff)

      await ticket_channel.send(embed=b)

      question2 = await client.wait_for('message', check=check)

      c = discord.Embed(title="Question 3",
                        description=f"Please explain your issue.",
                        color=0x00a8ff)

      await ticket_channel.send(embed=c)

      question3 = await client.wait_for('message', check=check)

      d = discord.Embed(title="Question 4",
                        description=f"Please provide any evidence, if applicable",
                        color=0x00a8ff)

      await ticket_channel.send(embed=d)

      question4 = await client.wait_for('message', check=check)

      staff_role = discord.utils.get(guild.roles, name="Support Team")
      staff_role2 = discord.utils.get(guild.roles, name="Staff Team")

      x = f'Support will be with you shortly.'

      em = discord.Embed(title="Responses:",
                        description=f"**Server**: {question1.content} \n**Name**: {question2.content}\n**Issue**: {question3.content} \n**Evidence**: {question4.content}",
                        color=0x00a8ff)
      
      msg = await ticket_channel.send(content=x, embed=em)

      await msg.add_reaction('🔒')

  if str(payload.emoji) == '<:AdminAbooz:862472131446439957>' and (payload.message_id) == 862474024470970408:

      await client.wait_until_ready()

      with open("data.json") as f:
        data = json.load(f)
      
      ticket_number = int(data["ticket-counter"])
      ticket_number += 1

      category_channel = guild.get_channel(858587258454147105)
      ticket_channel = await category_channel.create_text_channel(
	    "ticket-{}".format(ticket_number))
      await ticket_channel.set_permissions(guild.get_role(guild.id),
                          send_messages=False,
                          read_messages=False)
     
      for role_id in data["valid-roles"]:
        role = guild.get_role(role_id)

        await ticket_channel.set_permissions(role,
                                            send_messages=True,
                                            read_messages=True,
                                            embed_links=True,
                                            attach_files=True,
                                            read_message_history=True,
                                            external_emojis=True)
                                          
      await ticket_channel.set_permissions(payload.member,
                                          send_messages=True,
                                          read_messages=True,
                                          add_reactions=True,
                                          embed_links=True,
                                          attach_files=True,
                                          read_message_history=True,
                                          external_emojis=True)

      staff_role = discord.utils.get(guild.roles, name="Support")

      pinged_msg_content = ""
      non_mentionable_roles = []

      if data["pinged-roles"] != []:

        for role_id in data["pinged-roles"]:
          role = payload.guild.get_role(role_id)

          pinged_msg_content += role.mention
          pinged_msg_content += " "

          if role.mentionable:
            pass
          else:
            await role.edit(mentionable=True)
            non_mentionable_roles.append(role)
        
        await ticket_channel.send(pinged_msg_content)

        for role in non_mentionable_roles:
          await role.edit(mentionable=False)

      data["ticket-channel-ids"].append(ticket_channel.id)

      data["ticket-counter"] = int(ticket_number)
      with open ("data.json", 'w') as f:
        json.dump(data, f)

      created_em = discord.Embed(
        title="RandomNetwork Tickets",
        description="Your ticket has been created at {}".format(
          ticket_channel.mention),
        color=0x00a8ff)

      pp = guild.get_channel(payload.channel_id)

      await pp.send(embed=created_em, delete_after=10)

      await ticket_channel.send(
        f'{payload.member.mention}, please answer the following questions.'
      )

      await ticket_channel.send('-----------------------------------------------')

      channel = client.get_channel(payload.channel_id)
      message = await channel.fetch_message(payload.message_id)
      user = client.get_user(payload.user_id)
      emoji = "<:AdminAbooz:862472131446439957>"
      await message.remove_reaction(emoji, user)


      def check(message):
        return message.channel == ticket_channel and message.author == payload.member

      a = discord.Embed(title="Question 1",
                        description=f"What is your IGN?",
                        color=0x00a8ff)

      await ticket_channel.send(embed=a)

      question1 = await client.wait_for('message', check=check)

      b = discord.Embed(title="Question 2",
                        description=f"Why should you be unbanned/unmuted?",
                        color=0x00a8ff)

      await ticket_channel.send(embed=b)

      question2 = await client.wait_for('message', check=check)

      c = discord.Embed(title="Question 3",
                        description=f"Please provide any evidence, if applicable.",
                        color=0x00a8ff)

      await ticket_channel.send(embed=c)

      question3 = await client.wait_for('message', check=check)

      staff_role = discord.utils.get(guild.roles, name="Support Team")
      staff_role2 = discord.utils.get(guild.roles, name="Staff Team")

      x = f'Support will be with you shortly.'

      em = discord.Embed(title="Responses:",
                        description=f"**IGN**: {question1.content}\n**Reasoning**: {question2.content} \n**Evidence**: {question3.content}",
                        color=0x00a8ff)
      
      msg = await ticket_channel.send(content=x, embed=em)

      await msg.add_reaction('🔒')

  if str(payload.emoji) == '<a:BanHammer:862472442785300501>' and (payload.message_id) == 862474024470970408:

      await client.wait_until_ready()

      with open("data.json") as f:
        data = json.load(f)
      
      ticket_number = int(data["ticket-counter"])
      ticket_number += 1

      category_channel = guild.get_channel(858587258454147105)
      ticket_channel = await category_channel.create_text_channel(
	    "ticket-{}".format(ticket_number))
      await ticket_channel.set_permissions(guild.get_role(guild.id),
                          send_messages=False,
                          read_messages=False)
     
      for role_id in data["valid-roles"]:
        role = guild.get_role(role_id)

        await ticket_channel.set_permissions(role,
                                            send_messages=True,
                                            read_messages=True,
                                            embed_links=True,
                                            attach_files=True,
                                            read_message_history=True,
                                            external_emojis=True)
                                          
      await ticket_channel.set_permissions(payload.member,
                                          send_messages=True,
                                          read_messages=True,
                                          add_reactions=True,
                                          embed_links=True,
                                          attach_files=True,
                                          read_message_history=True,
                                          external_emojis=True)

      staff_role = discord.utils.get(guild.roles, name="Support")

      pinged_msg_content = ""
      non_mentionable_roles = []

      if data["pinged-roles"] != []:

        for role_id in data["pinged-roles"]:
          role = payload.guild.get_role(role_id)

          pinged_msg_content += role.mention
          pinged_msg_content += " "

          if role.mentionable:
            pass
          else:
            await role.edit(mentionable=True)
            non_mentionable_roles.append(role)
        
        await ticket_channel.send(pinged_msg_content)

        for role in non_mentionable_roles:
          await role.edit(mentionable=False)

      data["ticket-channel-ids"].append(ticket_channel.id)

      data["ticket-counter"] = int(ticket_number)
      with open ("data.json", 'w') as f:
        json.dump(data, f)

      created_em = discord.Embed(
        title="RandomNetwork Tickets",
        description="Your ticket has been created at {}".format(
          ticket_channel.mention),
        color=0x00a8ff)

      pp = guild.get_channel(payload.channel_id)

      await pp.send(embed=created_em, delete_after=10)

      await ticket_channel.send(
        f'{payload.member.mention}, please answer the following questions.'
      )

      await ticket_channel.send('-----------------------------------------------')

      channel = client.get_channel(payload.channel_id)
      message = await channel.fetch_message(payload.message_id)
      user = client.get_user(payload.user_id)
      emoji = "<a:BanHammer:862472442785300501>"
      await message.remove_reaction(emoji, user)


      def check(message):
        return message.channel == ticket_channel and message.author == payload.member

      a = discord.Embed(title="Question 1",
                        description=f"What is your IGN?",
                        color=0x00a8ff)

      await ticket_channel.send(embed=a)

      question1 = await client.wait_for('message', check=check)

      b = discord.Embed(title="Question 2",
                        description=f"Who are you reporting?",
                        color=0x00a8ff)

      await ticket_channel.send(embed=b)

      question2 = await client.wait_for('message', check=check)

      c = discord.Embed(title="Question 3",
                        description=f"Why should we punish this player?",
                        color=0x00a8ff)

      await ticket_channel.send(embed=c)

      question3 = await client.wait_for('message', check=check)

      d = discord.Embed(title="Question 4",
                        description=f"Please provide any evidence, if applicable.",
                        color=0x00a8ff)

      await ticket_channel.send(embed=d)

      question4 = await client.wait_for('message', check=check)

      staff_role = discord.utils.get(guild.roles, name="Support Team")
      staff_role2 = discord.utils.get(guild.roles, name="Staff Team")

      x = f'Support will be with you shortly.'

      em = discord.Embed(title="Responses:",
                        description=f"**IGN**: {question1.content}\n**Player**: {question2.content} \n**Reason**: {question3.content} \n**Evidence**: {question4.content}",
                        color=0x00a8ff)
      
      msg = await ticket_channel.send(content=x, embed=em)

      await msg.add_reaction('🔒')

  if str(payload.emoji) == '<a:GlitchCat:862472688396140586>' and (payload.message_id) == 862474024470970408:

      await client.wait_until_ready()

      with open("data.json") as f:
        data = json.load(f)
      
      ticket_number = int(data["ticket-counter"])
      ticket_number += 1

      category_channel = guild.get_channel(858587258454147105)
      ticket_channel = await category_channel.create_text_channel(
	    "ticket-{}".format(ticket_number))
      await ticket_channel.set_permissions(guild.get_role(guild.id),
                          send_messages=False,
                          read_messages=False)
     
      for role_id in data["valid-roles"]:
        role = guild.get_role(role_id)

        await ticket_channel.set_permissions(role,
                                            send_messages=True,
                                            read_messages=True,
                                            embed_links=True,
                                            attach_files=True,
                                            read_message_history=True,
                                            external_emojis=True)
                                          
      await ticket_channel.set_permissions(payload.member,
                                          send_messages=True,
                                          read_messages=True,
                                          add_reactions=True,
                                          embed_links=True,
                                          attach_files=True,
                                          read_message_history=True,
                                          external_emojis=True)

      staff_role = discord.utils.get(guild.roles, name="Support")

      pinged_msg_content = ""
      non_mentionable_roles = []

      if data["pinged-roles"] != []:

        for role_id in data["pinged-roles"]:
          role = payload.guild.get_role(role_id)

          pinged_msg_content += role.mention
          pinged_msg_content += " "

          if role.mentionable:
            pass
          else:
            await role.edit(mentionable=True)
            non_mentionable_roles.append(role)
        
        await ticket_channel.send(pinged_msg_content)

        for role in non_mentionable_roles:
          await role.edit(mentionable=False)

      data["ticket-channel-ids"].append(ticket_channel.id)

      data["ticket-counter"] = int(ticket_number)
      with open ("data.json", 'w') as f:
        json.dump(data, f)

      created_em = discord.Embed(
        title="RandomNetwork Tickets",
        description="Your ticket has been created at {}".format(
          ticket_channel.mention),
        color=0x00a8ff)

      pp = guild.get_channel(payload.channel_id)

      await pp.send(embed=created_em, delete_after=10)

      await ticket_channel.send(
        f'{payload.member.mention}, please answer the following questions.'
      )

      await ticket_channel.send('-----------------------------------------------')

      channel = client.get_channel(payload.channel_id)
      message = await channel.fetch_message(payload.message_id)
      user = client.get_user(payload.user_id)
      emoji = "<a:GlitchCat:862472688396140586>"
      await message.remove_reaction(emoji, user)


      def check(message):
        return message.channel == ticket_channel and message.author == payload.member

      a = discord.Embed(title="Question 1",
                        description=f"What is your IGN?",
                        color=0x00a8ff)

      await ticket_channel.send(embed=a)

      question1 = await client.wait_for('message', check=check)

      b = discord.Embed(title="Question 2",
                        description=f"What server is the bug from?",
                        color=0x00a8ff)

      await ticket_channel.send(embed=b)

      question2 = await client.wait_for('message', check=check)

      staff_role = discord.utils.get(guild.roles, name="Support Team")
      staff_role2 = discord.utils.get(guild.roles, name="Staff Team")

      x = f'Support will be with you shortly.'

      em = discord.Embed(title="Responses:",
                        description=f"**IGN**: {question1.content}\n**Bug**: {question2.content}",
                        color=0x00a8ff)
      
      msg = await ticket_channel.send(content=x, embed=em)

      await msg.add_reaction('🔒')

  if str(payload.emoji) == '<:Money:862472891462451201>' and (payload.message_id) == 862474024470970408:

      await client.wait_until_ready()

      with open("data.json") as f:
        data = json.load(f)
      
      ticket_number = int(data["ticket-counter"])
      ticket_number += 1

      category_channel = guild.get_channel(858587258454147105)
      ticket_channel = await category_channel.create_text_channel(
	    "ticket-{}".format(ticket_number))
      await ticket_channel.set_permissions(guild.get_role(guild.id),
                          send_messages=False,
                          read_messages=False)
     
      for role_id in data["valid-roles"]:
        role = guild.get_role(role_id)

        await ticket_channel.set_permissions(role,
                                            send_messages=True,
                                            read_messages=True,
                                            embed_links=True,
                                            attach_files=True,
                                            read_message_history=True,
                                            external_emojis=True)
                                          
      await ticket_channel.set_permissions(payload.member,
                                          send_messages=True,
                                          read_messages=True,
                                          add_reactions=True,
                                          embed_links=True,
                                          attach_files=True,
                                          read_message_history=True,
                                          external_emojis=True)

      staff_role = discord.utils.get(guild.roles, name="Support")

      pinged_msg_content = ""
      non_mentionable_roles = []

      if data["pinged-roles"] != []:

        for role_id in data["pinged-roles"]:
          role = payload.guild.get_role(role_id)

          pinged_msg_content += role.mention
          pinged_msg_content += " "

          if role.mentionable:
            pass
          else:
            await role.edit(mentionable=True)
            non_mentionable_roles.append(role)
        
        await ticket_channel.send(pinged_msg_content)

        for role in non_mentionable_roles:
          await role.edit(mentionable=False)

      data["ticket-channel-ids"].append(ticket_channel.id)

      data["ticket-counter"] = int(ticket_number)
      with open ("data.json", 'w') as f:
        json.dump(data, f)

      created_em = discord.Embed(
        title="RandomNetwork Tickets",
        description="Your ticket has been created at {}".format(
          ticket_channel.mention),
        color=0x00a8ff)

      pp = guild.get_channel(payload.channel_id)

      await pp.send(embed=created_em, delete_after=10)

      await ticket_channel.send(
        f'{payload.member.mention}, please answer the following questions.'
      )

      await ticket_channel.send('-----------------------------------------------')

      channel = client.get_channel(payload.channel_id)
      message = await channel.fetch_message(payload.message_id)
      user = client.get_user(payload.user_id)
      emoji = "<:Money:862472891462451201>"
      await message.remove_reaction(emoji, user)


      def check(message):
        return message.channel == ticket_channel and message.author == payload.member

      a = discord.Embed(title="Question 1",
                        description=f"What is your IGN?",
                        color=0x00a8ff)

      await ticket_channel.send(embed=a)

      question1 = await client.wait_for('message', check=check)

      b = discord.Embed(title="Question 2",
                        description=f"What did you purchase?",
                        color=0x00a8ff)

      await ticket_channel.send(embed=b)

      question2 = await client.wait_for('message', check=check)

      c = discord.Embed(title="Question 3",
                        description=f"What issue are you facing?",
                        color=0x00a8ff)

      await ticket_channel.send(embed=c)

      question3 = await client.wait_for('message', check=check)

      staff_role = discord.utils.get(guild.roles, name="Support Team")
      staff_role2 = discord.utils.get(guild.roles, name="Staff Team")

      x = f'Support will be with you shortly.'

      em = discord.Embed(title="Responses:",
                        description=f"**IGN**: {question1.content}\n**Purchase**: {question2.content} \n**Issue**: {question3.content}",
                        color=0x00a8ff)
      
      msg = await ticket_channel.send(content=x, embed=em)

      await msg.add_reaction('🔒')

  if str(payload.emoji) == '<a:Hmmm:862473071679635456>' and (payload.message_id) == 862474024470970408:

      await client.wait_until_ready()

      with open("data.json") as f:
        data = json.load(f)
      
      ticket_number = int(data["ticket-counter"])
      ticket_number += 1

      category_channel = guild.get_channel(858587258454147105)
      ticket_channel = await category_channel.create_text_channel(
	    "ticket-{}".format(ticket_number))
      await ticket_channel.set_permissions(guild.get_role(guild.id),
                          send_messages=False,
                          read_messages=False)
     
      for role_id in data["valid-roles"]:
        role = guild.get_role(role_id)

        await ticket_channel.set_permissions(role,
                                            send_messages=True,
                                            read_messages=True,
                                            embed_links=True,
                                            attach_files=True,
                                            read_message_history=True,
                                            external_emojis=True)
                                          
      await ticket_channel.set_permissions(payload.member,
                                          send_messages=True,
                                          read_messages=True,
                                          add_reactions=True,
                                          embed_links=True,
                                          attach_files=True,
                                          read_message_history=True,
                                          external_emojis=True)

      staff_role = discord.utils.get(guild.roles, name="Support")

      pinged_msg_content = ""
      non_mentionable_roles = []

      if data["pinged-roles"] != []:

        for role_id in data["pinged-roles"]:
          role = payload.guild.get_role(role_id)

          pinged_msg_content += role.mention
          pinged_msg_content += " "

          if role.mentionable:
            pass
          else:
            await role.edit(mentionable=True)
            non_mentionable_roles.append(role)
        
        await ticket_channel.send(pinged_msg_content)

        for role in non_mentionable_roles:
          await role.edit(mentionable=False)

      data["ticket-channel-ids"].append(ticket_channel.id)

      data["ticket-counter"] = int(ticket_number)
      with open ("data.json", 'w') as f:
        json.dump(data, f)

      created_em = discord.Embed(
        title="RandomNetwork Tickets",
        description="Your ticket has been created at {}".format(
          ticket_channel.mention),
        color=0x00a8ff)

      pp = guild.get_channel(payload.channel_id)

      await pp.send(embed=created_em, delete_after=10)

      await ticket_channel.send(
        f'{payload.member.mention}, please answer the following questions.'
      )

      await ticket_channel.send('-----------------------------------------------')

      channel = client.get_channel(payload.channel_id)
      message = await channel.fetch_message(payload.message_id)
      user = client.get_user(payload.user_id)
      emoji = "<a:Hmmm:862473071679635456>"
      await message.remove_reaction(emoji, user)


      def check(message):
        return message.channel == ticket_channel and message.author == payload.member

      a = discord.Embed(title="Question 1",
                        description=f"What is your IGN?",
                        color=0x00a8ff)

      await ticket_channel.send(embed=a)

      question1 = await client.wait_for('message', check=check)

      b = discord.Embed(title="Question 2",
                        description=f"Please give us a description on why you made this ticket.",
                        color=0x00a8ff)

      await ticket_channel.send(embed=b)

      question2 = await client.wait_for('message', check=check)

      staff_role = discord.utils.get(guild.roles, name="Support Team")
      staff_role2 = discord.utils.get(guild.roles, name="Staff Team")

      x = f'Support will be with you shortly.'

      em = discord.Embed(title="Responses:",
                        description=f"**IGN**: {question1.content}\n**Issue**: {question2.content}",
                        color=0x00a8ff)
      
      msg = await ticket_channel.send(content=x, embed=em)

      await msg.add_reaction('🔒')

@client.event
async def on_message(message):
    randomnetwork = client.get_guild(774501063557382155)
    verifychannel = client.get_channel(836708196945100820)
    suggestionchannel = client.get_channel(819426954356326430)
    notificationchannel = client.get_channel(846199910273253407)
    prefixes = ["!","@","#","$","%","^","&","*","/","~"]  
    if message.content.startswith("prefix"):
      await message.channel.send("My Prefix Is: **#**")
    for prefix in prefixes:
        if message.content.startswith(prefix + "prefix"):
            await message.channel.send("My Prefix Is: **.**")
    if not message.content.startswith(".suggest") and (message.channel == suggestionchannel) and (message.author.id != 503641822141349888) and (message.author.id != 824521210053918730) and (message.author.id != 814507814407110698):
      await message.delete()
      embed=discord.Embed(title="Suggestion Error", url="", 
      description="You can only type `.suggest {suggestion}` here!", 
      color=discord.Color.red())
      await message.author.send(embed=embed)
    await client.process_commands(message)

@client.command()
async def suggest(ctx, *, description):
	await ctx.message.delete()
	embed = discord.Embed(
	    title='Suggestion',
	    description=
	    f'{description}',
	    color=discord.Color.purple())
	time = datetime.now(tz=pytz.timezone('America/Denver'))
	formatted = time.strftime("%m/%d/%y")
	embed.set_footer(text=f"RandomDupes • " + formatted)
	embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
	suggestionchannel = ctx.guild.get_channel(819426954356326430)
	msg = await suggestionchannel.send(embed=embed)
	await msg.add_reaction('👍')
	await msg.add_reaction('🤷‍♂️')
	await msg.add_reaction('👎')
	embed = discord.Embed(
	    title='Suggestions Success',
	    description=
	    f'Thank you for your suggestion! It has been added in <#819426954356326430>, please wait for it to be accepted/denied.',
	    color=discord.Color.green())
	msg = await ctx.author.send(embed=embed)
    
@client.command()
async def unmute(ctx, member : discord.Member = None, *, reason=None):
    authorperms = ctx.author.permissions_in(ctx.channel)
    await ctx.message.delete()
    if authorperms.manage_roles:
        role = discord.utils.get(ctx.guild.roles, name='Muted')
        if member == None:
            await ctx.send("Please specify who you want to unmute!")
        if member != None:
            embed = discord.Embed(
                title=f'{member} Was Unmuted',
                description=f'{member.mention} Has Been Unmuted',
                colour= discord.Colour.blurple()
            )
            embed.add_field(name='Reason:', value=f'{reason}', inline=True)
            embed.set_thumbnail(url='')

            embed.add_field(name='Unmuted by:', value=f'{ctx.author.mention}')
            await ctx.send(embed=embed)
            role = discord.utils.get(ctx.guild.roles, name='Muted')
            await member.remove_roles(role)
            role1 = discord.utils.get(ctx.guild.roles, name='Member')
            await member.add_roles(role1)
    else:
        if authorperms.manage_roles:
            pass
        else:
            await ctx.message.delete()
            await ctx.send(f"**{ctx.author.mention} you don't have the permissions to do that!**")

@client.command()
async def mute(ctx, member : discord.Member = None, *, reason=None):
    authorperms = ctx.author.permissions_in(ctx.channel)
    await ctx.message.delete()
    if authorperms.manage_roles:
        if member == None:
            await ctx.send("Please specify who you want to mute!")
        if member != None:
            embed = discord.Embed(
                title=f'{member} Was Muted',
                description=f'{member.mention} Has Been Muted!',
                colour= discord.Colour.blurple()
            )
            embed.add_field(name='Reason:', value=f'{reason}', inline=True)
            embed.set_thumbnail(url='')

            embed.add_field(name='Muted By:', value=f'{ctx.author.mention}')
            await ctx.send(embed=embed)
            role = discord.utils.get(ctx.guild.roles, name='Muted')
            await member.add_roles(role)
            role1 = discord.utils.get(ctx.guild.roles, name='Member')
            await member.remove_roles(role1)
    else:
        if authorperms.manage_roles:
            pass
        else:
            await ctx.message.delete()
            await ctx.send(f"**{ctx.author.mention} you don't have the permissions to do that!**")
            
@client.command()
async def sm(ctx, seconds: int):
  await ctx.channel.edit(slowmode_delay=seconds)
  await ctx.send(f"Set the slowmode delay in this channel to **{seconds}** seconds!")
  await ctx.message.delete()

@client.command(aliases=["remove","delete","bad"])
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="No Reason Provided"):

  try:
	  embed=discord.Embed(title="Bans", url="",
	  description=f"You've been banned in **{ctx.guild.name}** \nBy: **{ctx.author.mention}** \nFor: **{reason}**",
	  color=discord.Color.red())
	  await member.send(embed=embed)
	  await ctx.message.delete()

	  embed=discord.Embed(title="Banned", url="",
	  description=f"**{member.mention}** has been banned. \nBy: **{ctx.author.mention}** \nFor: **{reason}**",
	  color=discord.Color.red())
	  await ctx.channel.send(embed=embed)
	  await member.ban(reason=reason)

  except Exception:

    await ctx.message.delete()
    embed=discord.Embed(title="Banned", url="", description=f"**{member.mention}** has been banned. \nBy: **{ctx.author.mention}** \nFor: **{reason}**",
    color=discord.Color.red())
    await ctx.channel.send(embed=embed)
    await member.ban(reason=reason)

@ban.error
async def ban_error(ctx, error):
  if isinstance(error, commands.MissingPermissions):
    await ctx.send("Hey, {}! You cannot do that!".format(ctx.author.mention), delete_after=10)

@commands.has_permissions(kick_members=True)
@client.command()
async def kick(ctx, user: discord.Member, *, reason="No reason provided"):
  try:
	  kick = discord.Embed(
	      title=f"**Kicked** {user.name}!",
	      description=f"Reason: {reason}\nBy: {ctx.author.mention}")
	  await user.send(embed=kick)
	  await ctx.message.delete()
	  await ctx.channel.send(embed=kick)
	  await user.kick(reason=reason)
    
  except Exception:
	  kick = discord.Embed(
	      title=f"**Kicked** {user.name}!",
	      description=f"Reason: {reason}\nBy: {ctx.author.mention}")
	  await ctx.message.delete()
	  await ctx.channel.send(embed=kick)
	  await user.kick(reason=reason)

@kick.error
async def kick_error(ctx, error):
  if isinstance(error, commands.MissingPermissions):
    await ctx.send("Hey, {}! You cannot do that!".format(ctx.author.mention), delete_after=10)

@client.command(pass_context=True)
@commands.has_permissions(manage_messages=True)
async def clean(ctx, limit: int):
    await ctx.channel.purge(limit=limit+1)
    await ctx.send('Cleared By: {}'.format(ctx.author.mention), delete_after=2)

@clean.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You cannot do that!")

    if isinstance(error, commands.MissingRequiredArgument):
      await ctx.message.delete()
      await ctx.send(f"Hey {ctx.author.mention}, please put an argument (number)R to remove messages! \n \n*Example:* **.clean 5** `(Removes 5 Messages)`", delete_after=10)

@client.command()
async def help(ctx):
    try:
        embed = discord.Embed(title="Random Staff Help", url="", description="[Global Commands](https://docs.google.com/document/d/1Nre6i8VU9nmdQSyIZfJF-lZxk0sHjwutdlbUutp70Mc/edit?usp=sharing) \n \n[Staff Commands](https://docs.google.com/document/d/1Q2Ma-lHaMmEO1TlY1pgIhlTQt-2qlZddlLYwpmRUa74/edit?usp=sharing)", color=discord.Color.green())
        await ctx.message.delete()
        await ctx.author.send(embed=embed)
        await ctx.send(f'{ctx.author.mention}, You have mail!', delete_after=10)
    except Exception:
        await ctx.send("**Error**! Your PMs Are Closed!", delete_after=10)

@client.command()
@commands.cooldown(1, 30, commands.BucketType.user)
async def new(ctx, *, args=None):

	await client.wait_until_ready()

	if args == None:
		message_content = "Please be patient while I ask a few questions."

	else:
		message_content = "".join(args)

	with open("data.json") as f:
		data = json.load(f)

	ticket_number = int(data["ticket-counter"])
	ticket_number += 1

	category_channel = ctx.guild.get_channel(831416170619600927)
	ticket_channel = await category_channel.create_text_channel(
	    "ticket-{}".format(ticket_number))
	await ticket_channel.set_permissions(ctx.guild.get_role(ctx.guild.id),
	                                     send_messages=False,
	                                     read_messages=False)

	for role_id in data["valid-roles"]:
		role = ctx.guild.get_role(role_id)

		await ticket_channel.set_permissions(role,
		                                     send_messages=True,
		                                     read_messages=True,
		                                     add_reactions=True,
		                                     embed_links=True,
		                                     attach_files=True,
		                                     read_message_history=True,
		                                     external_emojis=True)

	await ticket_channel.set_permissions(ctx.author,
	                                     send_messages=True,
	                                     read_messages=True,
	                                     add_reactions=True,
	                                     embed_links=True,
	                                     attach_files=True,
	                                     read_message_history=True,
	                                     external_emojis=True)

	staff_role = discord.utils.get(ctx.guild.roles, name="Support")

	pinged_msg_content = ""
	non_mentionable_roles = []

	if data["pinged-roles"] != []:

		for role_id in data["pinged-roles"]:
			role = ctx.guild.get_role(role_id)

			pinged_msg_content += role.mention
			pinged_msg_content += " "

			if role.mentionable:
				pass
			else:
				await role.edit(mentionable=True)
				non_mentionable_roles.append(role)

		await ticket_channel.send(pinged_msg_content)

		for role in non_mentionable_roles:
			await role.edit(mentionable=False)

	data["ticket-channel-ids"].append(ticket_channel.id)

	data["ticket-counter"] = int(ticket_number)
	with open("data.json", 'w') as f:
		json.dump(data, f)

	created_em = discord.Embed(
	    title="RandomNetwork Tickets",
	    description="Your ticket has been created at {}".format(
	        ticket_channel.mention),
	    color=0x00a8ff)
    
	await ctx.send(embed=created_em, delete_after=10)
	await ctx.message.delete()
	await ticket_channel.send(
	    f'{ctx.author.mention}, please answer the following questions.'
	)

	await ticket_channel.send('-----------------------------------------------')

	def check (message):
		return message.channel == ticket_channel and message.author == ctx.author

	a = discord.Embed(title="Question 1",
	                   description=f"What is your IGN (In Game Name)?",
	                   color=0x00a8ff)

	await ticket_channel.send(embed=a)

	question1 = await client.wait_for('message', check=check)
	
	b = discord.Embed(title="Question 2",
	                   description=f"What server do you need help with?",
	                   color=0x00a8ff)

	await ticket_channel.send(embed=b)

	question2 = await client.wait_for('message', check=check)

	c = discord.Embed(title="Question 3",
	                   description=f"How may we help you today?",
	                   color=0x00a8ff)

	await ticket_channel.send(embed=c)

	question3 = await client.wait_for('message', check=check)

	em = discord.Embed(title="Responses:",
	                   description=f"IGN: {question1.content} \nServer: {question2.content}\nQuestion: {question3.content}",
	                   color=0x00a8ff)

	await ticket_channel.send(embed=em)

	staff_role = discord.utils.get(ctx.guild.roles, name="Support")

	await ticket_channel.send(f'Support will be with you shortly. \n \n||Tags: {staff_role.mention}||')

@client.command()
async def close(ctx):
	with open('data.json') as f:
		data = json.load(f)

	if ctx.channel.id in data["ticket-channel-ids"]:

		channel_id = ctx.channel.id

		await ctx.message.delete()
		
		def check(message):
			return message.author == ctx.author and message.channel == ctx.channel and message.content.lower(
			) == "close"

		try:
			em = discord.Embed(
			    title="RandomNetwork Tickets",
			    description=
			    "Are you sure you want to close this ticket? Reply with `close` if you are sure.",
			    color=0x00a8ff)

			await ctx.send(embed=em)
			await client.wait_for('message', check=check, timeout=60)

			await ctx.send('Ticket will close in 15 seconds.', mention_author=False)

			await asyncio.sleep(15)

			await ctx.channel.delete()

			index = data["ticket-channel-ids"].index(channel_id)
			del data["ticket-channel-ids"][index]

			with open('data.json', 'w') as f:
				json.dump(data, f)

		except asyncio.TimeoutError:
			em = discord.Embed(
			    title="RandomNetwork Tickets",
			    description=
			    "You have run out of time to close this ticket. Please run the command again.",
			    color=0x00a8ff)
			await ctx.send(embed=em)

@client.command()
@has_permissions(administrator=True)
async def forceclose(ctx):
	with open('data.json') as f:
		data = json.load(f)

	if ctx.channel.id in data["ticket-channel-ids"]:

		channel_id = ctx.channel.id

		await ctx.message.delete()

		ticketlog_channel = ctx.guild.get_channel(841111507559383100)
      
		em = discord.Embed(title="Ticket Logs (Force)",
	                   description=f"",
	                   color=0x00a8ff)
		em.add_field(name="Force Closer", value=f"{ctx.author.mention}", inline=True)
		em.add_field(name="Ticket", value=f"{ctx.channel.name}", inline=True)
		time = datetime.now(tz=pytz.timezone('America/Denver'))
		formatted = time.strftime("%m/%d/%y, %I:%M %p")
		em.set_footer(text=formatted)

		await ticketlog_channel.send(embed=em)

		await ctx.channel.delete()

		index = data["ticket-channel-ids"].index(channel_id)
		del data["ticket-channel-ids"][index]

		with open('data.json', 'w') as f:
			json.dump(data, f)

@client.command()
async def addaccess(ctx, role_id=None):

	with open('data.json') as f:
		data = json.load(f)

	valid_user = False

	for role_id in data["verified-roles"]:
		try:
			if ctx.guild.get_role(role_id) in ctx.author.roles:
				valid_user = True
		except:
			pass

	if valid_user or ctx.author.guild_permissions.administrator:
		role_id = int(role_id)

		if role_id not in data["valid-roles"]:

			try:
				role = ctx.guild.get_role(role_id)

				with open("data.json") as f:
					data = json.load(f)

				data["valid-roles"].append(role_id)

				with open('data.json', 'w') as f:
					json.dump(data, f)

				em = discord.Embed(
				    title="RandomNetwork tickets",
				    description=
				    "You have successfully added `{}` to the list of roles with access to tickets."
				    .format(role.name),
				    color=0x00a8ff)

				await ctx.send(embed=em)

			except:
				em = discord.Embed(
				    title="RandomNetwork Tickets",
				    description=
				    "That isn't a valid role ID. Please try again with a valid role ID."
				)
				await ctx.send(embed=em)

		else:
			em = discord.Embed(
			    title="RandomNetwork Tickets",
			    description="That role already has access to tickets!",
			    color=0x00a8ff)
			await ctx.send(embed=em)

	else:
		em = discord.Embed(
		    title="RandomNetwork Tickets",
		    description="Sorry, you don't have permission to run that command.",
		    color=0x00a8ff)
		await ctx.send(embed=em)


@client.command()
async def delaccess(ctx, role_id=None):
	with open('data.json') as f:
		data = json.load(f)

	valid_user = False

	for role_id in data["verified-roles"]:
		try:
			if ctx.guild.get_role(role_id) in ctx.author.roles:
				valid_user = True
		except:
			pass

	if valid_user or ctx.author.guild_permissions.administrator:

		try:
			role_id = int(role_id)
			role = ctx.guild.get_role(role_id)

			with open("data.json") as f:
				data = json.load(f)

			valid_roles = data["valid-roles"]

			if role_id in valid_roles:
				index = valid_roles.index(role_id)

				del valid_roles[index]

				data["valid-roles"] = valid_roles

				with open('data.json', 'w') as f:
					json.dump(data, f)

				em = discord.Embed(
				    title="RandomNetwork Tickets",
				    description=
				    "You have successfully removed `{}` from the list of roles with access to tickets."
				    .format(role.name),
				    color=0x00a8ff)

				await ctx.send(embed=em)

			else:

				em = discord.Embed(
				    title="RandomNetwork Tickets",
				    description=
				    "That role already doesn't have access to tickets!",
				    color=0x00a8ff)
				await ctx.send(embed=em)

		except:
			em = discord.Embed(
			    title="RandomNetwork Tickets",
			    description=
			    "That isn't a valid role ID. Please try again with a valid role ID."
			)
			await ctx.send(embed=em)

	else:
		em = discord.Embed(
		    title="RandomNetwork Tickets",
		    description="Sorry, you don't have permission to run that command.",
		    color=0x00a8ff)
		await ctx.send(embed=em)


@client.command()
async def addpingedrole(ctx, role_id=None):

	with open('data.json') as f:
		data = json.load(f)

	valid_user = False

	for role_id in data["verified-roles"]:
		try:
			if ctx.guild.get_role(role_id) in ctx.author.roles:
				valid_user = True
		except:
			pass

	if valid_user or ctx.author.guild_permissions.administrator:

		role_id = int(role_id)

		if role_id not in data["pinged-roles"]:

			try:
				role = ctx.guild.get_role(role_id)

				with open("data.json") as f:
					data = json.load(f)

				data["pinged-roles"].append(role_id)

				with open('data.json', 'w') as f:
					json.dump(data, f)

				em = discord.Embed(
				    title="RandomNetwork Tickets",
				    description=
				    "You have successfully added `{}` to the list of roles that get pinged when new tickets are created!"
				    .format(role.name),
				    color=0x00a8ff)

				await ctx.send(embed=em)

			except:
				em = discord.Embed(
				    title="RandomNetwork Tickets",
				    description=
				    "That isn't a valid role ID. Please try again with a valid role ID."
				)
				await ctx.send(embed=em)

		else:
			em = discord.Embed(
			    title="RandomNetwork Tickets",
			    description=
			    "That role already receives pings when tickets are created.",
			    color=0x00a8ff)
			await ctx.send(embed=em)

	else:
		em = discord.Embed(
		    title="RandomNetwork Tickets",
		    description="Sorry, you don't have permission to run that command.",
		    color=0x00a8ff)
		await ctx.send(embed=em)


@client.command()
async def delpingedrole(ctx, role_id=None):

	with open('data.json') as f:
		data = json.load(f)

	valid_user = False

	for role_id in data["verified-roles"]:
		try:
			if ctx.guild.get_role(role_id) in ctx.author.roles:
				valid_user = True
		except:
			pass

	if valid_user or ctx.author.guild_permissions.administrator:

		try:
			role_id = int(role_id)
			role = ctx.guild.get_role(role_id)

			with open("data.json") as f:
				data = json.load(f)

			pinged_roles = data["pinged-roles"]

			if role_id in pinged_roles:
				index = pinged_roles.index(role_id)

				del pinged_roles[index]

				data["pinged-roles"] = pinged_roles

				with open('data.json', 'w') as f:
					json.dump(data, f)

				em = discord.Embed(
				    title="RandomNetwork Tickets",
				    description=
				    "You have successfully removed `{}` from the list of roles that get pinged when new tickets are created."
				    .format(role.name),
				    color=0x00a8ff)
				await ctx.send(embed=em)

			else:
				em = discord.Embed(
				    title="RandomNetwork Tickets",
				    description=
				    "That role already isn't getting pinged when new tickets are created!",
				    color=0x00a8ff)
				await ctx.send(embed=em)

		except:
			em = discord.Embed(
			    title="RandomNetwork Tickets",
			    description=
			    "That isn't a valid role ID. Please try again with a valid role ID."
			)
			await ctx.send(embed=em)

	else:
		em = discord.Embed(
		    title="RandomNetwork Tickets",
		    description="Sorry, you don't have permission to run that command.",
		    color=0x00a8ff)
		await ctx.send(embed=em)


@client.command()
@has_permissions(administrator=True)
async def addadminrole(ctx, role_id=None):

	try:
		role_id = int(role_id)
		role = ctx.guild.get_role(role_id)

		with open("data.json") as f:
			data = json.load(f)

		data["verified-roles"].append(role_id)

		with open('data.json', 'w') as f:
			json.dump(data, f)

		em = discord.Embed(
		    title="RandomNetwork Tickets",
		    description=
		    "You have successfully added `{}` to the list of roles that can run admin-level commands!"
		    .format(role.name),
		    color=0x00a8ff)
		await ctx.send(embed=em)

	except:
		em = discord.Embed(
		    title="RandomNetwork Tickets",
		    description=
		    "That isn't a valid role ID. Please try again with a valid role ID."
		)
		await ctx.send(embed=em)


@client.command()
@has_permissions(administrator=True)
async def deladminrole(ctx, role_id=None):
	try:
		role_id = int(role_id)
		role = ctx.guild.get_role(role_id)

		with open("data.json") as f:
			data = json.load(f)

		admin_roles = data["verified-roles"]

		if role_id in admin_roles:
			index = admin_roles.index(role_id)

			del admin_roles[index]

			data["verified-roles"] = admin_roles

			with open('data.json', 'w') as f:
				json.dump(data, f)

			em = discord.Embed(
			    title="RandomNetwork Tickets",
			    description=
			    "You have successfully removed `{}` from the list of roles that get pinged when new tickets are created."
			    .format(role.name),
			    color=0x00a8ff)

			await ctx.send(embed=em)

		else:
			em = discord.Embed(
			    title="RandomNetwork Tickets",
			    description=
			    "That role isn't getting pinged when new tickets are created!",
			    color=0x00a8ff)
			await ctx.send(embed=em)

	except:
		em = discord.Embed(
		    title="RandomNetwork Tickets",
		    description=
		    "That isn't a valid role ID. Please try again with a valid role ID."
		)
		await ctx.send(embed=em)

@client.command()
@has_permissions(administrator=True)
async def resolved(ctx):
	embed = discord.Embed(
	    title='Resolved?',
	    description=
	    f'If the ticket is resolved, please type `.close` and follow those steps.',
	    color=discord.Color.green())
	await ctx.channel.send(embed=embed)
	await ctx.message.delete()
    
@client.command()
@has_permissions(manage_nicknames=True)
async def warn(ctx, member : discord.Member = None, *, reason=None):
  if member is None:
    await ctx.message.delete()
    embed=discord.Embed(title="Warning Error", url="", 
    description=f"{ctx.author.mention}, \n \nYou can't warn nothing! Please mention a user!", 
    color=discord.Color.red())
    embed.set_footer(text="Ex: .warn @Someone Spamming")
    await ctx.channel.send(embed=embed, delete_after=10)
    return
  if reason is None:
    await ctx.message.delete()
    embed=discord.Embed(title="Warning Error", url="", 
    description=f"{ctx.author.mention}, \n \nPlease state a reason to your warning!", 
    color=discord.Color.red())
    embed.set_footer(text="Ex: .warn @Someone Spamming")
    await ctx.channel.send(embed=embed, delete_after=10)
    return
  warnchannel = client.get_channel(858639477416263681)
  embed=discord.Embed(title="Warnings", url="", 
  description=f"**{member.mention}** has been warned! \n \nReason: **{reason}** \n \nBy: **{ctx.author.mention}**", 
  color=discord.Color.purple())
  await warnchannel.send(embed=embed)
  embed=discord.Embed(title="Warnings", url="", 
  description=f"You have been warned in **{ctx.guild.name}**! \n \n**Reason**: {reason} \n \n**By**: {ctx.author.mention}", 
  color=discord.Color.red())
  await member.send(embed=embed)
  await ctx.message.delete()

@warn.error
async def warn_error(ctx, error):
  if isinstance(error, commands.MemberNotFound):
    embed=discord.Embed(title="Warnings Error", url="", 
    description=f"{ctx.author.mention}, \nThat member is not found. Please try again!", 
    color=discord.Color.red())
    await ctx.channel.send(embed=embed, delete_after=10)
    await ctx.message.delete()

@client.command()
@has_permissions(administrator=True)
async def gcreate(ctx, time=None, *, prize=None):
    if time == None:
        return await ctx.send('Please include a time!')
    elif prize == None:
        return await ctx.send('Please include a prize!')
    await ctx.message.delete()
    embed = discord.Embed(title='New Giveaway', description=f'{ctx.author.mention} is giving away **{prize}**!')
    time_convert = {"s":1, "m":60, "h":3600, "d": 86400}
    gawtime = int(time[0]) * time_convert[time[-1]]
    embed.set_footer(text=f'Giveaway ends in {time}')
    gaw_msg = await ctx.send(embed = embed)
    await gaw_msg.add_reaction("🎉")
    await asyncio.sleep(gawtime)
    new_gaw_msg = await ctx.channel.fetch_message(gaw_msg.id)
    gaw_msg.reactions
    users = await new_gaw_msg.reactions[0].users().flatten()
    users.pop(users.index(client.user))
    winner = random.choice(users)
    await ctx.send(f"{winner.mention} has won the giveaway for {prize}! GG")
    
@client.command()
async def invites(ctx):
    totalInvites = 0
    for i in await ctx.guild.invites():
        if i.inviter == ctx.author:
            totalInvites += i.uses
    await ctx.send(f"{ctx.author.mention}, you've invited **{totalInvites} member{'' if totalInvites == 1 else 's'}** to the server!")
    await ctx.message.delete()

@client.command()
async def info(ctx):
  await ctx.message.delete()
  embed=discord.Embed(title="RandomNetwork Info", url="", 
  description=f"[Global Information](https://docs.google.com/document/d/18LBu3Lj3qtmNsMg5dXDKBiA903FXep88Hj86eivuiiE/edit?usp=sharing)", 
  color=discord.Color.purple())
  await ctx.author.send(embed=embed)
  await ctx.send(f"{ctx.author.mention}, you've gotten mail!", delete_after=10)

@client.command()
@has_permissions(administrator=True)
async def tickets(ctx):
  await ctx.message.delete()
  embed=discord.Embed(title="Support Tickets", url="", 
  description=f"For support on the network, please type `.new`, this will create a support channel for you.", 
  color=discord.Color.green())
  await ctx.channel.send(embed=embed)
  embed=discord.Embed(title="Appeal Tickets", url="", 
  description=f"For a punishment appeal, please type `.appeal`, this will create an appeal channel for you.", 
  color=discord.Color.red())
  await ctx.channel.send(embed=embed)
  embed=discord.Embed(title="Rank Claiming", url="", 
  description=f"To claim a previous rank, type `.claim` this will create a rank claiming ticket for you.", 
  color=discord.Color.purple())
  await ctx.channel.send(embed=embed)

@client.command(aliases=['rank'])
async def level(ctx, member: discord.Member = None):
    if not member:
        id = ctx.message.author.id
        with open('users.json', 'r') as f:
            users = json.load(f)
        lvl = users[str(id)]['level']
        await ctx.send(f'You are at level {lvl}!')
    else:
        id = member.id
        with open('users.json', 'r') as f:
            users = json.load(f)
        lvl = users[str(id)]['level']
        await ctx.send(f'{member} is at level {lvl}!')

@client.command(aliases=['av'])
async def avatar(ctx, member:discord.Member=None):
	if member is None:
		await ctx.send(ctx.author.avatar_url)
		await ctx.message.delete()
	else:
		await ctx.send(member.avatar_url)
		await ctx.message.delete()

@client.command()
async def notifications(ctx):
  embed=discord.Embed(title="Notifications", url="", 
  description=f"**__Adding__** \n \nFor **Poll** notifications, type `!polls`. \nFor **Giveaway** notifications, type `!giveaways`. \nFor **Spoiler** notifications, type `!spoilers`. \nFor **Changelog** notifications, type `!changelogs`. \nFor **All** notifications, type `!all`. \n \n**__Removing__** \n \nTo remove **Poll** notifications, type `!unpolls`. \nTo remove **Giveaway** notifications, type `!ungiveaways`. \nTo remove **Spoiler** notifications, type `!unspoilers`. \nTo remove **Changelog** notifications, type `!unchangelogs`. \nTo remove **All** notifications, type `!unall`.", 
  color=discord.Color.purple())
  await ctx.channel.send(embed=embed)
  await ctx.message.delete()

@client.command()
@commands.cooldown(1, 30, commands.BucketType.user)
async def serverpfp(ctx):
  await ctx.send(f"{ctx.guild.icon_url}")

@client.command()
@commands.has_permissions(administrator=True)
async def staff(ctx):
  embed=discord.Embed(title="Staff List", url="", 
  description=f"**__Owners__** \n» <@814507814407110698> \n» <@503641822141349888> \n \n**__Co-Owner__** \n» <@386266705091100682> \n \n**__Sr. Admin__** \n» <@700427151970926633> \n \n**__Jr. Admin__** \n» <@429488496445620225> \n \n**__Helpers__** \n» <@831213491343720448> \n» <@745451384287002708> \n \n**__Discord Manager__** \n» <@429488496445620225>", 
  color=discord.Color.purple())
  await ctx.channel.send(embed=embed)
  await ctx.message.delete()

@client.command()
@commands.has_permissions(administrator=True)
async def rules(ctx):
    embed = discord.Embed(
        title="Rules",
        url="",
        description=
        f"[Click Here For The Rules](https://docs.google.com/document/d/1iWWeCxXRphrXnrYrZ3EK0gzB6ZfRV-xOt7HebDMvU4M/edit?usp=sharing)",
        color=discord.Color.purple())
    x = "[@everyone]"
    msg = await ctx.channel.send(content=x, embed=embed)
    await ctx.message.delete()

@client.event
async def on_command_error(ctx, error):
  if isinstance(error, commands.CommandInvokeError):
    error = error.original
    return
  if isinstance(error, commands.CommandNotFound):
      return
  elif isinstance(error, commands.MemberNotFound):
      return
  elif isinstance(error, commands.CommandOnCooldown):
      await ctx.channel.send(f"Hey {ctx.author.mention}! You can't use that command yet! \n \nTry again in {error.retry_after:.2f}s.", delete_after=10)
      await ctx.message.delete()
  elif isinstance(error, discord.Forbidden):
      return
  else:
      print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
      traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

client.run('')
