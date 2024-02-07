# Import necessary libraries
from collections import defaultdict, deque
import heapq

# Define a class for representing the metro graph and implementing various algorithms
class Graph:
    def __init__(self):
        # Initialize an empty graph using defaultdict and dictionaries for storing edge information
        self.graph = defaultdict(dict)
        # Dictionary to map station names to numbers
        self.station_numbers = {}
        # Counter for assigning unique station numbers
        self.number_counter = 10  # Starting number for stations

    # Method to add an edge to the graph
    def addEdge(self, station1, station2, distance, travel_time, cost):
        # Assign numbers to stations if not already assigned
        if station1 not in self.station_numbers:
            self.station_numbers[station1] = self.number_counter
            self.number_counter += 1
        if station2 not in self.station_numbers:
            self.station_numbers[station2] = self.number_counter
            self.number_counter += 1

        # Add edges to the graph
        self.graph[self.station_numbers[station1]][self.station_numbers[station2]] = {
            'distance': distance,
            'travel_time': travel_time,
            'cost': cost
        }
        self.graph[self.station_numbers[station2]][self.station_numbers[station1]] = {
            'distance': distance,
            'travel_time': travel_time,
            'cost': cost
        }

    # Method to get the station name based on the station number
    def get_station_name(self, station_number):
        for name, number in self.station_numbers.items():
            if number == station_number:
                return name

    # Dijkstra's algorithm for finding the shortest path and distance
    def dijkstra_shortest_path(self, start_station, end_station):
        distances = {station: float('inf') for station in self.graph}
        distances[start_station] = 0
        visited = set()
        previous = {}
        queue = [start_station]

        while queue:
            current_station = queue.pop(0)
            visited.add(current_station)

            for neighbor, info in self.graph[current_station].items():
                if neighbor not in visited:
                    new_distance = distances[current_station] + info['distance']
                    if new_distance < distances[neighbor]:
                        distances[neighbor] = new_distance
                        previous[neighbor] = current_station
                        queue.append(neighbor)
            
            queue.sort(key=lambda x: distances[x])  # Sort queue based on distances

        shortest_path = []
        current = end_station
        while current != start_station:
            shortest_path.insert(0, current)
            current = previous[current]
        shortest_path.insert(0, start_station)

        return shortest_path, distances[end_station]

    # Breadth-first search algorithm for finding the shortest path
    def bfs_shortest_path(self, start_station, end_station):
        queue = deque([(start_station, [start_station])])
        visited = set()

        while queue:
            current_station, path = queue.popleft()
            visited.add(current_station)

            for neighbor in self.graph[current_station]:
                if neighbor not in visited:
                    new_path = path + [neighbor]
                    if neighbor == end_station:
                        return new_path
                    queue.append((neighbor, new_path))

        return None  # If no path is found

    # Prim's algorithm for finding the minimum spanning tree and total travel time
    def prim_minimum_spanning_tree(self, start_station, end_station):
        mst = set()
        visited = set()
        heap = [(0, start_station, None)]

        while heap:
            cost, current_station, previous_station = heapq.heappop(heap)

            if current_station not in visited:
                visited.add(current_station)
                if previous_station is not None:
                    mst.add((previous_station, current_station, cost))

                for neighbor, info in self.graph[current_station].items():
                    if neighbor not in visited:
                        heapq.heappush(heap, (info['travel_time'], neighbor, current_station))

                # Check if the end station is reached
                if current_station == end_station:
                    break

        return mst

    # Kruskal's algorithm for finding the minimum spanning tree and total cost
    def kruskal_minimum_spanning_tree(self, start_station, end_station):
        edges = []
        for station1 in self.graph:
            for station2, info in self.graph[station1].items():
                edges.append((info['cost'], station1, station2))

        edges.sort()  # Sort edges based on cost
        mst = set()
        parent = {}

        def find_set(station):
            if station != parent.setdefault(station, station):
                parent[station] = find_set(parent[station])
            return parent[station]

        def union(u, v):
            root1 = find_set(u)
            root2 = find_set(v)
            if root1 != root2:
                parent[root2] = root1

        for cost, station1, station2 in edges:
            if find_set(station1) != find_set(station2):
                mst.add((station1, station2, cost))
                union(station1, station2)

                # Check if the end station is reached
                if find_set(start_station) == find_set(end_station):
                    break

        return mst

# Example usage:
metro_graph = Graph()

# Adding provided edges between stations along with distances, travel time, and cost
edges = [
    ("Noida Sector 62~B", "Botanical Garden~B", 8, 15, 50),
    ("Botanical Garden~B", "Yamuna Bank~B", 10, 20, 60),
    ("Yamuna Bank~B", "Vaishali~B", 8, 18, 55),
    ("Yamuna Bank~B", "Rajiv Chowk~BY", 6, 12, 45),
    ("Rajiv Chowk~BY", "Moti Nagar~B", 9, 22, 70),
    ("Moti Nagar~B", "Janak Puri West~BO", 7, 16, 52),
    ("Janak Puri West~BO", "Dwarka Sector 21~B", 6, 14, 48),
    ("Huda City Center~Y", "Saket~Y", 15, 30, 90),
    ("Saket~Y", "AIIMS~Y", 6, 13, 42),
    ("AIIMS~Y", "Rajiv Chowk~BY", 7, 15, 47),
    ("Rajiv Chowk~BY", "New Delhi~YO", 1, 5, 20),
    ("New Delhi~YO", "Chandni Chowk~Y", 2, 7, 25),
    ("Chandni Chowk~Y", "Vishwavidyalaya~Y", 5, 10, 35),
    ("New Delhi~YO", "Shivaji Stadium~O", 2, 6, 22),
    ("Shivaji Stadium~O", "DDS Campus~O", 7, 17, 55),
    ("DDS Campus~O", "IGI Airport~O", 8, 20, 65),
    ("Moti Nagar~B", "Rajouri Garden~BP", 2, 8, 30),
    ("Punjabi Bagh West~P", "Rajouri Garden~BP", 2, 8, 30),
    ("Punjabi Bagh West~P", "Netaji Subhash Place~PR", 3, 9, 32)
]

for edge in edges:
    metro_graph.addEdge(edge[0], edge[1], edge[2], edge[3], edge[4])

# User interface for interacting with the metro graph
while True:
    print("------Welcome to Delhi Metro------")
    print("\nMenu:")
    print("1. Shortest path using BFS algorithm")
    print("2. Shortest distance using Dijkstra's Algorithm")
    print("3. Shortest Time using Prim's Algorithm")
    print("4. Minimum Cost using Kruskal's Algorithm")
    print("5. Exit")

    # Print station numbers and names
    print("Station Numbers and Names:")
    for number, name in metro_graph.station_numbers.items():
        print(f"{number}: {name}")

    # Take user input for the desired operation
    choice = input("Enter your choice (1/2/3/4/5): ")

    if choice == "1":
        start_station = int(input("Enter the start station number: "))
        end_station = int(input("Enter the end station number: "))
        shortest_path_bfs = metro_graph.bfs_shortest_path(start_station, end_station)
        if shortest_path_bfs:
            bfs_path = " -> ".join(metro_graph.get_station_name(station) for station in shortest_path_bfs)
            print("----------------------------------")
            print(f"Shortest path using BFS: {bfs_path}")
        else:
            print("----------------------------------")
            print("No path found using BFS.")
    
    elif choice == "2":
        start_station = int(input("Enter the start station number: "))
        end_station = int(input("Enter the end station number: "))
        shortest_path_dijkstra, distance_dijkstra = metro_graph.dijkstra_shortest_path(start_station, end_station)
        path = " -> ".join(metro_graph.get_station_name(station) for station in shortest_path_dijkstra)
        print("----------------------------------")
        print(f"Distance using Dijkstra's algorithm: {distance_dijkstra} km")

    elif choice == "3":
        start_station = int(input("Enter the start station number: "))
        end_station = int(input("Enter the end station number: "))
        mst_prim = metro_graph.prim_minimum_spanning_tree(start_station, end_station)
        total_travel_time = sum(edge[2] for edge in mst_prim)
        if(len(str(total_travel_time)) > 2):
            total_travel_time = int(total_travel_time / 10)
        print("----------------------------------")
        print(f"Minimum Spanning Tree using Prim's Algorithm (Shortest Time) total travel time from {metro_graph.get_station_name(start_station)} to {metro_graph.get_station_name(end_station)}: {total_travel_time} minutes")

    elif choice == "4":
        start_station = int(input("Enter the start station number: "))
        end_station = int(input("Enter the end station number: "))
        mst_kruskal = metro_graph.kruskal_minimum_spanning_tree(start_station, end_station)
        total_cost = sum(edge[2] for edge in mst_kruskal)
        if (len(str(total_cost)) > 2):
            total_cost = int(total_cost / 10)
        print("----------------------------------")
        print(f"Minimum Spanning Tree using Kruskal's Algorithm (Shortest Distance) cost from {metro_graph.get_station_name(start_station)} to {metro_graph.get_station_name(end_station)}: ₹{total_cost}")

    elif choice == "5":
        print("Exiting the program. Goodbye!")
        break

    else:
        print("Invalid choice. Please enter a valid option.")
