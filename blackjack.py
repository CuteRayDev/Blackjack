import random

def NewCards():
    return{
        1 : 0,
        2 : 0,
        3 : 0,
        4 : 0,
        5 : 0,
        6 : 0,
        7 : 0,
        8 : 0,
        9 : 0,
        10 : 0,
        11 : 0,
        12 : 0,
        13 : 0
        }
    
def GetRandomCard(cardNos):
    result = random.randrange(1, 14)
    if cardNos[result] < 4:
        cardNos[result] += 1
        return result
    else:
        return GetRandomCard(cardNos)
    
def ExplainCard(card):
    if card > 10 or card == 1:
        match card:
            case 11:
                return "J"
            case 12:
                return "Q"
            case 13:
                return "K"
            case 1:
                return "A"
    else:
        return str(card)

def GetCardValue(card):
    if card <= 10:
        return card
    else:
        return 10
    
def GetCardsSum(cards):
    noAceSum = 0
    noOfAces = 0
    for card in cards:
        if card != 1 or noOfAces >= 1:
            noAceSum += GetCardValue(card)
        else:
            noOfAces += 1

    sum = []
    if noOfAces == 0:
        sum = [noAceSum]
    else:
        sum = [noAceSum + 1]
        if noAceSum + 11 <= 21:
            sum.append(noAceSum + 11)
    return sum

def GetAbsoluteCardSum(cards):
    sums = GetCardsSum(cards)
    if len(sums) == 1:
        return sums[0]
    else:
        return sums[1]

def PrintCardsInfo(cards, whom = "Your"):
    cardExplanations = ExplainCard(cards[0])
    for i in range (1, len(cards)):
        cardExplanations += f", {ExplainCard(cards[i])}"

    sum = GetCardsSum(cards)
    sumPoses = str(sum[0])
    for i in range (1, len(sum)):
        sumPoses += f" OR {sum[i]}"

    print(f"{whom} cards are: {cardExplanations}. Current Sum: {sumPoses}")
    
def Game():
    playerWealth = float(1000)
    while playerWealth > 0:
        print("================================================")
        print("================================================")

        gambleAmt = -1
        while gambleAmt > playerWealth or gambleAmt <= 0:
            print(f"You have: ${round(playerWealth, 1)}")
            try:
                gambleAmt = float(input("Enter The Amount Of Money You Would Like To Gamble: $"))
                if gambleAmt > playerWealth or gambleAmt <= 0:
                    print("Invalid Input, Please Try Again.")
            except:
                print("Invalid Input, Please Try Again.")

        playerFiveDragons = False
        playerTwoAces = False
        multiplier = 1
        cardNos = NewCards()
        dealercards = [GetRandomCard(cardNos), GetRandomCard(cardNos)]
        playercards = [GetRandomCard(cardNos), GetRandomCard(cardNos)]
        PrintCardsInfo(playercards)
        
        firstHand = True
        end = False
        while not end:
            choice = input("Hit Or Stand? (h/s): ")
            match choice:
                case "s":
                    end = True
                    if firstHand:
                        if GetAbsoluteCardSum(playercards) == 21:
                            multiplier *= 3
                            print("Blackjack! x3")
                        if playercards[0] == 1 and playercards[1] == 1:
                            multiplier *= 3
                            playerTwoAces = True
                            print("Two Aces! x3")
                    else:
                        if GetAbsoluteCardSum(playercards) == 21:
                            multiplier *= 2
                            print("Blackjack! x2")
                case "h":
                    firstHand = False
                    playercards.append(GetRandomCard(cardNos))
                    PrintCardsInfo(playercards)
                    if GetCardsSum(playercards)[0] > 21:
                        print("You Are Busted :(")
                        end = True
                    elif len(playercards) >= 5:
                        multiplier *= 3
                        print("Five Dragons! x3")
                        playerFiveDragons = True
                        end = True
                        if GetAbsoluteCardSum(playercards) == 21:
                            multiplier *= 2
                            print("Blackjack! x2")
                case _:
                    print("Invalid Input, Please Try Again.")

        print("================================================")
        
        dealerFiveDragons = False
        dealerTwoAces = False
        
        PrintCardsInfo(dealercards, "Dealer's")
        end = False

        if dealercards[0] == 1 and dealercards[1] == 1:
            dealerTwoAces = True
            print("Two Aces For Dealer!")
            end = True

        while not end:
            if GetAbsoluteCardSum(dealercards) < 17 or (GetAbsoluteCardSum(playercards) > GetAbsoluteCardSum(dealercards) and GetAbsoluteCardSum(playercards) <= 21):
                print("Dealer Hits!")
                dealercards.append(GetRandomCard(cardNos))
                PrintCardsInfo(dealercards, "Dealer's")
                if GetCardsSum(dealercards)[0] > 21:
                    print("Dealer is Busted :)")
                    end = True
                elif len(dealercards) >= 5:
                        print("Five Dragons For Dealer!")
                        dealerFiveDragons = True
                        end = True
            else:
                print("Dealer Stands!")
                end = True
        
        print("================================================")

        dealerSum = GetAbsoluteCardSum(dealercards)
        playerSum = GetAbsoluteCardSum(playercards)

        dealerPoint = str(dealerSum)
        if dealerSum > 21:
            dealerPoint = "Busted"
        playerPoint = str(playerSum)
        if playerSum > 21:
            playerPoint = "Busted"

        print(f"You: {playerPoint}, Dealer: {dealerPoint}.")

        if dealerSum > 21 and playerSum > 21:
            print("Both Busted. Wealth Change: -$0")
        elif (dealerSum == playerSum and not playerFiveDragons and not dealerFiveDragons and not playerTwoAces and not dealerTwoAces) or (playerFiveDragons and dealerFiveDragons) or (playerTwoAces and dealerTwoAces):
            print("Same Points. Wealth Change: -$0")
        elif (dealerSum < playerSum and not dealerFiveDragons and not dealerTwoAces and playerSum <= 21) or playerFiveDragons or playerTwoAces or dealerSum > 21:
            print(f"You Win! Wealth Change: +${round(gambleAmt * multiplier, 1)}")
            playerWealth += gambleAmt * multiplier
        else:
            print(f"You Lost. Wealth Change: -${round(gambleAmt, 1)}")
            playerWealth -= gambleAmt
        
        print(f"Your Updated Wealth: ${round(playerWealth, 1)}")

    print("================================================")

    print("No More Money Left. Game Over.")

    print("================================================")
    print("================================================")

gameContinue = True
while gameContinue:
    Game()
    inp = input("Stop Playing? (y): ")
    if inp == "y":
        gameContinue = False