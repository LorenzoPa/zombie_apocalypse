from django.db import models
from django.contrib.auth.models import User
import random
# Create your models here.

class Shelter(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default="My Shelter")
    food = models.IntegerField(default=10)
    survivors = models.IntegerField(default=3)
    defense = models.IntegerField(default=5)
    day = models.IntegerField(default=1)
    alive = models.BooleanField(default=True)
    
    def next_day(self):
        # Se il rifugio è già caduto, non fare nulla 
        if not self.alive:
            return {
                "day": self.day,
                "event": "The shelter has fallen. You can't continue.",
                "status": self.status()
            }

        self.day += 1
        self.food -= 2
        message = ""

        events = ["attack", "find_food", "disease", "quiet"]
        event = random.choice(events)

        if event == "attack":
            damage = random.randint(1, 4)
            self.defense -= damage
            if self.defense < 0:
                deaths = random.randint(1, 2)
                self.survivors -= deaths
                message = f"Zombie attack! Your defense is too low. You lost {deaths} survivors."
            else:
                message = f"Zombie attack! Defense -{damage}"

        elif event == "find_food":
            found = random.randint(2, 6)
            self.food += found
            message = f"You found {found} units of food."

        elif event == "disease":
            lost = random.randint(1, 2)
            self.survivors -= lost
            message = f"A disease spread! {lost} survivors died."

        else:
            message = "A calm night. Everyone is resting."

        # Effetto fame
        if self.food <= 0:
            self.survivors -= 1
            message += " Food too low. -1 survivor."

        # Se tutti morti
        if self.survivors <= 0:
            self.alive = False
            message += " The shelter has fallen!"

        # 🔥 Salvataggio sicuro
        self.save()

        return {
            "day": self.day,
            "event": message,
            "status": self.status()
        }

    def perform_action(self, action):
        if not self.alive:
            return {
                "event": "The shelter has fallen. You can't perform any actions.",
                "status": self.status()
            }

        message = ""
        if action == "search_food":
            found = random.randint(1, 6)
            self.food += found
            message = f"You searched for food and found {found} units!"

        elif action == "search_weapons":
            found = random.randint(0, 2)
            self.defense += found
            risk = random.randint(0, 1)
            if risk == 1:
                self.survivors -= 1
                message = f"You found {found} weapons, but one survivor didn't make it."
            else:
                message = f"You found {found} weapons and everyone made it back."

        elif action == "search_survivors":
            chance = random.random()
            if chance > 0.6:
                gained = random.randint(1, 2)
                self.survivors += gained
                message = f"You found {gained} new survivors!"
            else:
                loss = random.randint(1, 2)
                self.survivors -= loss
                message = f"You couldn't find anyone, and lost {loss} people in the process."

        elif action == "rest":
            recover = random.randint(1, 3)
            self.defense += recover
            message = f"You rested for a day. Defense +{recover}."

        else:
            message = "Invalid action."

        if self.survivors <= 0:
            self.alive = False
            message += " The shelter has fallen!"

        self.save()
        return {"event": message, "status": self.status()}
    
    def status(self):
        return {
            "day": self.day,
            "food": self.food,
            "defense": self.defense,
            "survivors": self.survivors,
            "alive": self.alive
        }

    def restart(self):
        self.name = "My Shelter"
        self.food = 10
        self.survivors = 3
        self.defense = 5
        self.day = 1
        self.alive = True
        self.save()
        return {
            "message": "Your shelter has been rebuilt. Day 1 begins again.",
            "status": self.status()
        }


