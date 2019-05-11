import random as r
import sys
import time as t


def done():
    print("----------------------Protocol has been executed.------------------------")
    sys.exit(0)


def getPacket(packNo, senderPack, receiverPack):
    global NumberOfPackets, PacketGenTime, TransmissionTime, TimeoutTime, PackLossPerc, totTime

    if (packNo <= NumberOfPackets):
        t.sleep(PacketGenTime / 1000)
        print("\nS:\tPacket ", packNo, "is generated at time : ", totTime)
        (checkList[senderPack][0], checkList[senderPack][1]) = (packNo, totTime)
        (checkList[senderPack][2], checkList[senderPack][3]) = (0, 0)

        # Here we use the random library to generate a random number between 1 and 100 to
        # estimate the probability of a packet being lost.

        c = r.randint(1, 100)
        if (c <= PackLossPerc):
            print("S:\tPacket will be lost/Won't be transmitted\n")
            checkList[senderPack][3] = totTime + TimeoutTime
        else:
            print("S:\tPacket will be transmitted without loss\n")
            checkList[senderPack][2] = totTime + (2 * TransmissionTime)


def GoBackN():
    global NumberOfPackets, PacketGenTime, TransmissionTime, TimeoutTime, PackLossPerc, totTime

    # Initialize the sender and receiver packet numbers

    sendPacket = 0
    receiverPacket = 0
    packNo = 1
    while (1):
        TimedOut = False
        if (checkList[receiverPacket][2] <= totTime + PacketGenTime and checkList[receiverPacket][2] != 0):

            # The above condition checks if the 3rd columns (No loss case) time is greater than 0,
            # and if it is, it checks whether it is less than the total time, in which case it will
            # have been acknowledged, so we print that it has been acknowledged at that time.

            print("R:\tPacket ", checkList[receiverPacket][0], "has been acknowledged. Time = ",
                  checkList[receiverPacket][2])
            if (checkList[receiverPacket][0] >= NumberOfPackets):
                # Here we check if the number of the current packet is greater than or equal to the total
                # number of packets, in which case all packets are sent and we can terminate.

                done()

            # Our packet has been receieved without loss, so we increase the window over at receiever

            receiverPacket = receiverPacket + 1
        elif (checkList[receiverPacket][3] <= totTime + PacketGenTime and checkList[receiverPacket][3] != 0):

            # Here we see if the 4th column (Loss case) time is greater than 0, and if it is, we check whether the
            # the total time has reached to the point where this packet will be timed out, and then we print that
            # this packet has timedout and then slide the sender window back to this packet

            t.sleep((checkList[receiverPacket][3] - totTime) / 1000)
            print("R:\tTimed out! Packet", checkList[receiverPacket][0], "hasn't been acknowledged. Time = ",
                  checkList[receiverPacket][3])
            sendPacket = receiverPacket
            TimedOut = True
            packNo = checkList[receiverPacket][0]

        else:
            pass
        totTime = totTime + PacketGenTime
        if (TimedOut):
            totTime = checkList[receiverPacket][3]
        else:
            pass

        # After each iteration of the while loop, we generate the next packet continuously based on the sender and
        # receiever windows

        getPacket(packNo, sendPacket, receiverPacket)
        packNo = packNo + 1
        sendPacket = sendPacket + 1


print("Enter the parameters (in ms)")

# Taking input of all parameters

NumberOfPackets = int(input("Enter the number of packets to send : "))
PacketGenTime = int(input("Enter the time taken to generate a packet : "))
TransmissionTime = int(input("Enter the transmission time (assume it to be same from S->R and R->S) : "))
TimeoutTime = int(input("Enter the timeout time(Max time for ACK to arrive) : "))
PackLossPerc = int(input("Enter the chance that a packet can be lost (out of 100): "))
totTime = 0

# Generating our control data structure, checkList

checkList = [[int(0) for i in range(4)] for j in range(NumberOfPackets)]
print("Running the protocol......")

# Calling the protocol

GoBackN()
