[README.md Tiếng Việt](README-vn.md)


# ROCK PAPER SCISSORS

This is a rock paper scissors program with Tkinter and AI logic

# Details

1. The program initializes the GUI by creating a class function and stores variables in the __init__ function.
2. The program uses different AIs in different difficulties chosen by the user.
3. The program uses a cascading menu (multi-level dropdown) to show various functions like showing "About", "License", "Options",...
4. The option menu shows a pop-up which contains AI toggling and difficulty options.
5. By default, the program will play random moves without any AI logic.
6. Easy AI guarantees a win, 100%.
7. Normal AI uses Markovian learning and unpredictablity that is usually expected in a normal RPS game.
8. Hard AI uses aggressive prediction with Markovian learning and the AI is deterministic, which will never pick moves randomly to maintain unpredictability.
9. The program records the game with a scoreboard and resets when the user clicked the action from the cascading menu.
10. The program gracefully exits with a confirmation popup.

Despite the AI logic, humans can counter-play the AI, therefore it's easy to defeat the AI with the correct patterns.
