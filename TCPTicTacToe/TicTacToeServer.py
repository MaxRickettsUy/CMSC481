#original code is python 2.7 syntax
from socket import *
import threading

def checkWinner(gameBoard):

    winner = checkDiagonal(gameBoard)

    if (winner == 0):
        return 0
    elif(winner == 1):
        return 1
    else:
        winner = checkHorizontal(gameBoard)
        if (winner == 0):
            return 0
        elif (winner == 1):
            return 1
        else:
            winner = checkVertical(gameBoard)
            if (winner == 0):
                return 0
            elif (winner == 1):
                return 1

            else:
                return 2

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

    return fullBoard

def serverMove(gameBoard):

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

def handler (connectionSocket, addr):

    gameBoard = ['_'] * 9

    print ("Client connected. Address: " + str(addr))

    #receives clients first send, which contains the value for the firstPlayer
    #either -c or server
    firstPlayer = connectionSocket.recv(1024)

    #the player who is making the current move
    #0 = server, 1 = client
    currentPlayer = 0

    #determine if the firstPlayer argument is the client
    if(firstPlayer == "-c"):
        print("The client has elected to goes first!")
        firstPlayerMsg = "You have the first move!"
        connectionSocket.send(firstPlayerMsg)
        currentPlayer = 1

    else:
        print("The server has first move!")
        firstPlayerMsg = "The server goes first!"
        connectionSocket.send(firstPlayerMsg)
        #print 'The server is ready to receive\n'

    gameInSession = True

    isWinner = False

    while gameInSession:

        winner = checkWinner(gameBoard)

        if (winner == 0 or winner == 1):
            isWinner  = True

        # print ("Press Ctrl + C at anytime to exit")

        #if current player is server
        if currentPlayer == 0:

            if(isWinner == True):

                print "There is a winner"

                connectionSocket.send(str(-1))

                break


            else:

                serverChoice = serverMove(gameBoard)

                gameBoard[serverChoice] = 0

                connectionSocket.send(str(serverChoice))


        #if current player is client
        else:

            clientChoice = connectionSocket.recv(1024)

            if(clientChoice == "quit"):
                break

            else:

                gameBoard[int(clientChoice)] = "X"


        if currentPlayer == 0:

            currentPlayer = 1
        else:
            currentPlayer = 0

    while isWinner == True:

        msg = connectionSocket.recv(1024)

        if(msg == "winner"):

            connectionSocket.send(str(winner))

            closeMsg = connectionSocket.recv(1024)

            if(closeMsg == "bye"):
                print("Closing connection")
                break

    connectionSocket.close()


def main():

    serverPort = 13037

    serverSocket = socket(AF_INET,SOCK_STREAM)

    serverSocket.bind(('',serverPort))

    serverSocket.listen(1)

    print "Server listening for clients."

    #creates threads
    while True:
        connectionSocket, addr = serverSocket.accept()
        t = threading.Thread(target=handler, args = (connectionSocket, addr))
        t.start()

    connectionSocket.close()

main()
