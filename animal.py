import configparser
import requests

config = configparser.ConfigParser()
config.read('config.ini',encoding='utf-8')

class Animal:
    def __init__(self,url,key):
        res = requests.get(url + 'search', params={'x-api-key':key,'has_breeds':1}).json()[0]
        self.id = res['id']
        req_animal = requests.get(url + self.id)
        animal = req_animal.json()

        self.pic = animal["url"]
        self.breeds = animal["breeds"][0]
        self.breedname = self.breeds["name"]
        self.temperament = self.breeds["temperament"]

    def description(self):
        if "description" in self.breeds:
            return self.temperament +"\n\n" + self.breeds["description"]
        else :
            return self.temperament

    def level(self):
        category = ["adaptability","affection_level","energy_level","intelligence","vocalisation","child_friendly"]

        levels = dict()

        for item in category:
            if item in self.breeds:
                 levels[item] = self.breeds[item]

        return levels

    def type(self):
        return self.__class__.__name__
    
class Cat(Animal):
    def __init__(self):
        key = config['CAT_API']['KEY']
        url = config['CAT_API']['URL']
        Animal.__init__(self,url,key)

class Dog(Animal):
    def __init__(self):
        key = config['DOG_API']['KEY']
        url = config['DOG_API']['URL'] 
        Animal.__init__(self,url,key)