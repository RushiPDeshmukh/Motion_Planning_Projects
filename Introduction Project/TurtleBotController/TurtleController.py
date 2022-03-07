from turtle import *
exit_condition = False
while(not exit_condition):
    input_action = input("Your input is my command! What shall i do now?")
    if input_action == 'w':
        forward(10)
    elif input_action == 's':
        back(10)
    elif input_action == 'd':
        input_action = input("Vague Command. Turn by how much?")
        right(int(input_action))
    elif input_action == 'a':
        input_action = input("Vague Command. Turn by how much?")
        left(int(input_action))
    else:
        exit_condition = True


    