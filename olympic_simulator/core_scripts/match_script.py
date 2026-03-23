import random

def get_prob(rank1, rank2, probs):
    dif = rank1 - rank2
    
    middle = len(probs)//2

    if dif > 0:
        return probs[max(middle - dif, 0):middle + 1][::-1][-1]
    elif dif < 0:
        return probs[middle:min(middle - dif + 1, len(probs))][-1]
    else:
        return probs[middle]
    
def generate_goal(prob):
    rand = random.random()
    if rand < prob:
        return 1
    else: 
        return 0
    
def generate_goal_bs(prob):
    rand = random.random()
    if rand < prob:
        return 1 + random.randint(1,3)
    else: 
        return 0
    
def get_list_of_probs(sport):
    sport = sport.replace(" Masculino","").replace(" Femenino","")    
    if sport in ['Futbol','Volleyball','Badminton','Tenis','Squash','Voley Playa','Tenis de Mesa','Tiro con Arco']:
        probs = [1/585, 1/475, 1/255, 1/184, 1/90, 1/60, 1/69, 1/50, 1/45, 1/34, 1/22, 1/9, 1/4]
    elif sport in ['Futsal', 'Hockey', 'Esgrima']:
        probs = [1/292, 1/237, 1/123, 1/92, 1/46, 1/35, 1/35, 1/25, 1/23, 1/17, 1/11, 1/5, 1/2]
    elif sport in ['Basketball','Rugby','Balonmano']:
        probs = [1/75.5, 1/55.5, 1/43.5, 1/35.5, 1/22.5, 1/17.5, 1/17.5, 1/12.5, 1/8.5, 1/5.5, 1/4.5, 1/2.5, 1/1.05]
    elif sport in ['Beisbol','Curling']:
        probs = [1/800, 1/650, 1/400, 1/290, 1/235, 1/225, 1/195, 1/185, 1/135, 1/110, 1/85, 1/65, 1/45]
    else:
        probs = [1/585, 1/475, 1/255, 1/184, 1/90, 1/60, 1/69, 1/50, 1/45, 1/34, 1/22, 1/9, 1/4]
    return probs

def simulate_match(rank1, rank2, probs):
    goals1 = 0
    goals2 = 0
    for i in range(90):
        goals1 += generate_goal(get_prob(rank1,rank2,probs))
        goals2 += generate_goal(get_prob(rank2,rank1,probs))

    return [goals1, goals2]

"""
n_matches = 300

vic1 = 0
vic2 = 0
draws = 0
timematch = 90

for j in range(n_matches):
    goals1 = 0
    goals2 = 0
    for i in range(timematch):
        goals1 += generate_goal(get_prob(1,6,probs))
        goals2 += generate_goal(get_prob(6,1,probs))
    if goals1 > goals2:
        vic1 += 1
    elif goals2 > goals1:
        vic2 += 1
    else:
        draws += 1
    print(str(j+1) + ": "+str(goals1) + " - " + str(goals2))
print("local: "+str(vic1)+", away: "+str(vic2)+", draws: "+str(draws) + ".")
print("local_rate: "+str((vic1/n_matches)*100)+"%, away_rate: "+str((vic2/n_matches)*100)+"%, draws_rate: "+str((draws/n_matches)*100)+"%", end=".")

vic1 = 0
vic2 = 0
draws = 0
timematch = 90

for j in range(n_matches):
    goals1 = 0
    goals2 = 0
    for i in range(timematch):
        goals1 += generate_goal(get_prob(1,6,probs_f))
        goals2 += generate_goal(get_prob(6,1,probs_f))
    if goals1 > goals2:
        vic1 += 1
    elif goals2 > goals1:
        vic2 += 1
    else:
        draws += 1
    print(str(j+1) + ": "+str(goals1) + " - " + str(goals2))
print("local: "+str(vic1)+", away: "+str(vic2)+", draws: "+str(draws) + ".")
print("local_rate: "+str((vic1/n_matches)*100)+"%, away_rate: "+str((vic2/n_matches)*100)+"%, draws_rate: "+str((draws/n_matches)*100)+"%", end=".")

vic1 = 0
vic2 = 0
draws = 0
timematch = 200
counter = 0
for j in range(n_matches):
    goals1 = 0
    goals2 = 0
    counter += 1
    for i in range(timematch):
        goals1 += generate_goal_bs(get_prob(2,2,probs_fs))
        goals2 += generate_goal_bs(get_prob(2,2,probs_fs))
        if goals1 == goals2 and counter == timematch:
            timematch += 50     

    if goals1 > goals2:
        vic1 += 1
    elif goals2 > goals1:
        vic2 += 1
    else:
        draws += 1
    print(str(j+1) + ": "+str(goals1) + " - " + str(goals2))
print("local: "+str(vic1)+", away: "+str(vic2)+", draws: "+str(draws) + ".")
print("local_rate: "+str((vic1/n_matches)*100)+"%, away_rate: "+str((vic2/n_matches)*100)+"%, draws_rate: "+str((draws/n_matches)*100)+"%", end=".")
"""
