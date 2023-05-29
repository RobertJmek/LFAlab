automat = {}
alfabet = []
stariFinale = []
stareInitiala = None

f = open("automat.txt", "r")
for line in f.readlines():
    line = line.strip('\n').split()
    tranzitii = dict()
    parsedLinie = [(line[i], line[i + 1]) for i in range(1, len(line) - 1, 2)]

    if "iF" in line[0]:
        stareInitiala = line[0][:-2]
        stariFinale.append(line[0][:-2])
        line[0] = line[0][:-2]
    elif line[0][-1] == "F":
        stariFinale.append(line[0][:-1])
        line[0] = line[0][:-1]
    elif line[0][-1] == "i":
        stareInitiala = line[0][:-1]
        line[0] = line[0][:-1]
    
    #If the current line starts with "iF", it updates stareInitiala to the current state, removes the "iF" suffix,
    # and adds the state to stariFinale. If the current line ends with "F", it removes the "F" suffix and adds the state to stariFinale. 
    # If the current line ends with "i", it updates stareInitiala to the current state and removes the "i" suffix.
    
    for tranzitie in parsedLinie:   
        if tranzitie[0] not in alfabet:
            alfabet.append(tranzitie[0])
            
    # It updates the alfabet list with all the unique input symbols found in the transitions.

    parsedLinie.append(('lambda', line[0])) # It adds a self-loop transition for the empty string lambda, mapping it to the current state.
    automat.update({line[0]: dict(parsedLinie)})
    
    # It adds the current state to the automat dictionary, with the transitions as a dictionary of dictionaries.

f.close()
#elimin starile inaccesibile
stariDeParcurs = [stareInitiala]
stariParcurse = []
while len(stariDeParcurs) != 0:
    stare = stariDeParcurs.pop(0)
    stariParcurse.append(stare)
    for litera in alfabet:
        if automat[stare][litera] not in stariParcurse and automat[stare][litera] not in stariDeParcurs:
            stariDeParcurs.append(automat[stare][litera])

#This section eliminates the unreachable states from the automat dictionary. 
# It initializes two lists, stariDeParcurs and stariParcurse, to keep track of 
# states to be processed and states that have been processed, respectively. It starts with the initial state and performs 
# a breadth-first search to find all reachable states. The reachable states are added to stariParcurse, and their transitions 
# are explored. If a state is found that has not been processed yet, 
# it is added to stariDeParcurs for further exploration. After this loop,
# only the reachable states remain in the automat dictionary.       
    
#print(stariParcurse)

#print(automat)

for stare in automat.copy():
    if stare not in stariParcurse:
        automat.pop(stare)

separabile = {stare:dict() for stare in automat.keys()}
#print(automat)

# This section builds a dictionary separabile, which stores the separable states for each state in the automat. 
# It iterates over each state in automat and checks for separability by comparing their behavior on all possible words of the alphabet. 
# If two states have different finality when following the same word, they are considered separable. 
# The separable pairs are added to the separabile dictionary.


lungime = 0
cuvinteDeParcurs = alfabet.copy()

maxN = max([int(x) for x in automat])
minN = min([int(x) for x in automat])

for i in range(maxN, minN - 1, -1):
    toAdd = []
    for j in range(i - 1, minN - 1, - 1):
        i = str(i)
        j = str(j)
        if i not in automat.keys() or j not in automat.keys():
            continue
        if (automat[i]['lambda'] in stariFinale and automat[j]['lambda'] not in stariFinale) or (automat[i]['lambda'] not in stariFinale and automat[j]['lambda'] in stariFinale):
            toAdd.append((j, 'lambda'))
    if i in automat.keys():
        separabile[str(i)].update(dict(toAdd)) #interpretarea este: i este separabil de j prin separabile[i][j], daca aleg dictionarul altfel sunt duplicate si nu pot avea lambda la mai multe

for _ in range(len(automat) + 2):
    for i in range(maxN, minN - 1, -1):
        if str(i) not in automat.keys():
            continue
        toAdd = []
        for j in range(i - 1, minN - 1, -1):
            if str(j) not in automat.keys():
                continue
            i = str(i)
            j = str(j)
            for cuvant in cuvinteDeParcurs:
                nod1 = i
                nod2 = j
                for litera in cuvant:
                    nod1 = automat[nod1][litera]
                    nod2 = automat[nod2][litera]
            
                if(nod1 in stariFinale and nod2 not in stariFinale) or (nod1 not in stariFinale and nod2 in stariFinale):
                    toAdd.append((j, cuvant))
        for tuplu in toAdd:
            if tuplu[0] not in separabile[str(i)]:
                separabile[str(i)].update({tuplu[0]: tuplu[1]})
    auxCuvinteDeParcurs = []
    for cuvant in cuvinteDeParcurs:
        for litera in alfabet:
            auxCuvinteDeParcurs.append(cuvant + litera)
    cuvinteDeParcurs = auxCuvinteDeParcurs.copy()
    
    #This section performs a refinement process to find the states that are indistinguishable in terms of their behavior on all possible words.
    # It uses a nested loop to compare each pair of states in the automat. For each pair and each word in cuvinteDeParcurs (initialized as the alphabet), 
    # it simulates the behavior of the pair on the word and checks if the resulting states have different finality. 
    # If they do, the pair is considered separable, and the separability information is added to the separabile dictionary. 
    # The list cuvinteDeParcurs is expanded by considering all possible concatenations of the original words with the alphabet.
    

#corectie pentru vid(unde nu pot fi separate => echivalente)
for i in range(maxN, minN - 1, -1):
    if str(i) not in automat.keys():
        continue
    for j in range(i - 1, minN - 1, -1):
        if str(j) not in automat.keys():
            continue
        i = str(i)
        j = str(j)
        if j not in separabile[i].keys():
            separabile[i][j] = 'vid'

newAutomat = dict()
stariConcatenate = []
for stare in separabile:
    if 'vid' in separabile[stare].values():
        for other in separabile[stare].keys():
            if 'vid' in separabile[stare][other]:
                newAutomat[other + "-" + stare] = {}
                stariConcatenate.append(other)
                stariConcatenate.append(stare)
    else:
        newAutomat[stare] = {}
        
    #This section handles the case where states cannot be separated by any word, i.e., they are equivalent.
    # It iterates over each pair of states and checks if they are already marked as separable in the separabile dictionary. 
    # If they are not, it marks them as inseparable by assigning the value 'vid' (empty string) to their separability relationship.

#elimin starile duplicate de genul 1, 1 2
for duplicate in stariConcatenate:
    try:
        newAutomat.pop(duplicate)
    except KeyError:
        continue

#folosesc tranzitivitatea pentru a verifica daca am cate 3 stari echivalente intr-un singur nod
auxAutomat = dict()
for newStare in newAutomat:
    if '-' in newStare:
        bigStare = set(newStare.split('-'))
        for othernewStare in newAutomat:
            if othernewStare == newStare:
                continue
            for stare in othernewStare.split('-'):
                if stare in bigStare:
                    for _ in othernewStare.split('-'):
                        bigStare.add(_)
                    break
        auxAutomat["-".join(sorted(bigStare))] = dict()
    else:
        auxAutomat[newStare] = dict()
newAutomat = auxAutomat

#This section constructs a new minimal automaton by merging the equivalent states. 
# It initializes an empty newAutomat dictionary and a stariConcatenate list to keep track of the states that need to be merged.
# It iterates over the separabile dictionary and identifies the states that can be merged into a single state. 
# It adds the merged state to newAutomat.

#print(newAutomat)

for newStare in newAutomat:
    for stare in newStare.split('-'):
        newAutomat[newStare] = automat[stare]

#newNotations = {'1':'1-2', '2': '1-2'}
newNotations = {}
for newStare in newAutomat:
    for stare in newStare.split('-'):
        newNotations[stare] = newStare

for newStare in newAutomat:
    for tranzitie in newAutomat[newStare].keys():
        try:
            newAutomat[newStare][tranzitie] = newNotations[newAutomat[newStare][tranzitie]]
        except KeyError: 
            pass
        
        

f = open("automat_minimal.txt", "w")

newStareInitiala = newNotations[stareInitiala]
newStariFinale = [newNotations[x] for x in stariFinale]

for node in newAutomat:
    newAutomat[node].pop('lambda')

auxCuvinteDeParcurs = alfabet.copy()
toPop = []
noPop = []
for _ in range(len(newAutomat) + 2):
    for stare in newAutomat:
        for cuvant in auxCuvinteDeParcurs:
            nod = stare
            for litera in cuvant:
                nod = newAutomat[nod][litera]
            if nod in newStariFinale:
                noPop.append(stare)
                break
    auxCuvinteDeParcurs = [x + y for x in auxCuvinteDeParcurs for y in alfabet]

for stare in newAutomat:
    if stare not in noPop:
        toPop.append(stare)
    
for stare in newAutomat:
    tranzitieToPop = []
    for tranzitie in newAutomat[stare]:
        if newAutomat[stare][tranzitie] in toPop:
            tranzitieToPop.append(tranzitie)
    for tranzitie in tranzitieToPop:
        newAutomat[stare].pop(tranzitie)

for stare in toPop:
    newAutomat.pop(stare)
    
    #This section removes unnecessary transitions from the newAutomat dictionary. 
    # It iterates over each state and checks if it leads to a final state. If it does, the state is marked as "noPop,"
    # indicating that it should not be removed. Otherwise, it is marked as "toPop," indicating that it should be removed.
    # After marking the states, it removes the unnecessary transitions from the dictionary.
    


for newStare in newAutomat:
    to_write = newStare
    if stareInitiala in newStare.split('-'):
        to_write += 'i'
    if newStare in newStariFinale:
        to_write += 'F'
    to_write += " "
    for newTranzitie in newAutomat[newStare]:
        to_write += newTranzitie + " " + newAutomat[newStare][newTranzitie] + " "
    f.write(to_write + '\n')

#This section writes the minimized automaton to the "automat_minimal.txt" file. 
# It iterates over each state in the newAutomat dictionary and writes the state,
# along with its transitions, to the file.

f.close()
input("DONE")