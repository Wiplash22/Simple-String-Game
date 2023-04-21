import tkinter as tk
from tkinter import messagebox

import random


class GUI:

    def __init__(self):
        
        self.root=tk.Tk()
        self.root.geometry("600x550")
        self.root.title("Game UI")
        
        self.label=tk.Label(self.root,text="Numerical String Game",font=('TimesNewRoman',18))
        self.label.pack(padx=25,pady=25)

        self.starting_string = [4, 5, 2, 7, 3]
        self.current_string = self.starting_string.copy()
        self.score = 0
        self.player = "human"

        self.depth = 4  # Set the default depth to 4

        self.create_widgets()

    def create_widgets(self):
        self.starting_string_label = tk.Label(self.root, text=f"Starting string: {self.starting_string}",font=('TimesNewRoman',14))
        self.starting_string_label.pack(padx=10,pady=10)

        self.score_label = tk.Label(self.root, text=f"Score: {self.score}",font=('TimesNewRoman',14))
        self.score_label.pack(padx=10,pady=10)

        self.current_string_label = tk.Label(self.root, text=f"Current string: {self.current_string}",font=('TimesNewRoman',14))
        self.current_string_label.pack(padx=10,pady=10)

        self.human_move_button = tk.Button(self.root, text="Human Move",font=('TimesNewRoman',12),command=self.human_move)
        self.human_move_button.pack(side=tk.LEFT)

        self.computer_move_button = tk.Button(self.root, text="Computer Move",font=('TimesNewRoman',12),command=self.computer_move)
        self.computer_move_button.pack(side=tk.LEFT)

        self.new_game_button = tk.Button(self.root, text="New Game",font=('TimesNewRoman',12),command=self.new_game)
        self.new_game_button.pack(padx=30)

    def human_move(self):
    # Clear the current GUI and create buttons for each adjacent pair of numbers
        
        for i in range(len(self.current_string) - 1):
            pair = [self.current_string[i], self.current_string[i+1]]
            sum = pair[0] + pair[1]
            if sum > 7:
                label = f"{pair[0]} + {pair[1]} = {sum} (replace with 1)"
                command = lambda i=i: self.make_move(i, i+1, 1)
            elif sum < 7:
                label = f"{pair[0]} + {pair[1]} = {sum} (replace with 3)"
                command = lambda i=i: self.make_move(i, i+1, 3)
            else:
                label = f"{pair[0]} + {pair[1]} = {sum} (replace with 2)"
                command = lambda i=i: self.make_move(i, i+1, 2)
            self.button = tk.Button(self.root, text=label, command=command)
            self.button.pack(padx=10, pady=5)
            
    def make_move(self, i, j, replacement):
    # Make the move and update the game state and score
        self.button.destroy()
        pair = [self.current_string[i], self.current_string[j]]
        self.current_string[i:j+1] = [replacement]
        self.current_string_label.config(text=f"Current string: {self.current_string}")#updates the string
        if replacement == 1:
            self.score += 1
        elif replacement == 3:
            self.score -= 1
        self.score_label.config(text=f"Score: {self.score}")#updates the score
    # Check if the game is over and show the winner if it is
        if len(self.current_string) == 1:
            if self.current_string[0] % 2 == 1:
                winner = self.player
                self.new_game(player)
            else:
                winner = "computer" if self.player == "human" else "human"
            messagebox.showinfo("Game Over", f"The winner is {winner}!")
            self.root.destroy()
            
        else:
        # Switch to the other player
            if self.player == "human": 
                self.player = "computer" 
            else:
                self.player ="human"

            if self.player == "computer":
                self.computer_move()
        
                self.current_string_label.config(text=f"Current string: {self.current_string}")
                self.human_move()
            else:
                
                self.human_move()


    def minimax(self,state, player, depth):
        if depth == 0 or len(state) == 1:
            # If we've reached the maximum depth or the game is over, evaluate the state
            return self.evaluate_state(state)

        if player == "computer":
            # If it's the computer's turn, maximize the score
            best_score = -float('inf')
            best_move = None
            for i in range(len(state)-1):
                new_state = state.copy()
                
                nm=[state[i], state[i+1]]
                new_state[i] = self.combine_numbers(nm)
                del new_state[i+1]
                score = self.minimax(new_state, "human", depth-1)
                if score > best_score:
                    best_score = score
                    best_move = i
            return best_move
        else:
        # If it's the human's turn, minimize the score
            best_score = float('inf')
            best_move = None
            for i in range(len(state)-1):
                new_state = state.copy()
                nm=[state[i], state[i+1]]
                new_state[i] = self.combine_numbers(nm)
                del new_state[i+1]
                score = self.minimax(new_state, "computer", depth-1)
                if score < best_score:
                    best_score = score
                    best_move = i
            return best_move

    def combine_numbers(self,numbers):
        #Combine adjacent numbers based on the given rules.
        i = 0
        lst=[]
        for x in numbers:
            if type(x) is list:
                x=x[0]
                lst.append(x)
            else: 
                lst.append(x)
        numbers=lst
        
        while i < len(numbers) - 1:
            
            if numbers[i] + numbers[i+1] > 7:
                numbers[i:i+2] = [1]
            elif numbers[i] + numbers[i+1] < 7:
                numbers[i:i+2] = [3]
            else:
                numbers[i:i+2] = [2]
            i += 1
        return numbers

    def evaluate_state(self,state):
        
        # A simple heuristic function that adds up the values of the numbers in the state
        print(state)
        if type(state[0]) is list:
            state=state[0][0]
            return state
        return sum(state)      

    def computer_move(self):
        if self.player != "computer":
            return

    # Use minimax algorithm to determine the best move for the computer player
        best_move = self.minimax(self.current_string, "computer", self.depth)

    # Make the best move
        self.make_move("computer", best_move, 1)
    
    


    def new_game(self,player):
    # Reset the score and string to their initial values
        self.score = 0
        self.current_string = self.starting_string.copy()
    
    # Set the player to the specified value
        self.player ="human"
    
    # Clear any existing widgets from the UI
        for widget in self.root.winfo_children():
            widget.destroy()
    
    # Add a label to display the current score
        self.score_label = tk.Label(self.root, text=f"Score: {self.score}",font=('TimesNewRoman',14))
        self.score_label.pack(padx=10,pady=10)
    
    # Add a label to display the current string
        self.current_string_label = tk.Label(self.root, text=f"Current string: {self.current_string}",font=('TimesNewRoman',14))
        self.current_string_label.pack(padx=10,pady=10)
    
    # Add a button to allow the player to make a move (if playing as human)
        if player == "human":
            self.human_move_button = tk.Button(self.root, text="Human Move",font=('TimesNewRoman',12),command=self.human_move)
            self.human_move_button.pack(side=tk.LEFT)
    
    # Start the game loop

    def run(self):
        self.root.mainloop()

if __name__ == '__main__':
    gui = GUI()
    gui.run()
