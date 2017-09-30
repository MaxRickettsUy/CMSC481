#File: TicTacToeClient.py
#Author:Max Ricketts-Uy

from socket import *
import sys


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

def main():

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

    currentPlayer = 0

    #determine if user has enter -c
    #if they have not, the firstPlayer name is server
    #as the server will be going first
    if len(sys.argv) == 2:
        firstPlayer = "server"
        serverName = str(sys.argv[1])

    #if -c was entered the client will go first
    else:
        firstPlayer = str(sys.argv[1])
        serverName = str(sys.argv[2])
        currentPlayer = 1
    
    serverPort = 13037

    clientSocket = socket(AF_INET, SOCK_STREAM)

    clientSocket.connect((serverName,serverPort))

    #first send first player character
    clientSocket.send(firstPlayer)

    #recieve message telling client who has the first move
    firstPlayerMsg = clientSocket.recv(1024)

    #displays the first player
    print 'From server:', firstPlayerMsg

    #basic information for client
    print ("Your symbol will be X. The server's symbol is 0.\n" +
            "Each turn you will be prompted to choose from the remaining positions on the board.")

    #displays current board which at first is "blank"
    print("\nThe current board:\n")
    printBoard(gameBoard)

    sentence = raw_input("\nWould you like to play? (press enter to continue; enter 'quit' to exit): ")

    isWinner = False
    boardIsFull = False

    while sentence != "quit":

        #if the server has the first turn, it will have already made its move
        #and the current board will be printed
        if (currentPlayer == 0):

            serverChoice = clientSocket.recv(1024)

            # print serverChoice

            if (serverChoice == "-1"):
                isWinner = True

                # print("Someone has won")

                # winner = serverChoice.split()
                #
                # if(winner[2] == "1"):
                #     print("You won!")
                # else:
                #     print("The server won!")

                break

            elif (serverChoice == "-2"):

                boardIsFull = True

                break


            else:

                remainingOptions[int(serverChoice)] = 1

                gameBoard[int(serverChoice)] = 0

                print("\nThe server chose " + boardOptions[int(serverChoice)] + "\n")

                currentPlayer = 1  #client has the next move

                sentence = raw_input("It is your move.\n")

        #if the client is going first they will be prompted to choose their first
        #spot on the board
        else:
            print ("\n" +
                "Enter the digit corresponding the board location (Ex. 0 = row 1, col 1): \n")
            printOptions(boardOptions,remainingOptions)
            #sentence = raw_input("Would you like to continue playing? (enter anything to continue and 'quit' to exit): ")

            print("\nThe current board\n")

            printBoard(gameBoard)

            clientChoice = input('\n(enter choice (0-9):')

            while(clientChoice < 0 or clientChoice > 8 ):
                clientChoice = input("\nPlease enter a choice between 0 and 9: ")

            gameBoard[clientChoice] = "X"

            remainingOptions[clientChoice] = 1

            clientSocket.send(str(clientChoice))

            currentPlayer = 0 #server has the next move

        sentence = raw_input("Would you like to continue playing? (press enter to continue; enter 'quit' to exit): ")

    while isWinner == True:

        # print "inside loop"

        clientSocket.send("winner")

        winner = clientSocket.recv(1024)

        # print winner

        printBoard(gameBoard)

        if(winner == "1"):
            print("You won")
        else:
            print("The server won")

        clientSocket.send("bye")

        break

    while boardIsFull == True:

        clientSocket.send("board full?")

        response = clientSocket.recv(1024)

        printBoard(gameBoard)

        print(response)

        clientSocket.send("bye")

        break

    clientSocket.close()

main()
