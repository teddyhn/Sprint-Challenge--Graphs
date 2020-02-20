from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
# map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversed_rooms = set()
traversal_graph = {}
traversal_path = []

for i in range(0, (len(world.rooms))):
    traversal_graph[i] = {}

def reverse_direction(direction):
    if direction == 'n':
        return 's'
    elif direction == 's':
        return 'n'
    elif direction == 'w':
        return 'e'
    elif direction == 'e':
        return 'w'
    else:
        return 'Invalid direction'

last_direction = ''

while len(traversed_rooms) < len(world.rooms):
    exits = player.current_room.get_exits()
    print(f'Exits: {exits}')
    room_id = player.current_room.id
    print(f'Current room id: {room_id}')

    traversed_rooms.add(room_id)

    if len(traversed_rooms) == len(world.rooms):
        break

    for exit in exits:
        if exit not in traversal_graph[room_id]:
            traversal_graph[room_id][exit] = '?'

    valid_dir = False
    dir_to_travel = ''

    while valid_dir == False:
        random_dir = exits[random.randint(0, len(exits) - 1)]
        if traversal_graph[room_id][random_dir] == '?':
            dir_to_travel = random_dir
            valid_dir = True
    
    player.travel(dir_to_travel)
    traversal_path.append(dir_to_travel)
    last_direction = dir_to_travel

    next_room_id = player.current_room.id

    traversal_graph[room_id][dir_to_travel] = next_room_id
    traversal_graph[next_room_id][reverse_direction(dir_to_travel)] = room_id


print(traversal_graph)



# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
