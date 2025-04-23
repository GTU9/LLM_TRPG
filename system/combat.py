class combat:
    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy

    def start_combat(self):
        print(f"Combat started between {self.player.name} and {self.enemy.name}!")
        while self.player.is_alive() and self.enemy.is_alive():
            self.player.attack(self.enemy)
            if self.enemy.is_alive():
                self.enemy.attack(self.player)
        if self.player.is_alive():
            print(f"{self.player.name} wins!")
        else:
            print(f"{self.enemy.name} wins!")