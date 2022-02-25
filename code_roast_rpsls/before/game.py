import random
from scoreboard import Scoreboard
from rules import Rules
from entity import Entity

class Game:
    """Game class
    """
    def __init__(self, user: str, max_round: int = 5) -> None:
        print("Rock paper scissor spock and lizard...\n Welcome to the game.")
        print("Rules are simple...")
        print("Scissors decapitate Lizard, Scissors cuts paper, paper covers rock, rock crushes lizard, lizard poisons Spock, Spock smashes scissors, scissors decapitates lizard, lizard eats paper, paper disproves Spock, Spock vaporizes rock, and as it always has, rock crushes scissors.")
        print("To begin press [Enter]")
        _ = input()
        
        self.scoreboard = Scoreboard()
        self.max_round = max_round
        self.entities = Entity
        self.rules = Rules()
        self.user: str = user
        self.cpu: str = "cpu"
        
        # register players in scoreboard
        self.scoreboard.register_player(self.user)
        self.scoreboard.register_player(self.cpu)
        
    
    def display_entity_to_select(self) -> None:
        """Displays the user choices
        """
        choices_text = ", ".join(f"({entity.value} for {entity.name})" for entity  in self.entities)
        print(f"Select {choices_text}:", end='\t')
    
    def get_user_input(self) -> Entity:
        """Takes user inputs and selects the entities

        Returns:
            Entity: Entity selected by user
        """
        available_choices = [entity.value for entity in self.entities]
        while True:
            try:
                self.display_entity_to_select()
                choice = int(input())
                
                if choice not in available_choices:
                    print("Please select from available choices")
                else:
                    return self.entities(choice)
            except ValueError:
                print("You entered something other than a number")
    
    def get_cpu_input(self) -> Entity:
        """Selects a random entity

        Returns:
            Entity: A random entity
        """
        cpu_choice = random.randint(1, len(self.entities))
        return self.entities(cpu_choice)
    
    def display_current_round(self, user_entity: Entity, cpu_entity: Entity) -> None:
        """Displays current round

        Args:
            user_entity (Entity): Entity selected by user
            cpu_entity (Entity): Entity selected by cpu
        """
        print(f"{self.user} ({user_entity.name}) x {self.cpu} ({cpu_entity.name})")
        print("....")
    
    def display_tie(self) -> None:
        """Display tie message
        """
        print(f"It's a tie..")
    
    def display_round_winner(self, winner_name: str, winner_entity: Entity, message: str) -> None:
        """Display the winner of the round

        Args:
            winner_name (str): Winner Name
            winner_entity (Entity): Entity selected by the winner
            message (str): Reason for wins
        """
        print(f"{winner_name} ({winner_entity.name}) wins the round as {message}")
    
    def do_turn(self) -> None:
        """Function to continue the rounds
        """
        user_entity = self.get_user_input()
        cpu_entity = self.get_cpu_input()
        
        self.display_current_round(user_entity, cpu_entity)
        if cpu_entity == user_entity:
            self.display_tie()
            return

        winner, message = self.rules.get_winner(user_entity, cpu_entity)
        if winner == user_entity:
            self.display_round_winner(self.user, user_entity, message)
            self.scoreboard.points[self.user] += 1
        else:
            self.display_round_winner(self.cpu, cpu_entity, message)
            self.scoreboard.points[self.cpu] += 1
    
    @staticmethod
    def get_user_name() -> str:
        """Static method to get user name as input

        Returns:
            str: Name enterd by user
        """
        print("Please enter your name:", end='\t')
        return str(input().strip())
        
    
    def play(self):
        for i in range(self.max_round):
            self.do_turn()
            self.scoreboard.display_scores()