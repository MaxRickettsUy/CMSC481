#File: TicTacToeClient.py
#Author:Max Ricketts-Uy
from socket import *
import sys

#list to represent tic tac toe board
#each element is X or 0 on board
gameBoard = ['_'] * 9

#the 9 locations on the tic tac toe board
boardOptions = ["row 1, col 1", "row 1, col 2", "row 1, col 3", "row 2, col 1", "row 2, col 2",
                "row 2, col 3", "row 3, col 1", "row 3, col 2", "row 3, col 3"]

#each element corresponds to a location on the board
#if the element is 0, the location is available
#elif 1, the spot is taken
remainingOptions = [0,0,0,0,0,0,0,0,0]

#this function displays the current board to the
#client after each turn by the client and server
def printBoard(board):
    print("   |" + str(board[0]) + "|" + str(board[1]) + "|" + str(board[2]) + "|")
    print("   |" + str(board[3]) + "|" + str(board[4]) + "|" + str(board[5]) + "|")
    print("   |" + str(board[6]) + "|" + str(board[7]) + "|" + str(board[8]) + "|")

#prints the remaining spots on the board available to the client
def printOptions(boardOptions,remainingOptions):
    for i in range (0, 9):
        if(remainingOptions[i] == 0):
            print(str(i) + " = " + boardOptions[i])
        if((i+1) % 3 == 0 and i != 8):
            print ("------------")

def checkWinner(clientSocket,serverName,serverPort):

    winner = ""
    isWinner = False

    #after each serverMove check for winner
    clientSocket.sendto(("checkWinner").encode(), (serverName, serverPort))

    winnerResponse, clientInfo = clientSocket.recvfrom(2048)

    #print("winner response: " + winnerResponse)

    if (winnerResponse.decode() == "0" or winnerResponse.decode() == "1"):

        isWinner = True

        winner = winnerResponse

    return (isWinner, winner)

def checkBoardIsFull(clientSocket,serverName,serverPort):

    boardIsFull = False

    clientSocket.sendto(("checkFullBoard").encode(), (serverName, serverPort))

    fullBoardResponse, clientInfo = clientSocket.recvfrom(2048)

    #print("fullBoardResponse: " + fullBoardResponse)

    if(fullBoardResponse == "1"):
        boardIsFull = True

    #print(boardIsFull)

    return (boardIsFull)

def clientMove(clientSocket,serverName,serverPort,isWinner,boardIsFull):

    winner = ""

    print ("\n"
        + "Enter the digit corresponding the board location (Ex. 0 = row 1, col 1):"
        + "\n")

    printOptions(boardOptions,remainingOptions)

    print("\nThe current board\n")

    printBoard(gameBoard)

    clientChoice = input('\nenter choice (0-8):')

    while(clientChoice < 0 or clientChoice > 8 ):
        clientChoice = input("\nPlease enter a choice between 0 and 8: ")

    #place 'X' in gameboard list at clientChoice index
    gameBoard[clientChoice] = "X"

    remainingOptions[clientChoice] = 1

    #send client choice to server
    clientSocket.sendto(str(clientChoice).encode(), (serverName, serverPort))

    choiceResponse, clientInfo = clientSocket.recvfrom(2048)

    #check winner

    isWinner,winner = checkWinner(clientSocket,serverName,serverPort)

    #check for full board

    boardIsFull = checkBoardIsFull(clientSocket,serverName,serverPort)

    return(isWinner,boardIsFull,winner)

def serverMove(clientSocket,serverName,serverPort,isWinner,boardIsFull):

    winner = ""

    clientSocket.sendto(("serverMove").encode(),(serverName,serverPort))

    #receive server's choice
    serverChoice = clientSocket.recv(1024)

    remainingOptions[int(serverChoice.decode())] = 1

    gameBoard[int(serverChoice.decode())] = 0

    print("\nThe server chose " + boardOptions[int(serverChoice.decode())] + "\n")

    #after each serverMove check for winner

    isWinner, winner = checkWinner(clientSocket, serverName, serverPort)

    #print("winner response: " + winner)

    boardIsFull = checkBoardIsFull(clientSocket,serverName,serverPort)

    sentence = raw_input("It is your move.\n")

    return(isWinner,boardIsFull,winner)

def main():

    #by default server is the first player
    currentPlayer = 0

    #determine if user has enter -c
    #if they have not, the firstPlayer name is server
    #as the server will be going first
    if len(sys.argv) == 2:
        firstPlayer = "server"
        serverName = str(sys.argv[1])

    #if -c was entered the client will go first
    else:
        #arg 1 = "-c"
        firstPlayer = str(sys.argv[1])
        serverName = str(sys.argv[2])
        currentPlayer = 1

    serverPort = 13037

    clientSocket = socket(AF_INET, SOCK_DGRAM)

    clientMsg = "newclient"

    #send "newclient" message for server to create new entry for this client
    clientSocket.sendto(clientMsg.encode(),(serverName, serverPort))

    if(currentPlayer == 0):
        clientMsg = "serverMove"
    else:
        clientMsg = "clientmove"

    #print("first player: " + firstPlayer)

    #send firstPlayer data to server
    clientSocket.sendto(firstPlayer.encode(),(serverName,serverPort))

    #recieve message telling client who has the first move and their index
    #the index is needed by the server to keep track of the client
    firstPlayerMsg, clientInfo = clientSocket.recvfrom(2048)

    print(firstPlayerMsg)

    #basic information for client
    print ("Your symbol will be X. The server's symbol is 0.\n" +
            "Each turn you will be prompted to choose from the" +
            "remaining positions on the board.")

    #displays current board which at first is "blank"
    print("\nThe current board:\n")
    printBoard(gameBoard)

    isWinner = False
    boardIsFull = False
    winner = ""

    print("\nYou are ready to play.\n")

    while (isWinner == False and boardIsFull == False):

        #if currentPlayer == 0, server is current player
        if (currentPlayer == 0):
            isWinner,boardIsFull,winner = serverMove(clientSocket,serverName,serverPort,isWinner,boardIsFull)

        #client move
        else:
            isWinner,boardIsFull,winner = clientMove(clientSocket,serverName,serverPort,isWinner,boardIsFull)

        if(currentPlayer == 0):
            currentPlayer = 1
        else:
            currentPlayer = 0

    while isWinner == True:

        if(winner == "0"):
            print("The server won.")
        elif(winner == "1"):
            print("You won!")

        printBoard(gameBoard)

        break

    while boardIsFull == True:

        print("board is full with no winner. game over")

        printBoard(gameBoard)

        break

    clientSocket.close()


main()
