import queue
import heapq

def preprocess(Input):
    m=[]
    for i in range(6):
        m.append([0]*6)

    valid_dir=[]
    valid_dir.append([-1,-1])
    car=0

    for li in Input:
        car+=1
        index=li[0]+1
        y=li[1]
        x=li[2]
        Len=li[3]
        direction=li[4]
        if direction==1:
            valid_dir.append([0,2])
            x1=x
            for i in range(Len):
                m[y][x1]=index
                x1+=1
        else:
            valid_dir.append([1,3])
            y1=y
            for i in range(Len):
                m[y1][x]=index
                y1+=1
            
    initial_state=""
    for i in m:
        for j in i:
            if j<10:
                initial_state+="0"
            initial_state+=str(int(j))

    return initial_state, car, valid_dir


#direct: right=0, up=1, left=2, down=3
def move(ind, state, direct):
    tmp_m=[]
    tmp_s=state
    tmp=[]
    for i in range(0,72,2):
        s=int(tmp_s[i]+tmp_s[i+1])
        tmp.append(s)
        if i%12==10:
            tmp_m.append(tmp)
            tmp=[]
            
    target=[]
    for i in range(6):
        for j in range(6):
            if tmp_m[i][j]==ind:
                target.append([i,j])
    
    if direct==0:    #right
        t=target[-1]
        if t[1]<5 and tmp_m[t[0]][t[1]+1]==0:     #valid move
            t2=target[0]
            tmp_m[t2[0]][t2[1]]=0
            tmp_m[t[0]][t[1]+1]=ind
        else:
            return "0" #invaid move
    
    elif direct==1:  #up
        t=target[0]
        if t[0]>0 and tmp_m[t[0]-1][t[1]]==0:     #valid move
            t2=target[-1]
            tmp_m[t2[0]][t2[1]]=0
            tmp_m[t[0]-1][t[1]]=ind
        else:
            return "0" #invaid move
        
    elif direct==2:  #left
        t=target[0]
        if t[1]>0 and tmp_m[t[0]][t[1]-1]==0:     #valid move
            t2=target[-1]
            tmp_m[t2[0]][t2[1]]=0
            tmp_m[t[0]][t[1]-1]=ind
        else:
            return "0" #invaid move
        
    else:            #down
        t=target[-1]
        if t[0]<5 and tmp_m[t[0]+1][t[1]]==0:     #valid move
            t2=target[0]
            tmp_m[t2[0]][t2[1]]=0
            tmp_m[t[0]+1][t[1]]=ind
        else:
            return "0" #invaid move

    state_new=""
    for i in tmp_m:
        for j in i:
            if j<10:
                state_new+="0"
            state_new+=str(int(j))

    return state_new

def find_route(state_dict,terminal_state):
    route=[]
    route.append(terminal_state)
    st=terminal_state
    while st!="":
        st=state_dict[st]
        route.append(st)
    route.pop()
    route.reverse()
    return route

class state_node:
    def __init__(self,s,n):
        self.state=s
        self.step=n
        
    def g(self):
        return self.step
        
    def h(self): #count the number of car that block in front of the red car 
        target_row=[]
        s=self.state[24:36]
        for i in range(0,12,2):
            s1=int(s[i]+s[i+1])
            target_row.append(s1)
        cnt=0
        for i in reversed(target_row):
            if i==1:
                break
            if i!=0:
                cnt+=1
        return cnt
        
    
    def f(self): #f()=g()+h()
        return self.g()+self.h()

    def __lt__(self, nxt):
        return self.f() < nxt.f()

def A_Star(init_matrix):
    initial_state, car, valid_dir = preprocess(init_matrix)
    state_dict={}
    state_dict[initial_state]=""
    
    start=state_node(initial_state,0)
    state_pq=[]
    state_pq.append(start)
    heapq.heapify(state_pq)
    
    while True:
        '''
        li=[]
        for nodes in state_list:
            li.append(nodes.f())
        
        current_node=state_list[li.index(min(li))] #current_node=node who has minimum f
        state_list.remove(current_node)
        '''
        current_node=heapq.heappop(state_pq)
        now_state=current_node.state  
        
        if now_state[34]=="0" and now_state[35]=="1": #finish
            terminal_state=now_state
            break

        for i in range(car):
            new_state1=move(i+1,now_state,valid_dir[i+1][0])
            new_state2=move(i+1,now_state,valid_dir[i+1][1])
            if new_state1!="0" and state_dict.get(new_state1)==None: #push in state_list
                new_node=state_node(new_state1,current_node.step+1)
                #state_list.append(new_node)
                heapq.heappush(state_pq, new_node)
                state_dict[new_state1]=now_state
                
            if new_state2!="0" and state_dict.get(new_state2)==None: #push in state_list
                new_node=state_node(new_state2,current_node.step+1)
                #state_list.append(new_node)
                heapq.heappush(state_pq, new_node)
                state_dict[new_state2]=now_state
                
        
    A_star_route=find_route(state_dict,terminal_state)
    #print('A* route: '+str(len(A_star_route)-1)+' steps.')

    # put route in route dictionary
    padding = 150 - len(A_star_route)
    for i in range(padding):
        A_star_route.append("0")

    dic_route = [A_star_route]
    return dic_route

def str_to_mat(s):
    Li = []
    li = []
    for i in range(0,72,2):
        k = s[i] + s[i+1]
        li.append(int(k))
        if i % 12 == 10:
            Li.append(li)
            li = []
    return Li

def A_Star_next_state(curr_state, init_matrix):
    car = len(init_matrix)
    valid_dir = []
    valid_dir.append([-1, -1])
    for li in init_matrix:
        if li[4] == 1:
            valid_dir.append([0, 2])
        else:
            valid_dir.append([1, 3])

    initial_state = curr_state
    state_dict={}
    state_dict[initial_state]=""
    
    start=state_node(initial_state,0)
    state_pq=[]
    state_pq.append(start)
    heapq.heapify(state_pq)
    
    while True:
        current_node=heapq.heappop(state_pq)
        now_state=current_node.state  
        
        if now_state[34]=="0" and now_state[35]=="1": #finish
            terminal_state=now_state
            break

        for i in range(car):
            new_state1=move(i+1,now_state,valid_dir[i+1][0])
            new_state2=move(i+1,now_state,valid_dir[i+1][1])
            if new_state1!="0" and state_dict.get(new_state1)==None: #push in state_list
                new_node=state_node(new_state1,current_node.step+1)
                heapq.heappush(state_pq, new_node)
                state_dict[new_state1] = now_state
                
            if new_state2!="0" and state_dict.get(new_state2)==None: #push in state_list
                new_node=state_node(new_state2,current_node.step+1)
                heapq.heappush(state_pq, new_node)
                state_dict[new_state2] = now_state
                
        
    A_star_route = find_route(state_dict, terminal_state)
    return A_star_route


def find_next_state(curr_mat, route_dic, init_matrix):
    curr_state=""
    for i in curr_mat:
        for j in i:
            if j<10:
                curr_state+="0"
            curr_state+=str(int(j))
    # lookup route_dic
    for route in route_dic:
        for i in range(len(route)):
            if route[i] == curr_state:
                return route[i+1]

    A_star_route = A_Star_next_state(curr_state, init_matrix)
    # put route in route dictionary
    padding = 150 - len(A_star_route)
    for i in range(padding):
        A_star_route.append("0")
    route_dic.append(A_star_route)
    return A_star_route[1]






#init_matrix=[[0,2,0,2,1],[1,0,0,2,2],[2,0,3,3,1],[3,1,1,2,1],[4,1,3,2,2],[5,1,5,3,2],[6,2,2,2,2],[7,3,3,2,1],[8,4,2,2,2],[9,4,3,2,1],[10,5,3,3,1]]
#A_Star(init_matrix)

'''
f=open("prog1_puzzle/L25.txt")
lines=f.readlines()
Input=[]
for line in lines:
    I=[]
    for i in line.split():
        I.append(int(i))
    Input.append(I)

A_Star(Input)
'''
