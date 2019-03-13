import discord
import math
import random
import urllib.request
from urllib.request import urlopen, Request
import html2text
import logging
import json
from typing import NamedTuple

logging.basicConfig(level=logging.INFO)
TOKEN = 'XXXXXX' #bot token goes here
client = discord.Client()

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    #emoji IDs from this server - https://discord.gg/wvyCuam
    aces = ['<:AC:555040968307638274>', '<:AD:555040968718417922>', '<:AH:555040969410740235>', '<:AS:555040969104425000>']    
    twos = ['<:2C:555040953619054613>', '<:2D:555040954017644554>', '<:2H:555040955779252224>', '<:2S:555040956034842624>']
    threes = ['<:3C:555040956773302274>', '<:3D:555040956475244545>', '<:3H:555040956735553557>', '<:3S:555040956873834506>']
    fours = ['<:4C:555040959054741504>', '<:4D:555040958807408649>', '<:4H:555040959734218752>', '<:4S:555040959075844147>']
    fives = ['<:5C:555040959168118815>', '<:5D:555040960409501716>', '<:5H:555040961676443648>', '<:5S:555040961236041728>']
    sixes = ['<:6C:555040961563197441>', '<:6D:555040962095611914>', '<:6H:555040961881833492>', '<:6S:555040962196275222>']
    sevens = ['<:7C:555040962670362645>', '<:7D:555040966273138719>', '<:7H:555040967338623003>', '<:7S:555040966260817930>']
    eights = ['<:8C:555040969960062979>', '<:8D:555040968995373096>', '<:8H:555040968370421781>', '<:8S:555040968156643388>']
    nines = ['<:9C:555040969712467979>', '<:9D:555040969028927511>', '<:9H:555040969649553418>', '<:9S:555040968429142049>']
    tens = ['<:10C:555040969905668106>', '<:10D:555040969733570560>', '<:10H:555040970337419294>', '<:10S:555040969674850343>']
    jacks = ['<:JC:555040971306565632>', '<:JD:555040971038130196>', '<:JH:555040970484482049>', '<:JS:555040970719100938>']
    queens = ['<:QC:555040971281137674>', '<:QD:555040971310497802>', '<:QH:555040971331600409>', '<:QS:555040971377868820>']
    kings = ['<:KC:555040970803249182>', '<:KD:555040971285463041>', '<:KH:555040970354458674>', '<:KS:555040970723295242>']
    cards = [aces, twos, threes, fours, fives, sixes, sevens, eights, nines, tens, jacks, queens, kings]
    
    if message.content.startswith('$'): #default prefix is $
        msg = message.content[1:].lower()
        args = msg.split()
        command = args[0]
        del args[0]

        #sends an embed with info on all commands
        if command == 'help':
            embed = discord.Embed(color=0x4A769A)
            embed.add_field(name="$8ball", value="Ask the magic 8 ball a question.", inline=False)
            embed.add_field(name="$quote", value="Gives a randomly generated inspirobot quote.", inline=False)
            embed.add_field(name="$coins", value="View how many coins you have. Must be used before doing any other currency related commands.", inline=False)
            embed.add_field(name="$rps", value="Play rock paper scissors. Usage: `$rps [rock/paper/scissors] [bet amount]`.", inline=False) 
            embed.add_field(name="$bet", value="Bet some coins for a 50/50 chance of winning more.", inline=False)
            embed.add_field(name="$beg", value="Beg for more money.", inline=False)
            embed.add_field(name="$highlow", value="Play a guessing game for money. Usage: `$highlow [bet amount]`. Enter `h` or `l` when prompted to guess.", inline=False)
            embed.add_field(name="$bj", value="Play a game of blackjack for money. Usage: `$bj [bet amount]`.", inline=False)
            await client.send_message(message.channel, embed=embed)

        #blackjack game
        elif command == 'bj':
            with open('users.txt', 'r') as filehandle:
                users = json.load(filehandle)
            with open('currency.txt', 'r') as filehandle:
                currency = json.load(filehandle)
            if message.author.id not in users:
                return await client.send_message(message.channel, "Please do $coins before using this command")
            try:
                int(args[0])
            except ValueError:
                return await client.send_message(message.channel, "Please enter a valid amount of coins to gamble")
            i = users.index(message.author.id)
            betamount = int(args[0])
            useramount = int(currency[i])
            if betamount < 1:
                return await client.send_message(message.channel, "Please enter a number greater than 0")
            if betamount > useramount:
                return await client.send_message(message.channel, "You don't have enough coins to do that!")

            class Card(NamedTuple):
                img: str
                val: int
                name: str
                suit: str
                ace: bool
            def getCard():
                cardNum = math.floor(random.random() * 13)
                cardSuit = math.floor(random.random() * 4)
                if cardNum > 9:
                    cardVal = 10
                    isAce = False
                    if cardNum == 10:
                        cName = 'J'
                    elif cardNum == 11:
                        cName = 'Q'
                    else:
                        cName = 'K'
                elif cardNum == 0:
                    cardVal = 11
                    cName = 'A'
                    isAce = True
                else:
                    cardVal = cardNum+1
                    cName = str(cardNum+1)
                    isAce = False
                if cardSuit == 0:
                    suitEmoji = ':clubs:'
                elif cardSuit == 1:
                    suitEmoji = ':diamonds:'
                elif cardSuit == 2:
                    suitEmoji = ':hearts:'
                else:
                    suitEmoji = ':spades:'
                
                return Card(cards[cardNum][cardSuit], cardVal, cName, suitEmoji, isAce)

            gameOver=False
            choiceMade=False
            dcards = []
            pcards = []
            dcards.append(getCard())
            dcards.append(getCard())
            pcards.append(getCard())
            pcards.append(getCard())

            def getDisplay(array):
                display = ''
                for x in array:
                    display+=x.img
                display+='\n'
                for x in array:
                    display+=x.name
                    display+=x.suit
                return display

            def getTotal(array):
                total = 0
                for x in array:
                    total+=x.val
                return total

            def checkForAce(array):
                a = False
                i = 0
                for x in array:
                    if x.ace == True and x.val == 11:
                        a = True
                        i = array.index(x)
                return a, i

            pdisplay = getDisplay(pcards)
            ptotal = getTotal(pcards)
            dtotal = getTotal(dcards)
            if ptotal > 21:
                pcards[1] = pcards[1]._replace(val=1)
                ptotal = getTotal(pcards)
            if dtotal > 21:
                dcards[1] = dcards[1]._replace(val=1)
                dtotal = getTotal(dcards)
            
            embed = discord.Embed(color=0x4A769A)
            embed.add_field(name="Playing a game of blackjack", value="Type 'hit' to draw a new card, or 'stay' to stick with what you've got", inline=False)
            embed.add_field(name="Your total: " + str(ptotal), value=pdisplay, inline=True)
            embed.add_field(name="Dealer's total: ?", value=dcards[0].img + '<:Gray_back:555053721847857152>' + '\n' + dcards[0].name + dcards[0].suit + '??', inline=True)
            await client.send_message(message.channel, embed=embed)

            while gameOver == False:
                while choiceMade == False:
                    msg = await client.wait_for_message(author=message.author)
                    if msg:
                        if msg.content.lower() == 'hit':
                            choiceMade = True
                            pcards.append(getCard())
                            ptotal = getTotal(pcards)
                            if ptotal > 21:
                                ace, index = checkForAce(pcards)
                                if ace == True:
                                    pcards[index] = pcards[index]._replace(val=1)
                                    ptotal = getTotal(pcards)
                                else:
                                    gameOver=True
                                    result='loss'
                            elif ptotal == 21: 
                                gameOver=True
                                if dtotal == 21:
                                    result='draw'
                                else:
                                    result='win'
                            if dtotal < 17 and gameOver == False:
                                dcards.append(getCard())
                                dtotal = getTotal(dcards)
                            if dtotal > 21 and gameOver == False:
                                ace, index = checkForAce(dcards)
                                if ace == True:
                                    dcards[index] = dcards[index]._replace(val=1)
                                    dtotal = getTotal(dcards)
                                else:
                                    gameOver=True
                                    result='win'
                        elif msg.content.lower() == 'stay':
                            choiceMade = True
                            gameOver = True
                            if dtotal < 17:
                                dcards.append(getCard())
                                dtotal = getTotal(dcards)
                            if ptotal == 21:
                                if dtotal == 21:
                                    result='draw'
                                else:
                                    result='win'
                            elif ptotal > dtotal:
                                result='win'
                            elif ptotal < dtotal:
                                result='loss'
                            else:
                                result='draw'
                        else:
                            await client.send_message(message.channel, "Please type 'hit' or 'stay'")
                            
                    if gameOver==False and choiceMade==True:
                        pdisplay = getDisplay(pcards)
                        embed = discord.Embed(color=0x4A769A)
                        embed.add_field(name="Playing a game of blackjack", value="Type 'hit' to draw a new card, or 'stay' to stick with what you've got", inline=False)
                        embed.add_field(name="Your total: " + str(ptotal), value=pdisplay, inline=True)
                        embed.add_field(name="Dealer's total: ?", value=dcards[0].img + '<:Gray_back:555053721847857152>' + '\n' + dcards[0].name + dcards[0].suit + '??', inline=True)
                        await client.send_message(message.channel, embed=embed)
                        choiceMade=False
                        
                if gameOver==True:
                    pdisplay = getDisplay(pcards)
                    ddisplay = getDisplay(dcards)
                    embed = discord.Embed(color=0x4A769A)
                    if result == 'win':
                        useramount+=betamount
                        currency[i] = str(useramount)
                        with open('currency.txt', 'w') as filehandle:
                            json.dump(currency, filehandle)
                        embed.add_field(name="Game over!", value="You win! You gained " + str(betamount) + " coins. Your total balance is now " + str(useramount), inline=False)
                    elif result == 'loss':
                        useramount-=betamount
                        currency[i] = str(useramount)
                        with open('currency.txt', 'w') as filehandle:
                            json.dump(currency, filehandle)
                        embed.add_field(name="Game over!", value="You lose! You lost " + str(betamount) + " coins. Your total balance is now " + str(useramount), inline=False)
                    else:
                        embed.add_field(name="Game over!", value="It's a draw! You get your bet back", inline=False)
                    embed.add_field(name="Your total: " + str(ptotal), value=pdisplay, inline=True)
                    embed.add_field(name="Dealer's total: " + str(dtotal), value=ddisplay, inline=True)
                    await client.send_message(message.channel, embed=embed)

        #higher or lower game                            
        elif command == 'highlow':
            with open('users.txt', 'r') as filehandle:
                users = json.load(filehandle)
            with open('currency.txt', 'r') as filehandle:
                currency = json.load(filehandle)
            if message.author.id not in users:
                return await client.send_message(message.channel, "Please do $coins before using this command")
            try:
                int(args[0])
            except ValueError:
                return await client.send_message(message.channel, "Please enter a valid amount of coins to gamble")
            i = users.index(message.author.id)
            betamount = int(args[0])
            useramount = int(currency[i])
            if betamount < 1:
                return await client.send_message(message.channel, "Please enter a number greater than 0")
            if betamount > useramount:
                return await client.send_message(message.channel, "You don't have enough coins to do that!")

            class Card(NamedTuple):
                img: str
                val: int
                name: str
                suit: str
            def getCard():
                cardNum = math.floor(random.random() * 13)
                cardSuit = math.floor(random.random() * 4)
                
                if cardNum == 10:
                    showNum = 'J'
                elif cardNum == 11:
                    showNum = 'Q'
                elif cardNum == 12:
                    showNum = 'K'
                elif cardNum == 0:
                    showNum = 'A'
                else:
                    showNum = str(cardNum+1)
                if cardSuit == 0:
                    showSuit = ':clubs:'
                elif cardSuit == 1:
                    showSuit = ':diamonds:'
                elif cardSuit == 2:
                    showSuit = ':hearts:'
                else:
                    showSuit = ':spades:'

                return Card(cards[cardNum][cardSuit], cardNum, showNum, showSuit)

            card1 = getCard()
                
            embed = discord.Embed(color=0x4A769A)
            embed.add_field(name="Will the next card be higher or lower?", value=card1.img + '  <:Gray_back:555053721847857152>\n' + card1.name + card1.suit + '? ?', inline=False)
            await client.send_message(message.channel, embed=embed)

            winnings = 0
            card2 = getCard()
            choiceMade = False
            gameOver = False
            
            while gameOver == False:
                while choiceMade == False:
                    msg = await client.wait_for_message(author=message.author)
                    if msg:
                        if msg.content.lower() == 'h':
                            choiceMade = True
                            if card2.val > card1.val:
                                result = 'win'
                            elif card2.val == card1.val:
                                result = 'draw'
                            else:
                                result = 'loss'
                                gameOver = True
                        elif msg.content.lower() == 'l':
                            choiceMade = True
                            if card2.val < card1.val:
                                result = 'win'
                            elif card2.val == card1.val:
                                result = 'draw'
                            else:
                                result = 'loss'
                                gameOver = True
                        elif msg.content.lower() == 'q':
                            gameOver = True
                            choiceMade = True
                            result = ''
                        else:
                            await client.send_message(message.channel, "Please enter either 'h' or 'l', or enter 'q' to end the game.")
                if gameOver == False:
                    card1 = card2
                    card2 = getCard()
                choiceMade = False
                embed = discord.Embed(color=0x4A769A)
                if result == 'win':
                    embed.add_field(name="Correct! Guess whether the next card will be higher or lower, or type 'q' to end the game", value=card1.img + '  <:Gray_back:555053721847857152>\n' + card1.name + card1.suit + '? ?', inline=False)
                    await client.send_message(message.channel, embed=embed)
                    winnings += betamount
                elif result == 'draw':
                    embed.add_field(name="They were the same! Guess whether the next card will be higher or lower, or type 'q' to end the game", value=card1.img + '  <:Gray_back:555053721847857152>\n' + card1.name + card1.suit + '? ?', inline=False)
                    await client.send_message(message.channel, embed=embed)
                elif result == 'loss':
                    winnings-=betamount
            
            embed = discord.Embed(color=0x4A769A)
            if winnings > 0:
                useramount += winnings
                currency[i] = str(useramount)
                with open('currency.txt', 'w') as filehandle:
                    json.dump(currency, filehandle)
                embed.add_field(name="Game over! You won " + str(winnings) + " coins in total. Your new balance is " + str(useramount), value=card1.img + '  ' + card2.img + '\n' + card1.name + card1.suit + card2.name + card2.suit, inline=False)
            elif winnings < 0:
                useramount -= betamount
                currency[i] = str(useramount)
                with open('currency.txt', 'w') as filehandle:
                    json.dump(currency, filehandle)
                embed.add_field(name="Game over! You lost " + str(betamount) + " coins. Your new balance is " + str(useramount), value=card1.img + '  ' + card2.img + '\n' + card1.name + card1.suit + card2.name + card2.suit, inline=False)
            else:
                embed.add_field(name="Game over! You didn't win any coins.", value=card1.img + '  ' + card2.img + '\n' + card1.name + card1.suit + card2.name + card2.suit, inline=False)
            await client.send_message(message.channel, embed=embed)                  
                    
        #8ball
        elif command == '8ball':
            response = ["Signs point to yes", "It is certain", "Most likely", "Better not tell you now", "Concentrate and ask again", "Don't count on it", "My sources say no", "Outlook not so good"]
            rannum = math.floor(random.random() * len(response))
            embed = discord.Embed(color=0x4A769A)
            embed.add_field(name=":grey_question: You asked: :grey_question:", value='*' + ' '.join(args) + '*', inline=False) 
            embed.add_field(name=":8ball: The magic 8 ball says: :8ball:", value='*' + response[rannum] + '*', inline=False)
            await client.send_message(message.channel, embed=embed)

        #rock paper scissors
        elif command == 'rps':
            opt = ['rock', 'paper', 'scissors']
            with open('users.txt', 'r') as filehandle:
                users = json.load(filehandle)
            with open('currency.txt', 'r') as filehandle:
                currency = json.load(filehandle)
            if message.author.id not in users:
                return await client.send_message(message.channel, "Please do $coins before using this command")
            try:
                int(args[1])
            except ValueError:
                return await client.send_message(message.channel, "Please enter a valid amount of coins to gamble")
            i = users.index(message.author.id)
            betamount = int(args[1])
            useramount = int(currency[i])
            if betamount < 1:
                return await client.send_message(message.channel, "Please enter a number greater than 0")
            if betamount > useramount:
                return await client.send_message(message.channel, "You don't have enough coins to do that!")
            if args[0] not in opt:
                return await client.send_message(message.channel, "Please choose either rock, paper or scissors.")
            botchoice = opt[math.floor(random.random() * len(opt))]
            if args[0] == botchoice:
                result = "It's a draw! You get your bet back"
            elif args[0] == opt[0] and botchoice == opt[1] or args[0] == opt[1] and botchoice == opt[2] or args [0] == opt[2] and botchoice == opt[0]:
                useramount -= betamount
                currency[i] = str(useramount)
                with open('currency.txt', 'w') as filehandle:
                    json.dump(currency, filehandle)
                result = "Bot wins! :frowning: You lost " + str(betamount) + " coins. Your new balance is " + str(useramount)
            else:
                useramount += betamount
                currency[i] = str(useramount)
                with open('currency.txt', 'w') as filehandle:
                    json.dump(currency, filehandle)
                result = "You win! :smile: You won " + str(betamount) + " coins. Your new balance is " + str(useramount)
            embed = discord.Embed(title="Rock, paper, scissors", description=result, color=0x4A769A)
            embed.add_field(name="You chose:", value=args[0].capitalize(), inline=True)
            embed.add_field(name="The bot chose:", value=botchoice.capitalize(), inline=True)
            await client.send_message(message.channel, embed=embed)

        #used to add new user to the users.txt and currency.txt file
        elif command == 'coins':
            with open('users.txt', 'r') as filehandle:
                users = json.load(filehandle)
            with open('currency.txt', 'r') as filehandle:
                currency = json.load(filehandle)
            if message.author.id not in users:
                users.append(message.author.id)
                currency.append('10')
                await client.send_message(message.channel, "You have been given 10 free coins! You can now use all other gambling commands")
                with open('users.txt', 'w') as filehandle:
                    json.dump(users, filehandle)
                with open('currency.txt', 'w') as filehandle:
                    json.dump(currency, filehandle)
            else:
                i = users.index(message.author.id)
                await client.send_message(message.channel, "You have " + currency[i] + " coins")

        #50/50 coinflip gambling
        elif command == 'bet':
            with open('users.txt', 'r') as filehandle:
                users = json.load(filehandle)
            with open('currency.txt', 'r') as filehandle:
                currency = json.load(filehandle)
            if message.author.id not in users:
                return await client.send_message(message.channel, "Please do $coins before trying to gamble")
            try:
                int(args[0])
            except ValueError:
                return await client.send_message(message.channel, "Please enter a valid amount of coins to gamble")
            i = users.index(message.author.id)
            betamount = int(args[0])
            useramount = int(currency[i])
            if betamount < 1:
                return await client.send_message(message.channel, "Please enter a number greater than 0")
            if betamount > useramount:
                return await client.send_message(message.channel, "You don't have enough coins to do that!")
            rannum = math.floor(random.random() * 2)
            if rannum == 0:
                useramount -= betamount
                currency[i] = str(useramount)
                with open('currency.txt', 'w') as filehandle:
                    json.dump(currency, filehandle)
                await client.send_message(message.channel, "You lost! You now have " + str(useramount) + " coins")
            elif rannum == 1:
                useramount += betamount
                currency[i] = str(useramount)
                with open('currency.txt', 'w') as filehandle:
                    json.dump(currency, filehandle)
                await client.send_message(message.channel, "You won! You now have " + str(useramount) + " coins")

        #gives user a random amount of currency from 0-10
        elif command == 'beg':
            with open('users.txt', 'r') as filehandle:
                users = json.load(filehandle)
            with open('currency.txt', 'r') as filehandle:
                currency = json.load(filehandle)
            if message.author.id not in users:
                return await client.send_message(message.channel, "Please do $coins before trying to beg for money")
            i = users.index(message.author.id)
            rannum = math.floor(random.random() * 11)
            useramount = int(currency[i])
            if rannum == 0:
                return await client.send_message(message.channel, "Go away peasant, no money for you")
            else:
                useramount += rannum
                currency[i] = str(useramount)
                with open('currency.txt', 'w') as filehandle:
                    json.dump(currency, filehandle)
                await client.send_message(message.channel, "Fine, you can have " + str(rannum) + " coins. You now have " + str(useramount) + " coins in total")

        #sends a generated inspirobot.me image to the channel
        elif command == 'quote':
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
            reg_url = "https://inspirobot.me/api?generate=true"
            req = Request(url=reg_url, headers=headers) 
            shit = urlopen(req)
            html = shit.read()
            charset = shit.headers.get_content_charset()
            html = html.decode(charset)
            await client.send_message(message.channel, html2text.html2text(html))


@client.event
async def on_ready():
    print('Logged in as:')
    print(client.user.name)
    print(client.user.id)

client.run(TOKEN)
