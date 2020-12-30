# -*- coding: utf-8 -*-
import random
import itertools as it
import json

class SakClass:
    letter_dict = {'Α':[12,1],'Β':[1,8],'Γ':[2,4],'Δ':[2,4],'Ε':[8,1],
                        'Ζ':[1,10],'Η':[7,1],'Θ':[1,10],'Ι':[8,1],'Κ':[4,2],
                        'Λ':[3,3],'Μ':[3,3],'Ν':[6,1],'Ξ':[1,10],'Ο':[9,1],
                        'Π':[4,2],'Ρ':[5,2],'Σ':[7,1],'Τ':[8,1],'Υ':[4,2],
                        'Φ':[1,8],'Χ':[1,8],'Ψ':[1,10],'Ω':[3,3]}
    def __init__(self):
        self.sak = SakClass.letter_dict
        self.amount_of_letters = self.calculateAmountOfLetters()

    def calculateAmountOfLetters(self):
        s = 0
        for x in self.sak.values():
            s += x[0]
        return s
    
    def randomizeSak(self, letter_list, n=7):
        random.shuffle(letter_list) #Ανακατέβει τη λιστα
        new_list = random.sample(letter_list,n)
        return new_list

    def checkAmount(self, n):
        if n <= self.amount_of_letters:
            return True
        else:
            return False

    def getLetters(self, n=7):
        letter_list = []
        for x in self.sak:
           for j in range(self.sak.get(x)[0]):
               letter_list.append(x) #Πάρε όλα τα γράμματα στο σακουλάκι και βάλε τα σε μία λίστα
        random_letters = self.randomizeSak(letter_list, n) #Πάρε την νέα λίστα
        self.amount_of_letters -= random_letters.__len__() #Μείωσε το συνολικό αριθμό των γραμμάτων στο σακουλάκι
        for x in random_letters:
            self.sak.get(x)[0] -= 1 #Μείωσε τον αριθμό του γράμμάτων της νέας λίστας
        return random_letters
        
    def putBackLetters(self, letter_list):
        self.amount_of_letters += letter_list.__len__() #Αύξησε τον αριθμό των συνολικών γραμμάτων στο σακουλάκι
        for x in letter_list:
            self.sak.get(x)[0] += 1 #Αύξησε τον αριθμό των γραμμάτων που έβαλες πίσω στο σακουλάκι
        
class Player:
    def __init__(self, sak):
        self.letters = sak.getLetters()
        
    def __repr__(self):
        return ("Player")
    
    def play(self, amount_of_letters):
        print("Στο σακουλάκι: ", amount_of_letters, " γράμματα - ", self)
        if isinstance(self, Computer):
            print("Γράμματα Η/Υ: ", end = ' ')
        else:
            print("Διαθέσιμα γράμματα:", end = ' ')
        i = 0
        for x in self.letters:
            if i != self.letters.__len__()-1:
                print(x, SakClass.letter_dict.get(x)[1], sep = ',',end = ' - ')
                i += 1
        print(self.letters[i], SakClass.letter_dict.get(x)[1], sep = ',')
    
class Human(Player):
    def __init__(self, sak):
        Player.__init__(self, sak)
        
    def __repr__(self):
        return("Σειρά σου:")
        
    def play(self, letter_sak):
        Player.play(self, letter_sak.amount_of_letters)
        while True:
            print("Λέξη:",end = ' ')
            w = input()
            if w.__len__() > 7:
                print("Η λέξη πρεπει να είναι μέχρι 7 χαρακτήρες")
                continue
            if w == 'p':
                if letter_sak.checkAmount(7):
                    temp_list = self.letters
                    self.letters = letter_sak.getLetters() #Παίρνει νέα γράμματα
                    letter_sak.putBackLetters(temp_list) #Βάζει τα τρέχοντα πίσω στο σακουλάκι
                    return "pass"
                else:
                    return "end"
            elif w == 'q':
                return "end"
            else:
                flag = True
                temp_l = self.letters.copy() #Αντιγράφει τα γράμματα που έχει στην διάθεση του ο παίκτης
                for x in w: #Για όλα τα γράμματα της λέξης
                    if x not in self.letters:
                        flag = False #Υπάρχει γράμμα στην λέξη που δεν υπάρχει στο χέρι άρα υπάρχει λάθος
                        break
                    else:
                        if x in temp_l: #Το βγάζει απο το αντίγραφο
                            temp_l.remove(x)
                        else: #Δεν υπάρχει στο δυναμικό αντίγραφο γραμμάτων άρα υπάρχει λάθος
                            flag = False 
                            break
                if flag: #Η λεξη αποτελείται απο τα γράμματα που έχει ο παίκτης
                    return w
                else:
                    print("Η λέξη που εισήγαγες δεν αποτελείται απο τα γράμματα που διαθέτεις")
                   
class Computer(Player):
    def __init__(self, sak):
        Player.__init__(self, sak)
        self.difficulty = "easy"
        self.chance = 0.4
        self.constant = 0.04
        
    def __repr__(self):
        return("Σειρα του Η/Υ:")

    def setDifficulty(self, s):
        #Οσο μεγαλώνει η δυσκολία γίνεται λιγότερο πιθανό να αγνοήσει μία λέξη με μεγάλη βαθμολογία
        if s == "easy":
            self.chance = 0.4 #Μία πιθανότητα που προσομοιώνει την πιθανότητα να περάσει μια λέξη με μεγάλη βαθμολογία
            self.constant = 0.04 #Κάνει μεγάλες λέξεις λιγότερο πιθανό να βρεθούν απο τον Η/Υ
            self.difficulty = "easy"
        elif s == "intermediate":
            self.chance = 0.6 
            self.constant = 0.03
            self.difficulty = "intermediate"
        elif s == "hard":
            self.chance = 0.8
            self.constant = 0.02
            self.difficulty = "hard"

    def Fail(self, tuples_list):
        if self.difficulty == "easy":
            worst_case = len(tuples_list)//2 #Αν περάσει όλες τις λέξεις ο Fail πρέπει να επιστρέψει αναγκαστικά μία
        elif self.difficulty == "intermediate":
            worst_case = (3*len(tuples_list))//4
        elif self.difficulty == "hard":
            worst_case = len(tuples_list)//4
        temp_chance = self.chance
        for x in tuples_list: #Για όλες τις λέξεις μετράει δύο πιθανότητες και είτε επιλέγει την λέξη ή προχωράει στην επόμενη
            difficulty_chance = temp_chance
            random_number = random.uniform(0,1)
            difficulty_chance -= len(x[0]) * self.constant
            if difficulty_chance >= random_number:
                return x
        return tuples_list[worst_case]
        
    def Smart(self, letter_sak, dictionary):
        list_of_tuples = []
        for x in range(2,8): #Ο αριθμός των γραμμάτων των μεταθέσεων
            word_tuples = it.permutations(self.letters, x) #Φτιάχνει όλες τις μεταθέσεις
            for w in word_tuples:
                word = ''.join(w) #Ενώνει τα γράμματα
                tup = (word, dictionary.get(word)) 
                if word in dictionary and tup not in list_of_tuples: #Αν υπάρχει η λέξη στο λεξικό και δεν ξαναυπάρχει, εισήγαγέ τη
                    list_of_tuples.append(tup)
        list_of_tuples.sort(key = lambda tup:tup[1], reverse = True) #Κανει ταξινόμηση με βάση τους πόντους των λέξεων
        return list_of_tuples
           
    def play(self, letter_sak, dictionary, mode):
        Player.play(self, letter_sak.amount_of_letters)
        if mode == 1:   
            tuples_list = self.Smart(letter_sak, dictionary) #Βρίσκει όλες τις λέξεις
            if not tuples_list: #Άμα είναι άδεια
                return None
            word_value_tuple = self.Fail(tuples_list) #Επιλέγει μια δυάδα απο την Fail
        return word_value_tuple

class Game:
    def __init__(self):
        self.empty_score = False
        self.game_mode = 1
        self.human_points = 0
        self.pc_points = 0
        self.human_turns = 0
        self.pc_turns = 0
        self.letter_sak = SakClass()
        self.human = Human(self.letter_sak)
        self.pc = Computer(self.letter_sak)
        self.dict = {}
        #Προσπαθεί να ανοίξει το λεξικό απο το αρχείο json και αμα δεν υπάρχει το κατασκευάζει απο το greek7.txt
        try:
            with open('dict.json','r') as f:
                self.dict = json.load(f)
        except FileNotFoundError:
            with open("greek7.txt",encoding = "utf-8") as gr:
                words = gr.readlines()
            for index,i in enumerate(words):
                words[index] = i.strip('\n')
            for x in words:
                self.dict[x] = self.value(x)
            with open('dict.json','w') as f:
                json.dump(self.dict, f)
        #Διαβάζει το αρχείο λεξικού εκτος αν δεν υπάρχει οποτε φτιαχνει ένα κενό
        try:
            with open('score.json','r') as sc:
                self.score_dict = json.load(sc)
        except FileNotFoundError:
            self.empty_score = True
            self.score_dict = {'pc_points' : [], 'human_points' : [], 'human_average_points' : [],
                          'pc_average_points' : [], 'turns' : [], 'difficulty' : []}
    def __repr__(self):
        return ("παιχνίδι")
    
    def value(self, word):
        sum = 0
        for x in word:
           sum += self.letter_sak.sak.get(x)[1]
        return sum

    def setup(self):
        while True:
            print("1: Σκορ \n2: Ρυθμίσεις \n3: Παιχνίδι \n4: Οδηγίες Παιχνιδιού \n5: Έξοδος")
            try:
                ans = int(input("Γράψε τι θές να κάνεις και πάτα Enter: "))
                print("----------------------------------------------------")
                if ans == 1:
                    self.score()
                elif ans == 2:
                    self.settings()
                elif ans == 3:
                    self.play()
                    break
                elif ans == 4:
                    print("Tο παιχνίδι ειναι μια απολοποιημένη έκδοση του σκραμπλ, παρουσιάζονται στον παίκτη 7 κεφαλαία γράμματα με τα οποία πρέπει να σχηματίσει Ελληνικές λέξεις.")
                    print("Δίπλα σε κάθε γράμμα αναγράφεται πόσους πόντους δίνει.")
                    print("Μπορεί ο παίκτης να περάσει τη σειρά του δίνοντας ως λέξη το γράμμα 'p' ή 'q' αν επιθυμεί να τελείωσει την παρτίδα.")
                    print("To παιχνίδι τελειώνει όταν αποφασίσει ο παίκτης, δεν υπάρχουν αρκετά γράμματα στο σακουλάκι ή δεν βρει σωστή λέξη ο Η/Υ.")        
                    print("----------------------------------------------------")
                elif ans == 5:
                    quit()
                else:
                     print("Εισήγαγε έναν αριθμό από 1-5")
            except ValueError:      
               print("Εισήγαγε έναν αριθμό από 1-5")

    def score(self):
        if self.empty_score:
            print("Δεν υπάρχουν στοιχεία, ολοκλήρωσε μία παρτίδα πρώτα!")
            print("----------------------------------------------------")
        else:    
            length = len(self.score_dict.get('turns'))
            for i in range(length):
                print("Παιχνίδι: ", i+1)
                print("Πόντοι Παίκτη: ", self.score_dict.get('human_points')[i])
                print("Πόντοι Η/Υ: ", self.score_dict.get('pc_points')[i])
                print("M.Ο πόντων ανά λέξη παίκτη: ", self.score_dict.get('human_average_points')[i],)
                print("Μ.Ο πόντων ανά λέξη Η/Υ: ", self.score_dict.get('pc_average_points')[i])
                print("Αριθμός γύρων: ", self.score_dict.get('turns')[i])
                print("Επίπεδο δυσκολίας: ", self.score_dict.get('difficulty')[i])
                print("----------------------------------------------------")
               
    def settings(self):
        while True:   
            print("1: Μέθοδοι παιξίματος \n2: Δυσκολία Η/Υ \n3: Πήγαινε πίσω ")
            try:
                a = int(input("Τι θα ήθελες να κάνεις: "))
                print("----------------------------------------------------")
                if a == 1:
                    print("Οι διαθέσιμοι μέθοδοι παιξίματος του ", self.pc, "είναι οι:")
                    while True:
                        try:
                            print("1: SMART-FAIL")
                            ans = int(input("Με ποια μέθοδο θα ήθελες να παίξει ο Η/Υ: "))
                            if ans == 1:
                                self.game_mode = 1
                                break
                            else:
                                print("Γράψε τον αριθμό που αντιστοιχεί στην μέθοδο που επιθυμείς να διαλέξεις και πατα Enter")
                                print("----------------------------------------------------")
                        except ValueError:
                            print("Γράψε τον αριθμό που αντιστοιχεί στην μέθοδο που επιθυμείς να διαλέξεις και πατα Enter")
                            print("----------------------------------------------------")
                elif a == 2:
                    print("Τα επίπεδα δυσκολίας του ", self.pc, "είναι:")
                    while True:
                        try:
                            print("1: Αρχάριος \n2: Μεσαίος \n3: Δύσκολος")
                            ans = int(input("Τι δυσκολία θες να έχει ο Η/Υ: "))
                            print("----------------------------------------------------")
                            if ans == 1:
                                self.pc.setDifficulty("easy")
                                break
                            elif ans == 2:
                                self.pc.setDifficulty("intermediate")
                                break
                            elif ans == 3:
                                self.pc.setDifficulty("hard")
                                break
                            else:
                                print("Προσπάθησε ξανά")
                                
                        except ValueError:
                                print("Γράψε τον αριθμό που αντιστοιχεί στην δυσκολία που επιθυμείς να διαλέξεις και πατα Enter")
                                print("----------------------------------------------------")
                elif a == 3:
                    self.setup()
            except ValueError:
                        print("Λάθος είσοδος")
                
    def humanTurn(self):
        self.human_turns += 1
        while True:
            word = self.human.play(self.letter_sak) #
            if word == "pass":
                print("Πέρασες τη σειρά σου")
                return True
            elif word == "end":
                print("Το παιχνίδι τερμάτισε")
                return False
            else:
                if self.dict.get(word) == None:
                    print("Η λέξη που εισήγαγες δεν υπάρχει στο λεξικό, δοκίμασε ξανά")
                    continue
                else:
                    points = self.dict.get(word)
                    self.human_points += points
                    print("Αποδεκή λέξη - Βαθμοί: ", points, " - Σκορ: ", self.human_points)
                    for x in word:
                        self.human.letters.remove(x)
                    input("Enter για συνέχεια")
                    print("----------------------------------------------------")
                    if self.letter_sak.checkAmount(len(word)): #Αμα μπορει να αναπληρώσει γράμματα
                        self.human.letters += self.letter_sak.getLetters(len(word)) #Παιρνει νέα γράμματα και τα προσθέτει στην υπάρχουσα λίστα
                        return True
                    else:
                        return False
                    
    def pcTurn(self):
        self.pc_turns += 1
        word_tuple = self.pc.play(self.letter_sak, self.dict, self.game_mode) #Aμα δεν βρει λέξη ο Η/Υ επιστρέφει None
        if word_tuple == None:
            print("O Η/Υ δεν βρήκε κάποια λέξη να παίξει, το παιχνίδι τερματίζεται")
            print("----------------------------------------------------")
            return False
        word = word_tuple[0]
        points = word_tuple[1]
        self.pc_points += points
        print("Λέξη Η/Υ: ", word, ", Βαθμοί: ", points, " - Σκορ Η/Y: ", self.pc_points)   
        print("----------------------------------------------------")
        for x in word:
            self.pc.letters.remove(x) #Αφαιρεί τα γράμματα της λέξης που έπαιξε απο τα τρέχοντα
        if self.letter_sak.checkAmount(len(word)): #Αν έχει αρκετά γράμματα το σακουλάκι                     
            self.pc.letters += self.letter_sak.getLetters(len(word)) #Παίρνει νέα γράμματα
            return True
        else:
            print("Δεν υπάρχουν άλλα γράμματα στο σακουλάκι")
            return False
    
    def play(self):
        flag1, flag2 = True,True
        while flag1 and flag2:
            flag1 = self.humanTurn()
            flag2 = self.pcTurn()     
        self.end()
        
    def end(self):
        #Αποθηκεύει το νέο λεξικό με τα καινούρια στατιστικά
        if self.human_turns > 0 and self.pc_turns > 0:
            print("Πόντοι παίκτη: ", self.human_points)
            print("Πόντοι H/Y: ", self.pc_points)
            if self.human_points > self.pc_points:
                print("Νικητής ο παίκτης, συγχαρητήρια!")
            elif self.human_points < self.pc_points:
                print("Νικητής ο H/Y")
            else:
                print("Ισοπαλία")  
            self.score_dict['pc_points'].append(self.pc_points)
            self.score_dict['human_points'].append(self.human_points)
            self.score_dict['human_average_points'].append(self.human_points/self.human_turns)
            self.score_dict['pc_average_points'].append(self.pc_points/self.pc_turns)
            self.score_dict['turns'].append((self.pc_turns + self.human_turns)//2)
            self.score_dict['difficulty'].append(self.pc.difficulty)
            with open('score.json','w') as f:
                json.dump(self.score_dict, f)
            quit()
        else:
             print("Δεν υπάρχουν αρκετά στοιχεία παιχνιδιού")
             quit()
