from gesture import GestureRecogniser

class RPSLogic:
    def __init__(self):
        self.recognizer = GestureRecogniser()

    def play_round(self, img1, img2):
        gesture1 = self.recognizer.classify_image(img1)
        gesture2 = self.recognizer.classify_image(img2)

        winner = self.get_winner(gesture1, gesture2)
        return {
            'player1': gesture1,
            'player2': gesture2,
            'winner': winner
        }

    def get_winner(self, g1, g2):
        if g1 == g2:
            return 'Draw'
        elif (g1 == 'ROCK' and g2 == 'SCISSORS') or \
             (g1 == 'PAPER' and g2 == 'ROCK') or \
             (g1 == 'SCISSORS' and g2 == 'PAPER'):
            return 'Player 1'
        else:
            return 'Player 2'
