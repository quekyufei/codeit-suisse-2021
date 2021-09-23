def solve(input):
    solution = []
    for room in input:
        solution.append(RoomSolver(room).solve())
    
    return solution

class RoomSolver():
    def __init__(self, room):
        self.grid = room['grid']
        self.num_rows = len(self.grid)
        self.num_cols = len(self.grid[0])
        self.interested = room['interestedIndividuals']
        self.room_num = room['room']
        self.healthy_dudes = []
        self.any_vaccinated = False

    def solve(self):
        bfs_queue_A = []
        bfs_queue_B = []
        bfs_queue_X = []
        for r in range(self.num_cols):
            for c in range(self.num_cols):
                if self.grid[r][c] == 1:
                    self.healthy_dudes.append((r,c))
                elif self.grid[r][c] == 2:
                    self.any_vaccinated = True
                elif self.grid[r][c] == 3:
                    bfs_queue_A.append((r,c))
                    bfs_queue_B.append((r,c))
                    bfs_queue_X.append((r,c))
                    self.grid[r][c] = [3, 0, 0, 0]
                    continue

                self.grid[r][c] = [self.grid[r][c], -1, -1, -1]

        self.bfs(bfs_queue_A, 1)
        self.bfs(bfs_queue_B, 2)
        self.bfs_energy(bfs_queue_X)
        solution = {'room': self.room_num, 'p1': {}}
        for interested in self.interested:
            ir, ic = [int(x) for x in interested.split(',')]            
            solution['p1'][interested] = self.grid[ir][ic][1]
        
        solution['p2'] = self.find_max_time(1)
        solution['p3'] = self.find_max_time(2)
        solution['p4'] = self.find_max_time(3)
        return solution

    def bfs(self, bfs_queue, type):
        time = 1
        while len(bfs_queue) > 0:
            # infect adjacent ones
                # and add newly infected ones to the queue
            r, c = bfs_queue.pop(0)
            adj_list = self.get_adjacent(r, c, type)
            for ar, ac in adj_list:
                if self.grid[ar][ac][0] == 1 and self.grid[ar][ac][type] == -1:
                    self.grid[ar][ac][type] = time
                    bfs_queue.append((ar, ac))
            
            # increment time
            time += 1
        
        return time

    def bfs_energy(self, bfs_queue):
        while len(bfs_queue) > 0:
            r, c = bfs_queue.pop(0)
            current_energy = self.grid[r][c][3]
            adj_list = self.get_adjacent(r, c, 3)
            for ar, ac in adj_list:
                if self.grid[ar][ac][0] in [0, 2]:
                    if (current_energy + 1 < self.grid[ar][ac][3]) or self.grid[ar][ac][3] == -1:
                        self.grid[ar][ac][3] = current_energy + 1
                        bfs_queue.append((ar, ac))
                
                elif self.grid[ar][ac][0] == 2:
                    if current_energy < self.grid[ar][ac][3] or self.grid[ar][ac][3] == -1:
                        self.grid[ar][ac][3] = current_energy + 1
                        bfs_queue.append((ar, ac))


    def get_adjacent(self, r, c, type):
        list_adj = []
        if (r - 1) >= 0:
            list_adj.append((r - 1, c))
        
        if (r + 1) < self.num_rows:
            list_adj.append((r + 1, c))

        if (c - 1) >= 0:
            list_adj.append((r, c - 1))
        
        if (c + 1) < self.num_cols:
            list_adj.append((r, c + 1))

        if type == 2:
            if (r - 1) >= 0:
                if (c - 1) >= 0:
                    list_adj.append((r - 1, c - 1))
                if (c + 1) < self.num_cols:
                    list_adj.append((r - 1, c + 1))
            if (r + 1) < self.num_rows:
                if (c - 1) >= 0:
                    list_adj.append((r + 1, c - 1))
                if (c + 1) < self.num_cols:
                    list_adj.append((r + 1, c + 1))
        
        return list_adj
        
    def find_max_time(self, type):
        max_time = 0
        for r, c in self.healthy_dudes:
            if self.grid[r][c][type] == -1:
                return -1
            else:
                max_time = max(max_time, self.grid[r][c][type])
        return max_time
    
    def any_more_infected_dudes(self, type):
        for r, c in self.healthy_dudes:
            if self.grid[r][c][type] == -1:
                return True
        return False

[
  {
    "room": 1,
    "grid": [
      [0, 3],
      [0, 1]
    ],
    "interestedIndividuals": [
      "0,0"
    ]
  },
  {
    "room": 2,
    "grid": [
      [0, 3, 2],
      [0, 1, 1],
      [1, 0, 0]
    ],
    "interestedIndividuals": [
      "0,2", "2,0", "1,2"
    ]
  }
]