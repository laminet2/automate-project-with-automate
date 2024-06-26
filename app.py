from tkinter import *
import os
try:
    from PIL import Image,ImageTk
except ImportError:
    os.system("pip install pillow")
    from PIL import Image,ImageTk
from tkinter import messagebox
from collections import Counter

Automate=[set(),[],dict(),set(),set()] #etat ,alphabet,Table de transition,initaux,acceptant
AFN=False

root=Tk()
root.title("Simulateur d'Automate")


#Taille de la fenetre racine et son emplacement au lancement 
window_width = 754
window_height = 521
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x}+{y-40}")
temporisateur=0
motAnalyser=""
nextEtatEnsemble=set()
positionx=10
postionSave=dict()
pere=dict()
epsilon=False


#--------- ACCEUILL ---------------------#
## MENU

#-Menu principal
rootMenu=Menu(root)
automate_menu=Menu(rootMenu,tearoff=0)
transition_menu=Menu(rootMenu,tearoff=0)

rootMenu.add_cascade(label="Automate",menu=automate_menu)
rootMenu.add_cascade(label="Table de transition",menu=transition_menu)

#-Transition Menu
transition_menu.add_command(label="Modifier/mettre a jour la table",command=lambda:windowsEditTable(root))
transition_menu.add_separator() 
transition_menu.add_command(label="Afficher la Table de transitions",command=lambda:afficherTableTransition(root))

#-Automate menu
automate_menu.add_command(label="Definir/modifier un automate",command=lambda:automateWindows(root))
root.config(menu=rootMenu)

# BACKGROUND
bg=Image.open("images/bg.jpg")
resizedPictures=bg.resize((window_width,window_height))
convertedImage=ImageTk.PhotoImage(resizedPictures)
bgimage=Label(root,image=convertedImage)
bgimage.place(relheight=1,relwidth=1)

#- TEXTE LAYOUT

texteEntrer = Label(root, text="SIMULATEUR D'AUTOMATE",font=("Lato",24,"bold"))
texteEntrer.pack(padx=20, pady=40)

# - Layout that start with recommendatation
recommendation=Canvas()
recommendation.pack()

subtext=Label(recommendation,text="AVANT DE POUVOIR ANALYSER UN MOT,\n VEUILLEZ RESPECTER CES ETAPES",font=("Helvetica Light",12),justify="center")
subtext.pack()

frame1=Frame(recommendation,height=window_height-368,padx=100)

#column 1
picture11=ImageTk.PhotoImage(Image.open("icons/number1.png").resize((74,76)))
picture1=Label(frame1,image=picture11)
picture1.grid(row=0,column=0,padx=10,pady=5)
text1=Label(frame1,text="DEFINISER UN\n AUTOMATE",justify="center")
text1.grid(row=1,column=0)

#column 2
picture12=ImageTk.PhotoImage(Image.open("icons/number2.png").resize((74,76)))
picture2=Label(frame1,image=picture12)
picture2.grid(row=0,column=1,padx=10,pady=5)
text2=Label(frame1,text="MODIFIER LA TABLE\n DE TRANSITION",justify="center")
text2.grid(row=1,column=1,padx=10)

#column 3
picture13=ImageTk.PhotoImage(Image.open("icons/check.png").resize((74,76)))
picture3=Label(frame1,image=picture13)
picture3.grid(row=0,column=2,padx=10,pady=5)
text3=Label(frame1,text="ANALYSER LE \n MOT",justify="center",font=("Lato",10,"bold"),fg="#32B55E")
text3.grid(row=1,column=2)
frame1.pack()



# Layout with the champ  mot a analyser


#Function systeme
def renitianiliser_saisie():
    #Il manque a renitialisez la fonction de traitement des mots
    #effacer et depackager la zone de dessein
    #effacer et depackager le sort du mot
    global temporisateur,motAnalyser,nextEtat,sectionSortDuMot,sortDuMot,positionx
    wordToAnalyse.delete(0, 'end')
    temporisateur=0
    motAnalyser=""
    nextEtat=0
    positionx=10
    sectionSortDuMot.pack_forget()
    sortDuMot.pack_forget()
    sectionDessein.delete("all")
    sectionDessein.pack_forget()

def activer_desactiver_epsilon(popup,root):
    global epsilon
    if epsilon==True:
        epsilon=False
    else:
        
        epsilon = True
    popup.destroy()
    windowsEditTable(root)

#champ saisir mot
champ_analyse=Canvas(root)
#champ_analyse.pack()
champMotAnalyse=Frame(champ_analyse,width=window_width-285,height=43)
texte1=Label(champMotAnalyse,text="ENTRER LE MOT A ANALYSER",font=('Inter Light',13))
texte1.grid(column=0,row=0,padx=30,pady=20)

wordToAnalyse=Entry(champMotAnalyse)
wordToAnalyse.grid(column=1,row=0,padx=5)

iconeNext=ImageTk.PhotoImage(Image.open("icons/next.png").resize((27,25)))
nextButton=Button(champMotAnalyse,image=iconeNext,command=lambda:analyseMot(wordToAnalyse.get()))
nextButton.grid(row=0,column=2,padx=5)

iconeRenitialiser=ImageTk.PhotoImage(Image.open("icons/reset.png").resize((27,25)))
renitianilserButton=Button(champMotAnalyse,image=iconeRenitialiser,command=renitianiliser_saisie)
renitianilserButton.grid(row=0,column=3,padx=5)

#champ dessein
sectionDessein=Canvas(root,width=window_width-108,height=window_height-250,bg='white')
#sectionDessein.pack()
#Background section dessein
# bg2 = ImageTk.PhotoImage(Image.open("images/RectangleBlur.png").resize((window_width-108,window_height-250)))
# sectionDessein.create_image(0, 0, anchor="nw", image=bg2)

#champ mot refuser ou accepter
sectionSortDuMot=Canvas(root,width=window_width-484,height=34)
sortDuMot=Label(sectionSortDuMot, width=30,font=('Lato',14,'bold'),fg='white')
# sectionSortDuMot.pack()
# sortDuMot.pack()

champMotAnalyse.pack()

#-----------Automate ---------------#
def automateValide(automate):
    #etat,alphabet,t,initaux,acceptant
    (nbrEtat,alphabet,t,initiaux,acceptant)=automate

    try:
        nbrEtat=int(nbrEtat)
        initiaux=list(map(int, initiaux.split(',')))
        acceptant=list(map(int, acceptant.split(',')))
    except Exception:
        print("initiaux et accepetant pas en chiffre")
        return False
    
    alphabet=alphabet.split(",")
    compteur=Counter(alphabet)
    for i in compteur:
        if(compteur[i]>1):
            print("2 lettre de l'alphabet sont identiques")
            return False

    if (nbrEtat==0 or len(alphabet)==0 or len(initiaux)==0 or len(acceptant)==0):
        print("longueur = 0")
        return False
    else:
        for i in initiaux:
            if(i>nbrEtat or i==0):
                print("nbr d'etat initaux> 0 ")
                return False
        for i in acceptant:
            if(i>nbrEtat or i==0):
                print("nbr d'etat initaux> 0 ")
                return False
    return True

def verificationAutomate(automate,popupWindows):
    if(automateValide(automate)):
        messagebox.showinfo("Automate Valide","Vous pouriez l'enregistrer sans compromis")

    else:
        #messagebox.showwarning("Automate Invalide","Veuillez respecter la note susmentionner,tout les \nchamps sont obligatoires et saisisez \ndes chiffres pour les etats et veuillez a ce \nque ces chiffres inférieur au nommbre d'Etat,\negelement ne saisissez pas deux lettre \nidentique pour l'alphabet")
        messagebox.showwarning("Automate Invalide","Veuillez respecter la note susmentionner,tout les \nchamps sont obligatoires et saisisez des \nchiffres pour les etats en respectant\nles régles d'écriture d'automate")

    popupWindows.focus_set()    

def enregistrerAutomate(automate,popupWindows):
    global Automate,AFN
    (nbrEtat,alphabet,t,initiaux,acceptant)=automate

    if(automateValide(automate)):
        nbrEtat=int(nbrEtat)
        initiaux=set(map(int, initiaux.split(',')))
        acceptant=set(map(int, acceptant.split(',')))
        alphabet=alphabet.split(",")
        Automate=[{i for i in range(1,nbrEtat+1)},alphabet,t,initiaux,acceptant]

        #A Transformer en toast notification
        if(len(initiaux)>1):
            messagebox.showinfo("Automate Enregistrer","AFN enregristrer avec success")
            AFN=True
        else:
            messagebox.showinfo("Automate Enregistrer","Votre Automate a ete rengistrer avec succes")
        popupWindows.destroy()
        
    else:
        messagebox.showerror("Automate Invalide","Veuillez respecter la note susmentionner,tout les \nchamps sont obligatoires et saisisez des \nchiffres pour les etats en respectant\nles régles d'écriture d'automate")
        popupWindows.focus_set()

def automateWindows(root):
    global window_width,window_height,Automate
    popup_widht=window_width-409
    popup_height=window_height-230
    x,y=((screen_width - popup_widht) // 2),((screen_height - popup_height) // 2)

    popupWindows=Toplevel(root)
    popupWindows.title("Definisions Automate")
    popupWindows.geometry(f"{popup_widht}x{popup_height}+{x}+{y-40}")

    frame=Frame(popupWindows,width=popup_widht)
    noteFrame=LabelFrame(frame,text="A noter")
    noteFrame.grid(row=0,column=0,pady=2)
    label1=Label(noteFrame,text="A noter, afin de mentionner plusieurs états,veuillez les séparer \npar des virgules. Par ailleurs pas besoins de specifier si \nl’automate fini est deterministe (AFD) ou non (AFN)",justify='left')
    label1.pack()

    automateFrame=Frame(frame)
    automateFrame.grid(column=0,row=1,pady=20)

    text1=Label(automateFrame,text="Alphabet")
    text1.grid(column=0,row=0,padx=5)
    text2=Label(automateFrame,text="Nombre d'etat")
    text2.grid(column=1,row=0,padx=5)
    text3=Label(automateFrame,text="Etat(s) initial(aux)")
    text3.grid(column=0,row=2,padx=5)
    text4=Label(automateFrame,text="Etat(s) acceptant(s)")
    text4.grid(column=1,row=2,padx=5)

    alphabet=Entry(automateFrame)
    alphabet.insert(0,(','.join(Automate[1]))) 
    alphabet.grid(column=0,row=1,padx=5)

    # Variable pour stocker la valeur de la Spinbox
    spinbox_value = IntVar(value=len(Automate[0]))
    nbrEtat=Spinbox(automateFrame,from_=0,to=100,textvariable=spinbox_value)

    nbrEtat.grid(row=1,column=1,padx=5)
    etatInitiaux=Entry(automateFrame)
    etatInitiaux.insert(0,(','.join(map(str,list(Automate[3])))))
    etatInitiaux.grid(row=3,column=0,padx=5)
    etatAcceptant=Entry(automateFrame)
    etatAcceptant.insert(0,(','.join(map(str,list(Automate[4])))))
    etatAcceptant.grid(row=3,column=1,padx=5)


    buttonFrame=Frame(frame)
    buttonFrame.grid(column=0,row=2)
    cancelButton=Button(buttonFrame,text="Annuler",command=popupWindows.destroy)
    cancelButton.grid(column=0,row=0) 
    verificationButton=Button(buttonFrame,text="Verifier\n Automate Valide",command=lambda:verificationAutomate([nbrEtat.get(),alphabet.get(),dict(),etatInitiaux.get(),etatAcceptant.get()],popupWindows))
    verificationButton.grid(column=1,row=0,pady=15,padx=15)
    validateButton=Button(buttonFrame,text="Enregistrer",command=lambda:enregistrerAutomate([nbrEtat.get(),alphabet.get(),dict(),etatInitiaux.get(),etatAcceptant.get()],popupWindows))
    validateButton.grid(column=2,row=0)
    frame.pack()
    popupWindows.mainloop()
#-----------------------------------#


#---------- TRANSITIONS ------------#


def verificationEntrer(Table):
    global Automate
    (Etat,alphabet,t,initiaux,acceptant)=Automate
    Table = [x for x in Table if x != ''] #supprimer tout les espaces
    #print(Table)
    try:
        for caractere in Table:
            entierCaracteres=map(int, caractere.split(','))
            for entierCaractere in entierCaracteres:
                if(entierCaractere not in Etat):
                    return False
                
    except Exception:
        return False
    return True

def verificationEntrerTable(Table,popup):
    if(verificationEntrer(Table)):
        messagebox.showinfo("Table de Transition Valide","La table entrer est valide vous pouviez\n l'enregistrer sans compromis")
    else:
        messagebox.showwarning("Table incorrect","Les informations entrer sont incoherant avec celle de l'automate")
    popup.focus_set()

def afficherTableTransition(root):
    global window_width,window_height,Automate
    (Etat,alphabet,tt,initiaux,acceptant)=Automate
    if(tt==dict()):
        return False
    popup_widht=window_width-400
    popup_height=window_height-250
    x,y=window_width,((screen_height - popup_height) // 2)
    popupWindows=Toplevel(root)
    popupWindows.title("Afficher Table")
    popupWindows.geometry(f"{popup_widht}x{popup_height}+{window_width+392}+{y-40}")

    alphabett=alphabet[:]
    if(epsilon):
        alphabett.append("€")
    canvas2=Canvas(popupWindows)
    canvas2.pack(padx=10)
    etats=list(Etat)
    widthR,heightR,x,y=83,30,20,0
    couleur=["lightcyan1","green","lightyellow1"]
    for ligne in range(len(Etat)+1):
        for column in range(len(alphabett)+1):
            if(ligne==0 and column==0):
                rectangle=canvas2.create_rectangle(x,y,x+widthR,y+heightR,fill=couleur[0])
                canvas2.create_text(x+(widthR/2),y+(heightR/2),text="Q\∑",font=("Lato",14,"bold"))
         
            elif(ligne==0):
                #Ligne des entete etat
                rectangle=canvas2.create_rectangle(x,y,x+widthR,y+heightR,fill=couleur[0])
                canvas2.create_text(x+(widthR/2),y+(heightR/2),text=f"{alphabett[column-1]}",font=("Lato",14,"bold"))
                
            elif(column==0):
                #etats
                etat=etats[ligne-1]
                if(etat in initiaux):
                    canvas2.create_line(0,y+(heightR/2),20,y+(heightR/2),arrow=LAST)
                rectangle=canvas2.create_rectangle(x,y,x+widthR,y+heightR,fill=couleur[1 if etat in acceptant else 0])
                canvas2.create_text(x+(widthR/2),y+(heightR/2),text=f"{etat}",font=("Lato",14,"bold"))
            else:
                rectangle=canvas2.create_rectangle(x,y,x+widthR,y+heightR,fill=couleur[2])
                if((ligne,alphabett[column-1]) in tt):
                    caracT= ",".join(map(str, list(tt[(ligne,alphabett[column-1])]))) if len(tt[(ligne,alphabett[column-1])])>1 else str(list(tt[(ligne,alphabett[column-1])])[0])
                    canvas2.create_text(x+(widthR/2),y+(heightR/2),text=f"{caracT}",font=("Lato",14,"bold"))
                
            x=x+widthR
        y+=heightR
        x=20


def enregistrerTable(Table,popup,Automate,root):
    global AFN
    if(verificationEntrer(list(Table.values()))):
        newTable=dict()
        for element in Table:
           destination=Table[element]
           if (destination!='') :
            newTable[element]=set(map(int, destination.split(',')))
            if(len(newTable[element])>1):
                AFN=TRUE
        Automate[2]=newTable
        #print(Automate)
        result=messagebox.askquestion("Table enregistrer avec success","Voulez vous poursuivre les modifications ?")
        popup.destroy()
        changementAcceuil()
        if(result=="yes"):
            windowsEditTable(root)
    else:
        messagebox.showerror("Erreur d'enregistrement","La table entrer ne peut être enregistrer")
        popup.focus_set()


def rafraichirTable(popup,root):
    global Automate
    (Etat,alphabet,t,initiaux,acceptant)=Automate
    popup.destroy()
    Automate[2]=dict()
    windowsEditTable(root)
    # if(Automate[2]!=dict()):
    #     for i in Automate[2]:
    #         if (not isinstance(Automate[2][i], str)):
    #             Automate[2]=dict()
    #             t=[]
    #             break

    #renitialisez acceuil

def changementAcceuil():
    global Automate,champ_analyse,recommendation,sectionDessein,sectionSortDuMot
    if(Automate[2]!={}):
        #afficher zone ecriture
        champ_analyse.pack()
        #desactiver zone renseignement
        recommendation.pack_forget()
    else:
        #desactiver zone ecriture
        champ_analyse.pack_forget()
        #desactiver zone dessein
        sectionDessein.pack_forget()
        #desactiver zone mot
        sectionSortDuMot.pack_forget()
        #afficher recommendation
        champ_analyse.pack()
        
def completer(popup,root):
    global Automate
    Aut=Automate
    aut=Aut[2]
    alpha=Aut[1]
    sommet=Aut[0]
    liste=list(sommet)
    puit=max(liste)+1
    ok=True
    for i in sommet:
        for j in alpha:
            if (i,j) not in aut:
                aut[(i,j)]={puit}
                ok=False
    if ok==False:
        for j in alpha:
            aut[(puit,j)]={puit}
        sommet.add(puit)
    Automate=[Aut[0],Aut[1],aut,Aut[3],Aut[4]]
    popup.destroy()
    windowsEditTable(root)

def windowsEditTable(root):

    global window_width,window_height,epsilon
    (Etat,alphabet,t,initiaux,acceptant)=Automate
    #print(Automate[2])
    popup_widht=window_width-246
    popup_height=window_height-221
    x,y=((screen_width - popup_widht) // 2),((screen_height - popup_height) // 2)
    popupWindows=Toplevel(root)
    popupWindows.title("Edit Table Transitions")
    popupWindows.geometry(f"{popup_widht}x{popup_height}+{x}+{y-40}")
    #popupWindows.config(bg='red')
    
    ZoneButton=Canvas(popupWindows,height=50)
    ZoneButton.pack(padx=5,pady=10)

    zoneAction=LabelFrame(ZoneButton,text="Button d'Operations")
    zoneAction.grid(row=0,column=0,padx=7)
    
    zoneControle=LabelFrame(ZoneButton,text="Button de Controle")
    zoneControle.grid(row=0,column=1,padx=7)

    # Button
    emonderButton=Button(zoneAction,text="Emonder",command=lambda:emonder(popupWindows,root))
    emonderButton.grid(row=0,column=1,padx=2)

    completerButton=Button(zoneAction,text="Completer",command=lambda:completer(popupWindows,root))
    completerButton.grid(row=0,column=2,padx=2)

    determiniserButton=Button(zoneAction,text="Determiniser",command=lambda:déterminise(popupWindows,root))
    determiniserButton.grid(row=0,column=3,padx=2)

    alphabett=alphabet[:]
    if(epsilon):
        alphabett.append("€")
        epsilonTexte="Desactiver AFN€"
    else:
        epsilonTexte="Activer AFN€"
    epsilonButton=Button(zoneAction,text=epsilonTexte,command=lambda:activer_desactiver_epsilon(popupWindows,root))
    epsilonButton.grid(row=0,column=4,padx=2)
    

    verificationTable=Button(zoneControle,text="Verifier",command=lambda:verificationEntrerTable([tt[i].get() for i in tt],popupWindows))
    verificationTable.grid(row=0,column=0,padx=2)
    resetImage=ImageTk.PhotoImage(Image.open("icons/reset.png").resize((23,23)))
    rafraichirButton=Button(zoneControle,image=resetImage,command=lambda:rafraichirTable(popupWindows,root))
    rafraichirButton.grid(row=0,column=2,padx=2)
    saveButton=Button(zoneControle,text="Enregistrer",command=lambda:enregistrerTable({i:tt[i].get() for i in tt},popupWindows,Automate,root))
    saveButton.grid(row=0,column=1,padx=2)

    #Zone Dessein
    canvas=Canvas(popupWindows)
    canvas.pack(expand=TRUE,fill=BOTH,side=LEFT)

    
    my_scroll_bar_y=Scrollbar(canvas,orient=VERTICAL,command=canvas.yview)
    my_scroll_bar_y.pack(side="right",fill=Y)
    canvas.configure(yscrollcommand=my_scroll_bar_y.set)

    my_scroll_bar_x=Scrollbar(canvas,orient=HORIZONTAL,command=canvas.xview)
    my_scroll_bar_x.pack(side="bottom",fill=X)
    canvas.configure(xscrollcommand=my_scroll_bar_x.set)

    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    canvas2=Canvas(canvas)
    canvas2.pack(padx=10)
    etats=list(Etat)
    widthR,heightR,x,y=83,30,20,0
    couleur=["lightcyan1","green"]
    tt={}
    
    for ligne in range(len(Etat)+1):
        for column in range(len(alphabett)+1):
            
            if(ligne==0 and column==0):
                rectangle=canvas2.create_rectangle(x,y,x+widthR,y+heightR,fill=couleur[0])
                canvas2.create_text(x+(widthR/2),y+(heightR/2),text="Q\∑",font=("Lato",14,"bold"))
         
            elif(ligne==0):
                #Ligne des entete etat
                rectangle=canvas2.create_rectangle(x,y,x+widthR,y+heightR,fill=couleur[0])
                canvas2.create_text(x+(widthR/2),y+(heightR/2),text=f"{alphabett[column-1]}",font=("Lato",14,"bold"))
                
            elif(column==0):
                #etats
                etat=etats[ligne-1]
                if(etat in initiaux):
                    canvas2.create_line(0,y+(heightR/2),20,y+(heightR/2),arrow=LAST)
                rectangle=canvas2.create_rectangle(x,y,x+widthR,y+heightR,fill=couleur[1 if etat in acceptant else 0])
                canvas2.create_text(x+(widthR/2),y+(heightR/2),text=f"{etat}",font=("Lato",14,"bold"))
            else:
                entrer=Entry(canvas2,width=13)
                entrer.place(x=x,y=y)
                if((ligne,alphabett[column-1]) in t):
                    caracT= ",".join(map(str, list(t[(ligne,alphabett[column-1])]))) if len(t[(ligne,alphabett[column-1])])>1 else str(list(t[(ligne,alphabett[column-1])])[0])
                    entrer.insert(0,caracT)

                tt[(ligne,alphabett[column-1])]=entrer

            x=x+widthR
        y+=heightR
        x=20
    
    popupWindows.mainloop()

#--------- ANALYSE DU MOT ----------
def cloture(aut,i):
    (etats,al,T,init,Ac)=aut

    Cl={i} # La clôture de l'état i
    L=[i]
    while L:
        j=L.pop(0)
        if (j,'€') in T:
            for k in T[(j,'€')]:
                if not k in Cl:
                    Cl.add(k)
                    L.append(k)
    return (Cl)
#quand on renitialise mettre le temporisateur a 0
def analyseMot(motEntrer):
    global Automate,temporisateur,motAnalyser,nextEtatEnsemble,sectionSortDuMot,sortDuMot,sectionDessein,positionx,postionSave,pere
    (Etat,alphabet,tt,initiaux,acceptant)=Automate
    lettreEnListe=[]
    Cl={i:cloture(Automate,i) for i in Etat}
    rayon=50
    y=50
    dist=50
    # if(AFN):
    #     messagebox.showinfo("En Attente","La lecture d'un mot par un AFD n'est pas encore prise en compte")
    #     return False
    
    if(motEntrer==motAnalyser and motEntrer!=""):
        lettreEnListe=[k for k in motEntrer]
        #Dessein
        if(temporisateur>len(lettreEnListe)):
            nextEtatEnsemble=set()
        for nextEtat in nextEtatEnsemble:
            y=50
            while((positionx+dist,y,positionx+dist+rayon,y+rayon) in postionSave.values()):
                y+=52
            for k in pere[nextEtat]:
                sectionDessein.create_line(positionx,postionSave[k][1]+23,positionx+dist,y+23,arrow=LAST)
            sectionDessein.create_oval(positionx+dist,y,positionx+dist+rayon,y+rayon)
            postionSave[nextEtat]=(positionx+dist,y,positionx+dist+rayon,y+rayon)
            pere[nextEtat]=set()
            #print(nextEtat)
            if(nextEtat in acceptant):
                sectionDessein.create_oval(positionx+dist+(5),y+(5),positionx+dist+(rayon-5),y+(rayon-5))
            sectionDessein.create_text(dist+positionx+(rayon//2),y+23,text=f"{nextEtat}",font=("Lato",14,"bold"))

        if(temporisateur==len(lettreEnListe)):
            #donner le sort final du mot
            sectionSortDuMot.pack()
            #print(nextEtat)
            for nextEtat in nextEtatEnsemble:
                if(nextEtat in acceptant):
                    
                    sortDuMot.config(bg="green")
                    sortDuMot["text"]="MOT ACCEPTER"
                    sortDuMot.pack()
                    temporisateur+=1
                    return True
            temporisateur+=1
            sortDuMot.config(bg="red")
            sortDuMot["text"]="MOT REFUSER"
            sortDuMot.pack()
            return False

    elif(motEntrer!=""):
        #premiere analyse
        postionSave=dict()
        pere=dict()
        temporisateur=0
        motAnalyser=motEntrer
        nextEtatEnsemble=list(initiaux)  #For next ETAT
        for k in motEntrer:
            if(k not in alphabet):
                messagebox.showerror("Invalide","Le mot entrer contient des elements n'ont mentionner dans l'alphabet ")
                return False
            lettreEnListe.append(k)
        #Gestion Dessein
        sectionDessein.pack()
        
        for nextEtat in nextEtatEnsemble:
            sectionDessein.create_line(positionx,y+23,positionx+dist,y+23,arrow=LAST)
            sectionDessein.create_oval(positionx+dist,y,positionx+dist+rayon,y+rayon)
            postionSave[nextEtat]=(positionx+dist,y,positionx+dist+rayon,y+rayon)
            if(nextEtat in acceptant):
                sectionDessein.create_oval(30+(5),y+(5),30+(rayon-5),y+(rayon-5))
            sectionDessein.create_text(positionx+dist+(rayon//2),y+23,text=f"{nextEtat}",font=("Lato",14,"bold"))
            y+=52

    lettre=lettreEnListe[temporisateur]
    nextEtatEnsembleTempo=set()
    for nextEtat in nextEtatEnsemble:
        if((nextEtat,lettre) in tt):
            nextEtatEnsembleTempo = nextEtatEnsembleTempo | tt[(nextEtat,lettre)]
            for i in tt[(nextEtat,lettre)]:
                if(i not in pere):
                    pere[i]=set()
                pere[i].add(nextEtat)
        # else:
        #     messagebox.showwarning("Incomplet",'Automate INCOMPLET')

        if(epsilon==True and Cl[nextEtat]!=set()):
            for j in Cl[nextEtat]:
                    if(j!=nextEtat and (j,lettre) in tt):
                        for k in tt[(j,lettre)]:
                            nextEtatEnsembleTempo.add(k)
                            if(k not in pere):
                                pere[k]=set()
                            pere[k].add(nextEtat)
        
    nextEtatEnsemble=nextEtatEnsembleTempo
    temporisateur+=1
    positionx=positionx+dist+rayon
        

#----------------------------------

######------------Fonction
def getKeyFromValues(my_dict,value):
    return list(filter(lambda x: my_dict[x] == value, my_dict))[0]
    

def cloture(aut,i):
    (etats,al,T,init,Ac)=aut

    Cl={i} # La clôture de l'état i
    L=[i]
    while L:
        j=L.pop(0)
        if (j,'€') in T:
            for k in T[(j,'€')]:
                if not k in Cl:
                    Cl.add(k)
                    L.append(k)
    return (Cl)


def determiniserAFDepsilon():
    global Automate
    (etats,alpha,T,init,accept)=Automate
    
    Cl={i:cloture(Automate,i) for i in etats}
    Ac=set(accept)
    for e in etats:
        if Cl[e].intersection(accept)!=set() and not e in Ac:
            Ac.add(e)
    etatsD={1}
    k=1
    TD = {}
    initD={1}
    acceptD=set()
    if init.intersection(Ac)!=set():
                acceptD.add(1)
    L=[init] 
    LM=[init]
    while L:
        et=L.pop(0)
        for c in alpha:
            et2=set()
            for i in et:
                for e in Cl[i]:
                    if (e,c) in T:
                        et2=et2.union(T[(e,c)])

            if et2!=set():
                if  (et2 not in LM):
                    k+=1
                    etatsD.add(k)
                    LM.append(et2) 
                    L.append(et2)
                i=LM.index(et)+1
                j=LM.index(et2)+1
                TD[(i,c)]=j
                if et2.intersection(Ac)!=set():
                        acceptD.add(j)
    
    Automate=(etatsD,alpha,{i:{TD[i]} for i in TD},initD,acceptD)
    return True
        

def déterminise(popup,root):
    global Automate,AFD,epsilon
    (etats,alpha,Trans,init,accept)=Automate
    if(not AFN and not epsilon):
        messagebox.showwarning("AFD","Votre automate n'est pas un AFN")
        return False
    if(epsilon):
        determiniserAFDepsilon()
        activer_desactiver_epsilon(popup,root)
        return TRUE
    newEtat={1:init}
    TT=dict()
    newAccept=set()
    chiffreRomain=1
    while chiffreRomain<=len(newEtat.keys()):
        for lettre in alpha:
            newEtatt=set()
            for i in newEtat[chiffreRomain]:
                if(i,lettre) in Trans:
                    for k in Trans[(i,lettre)] :
                        newEtatt.add(k)
            if(newEtatt!=set()):
                if((newEtatt not in newEtat.values())):
                    newEtat[max(newEtat.keys())+1]=newEtatt
                TT[(chiffreRomain,lettre)]=getKeyFromValues(newEtat,newEtatt)
        
        #Traitement etant acceptant/ICI je cherche a savoir si le chiffre romain est un etat acceptant
        if(accept.intersection(newEtat[chiffreRomain])!=set()):
            newAccept.add(chiffreRomain)
        chiffreRomain+=1
    Automate=[set(newEtat.keys()),alpha,{i:{TT[i]} for i in TT},{1},newAccept]
    #print(Automate)
    AFD=False
    popup.destroy()
    windowsEditTable(root)


#####-----------------------

def emonder(popup,root):
    global Automate
    (etats,alpha,T,initiaux,Ac)=Automate
    #print("etat initaux debut",initiaux)
    A=accessible(Automate)
    #print("etat initaux fin",initiaux)
    B=coAccessible(Automate)

    C=A.intersection(B) # Les sommets accessibles et co-accessibles
    #print(C)
    L=list(C)
    #Les nouveaux états
    etats2={i+1 for i in range(len(C))}
    #print(etats2)
    # La bijection entre états
    bij={L[i]:i+1 for i in range(len(C))}
    #print(bij)    
    #Construction du nouvel automate
    Ac2={bij[i] for i in Ac}
    #print(Ac2)
    
    T2={ }
    for (i,c) in T:
        k=T[i,c]
        for j in k :
            if i in C and j in C:
                if((bij[i],c) not in T2):
                    T2[(bij[i],c)]=set()
                T2[(bij[i],c)].add(bij[j])
    
    init=set()
    cpt=0
    #print("Etat initiaux",initiaux)
    for i in initiaux:
        cpt=cpt+1
        if(i in bij):
            print("bij[i]",bij[i])
            init.add(bij[i])
    #print("le compteur",cpt)
    Automate=[etats2,alpha,T2,initiaux,Ac2]
    popup.destroy()
    windowsEditTable(root)


def coAccessible(aut):
    (etats,alpha,T,init,Ac)=aut
    #On construit le graphe inverse
    G={i:[] for i in etats}
    for i in etats:
        for c in alpha:
            if (i,c) in T:
                k=T[(i,c)]
                for j in k:
                    G[j].append(i)

                    
    coAccess={i for i in Ac}
    for e in Ac:
        L=[e]
        while L:
            i=L.pop(0)
            for j in G[i]:
                if not j in coAccess:
                    coAccess.add(j)
                    L.append(j)
    return coAccess
            
def accessible(aut):
    (etats,alpha,T,init,Ac)=aut
    Access=init.copy() 
    L=list(init)
    while L:
        i=L.pop(0)
        for c in alpha:
            if (i,c) in T:
                k=T[(i,c)]
                for j in k:
                    if not j in Access:
                        Access.add(j)
                        L.append(j)
    return Access  



#####---------------
    # for i in range(1,20):
    #     label= Label(canvas,text=f"label{i}",bg="yellow")
    #     label.pack()

    #label=Label(tableauSection,text="Test1")
    #contenue

    # for i in range(1,20):
    #     label= Label(ZoneButton,text=f"labelButton{i}")
    #     label.pack()

    # canvas=Canvas(popupWindows,width=100,height=120,scrollregion=(0,0,1000,1000))
    # my_scroll_bar=Scrollbar(popupWindows,orient=VERTICAL)
    # my_scroll_bar.pack(side=RIGHT,fill=Y)
    
    # frameRoot=Frame(canvas,bg='red',height=window_height)
    # frameRoot.pack(padx=20,pady=25,expand=TRUE)
    # my_scroll_bar.config(command=canvas.yview)
    # canvas.pack()

    #my_scroll_bar(canvas,command = canvas.yview,command=cnavas.)
    
    #canvas.create_window((0, 0), window=frameRoot, anchor="nw")

    # Ajout de quelques éléments pour tester le défilement
    
    # Redimensionner le canevas en fonction du cadre
    # frameRoot.update_idletasks()
    # canvas.config(scrollregion=canvas.bbox("all"))


#-----------------------------------#
root.mainloop()