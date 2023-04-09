import requests       # face solicitări HTTP către API-uri web.
from subprocess import Popen, PIPE     # executa comenzi externe in Python


def  execute_command(command):
    
    args=(command).split()     # imparte comanda respectiva
    proc=Popen(args,stdoutput=PIPE, stderr=PIPE)   # trece argumentele in subprocess pentru a fi executate
    output, err = proc.communicate()
    return output, err

def make_req(error):
    """
    Se face o solicitare la API-ul Stack Exchange si cauta intrebari care contin eroarea furnizata

    """    
    resp = requests.get("https://api.stackexchange.com/"+"/2.2/search?order=desc&sort=activity&tagged=python&intitle={}&site=stackoverflow".format(error))
    return resp.json()    # o sa fie returnat un dictionar de tip JSON care va contine informatiile din API

def get_urls(json_dict):
    url_list = []
    count = 0
    for i in json_dict["items"]:
        if i["is_answered"]:    # daca a gasit ca intrebarea a fost raspunsa o pune in url_list si se incrementeaza count 
            url_list.append(i["link"])
        count +=1
        if count==3 or count == len(i):  # pentru a deschide 3 pagini sau daca count este egal lungimea elementului din "items"
            break
    # pentru a deschide fiecare URL din url_list in browser: 
    import webbrowser
    for i in url_list:
        webbrowser.open(i)

#functia principala:
if __name__=="__main__":
    op, err = execute_command("python test.py")   # apeleaza execute_command pentru a executa comanda "python test.py", astfel obtinandu-se output-urile si erorile acesteia
    error_message = err.decode("utf-8").strip().split("\r\n")[-1]   # este extras mesajul de eroare de la sfarsit ([-1] ca sa ia ultima linie daca eroarea e pe mai multe linii), este decodat intr-un sir Unicode cu schema de codificare "utf-8" si este divizat in linii separate "\r\n"
    print(error_message)
    if error_message:     # verific daca exista un mesaj de eroare
        filter_err = error_message.split(":")   # este impartita eroarea 
        json1 = make_req(filter_err[0])    # face apel la API-ul Stack Exchange si returneaza un dictionar JSON cu informatii despre cuvantul cheie specificat si asociate cu python
        json2= make_req(filter_err[1])
        json3 = make_req(error_message)
        get_urls(json1)   # sunt obtinute primele 3 URL-uri asociate erorilor care au fost deja raspunse
        get_urls(json2)
        get_urls(json3)
    else:
        print("no error")
