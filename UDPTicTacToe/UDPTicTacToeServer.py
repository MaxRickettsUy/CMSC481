#original code is python 2.7 syntax
from socket import *
import threading

class playerStats:

    def __init__(self, currentPlayer, boardIsFull, isWinner, gameInSession):
        self.currentPlayer = currentPlayer
        self.boardIsFull = boardIsFull
        self.isWinner = isWinner
        self.gameInSession = gameInSession

    def setStats(self, playerStat, boardStat, winnerStat, gameStat):
        self.currentPlayer = playerStat
        self.boardIsFull = boardStat
        self.isWinner = winnerStat
        self.gameInSession = gameStat

    def setCurrentPlayer(self, playerStat):
        self.currentPlayer = playerStat

    def setBoardIsFull(self, boardStat):
        self.boardIsFull = boardStat

    def setIsWinner(self, winnerStat):
        self.isWinner = winnerStat

    def setGameInSession(self, gameStat):
        self.gameInSession = gameStat

    def getCurrentPlayer(self):
        return self.currentPlayer

    def getBoardIsFull(self):
        return self.boardIsFull

    def getIsWinner(self):
        return self.isWinner

    def getGameInSession(self):
        return self.gameInSession

    def getIndex(self):
        return self.index

#end playerStat class

#global variable containing number of clients, also used for client index
numClients = 0

#dictionary containing information for each client with an ongoing game with server
clientDict = {} #key = single int ex. 1, 10, 60, etc || value = ip address and socket of client

#dictionary containing gameboard for each game between server and client
boardDict = {}  #key = single int || value = gameboard for client game

#dictionary containing game stats for each client
gameDict = {} #key = single int corresponding to clientDict || value = player object

#this function displays the current board to the
#client after each turn by the client and server
def printBoard(board):
    print("   |" + str(board[0]) + "|" + str(board[1]) + "|" + str(board[2]) + "|")
    print("   |" + str(board[3]) + "|" + str(board[4]) + "|" + str(board[5]) + "|")
    print("   |" + str(board[6]) + "|" + str(board[7]) + "|" + str(board[8]) + "|")

def checkWinner(gameBoard):

    winner = checkDiagonal(gameBoard)

    if (winner == 0):
        return "0"
    elif(winner == 1):
        return "1"
    else:
        winner = checkHorizontal(gameBoard)
        if (winner == 0):
            return "0"
        elif (winner == 1):
            return "1"
        else:
            winner = checkVertical(gameBoard)
            if (winner == 0):
                return "0"
            elif (winner == 1):
                return "1"

            else:
                return "2"

def checkDiagonal(gameBoard):
    #top-left corner to bottom-right
    if(gameBoard[0] == 0 and gameBoard[4] == 0 and gameBoard[8] == 0):
        return 0
    elif (gameBoard[0] == 'X' and gameBoard[4] == 'X' and gameBoard[8] == 'X'):
        return 1

    #bottom-left corner to top-right corner
    elif (gameBoard[2] == 0 and gameBoard[4] == 0 and gameBoard[6] == 0):
        return 0
    elif (gameBoard[2] == 'X' and gameBoard[4] == 'X' and gameBoard[6] == 'X'):
        return 1

    else:
        return 2

def checkVertical(gameBoard):

    #first column
    if(gameBoard[0] == 0 and gameBoard[3] == 0 and gameBoard[6] == 0):
        return 0
    elif(gameBoard[0] == 'X' and gameBoard[3] == 'X' and gameBoard[6] == 'X'):
        return 1

    #second column
    elif(gameBoard[1] == 0 and gameBoard[4] == 0 and gameBoard[7] == 0):
        return 0
    elif(gameBoard[1] == 'X' and gameBoard[4] == 'X' and gameBoard[7] == 'X'):
        return 1


    #third column
    elif(gameBoard[2] == 0 and gameBoard[5] == 0 and gameBoard[8] == 0):
        return 0
    elif(gameBoard[2] == 'X' and gameBoard[5] == 'X' and gameBoard[8] == 'X'):
        return 1

    else:
        return 2


def checkHorizontal(gameBoard):

    #first row
    if(gameBoard[0] == 0 and gameBoard[1] == 0 and gameBoard[2] == 0):
        return 0
    elif(gameBoard[0] == 'X' and gameBoard[1] == 'X' and gameBoard[2] == 'X'):
        return 1

    #second row
    if(gameBoard[3] == 0 and gameBoard[4] == 0 and gameBoard[5] == 0):
        return 0
    elif(gameBoard[3] == 'X' and gameBoard[4] == 'X' and gameBoard[5] == 'X'):
        return 1

    #third row
    if(gameBoard[6] == 0 and gameBoard[7] == 0 and gameBoard[8] == 0):
        return 0
    elif(gameBoard[6] == 'X' and gameBoard[7] == 'X' and gameBoard[8] == 'X'):
        return 1

    else:
        return 2

def checkFullBoard(gameBoard):

    fullBoard = True

    for i in range(0,9):
        if (gameBoard[i] == '_'):
            fullBoard = False

    if(fullBoard == True):
        return "1"
    elif(fullBoard == False):
        return "0"

def serverStrat(gameBoard):

    if gameBoard[0] == '_':
        return 0

    if gameBoard[1] == '_':
        return 1

    if gameBoard[2] == '_':
        return 2

    if gameBoard[3] == '_':
        return 3

    if gameBoard[4] == '_':
        return 4

    if gameBoard[5] == '_':
        return 5

    if gameBoard[6] == '_':
        return 6

    if gameBoard[7] == '_':
        return 7

    else:
        return 8

def updateDictionaries(clientIndex,gameBoard,clientAddress):

    #clientDict --> clientIndex = clientaddress

    clientDict[clientIndex] = clientAddress

    #boardDict --> clientIndex = gameBoard

    boardDict[clientIndex] = gameBoard

def returnKey(dictName,client_Address):

    print("inside returnKey")

    if(dictName == "game"):
        print("dictName: " + dictName)
        for index, clientAddress in gameDict.items():
            print("index: " + str(index)
            + "value: ", clientAddress)
            if clientAddress == client_Address:
                print("index: " + str(index))
                return index

    elif(dictName == "client"):
        print("dictName: " + dictName)
        for index, clientAddress in clientDict.items():
            if clientAddress == client_Address:
                print("index: " +str(index))
                return index

    elif(dictName == "board"):
        print("dictName: " + dictName)
        for index, clientAddress in boardDict.items():
            if clientAddress == client_Address:
                print("index: " + str(index))
                return index


def createClient(serverSocket,clientAddress):

    print("Welcome! Setting up game environment.")

    #create blank board for new game
    gameBoard = ['_'] * 9

    #by default server is first player
    currentPlayer = 0

    #increment numClients interacting with server
    #count begins at 1
    global numClients

    numClients = numClients + 1

    clientIndex = numClients

    #print("current client index: " + str(clientIndex))

    #create new entry in clientDict to contain and keep track of current client
    clientDict[clientIndex] = clientAddress

    gameInSession = True

    boardIsFull = False

    isWinner = False

    newPlayer = playerStats(currentPlayer,boardIsFull,isWinner,gameInSession)

    #create new entry to keep track of gameplay for each client
    updateDictionaries(clientIndex,gameBoard,clientAddress)

    #create new entry in gameDict for client
    gameDict[clientIndex] = newPlayer

    print("Ready to go!")

    return

def startGame(serverSocket,clientAddress,firstPlayer,clientIndex):

    #determine if the firstPlayer argument is the client
    #firstPlayer is client
    if(firstPlayer == "-c"):
        print("The client has elected to goes first!")
        firstPlayerMsg = "You have the first move!"
        serverSocket.sendto(firstPlayerMsg.encode(), clientAddress)
        currentPlayer = 1
        gameDict[clientIndex].setCurrentPlayer(currentPlayer)

    #firstPlayer is server
    else:
        print("The server has first move!")
        firstPlayerMsg = "The server goes first!"
        serverSocket.sendto(firstPlayerMsg.encode(), clientAddress)

    return

def serverMove(serverSocket,clientAddress,clientIndex):

    #retrieve gameBoard
    gameBoard = boardDict[clientIndex]

    printBoard(gameBoard)

    #retrieve current player
    #using player getter method
    currentPlayer = gameDict[clientIndex].getCurrentPlayer()

    print("current player: " + str(currentPlayer))

    #determine serverChoice by calling serverMove function
    serverChoice = serverStrat(gameBoard)

    #place '0' in gameboard list at serverChoice index
    gameBoard[serverChoice] = 0

    updateDictionaries(clientIndex,gameBoard,clientAddress)

    #send server's choice to client
    serverSocket.sendto(str(serverChoice).encode(), clientAddress)

    return

def clientMove(serverSocket,clientAddress,clientIndex,clientChoice):

    #print("inside clientMove")

    #retrieve gameboard
    gameBoard = boardDict[clientIndex]

    #place x in gameboard list using client choice value
    gameBoard[clientChoice] = "X"

    updateDictionaries(clientDict[clientIndex], gameBoard, clientAddress)

    serverSocket.sendto(("choice entered").encode(), clientAddress)

    #retrieve currentPlayer

    currentPlayer = gameDict[clientIndex].getCurrentPlayer()

    if currentPlayer == 0:

        currentPlayer = 1

    else:
        currentPlayer = 0

    #updateDictionaries(clientAddress, gameBoard, currentPlayer)
    updateDictionaries(clientIndex, gameBoard,clientAddress)

    return


def main():

    serverPort = 13037

    serverSocket = socket(AF_INET, SOCK_DGRAM)

    serverSocket.bind(('',serverPort))

    print("The server is ready to play")

    #receive and store firstPlayer chosen by client and ip address of client
    #firstPlayer, clientAddress = serverSocket.recvfrom(2048)

    clientMsg, clientAddress = serverSocket.recvfrom(2048)


    while True:

        #if a new client is trying to start a game
        if((clientMsg).decode() == "newclient"):

            print("new client: ", clientAddress)

            createClient(serverSocket,clientAddress)

            clientMsg, clientAddress = serverSocket.recvfrom(2048)

            print(clientMsg + "\n")

        #firstPlayer == server
        elif((clientMsg).decode() == "server"):

            print("client sending firstPlayer info")

            firstPlayer = clientMsg.decode()

            #retrieve client index
            clientIndex = returnKey("client", clientAddress)

            #set current player variable of client at the index
            gameDict[clientIndex].setCurrentPlayer(firstPlayer)

            startGame(serverSocket,clientAddress,firstPlayer,clientIndex)

            clientMsg, clientAddress = serverSocket.recvfrom(2048)

            print(clientMsg + "\n")

        #firstPlayer == client
        elif((clientMsg).decode() == "-c"):

            print("client sending firstPlayer info")

            firstPlayer = clientMsg.decode()

            clientIndex = returnKey("client", clientAddress)

            gameDict[clientIndex].setCurrentPlayer(firstPlayer)

            startGame(serverSocket,clientAddress,firstPlayer,clientIndex)

            clientMsg, clientAddress = serverSocket.recvfrom(2048)

            print(clientMsg + "\n")

        #def serverMove(serverSocket,clientAddress,clientIndex)
        elif((clientMsg).decode() == "serverMove"):

            print("server move")

            #retrieve client index
            clientIndex = returnKey("client", clientAddress)

            print("current clientIndex: " + str(clientIndex))

            serverMove(serverSocket,clientAddress,int(clientIndex))

            clientMsg, clientAddress = serverSocket.recvfrom(2048)

            print(clientMsg + "\n")

        elif((clientMsg).decode() == "checkWinner"):

            print("checking for winner")

            #retrieve index
            clientIndex = returnKey("client",clientAddress)

            #retrieve game board
            gameBoard = boardDict[clientIndex]

            winnerResponse = checkWinner(gameBoard)

            print("winnerResponse: " + winnerResponse)

            serverSocket.sendto(winnerResponse.encode(),clientAddress)

            clientMsg, clientAddress = serverSocket.recvfrom(2048)

            print(clientMsg + "\n")

        elif((clientMsg).decode() == "checkFullBoard"):

            print ("checking for full board")

            #retrieve index
            clientIndex = returnKey("client",clientAddress)

            #retrieve game board
            gameBoard = boardDict[clientIndex]

            fullBoardResponse = checkFullBoard(gameBoard)

            serverSocket.sendto(fullBoardResponse.encode(), clientAddress)

            clientMsg, clientAddress = serverSocket.recvfrom(2048)

            print(clientMsg + "\n")

        #client choice
        elif(isinstance(int((clientMsg).decode()), (int, long))):

            print("client move")

            clientChoice = int((clientMsg).decode())

            #retrieve client index
            clientIndex = returnKey("client", clientAddress)

            print("current clientIndex: " + str(clientIndex))

            clientMove(serverSocket,clientAddress,int(clientIndex),clientChoice)

            clientMsg, clientAddress = serverSocket.recvfrom(2048)

            print(clientMsg + "\n")

main()
