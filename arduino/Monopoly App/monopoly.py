class Player:
    def __init__(self, housing=0, housing_price=0, net_worth=1500):
        self.housing = housing
        self.housing_price = housing_price
        self.net_worth = 1500
        





    
class Monopoly:
    def __init__(self, num_players, housing_price):
        self.players = [Player(housing_price=housing_price) for _ in range(num_players)]
        self.current_player = 0
    
    def add_housing(self):
        player = self.players[self.current_player]
        if player.cash >= player.housing_price:
            player.housing += 1
            player.cash -= player.housing_price
    
    def current_player_cash(self):
        return self.players[self.current_player].cash


import tkinter as tk


class MonopolyGUI:
    def __init__(self, players):
        self.players = players
        self.current_player_index = 0
        self.housing_price = 50
        
        # Create the main window
        self.root = tk.Tk()
        self.root.title("Monopoly")
        
        # Create the player information labels
        self.player_info_labels = []
        for i, player in enumerate(self.players):
            player_info_label = tk.Label(self.root, text=f"Player {i+1}: Housing = {player.housing}, Cash = {player.cash}")
            player_info_label.pack()
            self.player_info_labels.append(player_info_label)
        
        # Create the housing price label and entry
        self.housing_price_label = tk.Label(self.root, text=f"Housing Price: {self.housing_price}")
        self.housing_price_label.pack()
        
        self.housing_price_entry = tk.Entry(self.root)
        self.housing_price_entry.pack()
        
        # Create the add housing button
        self.add_housing_button = tk.Button(self.root, text="Add Housing", command=self.add_housing)
        self.add_housing_button.pack()
        
        # Create the current player cash label and entry
        self.current_player_cash_label = tk.Label(self.root, text=f"Player {self.current_player_index+1} Cash: {self.players[self.current_player_index].cash}")
        self.current_player_cash_label.pack()
        
        self.current_player_cash_entry = tk.Entry(self.root)
        self.current_player_cash_entry.pack()
        
        # Create the change cash button
        self.change_cash_button = tk.Button(self.root, text="Change Cash", command=self.change_cash)
        self.change_cash_button.pack()
        
        # Start the main loop
        self.root.mainloop()
    
    def add_housing(self):
        # Get the housing price from the entry and add housing for the current player
        self.housing_price = int(self.housing_price_entry.get())
        self.players[self.current_player_index].add_housing(self.housing_price)
        
        # Update the player information labels
        for i, player in enumerate(self.players):
            self.player_info_labels[i].config(text=f"Player {i+1}: Housing = {player.housing}, Cash = {player.cash}")
        
        # Clear the housing price entry
        self.housing_price_entry.delete(0, tk.END)
        
    def change_cash(self):
        # Get the cash amount from the entry and change the current player's cash
        cash_change = int(self.current_player_cash_entry.get())
        self.players[self.current_player_index].change_cash(cash_change)
        
        # Update the current player cash label and clear the cash entry
        self.current_player_cash_label.config(text=f"Player {self.current_player_index+1} Cash: {self.players[self.current_player_index].cash}")
        self.current_player_cash_entry.delete(0, tk.END)
