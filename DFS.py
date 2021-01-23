import simpleguitk as simplegui


# Constants
HEIGHT = 700
WIDTH = 1000

NODE_SPACE_ALLOWANCE = 20
EDGE_COLOR = "Blue"
EDGE_SIZE = 2
NODE_LABEL_COLOR = "White"
NODE_COLOR = "Yellow"
NODE_MARK_COLOR = "Green"

# Global variables
start = 0
goal = 0
placeNodes = True
setNodesRelation = False
draw_relations = False
draw_mark_relations = False
setGoal = False
setStart = False
displayResult = False
set_nodes = False
nodes = []

pos1 = [0, 0]
pos2 = [0, 0]
pos_lock = False
indx = 0
letter_label_default = "A"
letter_pos = 0
current_node_letters_low = []
current_node_letters_up = []


class Point:
    def __init__(self, pos, node_colour, node_mark_colour):
        self.pos = pos
        self.children = []
        self.radius = 8
        self.colour = node_colour
        self.mark_colour = node_mark_colour
        self.index = 0
        self.is_mark = False
        self.label = "A"

    def draw(self, canvas):
        if self.is_mark == False:
            canvas.draw_circle(self.pos, self.radius, 6, self.colour)
        else:
            canvas.draw_circle(self.pos, self.radius, 6, self.mark_colour)


def mouseclick(pos):
    global pos1, pos2, pos_lock, indx, draw_relations, draw_mark_relations, nodes, indx_mark_color
    global letter_label_default, letter_pos

    if placeNodes == True:
        nodes.append(Point(pos, NODE_COLOR, NODE_MARK_COLOR))
        nodes[-1].label = chr(ord(letter_label_default) + letter_pos)
        letter_pos += 1

    else:
        print("")

    # Sets up the edges or links
    if setNodesRelation == True:

        # If mouseclick pos is on top of a current node mark that node
        for i, position in enumerate(nodes):
            if (
                pos[0] >= (nodes[i].pos[0] - NODE_SPACE_ALLOWANCE)
                and pos[0] <= (nodes[i].pos[0] + NODE_SPACE_ALLOWANCE)
            ) and (
                pos[1] >= (nodes[i].pos[1] - NODE_SPACE_ALLOWANCE)
                and pos[1] <= (nodes[i].pos[1] + NODE_SPACE_ALLOWANCE)
            ):
                if pos_lock == False:
                    pos1[0] = pos[0]
                    pos1[1] = pos[1]

                    indx = i
                    indx_mark_color = i
                    pos_lock = True
                    draw_mark_relations = True
                    print("First Node is Selected")
                    break

                else:
                    print("Second node is selected")

                    # If it is the second node that is not the same of
                    # the first marked node, then creates a new relation/edge
                    if i != indx:
                        pos2[0] = pos[0]
                        pos2[1] = pos[1]

                        nodes[indx].children.append(i)
                        nodes[i].children.append(indx)

                        pos_lock = False
                        draw_relations = True
                        draw_mark_relations = False
                        break
                    else:
                        print(" self loop is not allowed.")


def button_set_nodes():
    global placeNodes, setNodesRelation, current_node_letters_up, nodes, current_node_letters_low

    # Can only set nodes if the set-up is right
    # Prevents locking nodes later in the program
    if (
        placeNodes == True
        and setNodesRelation == False
        and setStart == False
        and setGoal == False
    ):
        placeNodes = False
        setNodesRelation = True

        # Fills two new lists of all node labels(letters)
        # for later use in input start and goal
        if nodes:
            for n, obj in enumerate(nodes):
                current_node_letters_up.append(nodes[n].label)

            for let in current_node_letters_up:
                current_node_letters_low.append(let.lower())

        print("The nodes are now locked in!")
    else:
        print("This action is not allowed.")


def button_set_graph():
    global placeNodes, setNodesRelation, nodes, set_nodes

    if setNodesRelation is True:
        placeNodes = False
        setNodesRelation = False
        set_nodes = True

        # Sets the index of nodes list and apply it to each index attribute of Point class
        # for index/element reference only, for later use in DFS functions
        for d, dot in enumerate(nodes):
            nodes[d].index = d
            print("node" + str(d + 1) + ":", nodes[d].label)

            # This is important
            # This sorts the elements of children attribute list in ascending order
            nodes[d].children.sort()

        print("Graph is now set!")
    else:
        print("This action is not allowed.")


def input_start_handler(start_string):
    global start, nodes, setStart

    setStart = False
    if start_string in current_node_letters_up:
        start = ord(start_string) - 65
        setStart = True
        print("Start:", chr(start + 65))
    else:
        if start_string in current_node_letters_low:
            start = ord(start_string) - 97
            setStart = True
            print("Start:", chr(start + 97))
        else:
            print("Unknown input. Enter the node letter.")


def input_goal_handler(goal_string):
    global goal, nodes, setGoal

    setGoal = False
    if goal_string in current_node_letters_up:
        goal = ord(goal_string) - 65
        setGoal = True
        print("Goal:", chr(goal + 65))
    else:
        if goal_string in current_node_letters_low:
            goal = ord(goal_string) - 97
            setGoal = True
            print("Goal:"), chr(goal + 97)
        else:
            print("Unknown input. Enter the node letter.")

    global nodes, displayResult, result_string, queue_string, pointer_string
    displayResult = False
    pointer_string = ""

    # Resets all nodes markings (color)
    for d, marking_obj in enumerate(nodes):
        nodes[d].is_mark = False

    in_queue_result = False

    if (
        placeNodes == False
        and setNodesRelation == False
        and setStart == True
        and setGoal == True
    ):
        print(" ")
        print("DFS starts here:")

        # Checks queue if defined,
        # if it is, then go to else and empty the list; otherwise create new list
        try:
            queue
        except:
            queue = []
        else:
            del queue[:]

        # print queue
        queue.append(nodes[start])
        queue[0].is_mark = True
        # print "queue:", queue
        try:
            result
        except:
            result = []
        else:
            del result[:]

        try:
            temp_list
        except:
            temp_list = []
        else:
            del temp_list[:]

        while queue:
            pointer = queue[0]
            queue.pop(0)
            # print "pointer is", pointer
            pointer.is_mark = True
            print(" ")
            print("Pointer:", pointer.label)

            if pointer.index == goal:
                pointer_string = "Pointer: " + pointer.label
                result_string = "Result: "
                queue_string = "Queue: "

                for obj in result:
                    result_string += str(obj.label)
                    result_string += " "
                for objt in queue:
                    queue_string += str(objt.label)
                    queue_string += " "

                displayResult = True
                print("SUCCESS!")
                break
            else:
                result.append(pointer)
                del temp_list[:]

                for neighbor in pointer.children:
                    in_queue_result = False

                    for i in queue:
                        # print "neighbor:", neighbor+1, "queue:", i.index+1
                        if neighbor == i.index:
                            in_queue_result = True

                    for j in result:
                        # print "neighbor:", neighbor+1, "result:", j.index+1
                        if neighbor == j.index:
                            in_queue_result = True

                    if in_queue_result == False:
                        for obj in nodes:
                            if obj.index == neighbor:
                                temp_list.append(nodes[obj.index])

                if temp_list:
                    queue[0:0] = temp_list

            result_string = "Result: "
            queue_string = "Queue: "
            for obj in result:
                result_string += str(obj.label)
                result_string += " "
            print(result_string)

            for objt in queue:
                queue_string += str(objt.label)
                queue_string += " "
            print(queue_string)


def draw_handler(canvas):
    global result_string, queue_string, pointer_string
    global placeNodes, setNodesRelation, setStart, setGoal, pos1

    # Draws nodes
    if draw_mark_relations == True and setNodesRelation == True:
        canvas.draw_circle(nodes[indx_mark_color].pos, 15, 3, "Yellow", "Black")

    if nodes:
        for i, vertex in enumerate(nodes):
            nodes[i].draw(canvas)
            canvas.draw_text(
                nodes[i].label,
                (nodes[i].pos[0] - 30, nodes[i].pos[1]),
                20,
                NODE_LABEL_COLOR,
            )

    # Draws edges
    if draw_relations == True:
        for n, point in enumerate(nodes):
            if nodes[n].children:
                for child in nodes[n].children:
                    canvas.draw_line(
                        nodes[n].pos,
                        nodes[child].pos,
                        EDGE_SIZE,
                        EDGE_COLOR,
                    )

    # Display results
    if displayResult == True:

        canvas.draw_text(pointer_string, (30, 610), 15, "Red")
        canvas.draw_text(result_string, (30, 635), 15, "Red")
        #canvas.draw_text(queue_string, (30, 460), 15, "Red")


# Creates the frame window
frame = simplegui.create_frame("DFS Search", WIDTH, HEIGHT)

frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw_handler)

# Button, input and label controls for the frame window
button1 = frame.add_button("Set Nodes", button_set_nodes, 80)

label1 = frame.add_label(" ")

button2 = frame.add_button("Set Graph", button_set_graph, 80)
label2 = frame.add_label(" ")


input_start = frame.add_input("Start Node", input_start_handler, 100)
label4 = frame.add_label(" ")

input_goal = frame.add_input("Goal Node", input_goal_handler, 80)
label5 = frame.add_label(" ")
eae721b57
