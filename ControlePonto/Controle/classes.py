class url_simples():
     def __init__(self, tupla):
             self.tupla = tupla
             self.nome = tupla[0]
             self.link = tupla[1]

     def __str__(self):
             return "['%s','%s']" % (self.nome , self.link,)
            
     def __getitem__(self,chave):
             return self.tupla[chave]


class urls_type():
     def __init__(self,tuplas):
             self.nomes = []
             self.links = []
             self.urls = []
             for i in tuplas:
                     obj = url_simples(i)
                     self.nomes.append(obj.nome)
                     self.links.append(obj.link)
                     self.urls.append(obj)
     def __str__(self):
             return self.urls
     def __getitem__(self,chave):
             return self.urls[chave]

class estbank_simples():
     def __init__(self,nome,hora):
        self.nome = nome
        self.hora = hora

     def __str__(self):
          return "[%s,%s]" % (self.nome,self.hora)
          
class estbank_type():
     def __init__(self,saidaests,saidabanco):
        self.tudo = []
        for i in range(0,len(saidaests)):
            self.tudo.append(estbank_simples(saidaests[i],saidabanco[i]))
        

     def __str__(self):
          for i in self.tudo:
               print i
     
     def __getitem__(self,chave):
          return self.tudo[chave]
