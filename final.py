class Battleboard:
    """Generates a board to place and destroy ships"""
    
    def __init__(self, width=10, height=10):
        """Constructs the board"""
        self.width = width
        self.height = height
        self.board = [['-']*width for i in range(height)]
        self.shiplocs = []
        self.wipedlocs = []

    def getCoords(self, s):
        """Takes in a string containing the row letter and the column number, and converts it into coordinates on the 2D array. Ex: A5 = (0,4)"""
        return (ord(s[0])-65, int(s[1:])-1)

    def getCode(self, T):
        """Takes in a tuple containing coordinates on the 2D array, and returns a string representing the row letter and column number on the board."""
        return chr(65+(T[0]))+str(T[1]+1)

    def addShip(self, L):
        """Takes an array of valid piece locations, and places a ship on the board. Also adds all sets of ship locations into an array""" 
        L2 = []
        for i in range(len(L)):
            loc = self.getCoords(L[i])
            self.board[loc[0]][loc[1]]="s"
            L2.append(loc)
        self.shiplocs.append(L2)

    def updatewiped(self):
        """Updates the wipedlocs list so that the player has a record of ships it's already destroyed completely."""
        for i in range(len(self.shiplocs)):
            #print(self.shiplocs[i])
            if(len(list(filter(lambda x: self.board[x[0]][x[1]]=="x", self.shiplocs[i])))==3):
                #self.wipedlocs.append(self.shiplocs[i])
                for k in range(len(self.shiplocs[i])):
                    if(self.shiplocs[i][k] not in self.wipedlocs):
                        self.wipedlocs.append(self.shiplocs[i][k])

    def launchMissile(self, s):
        """Takes in a string containing the row and col in which the missile is meant to be launched at the board"""
        loc = self.getCoords(s)
        if(self.board[loc[0]][loc[1]]=="-"):
            self.board[loc[0]][loc[1]]="o"
        elif(self.board[loc[0]][loc[1]]=="s"):
            self.board[loc[0]][loc[1]]="x"
            self.updatewiped()
        

        
    def canLaunch(self, s):
        """Returns true if s is a valid location to launch a missile, returns False otherwise."""
        loc = self.getCoords(s)
        if(loc[0]>=self.height or loc[0]<0):
            return False
        elif(loc[1]>=self.width or loc[1]<0):
            return False
        elif(self.board[loc[0]][loc[1]]=="x" or self.board[loc[0]][loc[1]]=="o"):
            return False
        else:
            return True

    def canaddShip(self, s):
        """Returns true if s is a valid location to place a ship, returns False otherwise."""
        loc = self.getCoords(s)
        if(loc[0]>=self.height or loc[0]<0):
            return False
        elif(loc[1]>=self.width or loc[1]<0):
            return False
        elif(self.board[loc[0]][loc[1]]=="s"):
            return False
        else:
            return True


    def userview(self):
        """Returns a string containing the board display that the owner of the board would see, including ship locations."""
        s = 'Player Board:\n'   
        s+='\n'    
        s+=' '          
        for col in range(self.width):
            s += ' '+str(col+1)
        s+='\n'
        for row in range(self.height):     
            s+=chr(row+65)+' '     
            for col in range(self.width):
                s += self.board[row][col] + ' '
            s += '\n'
        s += '\n'
        return s             

    def opponentview(self):
        """Returns a string containing the board display that the opponent of the board owner would see, hiding ship locations."""
        s = 'Enemy Board:\n'         
        s+='\n'    
        s+=' '    
        for col in range(self.width):
            s += ' '+str(col+1)
        s+='\n'
        for row in range(self.height):     
            s+=chr(row+65)+' '     
            for col in range(self.width):
                if(self.board[row][col]=="s"):
                    s += '- '
                else:
                    s += self.board[row][col] + ' '
            s += '\n'
        s += '\n'
        return s    

    def sunkenShips(self):
        """Returns True if all ships on the board have sunk"""
        for i in range(self.height):
            for k in range(self.width):
                if(self.board[i][k]=="s"):
                    return False
        return True


#End of board class, now implementation of game itself

import random

def main():
    """Runs the Battleship program"""
    while True:
        print(rules())
        diff = input("Which difficulty will you play on? (easy or hard): ")
        numships = int(input("How many ships will you play with? "))
        playerboard = playersetupGame(numships)
        cpuboard = cpusetupGame(numships)
        print("Ready to play!")
        playGame(playerboard, cpuboard, diff)
        p = input("Would you like to play again? ")
        if(p=="yes"):
            print("Great!")
        elif(p=="no"):
            break
    print("Thanks for playing!")

def menu():
        """ prints the menu """
        print()
        print("Menu:")
        print("  (1) Continue playing")
        print("  (2) Rules")
        print("  (3) Load game")
        print("  (4) Save game")
        print("  (5) Quit")
        print()
        uc = input("Your choice: ")
        try:
            uc = int(uc) 
            if uc not in [1,2,3,4,5]:  
                print("    Didn't recognize that input\n")
            else:
                return uc  #

        except:  
            print("    Didn't understand that input\n")

def rules():
    """Returns string explaining how to play the game"""
    return "Welcome to BattleShip! Place a chosen number of ships on the grid, each of length 3, such that each ship component is in either a vertical or horizontal line. On each turn, launch a missile at a spot on your opponents board, in an attempt to take down every ship they have. If the missile hits, it will be marked on the grid with an x, and if it misses it will be an o."

def playersetupGame(n):
    """Designs the players board with input from the player"""
    pb = Battleboard()
    for i in range(n):
        print(pb.userview())
        print("Ship",(i+1),":")
        L=["?-1"]
        while(len(list(filter(pb.canaddShip, L)))!=3):
            L = input("Please input three valid adjacent ship locations separated by spaces ").split(" ")
        pb.addShip(L)
    print(pb.userview())
    return pb

def cpusetupGame(n):
    """Randomly designs the Computers board"""
    cb = Battleboard()
    for i in range(n):
        s = "?-1"
        x=-1
        y=-1
        L=[]
        while(cb.canaddShip(s)==False):
            x = random.randint(0,cb.height-1)
            y = random.randint(0,cb.width-1)
            s=chr(65+x)+str(y+1)
        if(random.randint(0,1)==0):
            if(x>=cb.height/2):
                L = [s,chr(64+x)+str(y+1),chr(63+x)+str(y+1) ]
            else:
                L = [s,chr(66+x)+str(y+1),chr(67+x)+str(y+1) ]
        else:
            if(y>=cb.width/2):
                L = [s,chr(65+x)+str(y),chr(65+x)+str(y-1) ]
            else:
                L = [s,chr(65+x)+str(y+2),chr(65+x)+str(y+3) ]
        cb.addShip(L)
    return cb

def cpusimplemove(pb):
    """Picks a random location on the players board for the cpu to fire at (easy mode). Takes in player board pb."""
    x = random.randint(0,pb.height-1)
    y = random.randint(0,pb.width-1)
    return pb.getCode((x,y))

def cpusmartmove(pb):
    """AI for choosing where CPU will launch a missile. Takes into account spots that have already been hit to pick a move with higher odds of hitting."""
    for i in range(0, pb.height):
        for j in range(0, pb.width):
            if((i,j) in pb.wipedlocs):
                pass
            elif(pb.board[i][j]=="x"):
                c1=0
                c2=0
                c3=0
                c4=0
                if(i!=0):
                    if(pb.board[i-1][j]=="x"):
                        c1=1
                if(j!=0):
                    if(pb.board[i][j-1]=="x"):
                        c2=1
                if(i!=pb.height-1):
                    if(pb.board[i+1][j]=="x"):
                        c3=1
                if(j!=pb.width-1):
                    if(pb.board[i][j+1]=="x"):
                        c4=1
                #if((c1+c3)==2 or (c2+c4)==2):
                #    pass    
                if(c1==1):
                    opt = list(filter(pb.canLaunch,[pb.getCode((i+1,j)), pb.getCode((i-2,j))]))
                    if(len(opt)!=0):
                        return random.choice(opt)
                if(c2==1):
                    opt = list(filter(pb.canLaunch,[pb.getCode((i,j+1)), pb.getCode((i,j-2))]))
                    if(len(opt)!=0):
                        return random.choice(opt)
                if(c3==1):
                    opt = list(filter(pb.canLaunch,[pb.getCode((i-1,j)), pb.getCode((i+2,j))]))
                    if(len(opt)!=0):
                        return random.choice(opt)
                if(c4==1):
                    opt = list(filter(pb.canLaunch,[pb.getCode((i,j-1)), pb.getCode((i,j+2))]))
                    if(len(opt)!=0):
                        return random.choice(opt)
                else:
                    opt = list(filter(pb.canLaunch, [pb.getCode((i+1,j)), pb.getCode((i,j+1)), pb.getCode((i-1,j)), pb.getCode((i,j-1))]))
                    if(len(opt)!=0):
                        return random.choice(opt)
    #Reaches this portion if there are no ships that have been partly damaged but not sunken
    #Keeps track of where cpu has fired missiles, to spread out locations across the board.
    quad1 = 0
    quad2 = 0
    quad3 = 0
    quad4 = 0
    for i in range(0, pb.height):
        for j in range(0, pb.width):
            if(pb.board[i][j]=="o"):
                if(i>=0 and i<pb.height//2):
                    if(j>=0 and j<pb.width//2):
                        quad1=quad1+1
                    else:
                        quad2=quad2+1
                else:
                    if(j>=0 and j<pb.width//2):
                        quad3=quad3+1
                    else:
                        quad4=quad4+1
    d = {"q1":quad1, "q2":quad2, "q3":quad3, "q4":quad4}
    order = sorted(d.items(),key=lambda x: x[1])
    pic = random.choice(order[0:2])
    if(quad1==quad2 and quad2==quad3 and quad3==quad4):
        x = random.randint(0,pb.height-1)
        y = random.randint(0,pb.width-1)
        return pb.getCode((x,y))
    if(pic[0]=="q1"):
        x = random.randint(0,pb.height//2-1)
        y = random.randint(0,pb.width//2-1)
        return pb.getCode((x,y))
    elif(pic[0]=="q2"):
        x = random.randint(0,pb.height//2-1)
        y = random.randint(pb.width//2,pb.width-1)
        return pb.getCode((x,y))
    elif(pic[0]=="q3"):
        x = random.randint(pb.height//2,pb.height-1)
        y = random.randint(0,pb.width//2-1)
        return pb.getCode((x,y))
    elif(pic[0]=="q4"):
        x = random.randint(pb.height//2,pb.height-1)
        y = random.randint(pb.width//2,pb.width-1)
        return pb.getCode((x,y))

def playGame(pb,cb,d):
    """Plays a game of Battleship"""
    while(not pb.sunkenShips() and not cb.sunkenShips()):
        val = menu()
        if(val==1):
            pass
        elif(val==2):
            print(rules())
        elif(val==3):
            res = load_game("gamefile.txt")
            pb.board = res[0]
            cb.board = res[1]
        elif(val==4):
            save_game(pb,cb,"gamefile.txt")
        elif(val==5):
            return
        print(pb.userview())
        print(cb.opponentview())
        #player move
        print("Your turn!")
        s1="!-1"
        while(not cb.canLaunch(s1)):
            s1 = input("Enter the valid location you wish to fire a missile on the opponents board: ")
        cb.launchMissile(s1)
        #opponent move
        print("Opponents turn!")
        s2="!-1"
        while(not pb.canLaunch(s2)):
            if(d=="easy"):
                s2= cpusimplemove(pb)
            elif(d=="hard"):
                s2= cpusmartmove(pb)
        pb.launchMissile(s2)
        print(pb.userview())
        print(cb.opponentview())
        
    print(pb.userview())
    print(cb.opponentview())
    print("Game!")
    if(pb.sunkenShips()):
        print("Computer wins!")
    elif(cb.sunkenShips()):
        print("You win!")
    else:
        print("Draw!")
            
def save_game(pb, cb, filename):
        """ save to a file """
        f = open(filename,"w")  # open file for writing
        print(pb.board,file=f)
        print(cb.board,file=f)
        f.close()
        print(filename, " saved.")


def load_game(filename):
        """ load from a file """
        f = open(filename,"r")  # open file for reading
        data1 = eval(f.readline())   # evaluate the results as a Python object
        data2 = eval(f.readline())
        f.close()
        print(filename, " loaded.")
        return (data1,data2)

if __name__ == '__main__':
    main()
