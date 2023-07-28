from environment import Environment
y,x=int(input("Enter initial y: ")),int(input("Enter initial x: "))
my_list = []
num_sets = int(input("How many tables do you wanna deliver? "))
for i in range(num_sets):
    elements_str = input("Enter the y and x separated by commas: ")
    elements = [int(x.strip()) for x in elements_str.split(',')]
    my_list.append(list(elements))
goal = my_list
Environment(5,5, y,x, goal)

