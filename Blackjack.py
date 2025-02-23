import random

class Card:
    def __init__(self,suit,rank):
        self.suit = suit
        self.rank = rank
    
    def get_suit(self):
        return self.suit
    
    def get_rank(self):
        return self.rank


class Deck:
    def __init__(self):
        self.suits = ["♦","♣","♠","♥"]
        self.ranks = ["2","3","4","5","6","7","8","9","10","J","Q","K","A"]
        self.deck = []   
    
    #appends 6 standard decks of cards to the self.deck array
    def create_deck(self):
        for i in range(0,6):
            for j in range(0,len(self.suits)):
                for k in range(0,len(self.ranks)):
                    self.deck.append(Card(self.suits[j],self.ranks[k]))
    
    #randomises the order of cards in the deck
    def shuffle_deck(self):
        random.shuffle(self.deck)
    
    def get_deck(self):
        return self.deck
    
    #Takes a card from the top of the deck array
    def get_card(self):
        return self.deck.pop(0)
    

class Hand:
    def __init__(self,deck):
        self.deck = deck
        self.hand = [] #Stores the current hand
        self.score = 0 #Stores the score of the current hand
    
    #Draws a card from the deck
    def hit(self):
        self.hand.append(self.deck.get_card())
    
    #Hits twice
    def initialise_hand(self):
        for i in range(0,2):
            self.hit()
    
    #Sends cards from hand to the bottom of the deck
    def reset(self):
        for i in range(len(self.hand)):
            self.deck.get_deck().append(self.hand.pop())
    
    #Calculates the score of the hand
    def calculate_score(self):
        self.score = 0  #Resets the old score
        
        numAces = 0     #Stores the number of aces currently in the hand
                        #and resets the number of aces
        
        for card in self.hand:                 #Loops for each card in hand
            
            curRank = card.get_rank()          #Checks the rank of the current card
            
            if curRank in ["J","Q","K"]:       #Adds the value of the face cards to the score
                self.score+=10
            
            elif curRank == "A":               #Increments numAces by one and the score by 11
                numAces+=1                     #if there is an ace
                self.score+=11
                    
            else:
                self.score+=int(curRank)       #Adds the value of numbered cards to the score
            
            while self.score>21 and numAces>0: #Changes the value of aces to 1 if the score is 
                self.score -= 10               #greater than 21 and there are aces in the hand
                numAces -= 1  
            
    def get_hand(self):
        return self.hand
    
    def get_score(self):
        return self.score
  

class Player:
    def __init__(self,deck):
        self.pHand = Hand(deck) #Creates an instance of the hand class for the player
    

class Dealer(Player):
    def __init__(self,deck):
        Player.__init__(self,deck) #Inherits the Player class
        
    #Draws cards until the score reaches 17 or more
    def draw_final(self):
        while self.pHand.score <17:
            self.pHand.hit()
            self.pHand.calculate_score()
  

class User(Player):
    def __init__(self,deck):
        Player.__init__(self,deck) #Inherits the Player class
        
        self.chips = 500           #Stores the number of chips the user has
    
    #Allows user to place a bet
    def bet(self):
        print("Chips:",self.chips) #Displays the number of chips the player currently has
        
        #Validates amount of chips input, ensures it's an integer
        #and within the number of chips the player currently has
        valid = False
        while valid == False:
            valid = True
            try:
                amount = int(input("How many chips do you want to bet? "))
                if (amount<=0) or (amount>self.chips):
                    print("Invalid amount")
                    valid = False
            except:
                print("Enter an integer value")
                valid = False
                
        self.chips -= amount        #Updates the number of chips the player has
        return amount
    
    def get_chips(self):
        return self.chips
    
    #Updates the number of chips after a round, the mult is determined
    #from whether the user wins, loses or draws. The amount is the number
    #of chips the player bet
    def update_chips(self,amount,mult):
        self.chips += (amount*mult)
    

class Game:
    def __init__(self):
        self.deck = Deck()                      #Creates an instance of the Deck class which
                                                #is shared amongst all players
                                                
        self.user = User(self.deck)             #Creates an instance of the User class
        self.dealer = Dealer(self.deck)         #Creates an instance of the Dealer 
    
    #These methods call other methods to make accessing them easier
    def create_deck(self):                      
        self.deck.create_deck()                                                     
    def shuffle_deck(self):                     
        self.deck.shuffle_deck()                                                    
    def place_bet(self):                        
        return self.user.bet()                  
    
    #Deals two cards to the player and dealer
    def deal_cards(self):
        self.user.pHand.initialise_hand()
        self.dealer.pHand.initialise_hand()
    
    #Calculates the score of the player and dealer
    def calculate_total_scores(self):
        self.user.pHand.calculate_score()
        self.dealer.pHand.calculate_score()
    
    #Displays the hands of the dealer and user. If "hidden" is passed in then
    #itt hides one of the dealer's cards, otherwise it shows all cards
    def display_hands(self,allOrHidden):
        uHand = self.user.pHand.get_hand()
        
        print("Your cards:")
        
        for card in uHand:
            print(card.get_suit(),card.get_rank())
        print("\n")
        
        dHand = self.dealer.pHand.get_hand()
        
        print("Dealer's cards:")
        
        if allOrHidden == "hidden":
            print(dHand[0].get_suit(),dHand[0].get_rank())
            print("Hidden card\n")
        else:
            for card in dHand:
                print(card.get_suit(),card.get_rank())
            print("\n")
            
    def play(self):
        self.user.pHand.reset()                                #Empties the Player and Dealer's hands into
        self.dealer.pHand.reset()                              #the deck
        
        self.shuffle_deck()                                                                
        self.deal_cards()                                                
        self.calculate_total_scores()                                                                
        
        #Conditional loop until the user busts or stands.
        #The user draws a card each time they hit
        while True and self.user.pHand.get_score()<21:                                
            self.display_hands("hidden")                       #Displays the player and dealers hand each loop                                         
            
            #Validates the users input to ensure its either "hit" or "stand"
            valid = False
            while valid == False:
                
                choice = input(("Hit or Stand? \n"))
                if choice.lower() not in ["hit","stand"]:
                    print("Invalid choice")
                else:
                    break
            if choice.lower() == "stand":
                break
            
            self.user.pHand.hit()
            self.calculate_total_scores()
            
        self.display_hands("hidden")                           #Displays the player and dealers hand after the loop
            
        if self.user.pHand.get_score()>21:                     #Checks for bust
            print("Bust!")
            return 0
        
        else:
            self.dealer.draw_final()                           #Dealer draws if user doesn't bust
        
        self.calculate_total_scores()

        self.display_hands("all")                              
        
        uScore = self.user.pHand.get_score()
        dScore = self.dealer.pHand.get_score()
        
        
        #This code checks all outcomes and returns a corresponding
        #integer to be used as a "mult" in the update_chips() method
        if dScore<=21 and dScore>uScore:
            print("Dealer wins!")
            return 0
        elif dScore>21:
            print("Dealer busts!")
            return 2
        elif dScore==uScore:
            print("Push!")
            return 1
        else:
            print("You win!")
            return 2
            
    def game(self):
        self.create_deck() #Creates a deck
        while True:        
            amount = self.place_bet()
            mult = int(self.play())
            self.user.update_chips(amount,mult)
            
            #Ends the game if the user has no chips left
            if self.user.chips == 0:
                print("You have no chips left...")
                break
            
            #Validates user input to ensure it's either "y" or "n"
            valid = False
            while valid == False:
                keepPlaying = input("Do you want to keep playing?(y/n) ")
                if keepPlaying.lower() not in ["y","n"]:
                    print("Invalid input")
                else:
                    break
            if keepPlaying == "n": #Ends the loop and the game if "n" is input
                break
                
           
blackjack = Game() #Creates an instance of the Game object 
blackjack.game()   #Calls the game() method
            
        