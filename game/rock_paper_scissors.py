def game_backend(your_item, pc_item):
    if pc_item == your_item:
        return "Draw"
    elif pc_item == 1 and your_item == 2 or pc_item == 2 and your_item == 3 or pc_item == 3 and your_item == 1:
        return "You won, and you get 4 credits"
    elif your_item == 1 and pc_item == 2 or your_item == 2 and pc_item == 3 or your_item == 3 and pc_item == 1:
        return "You lose"