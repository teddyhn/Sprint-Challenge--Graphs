from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

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

def bfs(current_room):
    queue = []
    queue.append([current_room])
    print('\nStarting breadth-first search...')

    visited = set()

    while len(queue) > 0:
        path = queue.pop(0)
        room = path[-1]

        if room not in visited:
            if '?' in list(traversal_graph[room].values()):
                path.pop(0)
                return path
            visited.add(room)

            exits = list(traversal_graph[room].keys())
            for exit in exits:
                if traversal_graph[room][exit] in visited:
                    print('Already visited')
                else:
                    new_path = list(path)
                    new_path.append(traversal_graph[room][exit])
                    queue.append(new_path)


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

while True:
    exits = player.current_room.get_exits()
    print(f'Exits: {exits}')
    room_id = player.current_room.id
    print(f'Current room id: {room_id}')

    traversed_rooms.add(room_id)

    for exit in exits:
        if exit not in traversal_graph[room_id]:
            traversal_graph[room_id][exit] = '?'

    if len(traversed_rooms) == len(world.rooms):
        break
    
    all_explored = True

    for exit in traversal_graph[room_id]:
        if traversal_graph[room_id][exit] == '?':
            all_explored = False
            break

    if len(traversed_rooms) < len(world.rooms) and all_explored == True:
        # Perform breadth-first search to find shortest path to room with unexplored exits
        path = bfs(player.current_room.id)
        print(f'Breadth-first search returned: {path}')

        for i in path:
            key_list = list(traversal_graph[player.current_room.id].keys()) 
            val_list = list(traversal_graph[player.current_room.id].values())

            player.travel(key_list[val_list.index(i)])
            traversal_path.append(key_list[val_list.index(i)])

        continue

    else:
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


print(f'\n \n{traversal_graph}')
print(f'{traversal_path}\n \n')


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
