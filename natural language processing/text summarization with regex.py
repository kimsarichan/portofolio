import re
with open("Chelsea vs Burnley.txt") as f:
    content = f.readlines()
event=['free kick', 'offside', 'subtitution', 'corner', 'miss attempt', 'attempt', 'blocked attempt',
'offside','yellow card', 'red card', 'assisted', 'goal']
add_time=re.compile(r'(\d*)\'\+(\d*)(.*)')

regex1= re.compile(r'(\d*)\'(free kick) ([a-z]*)([A-Z][a-z]*) (.*) \((.*)\).*')
regex1_1=re.compile(r'by (.*)')
regex2= re.compile(r'(\d*)\'([a-z]*)([A-Z][a-z]*) (.*)')
regex2_1=re.compile(r'(.*) \((.*)\).*')
regex3=re.compile(r'(\d*)\'(attempt) ([a-z]*)([A-Z][a-z]*) (.*)')
regex4=re.compile(r'(\d*)\'([a-z]*)[A-Z][a-z]*\, (.*)')
regex4_1=re.compile(r'(.*) replaces (.*)')
regex4_1_1=re.compile(r'(.*) because of (.*)')
regex4_2=re.compile(r'Conceded by (.*)')
regex4_3=re.compile(r'(.*) tries a through ball, but (.*) is caught offside')
regex5= re.compile(r'(\d*)\'(yellow|red) ([a-z]*)([A-Z][a-z]*) (.*) \((.*)\).*')
regex6= re.compile(r'(\d*)\'([a-z]*)([A-Z][a-z]*!) (.*) (\d*), (.*) (\d*)')
regex6_1=re.compile(r'(.*) \((.*)\)(.*)')
regex6_2=re.compile(r'(.*) by (.*)')
regex7= re.compile(r'(\d*)\'end (\d*)(.*), (.*) (\d*), (.*) (\d*)')

pre_processing=[]
for i in content:
    a= re.split('\.', re.sub('\n','',i))[:-1]
    if re.match(add_time,a[0]):
        #tambahan waktu
        menit1=int(re.sub(add_time ,r'\1',a[0]))
        menit2=int(re.sub(add_time ,r'\2',a[0]))
        event=re.sub(add_time ,r'\3',a[0])
        a[0]= str(menit1+menit2)+event
    if re.match(regex1,a[0]):
        #free kick
        menit= re.sub(regex1 ,r'\1 ',a[0])
        event= re.sub(regex1 ,r'\2 \3 ',a[0])
        cond= re.sub(regex1 ,r'\3',a[0])
        p= re.sub(regex1 ,r'\5',a[0])
        if(cond=="lost"):
            pemain= re.sub(regex1_1 ,r'\1 ',p)
        else:
            pemain= re.sub(regex1 ,r'\4 \5 ',a[0])
        team=re.sub(regex1 ,r'\6',a[0])
        dic={"event":event,"pemain":pemain,"team":team,"menit":int(menit),"cond":cond}
        pre_processing.append(dic)
    elif re.match(regex2,a[0]):
        #miss atempt
        menit= re.sub(regex2 ,r'\1 ',a[0])
        event= re.sub(regex2 ,r'\2 \3 ',a[0])
        pemain= re.sub(regex2_1 ,r'\1 ',a[1])
        team= re.sub(regex2_1 ,r'\2 ',a[1])
        if(len(a)==3):
            asssisted=re.sub(regex6_2,r'\2',a[2])
        else:
            asssisted=""
        dic={"event":event,"pemain":pemain,"team":team,"menit":int(menit),"asssisted":asssisted}
        pre_processing.append(dic)
    elif re.match(regex3,a[0]):
        #atempt
        menit= re.sub(regex3 ,r'\1',a[0])
        event= re.sub(regex3 ,r'\3 \4',a[0])
        pemain= re.sub(regex2_1 ,r'\1',a[1])
        team= re.sub(regex2_1 ,r'\2',a[1])
        if(len(a)==3):
            asssisted=re.sub(regex6_2,r'\2',a[2])
        else:
            asssisted=""
        dic={"event":event,"pemain":pemain,"team":team,"menit":int(menit),"asssisted":asssisted}
        pre_processing.append(dic)
    elif re.match(regex4,a[0]):
        #subtitution, corner,offside
        menit= re.sub(regex4 ,r'\1',a[0])
        event= re.sub(regex4 ,r'\2',a[0])
        team= re.sub(regex4 ,r'\3',a[0])
        if(event=="substitution"):
            player1=  re.sub(regex4_1 ,r'\1',a[1])
            player2=  re.sub(regex4_1 ,r'\2',a[1])
            if(re.match(regex4_1_1,player2)):
                cause= re.sub(regex4_1_1 ,r'\2',player2)
                player2=  re.sub(regex4_1_1 ,r'\1',player2)
            else:
                cause= ""
            dic={"event":event,"cause":cause,"subtitute":player1,"player":player2,"team":team,"menit":int(menit),"asssisted":asssisted}
            pre_processing.append(dic)
        elif(event=="corner"):
            player=  re.sub(regex4_2 ,r'\1',a[1])
            dic={"event":event,"player":player,"team":team,"menit":int(menit),"asssisted":asssisted}
            pre_processing.append(dic)
        elif(event=="offside"):
            player_tries=  re.sub(regex4_3 ,r'\1',a[1])
            player_offside=  re.sub(regex4_3 ,r'\1',a[1])
            dic={"event":event,"player_tries":player_tries,"player_offside":player_offside,
                 "team":team,"menit":int(menit)}
            pre_processing.append(dic)
    elif re.match(regex5,a[0]):
        #yellow and red card
        menit= re.sub(regex5 ,r'\1',a[0])
        event= re.sub(regex5 ,r'\2 card',a[0])
        team= re.sub(regex5 ,r'\6',a[0])
        player= re.sub(regex5 ,r'\4 \5',a[0])
        dic={"event":event,"player":player,
                 "team":team,"menit":int(menit)}
        pre_processing.append(dic)
    elif re.match(regex6,a[0]):
        #goal
        menit= re.sub(regex6 ,r'\1',a[0])
        event= re.sub(regex6 ,r'\2',a[0])
        team_a= re.sub(regex6 ,r'\4',a[0])
        score_a= re.sub(regex6 ,r'\5',a[0])
        team_b= re.sub(regex6 ,r'\6',a[0])
        score_b= re.sub(regex6 ,r'\7',a[0])
        goal_scorer= re.sub(regex6_1 ,r'\1',a[1])
        team_scorer = re.sub(regex6_1 ,r'\2',a[1])
        asssisted=re.sub(regex6_2,r'\2',a[2])
        event_goal=re.sub(regex6_1 ,r'\3',a[1])
        dic={"event":event,"goal_scorer":goal_scorer,"team_scorer":team_scorer,
                 "team_a":team_a,"score_a":score_a,"team_b":team_b,"score_b":score_b,"menit":int(menit),"asssisted":asssisted,
             "event_goal":event_goal}
        pre_processing.append(dic)
    elif re.match(regex7,a[0]):
        #end
        menit= re.sub(regex7 ,r'\1',a[0])
        event= re.sub(regex7 ,r'\3 half',a[0])
        winner= re.sub(regex7 ,r'\4',a[0])
        winner_score= re.sub(regex7 ,r'\5',a[0])
        loser= re.sub(regex7 ,r'\6',a[0])
        loser_score= re.sub(regex7 ,r'\7',a[0])
        dic={"menit":menit,"event":event,"winner_score":winner_score,"winner":winner,"loser":loser,"loser_score":loser_score}
        pre_processing.append(dic)

jumlah_attempt=0
jumlah_attempt_a=0
jumlah_attempt_b=0
goal_count=0
goal_count_loser = 0
yellow_count=0
red_count=0
yellow_count_loser=0
red_count_loser=0
freekicklost_winner=0
freekicklost_loser=0
freekickwin_winner=0
freekickwin_loser=0
count_sub=0
count_sub_lose=0
offside_winner=0
offside_loser=0
corner_winner=0
corner_loser=0
sub=""
sub_lose=""
injure_people=""
for i in pre_processing:
    if(i["event"]=="Second Half ends half"):
        winner_sehalf=i["winner"]
        lost_sehalf=i["loser"]
        winner_sehalf_score=i["winner_score"]
        lost_sehalf_score=i["loser_score"]
        time_game=i["menit"]
    elif(i["event"]=="First Half ends half"):
        winner_fihalf=i["winner"]
        lost_fihalf=i["loser"]
        winner_fihalf_score=i["winner_score"]
        lost_fihalf_score=i["loser_score"]
for i in pre_processing:
    if(i["event"]=="miss Attempt" or i["event"]=="blocked Attempt" or i["event"]=="saved Attempt" ):
        jumlah_attempt+=1
        if(i["team"]==winner_sehalf):
            jumlah_attempt_a+=1
        else:
            jumlah_attempt_b+=1
    elif(i["event"]=="goal"):
        if(i["team_scorer"]==winner_sehalf):
            goal_count+=1
            if(goal_count== int(winner_sehalf_score)):
                goal_winner=i["goal_scorer"]
                win_event=i["event_goal"]
            if(goal_count >1):
                goal_scorer=goal_scorer+", "+i["goal_scorer"]
                minute=minute+", "+str(i["menit"])
            else:
                goal_scorer=i["goal_scorer"]
                minute=str(i["menit"])
        else:
            goal_count_loser+=1
            if(goal_count_loser== lost_sehalf_score):
                    loser_best_goal=i["goal_scorer"]
            if(goal_count_loser >1):
                loser_goal_scorer=loser_goal_scorer+", "+i["goal_scorer"]
                minute_loser=minute_loser+", "+str(i["menit"])
            else:
                loser_goal_scorer=i["goal_scorer"]
                minute_loser=str(i["menit"])
    elif(i["event"]=="yellow card" or i["event"]=="red card"):
        if(i["team"]==winner_sehalf):
            if(i["event"]=="yellow card"):
                yellow_count+=1
                if(yellow_count ==1):
                    yellow_card_win=i["player"]
                else:
                    yellow_card_win=yellow_card_win+", "+i["player"]
            else:
                red_count+=1
                if(red_count ==1):
                    red_card_win=i["player"]
                else:
                    red_card_win=red_card_win+", "+i["player"]
        else:
            if(i["event"]=="yellow card"):
                yellow_count_loser+=1
                if(yellow_count_loser ==1):
                    yellow_card_lose=i["player"]
                else:
                    yellow_card_lose=yellow_card_lose+", "+i["player"]
            else:
                red_count_loser+=1
                if(red_count_loser ==1):
                    red_card_lose=i["player"]
                else:
                    red_card_lose=red_card_lose+", "+i["player"]
    elif(i["event"]=='free kick lost ' or i["event"]=='free kick won '):
        if(i["team"]==winner_sehalf):
            if(i["cond"]=="lost"):
                freekicklost_winner+=1
            else:
                freekickwin_winner+=1
        else:
            if(i["cond"]=="lost"):
                freekicklost_loser+=1
            else:
                freekickwin_loser+=1
    elif(i["event"]=="substitution"):
        if(i["team"]==winner_sehalf):
            count_sub+=1
            if(i["cause"]!=""):
                sub += i["subtitute"] + " replaces "+i["player"]+"<br>"
            else:
                sub += i["subtitute"] + " replaces "+i["player"]+"<br>"
        else:
            count_sub_lose+=1
            if(i["cause"]!=""):
                sub_lose += i["subtitute"] + " replaces "+i["player"]+"<br>"
            else:
                sub_lose += i["subtitute"] + " replaces "+i["player"]+"<br>"
                if(i["cause"]!="injury"):
                    injure_people+=i["subtitute"]+" is injury "+"<br>"
    elif(i["event"]=="offside"):
        if(i["team"]==winner_sehalf):
            offside_winner+=1
        else:
            offside_loser+=1
    elif(i["event"]=="corner"):
        if(i["team"]==winner_sehalf):
            corner_winner+=1
        else:
            corner_loser+=1
Title=winner_sehalf+" wins against "+lost_sehalf+" ("+winner_sehalf_score+"-"+lost_sehalf_score+")"
content_sumarize=""
with open("save.txt") as f:
    content_sumarize += "".join(f.readlines())
a= content_sumarize.replace("[winner]",winner_sehalf )
b= a.replace("[loser]",lost_sehalf )
c= b.replace("[time_game]",time_game )
if(jumlah_attempt_a>jumlah_attempt_b):
    d= c.replace("[most_attempt_team]",winner_sehalf )
    e= d.replace("[attempt_score]",str((jumlah_attempt_a*1.0/jumlah_attempt*1.0)*100) )
else:
    d= c.replace("[most_attempt_team]",lost_sehalf )
    e= d.replace("[attempt_score]",str((jumlah_attempt_b*1.0/jumlah_attempt*1.0)*100))
f= e.replace("[goal]",winner_score)
g= f.replace("[goal_scorer]",goal_scorer)
h= g.replace("[winner_scorer]",goal_winner)
final_paragraph= h.replace("[event]",win_event)

with open('newarticle.html', 'w') as myFile:
    myFile.write('<html>')
    myFile.write('<body>')
    myFile.write('<h2>'+Title+'</h2>')
    myFile.write('<p>'+final_paragraph+'</p>')
    myFile.write('<h4>Free Kick :</h4>')
    myFile.write('<h5>Free Kick Lost :</h5>')
    myFile.write('<p> Free Kick Lost from '+winner_sehalf+': '+str(freekicklost_winner)+'</p>')
    myFile.write('<p> Free Kick Lost from '+lost_sehalf+': '+str(freekicklost_loser)+'</p>')
    myFile.write('<h5>Free Kick Win :</h5>')
    myFile.write('<p> Free Kick Win from '+winner_sehalf+': '+str(freekickwin_winner)+'</p>')
    myFile.write('<p> Free Kick Win from '+lost_sehalf+': '+str(freekickwin_loser)+'</p>')
    myFile.write('<h4>Yellow Card :</h4>')
    myFile.write('<p> yellow card from '+winner_sehalf+': '+str(yellow_count)+'('+yellow_card_lose+')</p>')
    myFile.write('<p> yellow card from '+lost_sehalf+': '+str(yellow_count_loser)+'('+yellow_card_lose+')</p>')
    myFile.write('<h4>Corner :</h4>')
    myFile.write('<p> Corner from '+winner_sehalf+': '+str(corner_winner)+'</p>')
    myFile.write('<p> Corner from '+lost_sehalf+': '+str(corner_loser)+'</p>')
    myFile.write('<h4>Offside :</h4>')
    myFile.write('<p> Offside from '+winner_sehalf+': '+str(offside_winner)+'</p>')
    myFile.write('<p> Offside from '+lost_sehalf+': '+str(offside_loser)+'</p>')
    myFile.write('<h4>Subtitution :</h4>')
    myFile.write('<p> Sub from '+winner_sehalf+'</p>')
    myFile.write('<p> '+sub+'</p>')
    myFile.write('<p> Sub from '+lost_sehalf+'</p>')
    myFile.write('<p> '+sub_lose+'</p>')
    myFile.write('<h4>Injury :</h4>')
    myFile.write('<p> '+injure_people+'</p>')
    myFile.write('</body>')
    myFile.write('</html>')
