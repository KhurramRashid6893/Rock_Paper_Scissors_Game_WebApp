import random
from gesture import GestureRecogniser

class RPSLogic:
    def __init__(self):
        self.recognizer = GestureRecogniser()

    def get_random_gesture(self):
        return random.choice(['ROCK', 'PAPER', 'SCISSORS'])

    def play_round(self, img1, img2=None):
        # img1 is from the player, img2 is unused since computer is random
        gesture1 = self.recognizer.classify_image(img1)
        gesture2 = self.get_random_gesture()  # computer gesture

        print(f"Player Gesture: {gesture1}, Computer Gesture: {gesture2}")  # Debugging

        winner = self.get_winner(gesture1, gesture2)
        return {
            'player': gesture1,
            'computer': gesture2,
            'winner': winner
        }

    def get_winner(self, g1, g2):
        if g1 == "UNKNOWN" or g2 == "UNKNOWN":
            return "Draw"
        if g1 == g2:
            return "Draw"
        elif (g1 == 'ROCK' and g2 == 'SCISSORS') or \
             (g1 == 'PAPER' and g2 == 'ROCK') or \
             (g1 == 'SCISSORS' and g2 == 'PAPER'):
            return 'Player'
        else:
            return 'Computer'
