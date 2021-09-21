import time 
import math
import random


#####################################################
#                       CRYPTO                      #
#####################################################

#codex(B)=1
#Code erreur : -1
def codex(c) :
    try :
        c=str(c)
        c=c[0].upper()
    except : return -1
    n=ord(c)-ord('A')
    if(n>25 or n<0) : return -1
    return n

#xedoc(1)=B	
#Code erreur : '?'
def xedoc(n) :
    try : n=int(n)
    except : return '?'
    if(n>25 or n<0) : return '?'
    return chr(n+ord('A'))

#paquet("ABCD", 2)={0:1, 1:203}
#Code erreur : dico vide
def paquet(txt, paq=1) :
    try :
        txt=str(txt)
        paq=int(paq)
    except : return dict()
    if(paq<0) : return dict()

    res=dict()
    n=len(txt)
    i=0
    nb_paq=-1
    while(i<n) :
        if(i%paq==0) :
            nb_paq+=1
            res[nb_paq]=0
        x=codex(txt[i])
        if(x==-1) : return {}
        res[nb_paq]=res[nb_paq]*100+x
        i+=1

    while(i%paq!=0) : 
        res[nb_paq]*=100
        i+=1
    return res

#mod2base(2)=2526
#Code erreur : 26
def mod2base(paq=1) :
    try : paq=int(paq)
    except : return mod2base()
    res=0
    i=0
    while(i<paq) :
        res=100*res+25
        i+=1
    return res+1



#####################################################
#                   DICTIONNAIRES                   #
#####################################################

#Gestion des caractère accentué
def Filtre(txt) :
    res=""
    for c in txt.lower() :
        if(ord('a')<=ord(c)<=ord('z')) : res+=c
        if(c=='à' or c=='â' or c=='ä' or c=='á' or c=='å') : res+='a'
        elif(c=='ç') : res+='c'
        elif(c=='é' or c=='è' or c=='ê' or c=='ë') : res+='e'
        elif(c=='ï' or c=='î' or c=='ì' or c=='í') : res+='i'
        elif(c=='ö' or c=='ò' or c=='ô' or c=='ø' or c=='ó') : res+='o'
        elif(c=='û' or c=='ü' or c=='ù' or c=='ú') : res+='u'
        elif(c=='æ') : res+='ae'
        elif(c=='œ') : res+='oe'
        elif(c=='ÿ') : res+='y'
        elif(c=='ñ') : res+='n'
        elif(c=='ß') : res+='ss'
    return res


#Création d'un arbre représentant le dictionnaire
#En paramètre la langue FR, ANG
def MonDico(lang="FR") :
    try : lang=str(lang)
    except : lang="FR"

    Racine=dict()

    def constructBranche(mot):
        Arbre = Racine;
        for c in mot:
            #Si le cara c n'existe pas on le crée (permet en plus de gérer les répétitions éventuelles)
            if not (c in Arbre): 
                Arbre[c] = dict()
                Arbre[c]['FINMOT']=False
            #On avance dans l'arbre
            Arbre = Arbre[c]
        #Arrivé à la fin on marque que le mot est fini
        Arbre["FINMOT"] = True

    if(lang in {"ANG", "ALL", "ESP", "IT", "DAN", "NOR", "SWI", "NED"}) : dico = "Dictionnaires/Dictionnaire"+lang+".txt"
    else : dico = "Dictionnaires/DictionnaireFR.txt"

    with open(dico, "r", encoding='utf8') as f :
        for ligne in f.readlines() : 
            constructBranche(Filtre(ligne.strip()).upper())
    return Racine

#Calcul la pertinance d'une phrase avec l'arbre
def pertinence(phrase, arbre) :
    pert=0
    n=len(phrase)
    i=0
    while(i<n) :
        test=True
        j=i
        positionDico=arbre
        while(j<n) :
            cara=phrase[j]
            try : x=positionDico[cara]
            except : break
            if(x['FINMOT']) : pert+=1
            positionDico=x
            j+=1
        i+=1
    return pert


#####################################################
#                      MATRICES                     #
#####################################################

#Permet d'afficher des matrices (pour d'éventuel tests)
def MatAff(M) : 
    try:
        n=len(M)
        m=len(M[0])
    except : return ""

    res=""
    i=0
    while(i<n) :
        j=0
        while(j<m) :
            try : res+=str(M[i][j])
            except : return ""
            if(j<m-1) : res+='\t'
            j=j+1
        res+='\n'
        i=i+1
    return res

#renvoie le résultat du produit de matrice
#Matrice vide en cas d'erreur
def prodMat(A,B) :
    try : 
        lA=len(A)
        cA=len(A[0])
        lB=len(B)
        cB=len(B[0])
    except : return dict()
    if(cA!=lB) : return dict()

    res=dict()
    for i in range(lA) :
        res[i]=dict()
        for j in range(cB) :
            res[i][j]=0
            for k in range(cA) : res[i][j]+=A[i][k]*B[k][j]
    return res

#renoie la matrice A ou l'on a supprimé la ligne i et la colonne j
#Matrice vide en cas d'erreur (return dict())
def mineur(A, i, j) :

    try :
        l=len(A) #nb de ligne
        c=len(A[0]) #nb colonne
    except : return dict()

    res=dict()
    for u in range(l-1) :
        res[u]=dict()
        for v in range(c-1) :
            if(u<i) :
                if(v<j): res[u][v]=A[u][v]
                else : res[u][v]=A[u][v+1]
            else :
                if(v<j): res[u][v]=A[u+1][v]
                else : res[u][v]=A[u+1][v+1]
    return res

#Fonction qui renvoie le déterminant d'une matrice	
#0 en cas d'erreur
def det(A) : 
    try :
        l=len(A)
        c=len(A[0])
    except : return 0
    if(l!=c) : return 0

    if(l==1) : return A[0][0]

    p=1
    res=0
    for i in range(l) :
        res=res+p*A[i][0]*det(mineur(A,i,0))
        p=-p

    return res

#Renvoie l'inverse de A modulo n
#Matrice vide en cas d'erreur
def inv_mat_mod(A, d, n) :

    try :
        n=int(n)
        l=len(A)
        c=len(A[0])
    except : return dict()
    if(l!=c) : return dict()

    if(d==0) : return dict()

    res=dict()
    for i in range(l) :
        res[i]=dict()
        for j in range(c) : res[i][j]=((-1)**(i+j)*d*det(mineur(A,j,i)))%n

    return res

#liste des sous-ensemble à p élément avec E
def lst_ss_ens(E,p) :
    e=len(E)

    res=dict()
    if(e==p) : res[len(res)]=E
    if(e>p and e>0) :
        #Soit on ne contient pas le dernier élément
        F=dict()
        for i in range(e-1) : F[i]=E[i]
        X=lst_ss_ens(F,p)
        for i in X : res[len(res)]=X[i]

        #Soit on contient le dernier élément
        F=dict()
        for i in range(e-1) : F[i]=E[i]
        X=lst_ss_ens(F,p-1)
        for i in X : 
            X[i][len(X[i])]=E[e-1]
            res[len(res)]=X[i]

    return res