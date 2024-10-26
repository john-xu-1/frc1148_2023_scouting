import numpy # has matrix calculations
import TBA_Functions as tba
import pandas as pd




def coneNcubeOPR(event):   
    allTeam = tba.TBA_EventTeamsRaw(event)
    matches = tba.TBA_EventMatchKeys(event)# these are rthe event match keys
    
    # coneMatrix = [] 
    # cubeMatrix = []
    ampMatrix = []
    speakerMatrix = []
    teamMatrix = []
    ampCountMatrix = []
    speakerCountMatrix = []
    
    print ("len " + str(len(matches)) + " if this is zero that means matches isn't up")
    
    i = 0

    for match in matches:
        
        print (match)
        
        print (i)
        
        
        
        cur_match_data= tba.TBA_GetCurMatch(match)# ths gets the json of the match based on the matchkeys
        
        
        
        if (type(cur_match_data['score_breakdown']) is not type(None)):
         
            blueTeams = tba.GetBlueTeams(cur_match_data)
            print (i)
            
            
            
            redTeams = tba.GetRedTeams(cur_match_data)
            
            
            
            
            r = []
            for team in allTeam:
                if redTeams[0] == team or redTeams[1] == team or redTeams[2] == team:
                    r.append(1)
                else:
                    r.append(0)
            teamMatrix.append(r)
        
            b = []
            for team in allTeam:
                if blueTeams[0] == team or blueTeams[1] == team or blueTeams[2] == team:
                    b.append(1)
                else:
                    b.append(0)
            teamMatrix.append(b)
            
            

            
            BlueAmpPoints = tba.GetBlueTeleAmpPoints(cur_match_data)
            BlueTotalPoints = tba.GetBlueTele(cur_match_data)
            RedAmpPoints = tba.GetRedTeleAmpPoints(cur_match_data)
            RedTotalPoints = tba.GetRedTele(cur_match_data)
            
            
            BlueAmpCount = tba.GetBlueAmpCount(cur_match_data)
            BReg = tba.GetBlueSpeakerCount(cur_match_data)
            BAm = tba.GetBlueSpeakerAmpedCount(cur_match_data)
            BlueSpeakerCount = BReg+BAm
            
            RedAmpCount = tba.GetRedAmpCount(cur_match_data)
            RReg = tba.GetRedSpeakerCount(cur_match_data)
            RAm = tba.GetRedSpeakerAmpedCount(cur_match_data)
            RedSpeakerCount = RReg+RAm
            
            ampCountMatrix.append(BlueAmpCount)
            speakerCountMatrix.append(BlueSpeakerCount)
            
            ampCountMatrix.append(RedAmpCount)
            speakerCountMatrix.append(RedSpeakerCount)
            
            BlueSpeakerPoints = BlueTotalPoints-BlueAmpPoints
            
            ampMatrix.append(BlueAmpPoints)
            speakerMatrix.append(BlueSpeakerPoints)
            
            RedSpeakerPoints = RedTotalPoints-BlueAmpPoints
            
            ampMatrix.append(RedAmpPoints)
            
            speakerMatrix.append(RedSpeakerPoints)
                    
            # coneRedScore = 0
                    
            # for bottoms in redBototmPiece:
            #     if (bottoms == "Cone"):
            #         coneRedScore += 2
            
            # for middle in redMiddlePiece:
            #     if (middle == "Cone"):
            #         coneRedScore += 3
            
            # for top in redTopPiece:
            #     if (top == "Cone"):
            #         coneRedScore += 5
                
            # cubeMatrix.append([redTotalPiece - coneRedScore])
            
            # coneMatrix.append ([coneRedScore])
        
        
        
        
        # print(coneScore)
        # print (int(blueTotalPiece) - coneScore)
        
        
        
        
        #prettyPrint( TBA_MatchWinner(match))
        #we have the mathc data now, we fill in each match with the data, code not implemented yet
        
 
    
    teamMatrix = numpy.matrix(teamMatrix)
    # coneMatrix = numpy.matrix(coneMatrix)
    ampMatrix = numpy.matrix(ampMatrix)
    # cubeMatrix = numpy.matrix(cubeMatrix)
    speakerMatrix = numpy.matrix(speakerMatrix)
    
    ampCountMatrix = numpy.matrix(ampCountMatrix)
    
    speakerCountMatrix = numpy.matrix(speakerCountMatrix)
    
    pseudoinverse = numpy.linalg.pinv (teamMatrix)
    
    print("Shapes before multiplication:")
    print("pseudoinverse shape:", pseudoinverse.shape)
    print("ampMatrix shape:", ampMatrix.shape)    
    print (pseudoinverse)
    print (ampMatrix)
    
    ampCount = numpy.matmul(pseudoinverse,ampCountMatrix.T)
    
    speakerCount = numpy.matmul(pseudoinverse,speakerCountMatrix.T)
    
    print (ampCount)
    print (speakerCount)
    
    # pseudoinverse_reshaped = pseudoinverse.reshape((m, n))
    # ampMatrix_reshaped = ampMatrix.reshape((n, p))
    
    # coneOPR = numpy.matmul(pseudoinverse, coneMatrix)
    ampOPR = numpy.matmul(pseudoinverse,ampMatrix.T)
    # cubeOPR = numpy.matmul(pseudoinverse, cubeMatrix)
    speakerOPR = numpy.matmul(pseudoinverse,speakerMatrix.T)
    
    # print (coneOPR)
    
    AmpCountArray = []
    
    speakerCountArray = []
    # coneArray = []
    ampArray = []
    # cubeArray = []
    speakerArray = []
    
    # for cone in coneOPR:
    #     coneArray.append(float(cone[0][0]))
    # for cube in cubeOPR:
    #     cubeArray.append(float(cube[0][0]))
    
    for count in ampCount:
        AmpCountArray.append(float(count[0][0]))
    
    for count in speakerCount:
        speakerCountArray.append(float(count[0][0]))
    
    for amp in ampOPR:
        ampArray.append(float(amp[0][0]))
    
    for speaker in speakerOPR:
        speakerArray.append(float(speaker[0][0]))
    
    # print (coneArray)
    # print (cubeArray)
    # print("alteam:"+str(len(allTeam)))
    # print("coneOP:"+str(len(coneArray)))
    # print("cubeOP:"+str(len(cubeArray)))

#temp fix so that the write to sheets can run    
    # noneArray = [0]*len(allTeam)
    
    # if((len(coneArray)<len(allTeam))):
    #     coneArray = noneArray
        
    # if((len(cubeArray)<len(allTeam))):
    #     cubeArray = noneArray
    
    # df = pd.DataFrame( {"team": allTeam, "coneOPR": coneArray, "cubeOPR": cubeArray})
    print ("unicornssssssss")
    print (len(allTeam))
    print (len(AmpCountArray))
    print (len(speakerCountArray))

    df = pd.DataFrame( {"team": allTeam, "ampOPR": ampArray, "speakerOPR": speakerArray, "Amps":AmpCountArray, "Speakers":speakerCountArray})

    print (df)
    return df
    

    

#coneNcubeOPR("2023cala")
# teamNames = []

# for i in range (0, len(team),1):
#     teamNames.append(tba.TBA_TeamNickname(team[i]))

# print (teamNames)

# df = pd.DataFrame ({'Names': teamNames, 'Number': team})

#print (df)


    
