from matplotlib import pyplot as plt, colors
from matplotlib.lines import Line2D
import pandas as pd
import numpy as np
import random
from collections import Counter

class UnidirectionalOpenSegment():
    """ A first attempt to tackle the problem with a simplified
    proposition of a unidirectional node with only one holding
    volume and one direction. It has the __init__ and __str__
    functions but only two other attributes: instantaneous_ouput
    and entering_reservoir_from_int_src"""
    def __init__(self, limit_holding_volume, holding_volume,
                 exiting_flux, position, capacity, penalty,
                 id, neighbors_list = None) -> None:
        self.limit_holding_volume = limit_holding_volume
        self.holding_volume = holding_volume
        self.exiting_flux = exiting_flux
        self.capacity = capacity
        self.position = position
        self.penalty = penalty
        self.id = id
        self.neighbors_list = neighbors_list

    def __str__(self):
        descricao = f"""
_Unidirectional node with reservoir_
node maximum reservoir limit: {self.limit_holding_volume}
reservoir occupation : {self.holding_volume}
exiting flux : {self.exiting_flux}
pipe capacity : {self.capacity}
node coordinates : {self.position}
intrinsic penalty : {self.penalty}
unique id: {self.id}
neighbors ids : {self.neighbors_list}
"""
        return descricao

    def node_to_pipe(self):
        if self.holding_volume + self.exiting_flux <= self.capacity:
            self.exiting_flux = self.exiting_flux + self.holding_volume
            self.holding_volume = 0
            return self
        else :
            self.holding_volume = self.holding_volume - (self.capacity - self.exiting_flux)
            self.exiting_flux = self.exiting_flux + (self.capacity - self.exiting_flux)
            return self

    def exit_system(self):
        temp = self.exiting_flux
        self.exiting_flux = 0
        return temp

    def entering_reservoir_from_ext_src(self, value):
        if self.limit_holding_volume - self.holding_volume >= value:
            self.holding_volume = self.holding_volume + value
        else:
            self.holding_volume = self.limit_holding_volume
        return None

    def entering_from_reservoir(self, node_list):
        max_output_flux = 0
        aux = []
        if self.neighbors_list is not None:
            for i in self.neighbors_list:
                temp = node_list[i].limit_holding_volume - \
                                node_list[i].holding_volume
                max_output_flux = max_output_flux + temp
                aux.append(temp/node_list[i].limit_holding_volume)
            aux = np.array(aux)/sum(aux)
            if max_output_flux > self.exiting_flux:
                for i in range(len(self.neighbors_list)):
                    node_list[self.neighbors_list[i]].holding_volume =\
                    node_list[self.neighbors_list[i]].holding_volume + \
                    self.exiting_flux*aux[i]
                self.exiting_flux = 0
                return self
            else:
                for i in range(len(self.neighbors_list)):
                    if self.neighbors_list[i] is not None:
                        node_list[self.neighbors_list[i]].holding_volume =\
                        node_list[self.neighbors_list[i]].holding_volume + \
                        max_output_flux*aux[i]
                self.exiting_flux = self.exiting_flux - max_output_flux
                return self
        return self



class BidirectionalOpenSegment():
    def __init__(self, left_holding_volume, right_holding_volume,
                 top_holding_volume, bottom_holding_volume, exiting_flux,
                 init_position, end_position, capacity, flux_direction,
                 id, penalty, left_limiting_volume, right_limiting_volume,
                 top_limiting_volume, bottom_limiting_volume,
                 exiting_flux_type = "eq_split", left_link = None,
                 right_link = None, top_link = None, bottom_link = None,
                 nn = None, type = None) -> None: 
        self.left_limiting_volume = left_limiting_volume
        self.right_limiting_volume = right_limiting_volume
        self.top_limiting_volume = top_limiting_volume
        self.bottom_limiting_volume = bottom_limiting_volume
        self.left_holding_volume = left_holding_volume
        self.top_holding_volume = top_holding_volume
        self.bottom_holding_volume = bottom_holding_volume
        self.right_holding_volume = right_holding_volume
        self.exiting_flux = exiting_flux
        self.capacity = capacity
        self.initial_position = init_position
        self.final_position = end_position
        self.direction = flux_direction
        self.penalty = penalty
        self.id = id
        self.exiting_flux_type = exiting_flux_type
        self.left_link = left_link
        self.right_link = right_link
        self.top_link = top_link
        self.bottom_link = bottom_link
        self.nn = nn
        self.type = type

    def __str__(self):
        descricao = f"""
_Nodo bidirecional com reservatório objeto_
identificador: {self.id}
Volume reservado a esquerda : {self.left_holding_volume}
Volume reservado a direita : {self.right_holding_volume}
Volume reservado àcima : {self.top_holding_volume}
Volume reservado àbaixo : {self.bottom_holding_volume}
capacidade do cano : {self.capacity}
penalidade intrínseca : {self.penalty}
direção do fluxo : {self.direction}
modulo do fluxo : {self.exiting_flux}
coordenada inicial do cano : {self.initial_position}
coordenada final do cano : {self.final_position}
left neighbor id : {self.left_link}
right neighbor id : {self.right_link}
top neighbor id : {self.top_link}
bottom neighbor id: {self.bottom_link}
neighbor's number : {self.nn}
"""
        return descricao

    def exiting_reservoir(self, mode):
        if mode == "l":
            if self.left_holding_volume < self.capacity:
                self.exiting_flux = self.left_holding_volume + self.exiting_flux
                self.left_holding_volume = 0
                return self
            else:
                self.left_holding_volume = self.left_holding_volume - self.capacity
                self.exiting_flux = self.capacity + self.exiting_flux
                return self
        elif mode == "r":
            if self.right_holding_volume < self.capacity:
                self.exiting_flux = self.right_holding_volume + self.exiting_flux
                self.right_holding_volume = 0
                return self
            else :
                self.right_holding_volume = self.right_holding_volume - self.capacity
                self.exiting_flux = self.capacity + self.exiting_flux
                return self
        elif mode == 't':
            if self.top_holding_volume < self.capacity:
                self.exiting_flux = self.top_holding_volume + self.exiting_flux
                self.top_holding_volume = 0
                return self
            else :
                self.top_holding_volume = self.top_holding_volume - self.capacity
                self.exiting_flux = self.capacity + self.exiting_flux
                return self
        elif mode == "b":
            if self.bottom_holding_volume < self.capacity:
                self.exiting_flux = self.bottom_holding_volume + self.exiting_flux
                self.bottom_holding_volume = 0
                return self
            else :
                self.bottom_holding_volume = self.bottom_holding_volume - self.capacity
                self.exiting_flux = self.capacity + self.exiting_flux
                return self
        
        else:
            print(f"Error. p 141. Unknown direction option in [exiting_reservoir] function: {self.direction}")

    def entering_reservoir_from_int_src(self, add_flux, inc_src_obj, mode):
        if mode == 'l':
            self.left_holding_volume = self.left_holding_volume + add_flux
            inc_src_obj.exiting_flux = inc_src_obj.exiting_flux - add_flux
            return self
        elif mode == 'r':
            self.right_holding_volume = self.right_holding_volume + add_flux
            inc_src_obj.exiting_flux = inc_src_obj.exiting_flux - add_flux
            return self
        elif mode == 't':
            self.top_holding_volume = self.top_holding_volume + add_flux
            inc_src_obj.exiting_flux = inc_src_obj.exiting_flux - add_flux
            return self
        elif mode == 'b':
            self.bottom_holding_volume = self.bottom_holding_volume + add_flux
            inc_src_obj.exiting_flux = inc_src_obj.exiting_flux - add_flux
            return self
        else:
            print(f"Error. Unknown mode option: {mode}")
            return None

    def outside_incoming_flux(self, add_flux, mode):
        if mode == 'l':
            self.left_holding_volume = self.left_holding_volume + add_flux
            return self
        elif mode == 'r':
            self.right_holding_volume = self.right_holding_volume + add_flux
            return self
        elif mode == 't':
            self.top_holding_volume = self.top_holding_volume + add_flux
            return self
        elif mode == 'b':
            self.bottom_holding_volume = self.bottom_holding_volume + add_flux
            return self
        else:
            print(f"Error. Unknown mode option: {mode}")
            return None

    def exiting_system_from_pipe(self):
        if self.exiting_flux < self.capacity:
            self.exiting_flux = 0
            return self
        else:
            self.exiting_flux = self.exiting_flux - self.capacity
            return self

class SegmentNetwork():
    def __init__(self, pipes_number, link_list, objects_list,
                 list_incoming_flow, list_outcoming_flow,):
        self.pipes_number = pipes_number
        self.linked_pipes_list = link_list
        self.all_pipes_list = objects_list
        self.list_incoming_flow = list_incoming_flow
        self.list_outcoming_flow = list_outcoming_flow
        aux_in = 0 
        for i in self.list_incoming_flow:
            aux_in = aux_in + self.all_pipes_list[i[0]][1].exiting_flux
        self.overall_entering_flux = aux_in
        aux_out = 0 
        for i in self.list_outcoming_flow:
            aux_out = aux_out + self.all_pipes_list[i[0]][1].exiting_flux
        self.overall_exiting_flux = aux_out

    def __str__(self):
        description = """
Network of pipes object
linked pipes list :
"""
        for item in self.linked_pipes_list:
            description = description + str(item) + "\n"
        description = description + """
List of incoming flux : 
"""
        for item in self.list_incoming_flow:
            description = description + f"pipe id: {item[0]};" + f" flux : {item[1]};" + "\n"
        description = description + """
List of outcoming flux : 
"""
        for item in self.list_outcoming_flow:
            description = description + f"pipe id: {item[0]};" + f" flux : {item[1]};" + "\n"
        description = description + f"""
overall entering flux : {self.overall_entering_flux}
overall exiting flux : {self.overall_exiting_flux}"""
        return description

    def plot_network(self, plot_directions = False):
        llv, lhv, ef, c, x_i, y_i, id = [], [], [], [], [], [], []
        rlv, rhv, blv, bhv, tlv, thv =  [], [], [], [], [], []
        for item in self.all_pipes_list:
            llv.append(item[1].left_limiting_volume)
            lhv.append(item[1].left_holding_volume)
            rlv.append(item[1].right_limiting_volume)
            rhv.append(item[1].right_holding_volume)
            blv.append(item[1].bottom_limiting_volume)
            bhv.append(item[1].bottom_holding_volume)
            tlv.append(item[1].top_limiting_volume)
            thv.append(item[1].top_holding_volume)
            ef.append(item[1].exiting_flux)
            c.append(item[1].capacity)
            id.append(item[1].id)
            x_i.append(item[1].initial_position[0])
            y_i.append(item[1].initial_position[1])
        df = pd.DataFrame({"id": id, "xi": x_i, "yi": y_i, 
                           "ef": ef, "c": c, 'lhv': lhv, 'llv': llv,
                           'rhv': rhv, 'rlv': rlv,
                           'bhv': bhv, 'blv': blv,
                           'thv': thv, 'tlv': tlv,})
        #print(df)
        fig, ax = plt.subplots()
        cmap = plt.cm.viridis
        #norm = colors.Normalize(vmin=min(values), vmax=max(values))
        norm = colors.Normalize(vmin=-10, vmax=10)
        #for _, row in df.iterrows():
        ax.scatter(df.xi - 0.1, df.yi, c="black", marker='o', linewidth=1, s = df.llv, alpha = 0.1)
        ax.scatter(df.xi + 0.1, df.yi, c="black", marker='o', linewidth=1, s = df.rlv, alpha = 0.1)
        ax.scatter(df.xi, df.yi - 0.1, c="black", marker='o', linewidth=1, s = df.blv, alpha = 0.1)
        ax.scatter(df.xi, df.yi + 0.1, c="black", marker='o', linewidth=1, s = df.tlv, alpha = 0.1)
        #ax.scatter(df.xi, df.yi, marker='s', color=cmap(norm(df.ef.values)), s = 10*df.ef.values)
        ax.scatter(df.xi - 0.1, df.yi, marker='o', c="black", s = df.lhv, alpha = 0.9)
        ax.scatter(df.xi + 0.1, df.yi, marker='o', c="black", s = df.rhv, alpha = 0.9)
        ax.scatter(df.xi, df.yi - 0.1, marker='o', c="black", s = df.bhv, alpha = 0.9)
        ax.scatter(df.xi, df.yi + 0.1, marker='o', c="black", s = df.thv, alpha = 0.9)
        ax.set_xticks(df.xi)
        ax.set_yticks(df.yi)
        sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
        #fig.colorbar(sm)
        for i in self.all_pipes_list:
            ax.text(i[1].initial_position[0] + 0.01,
                    i[1].initial_position[1] + 0.01,
                    s = 'node ' + str(i[1].id), alpha = 0.4)
        
        for item in self.linked_pipes_list:
            #for _, row_2 in df.iterrows():
            #    if (row.xi, row.yi) != (row_2.xi, row_2.yi):
    
            #x = [df[df['id'] == item[0]]['xi'], df[df['id'] == item[1]]['xi']]
            #y = [df[df['id'] == item[0]]['yi'], df[df['id'] == item[1]]['yi']]
            x_0 = df.loc[df['id'] == item[0], 'xi'].to_list()[0]
            y_0 = df.loc[df['id'] == item[0], 'yi'].to_list()[0]
            x_1 = df.loc[df['id'] == item[1], 'xi'].to_list()[0]
            y_1 = df.loc[df['id'] == item[1], 'yi'].to_list()[0]
            x = [x_0, x_1]
            y = [y_0, y_1]
            
            #ax.plot([row.xi, row.xf], [row.yi, row.yf], c='black', lw=row.ef, alpha=0.5, linestyle=':')
            ax.plot( x, y, c='black', lw = df[df['id'] == item[0]]['ef'].tolist()[0], alpha=1, linestyle=':')
        
        if plot_directions:
            for item in self.all_pipes_list:
                if item[1].type == 'exit':
                    continue
                neighnor_id = []
                if item[1].left_link is not None:
                    neighnor_id.append(item[1].left_link)
                if item[1].right_link is not None:
                    neighnor_id.append(item[1].right_link)
                if item[1].bottom_link is not None:
                    neighnor_id.append(item[1].bottom_link)
                if item[1].top_link is not None:
                    neighnor_id.append(item[1].top_link)
                if len(neighnor_id) > 0:
                    for id in neighnor_id:
                        x = self.all_pipes_list[id][1].initial_position[0]
                        y = self.all_pipes_list[id][1].initial_position[1]
                        ax.annotate('', xy = (x, y),
                                    xytext = (item[1].initial_position[0], item[1].initial_position[1]),
                                    arrowprops = {'width': 0.5, 'headwidth': 5,
                                                'alpha': 0.2})
        

        plt.show()
        
        return None

    def join_pipes(self, first_pipe, second_pipe):
        if (first_pipe, second_pipe) not in self.linked_pipes_list:
            self.linked_pipes_list.append((first_pipe, second_pipe))
        return self
    
    def network_instantaneous_flux(self, objects_list, node_list, receiving = True):
        # flux entry
        
        # Counter of neighbors
        nodes_connected = [i[0] for i in self.linked_pipes_list]
        count_nodes = Counter(nodes_connected)
        for i in self.linked_pipes_list:
            if i[1] not in count_nodes.keys():
                count_nodes[i[1]] = 1
        count_nodes = pd.DataFrame.from_dict(count_nodes, orient='index').reset_index().rename(columns={'index':'id', 0:'count'})
        count_nodes["factor"] = count_nodes['count'].apply(lambda x: 1/x)
        count_nodes = pd.merge(count_nodes, node_list, on ='id')
        #print(node_list)
        count_nodes['left'] = None
        count_nodes['right'] = None
        count_nodes['top'] = None
        count_nodes['bottom'] = None

        
        for i in self.linked_pipes_list:
            if node_list['x'].values[i[1]] > node_list['x'].values[i[0]]:
                count_nodes.loc[count_nodes['id'] == i[0], 'left'] = i[1]
            if node_list['x'].values[i[1]] < node_list['x'].values[i[0]]:
                count_nodes.loc[count_nodes['id'] == i[0], 'right'] = i[1]
            if node_list['y'].values[i[1]] > node_list['y'].values[i[0]]:
                count_nodes.loc[count_nodes['id'] == i[0], 'top'] = i[1]
            if node_list['y'].values[i[1]] < node_list['y'].values[i[0]]:
                count_nodes.loc[count_nodes['id'] == i[0], 'bottom'] = i[1]
        #print(count_nodes)
        
        #for i in self.all_pipes_list:
        # getting from the reservoirs to the pipes
        if receiving is True:
            for i in self.list_incoming_flow:
                for j in objects_list:
                    if i[0] == j[0]:
                        if count_nodes['left'].values[i[0]] is not None:
                            j[1].left_holding_volume = j[1].left_holding_volume + i[1]
                        if count_nodes['right'].values[i[0]] is not None:
                            j[1].right_holding_volume = j[1].right_holding_volume + i[1]
                        if count_nodes['top'].values[i[0]] is not None:
                            j[1].top_holding_volume = j[1].top_holding_volume + i[1]
                        if count_nodes['bottom'].values[i[0]] is not None:
                            j[1].bottom_holding_volume = j[1].bottom_holding_volume + i[1]
                
                        
        for i in count_nodes['id'].values:
            for j in objects_list[i][1].direction:
                objects_list[i][1].exiting_reservoir(j[0])
        
        #print(count_nodes)
        #print(count_nodes['left'])
        for i in count_nodes['id'].values:
            id_left = count_nodes['left'].values[i]
            id_right = count_nodes['right'].values[i]
            id_top = count_nodes['top'].values[i]
            id_bottom = count_nodes['bottom'].values[i]
            add_flux = objects_list[i][1].exiting_flux * count_nodes['factor'].values[i] 
            print(i)
            print(objects_list[i][1].exiting_flux)
            if id_left is not None:
                objects_list[id_left][1].entering_reservoir_from_int_src(add_flux, mode='left')
            if id_right is not None:
                objects_list[id_right][1].entering_reservoir_from_int_src(add_flux, mode='right')
            if id_top is not None:
                objects_list[id_top][1].entering_reservoir_from_int_src(add_flux, mode='top')
            if id_bottom is not None:
                objects_list[id_bottom][1].entering_reservoir_from_int_src(add_flux, mode='bottom')
            #print(i)
            print(objects_list[i][1].exiting_flux)
        '''
        for i in count_nodes['id'].values:
            print(i)
            print(objects_list[i][1].exiting_flux)
            print(objects_list[i][1].capacity)
            print(objects_list[i][1].left_holding_volume)
            print(objects_list[i][1].right_holding_volume)
            print(objects_list[i][1].top_holding_volume)
            print(objects_list[i][1].bottom_holding_volume)
            print('\n\n')
        '''
        return self

class tools():
        
    def plot_rectangular_grid(grid_df):
        grid_df['color'] = grid_df["type"].apply(lambda x: "black" if x == "center" else \
                                                ("red" if x == "contour" else ("blue") if x == "entry" else "green"))
        ax = grid_df.plot.scatter(x = 'x', y = 'y', c = 'color', s = 20)
        for idx, row in grid_df.iterrows():
            if row['type'] == 'exit':
                continue
            neighnor_id = []
            if row['left'] is not None:
                neighnor_id.append(row['left'])
            if row['right'] is not None:
                neighnor_id.append(row['right'])
            if row['bottom'] is not None:
                neighnor_id.append(row['bottom'])
            if row['top'] is not None:
                neighnor_id.append(row['top'])
            if len(neighnor_id) > 0:
                for id in neighnor_id:
                    x = grid_df['x'][id]
                    y = grid_df['y'][id]
                    ax.annotate('', xy = (x, y),
                                xytext = (row['x'], row['y']),
                                arrowprops = {'width': 0.5, 'headwidth': 5,
                                            'alpha': 0.2})
        #grid_df.plot.scatter(x = 'x', y = 'y', c = 'color', s = 20, ax = ax)
        plt.show()
        return None

    def build_retangle_grid (inf_lim_x, sup_lim_x, inf_lim_y, sup_lim_y, entry_points_coor,                         
                            exit_points_coor,
                            exit_direction_list = ['r', 't'], visualization = False):
        temp_x = [i for i in range(inf_lim_x, sup_lim_x + 1)]
        temp_y = [i for i in range(inf_lim_y, sup_lim_y + 1)]
        x = pd.DataFrame({"x": temp_x})
        x['key'] = 1
        y = pd.DataFrame({"y": temp_y})
        y['key'] = 1
        nodes_df = pd.merge(x, y, on ='key').drop("key", 1)
        nodes_df['type'] = 'center'
        nodes_df['left'] = None
        nodes_df['right'] = None
        nodes_df['top'] = None
        nodes_df['bottom'] = None
        nodes_df['nn'] = None
        nodes_df.loc[nodes_df['x'] == inf_lim_x, 'type'] = "contour"
        nodes_df.loc[nodes_df['x'] == sup_lim_x, 'type'] = "contour"
        nodes_df.loc[nodes_df['y'] == inf_lim_y, 'type'] = "contour"
        nodes_df.loc[nodes_df['y'] == sup_lim_y, 'type'] = "contour"
        nodes_df['id'] = nodes_df.index
        for i in entry_points_coor:
            nodes_df.loc[(nodes_df['x'] == i[0]) & (nodes_df['y'] == i[1]), "type"] = 'entry'
        for i in exit_points_coor:
            idx = nodes_df.loc[(nodes_df['x'] == i[0]) & (nodes_df['y'] == i[1]), 'id']
            nodes_df.loc[idx, "type"] = "exit"
            #nodes_df.loc[idx, "nn"] = 0
            for j in exit_direction_list:
                if j == 'l':
                    nodes_df.loc[idx, "left"] = -1
                elif j == 'r':
                    nodes_df.loc[idx, "right"] = -1
                elif j == 'b':
                    nodes_df.loc[idx, "bottom"] = -1
                elif j == 't':
                    nodes_df.loc[idx, "top"] = -1
                else:
                    print(f'Unreconized [exit_direction_list] identifier: {j}')
                    return None
        for idx, row in nodes_df.iterrows():
            x = nodes_df['x'][idx]
            y = nodes_df['y'][idx]
            if row['type'] == 'center':
                right_n_id = nodes_df.loc[(nodes_df['x'] == x + 1) &\
                                (nodes_df['y'] == y), 'id'].to_list()[0]
                top_n_id = nodes_df.loc[(nodes_df['x'] == x) &\
                                (nodes_df['y'] == y + 1), 'id'].to_list()[0]
                nodes_df.loc[idx, 'right'] = right_n_id
                nodes_df.loc[idx, 'top'] = top_n_id
                nodes_df.loc[idx, 'nn'] = 2
            elif row['type'] == 'contour' or row['type'] == 'entry':
                if row['x'] == sup_lim_x:
                    if row['y'] == sup_lim_y:
                        bottom_n_id = nodes_df.loc[(nodes_df['x'] == x) &\
                                (nodes_df['y'] == y - 1), 'id'].to_list()[0]
                        nodes_df.loc[idx, 'bottom'] = bottom_n_id
                        nodes_df.loc[idx, 'nn'] = 1
                    else:
                        #left_n_id = nodes_df.loc[(nodes_df['x'] == x - 1) &\
                        #           (nodes_df['y'] == y), 'id'].to_list()[0]
                        top_n_id = nodes_df.loc[(nodes_df['x'] == x) &\
                                        (nodes_df['y'] == y + 1), 'id'].to_list()[0]
                        #nodes_df.loc[idx, 'right'] = right_n_id
                        nodes_df.loc[idx, 'top'] = top_n_id
                        nodes_df.loc[idx, 'nn'] = 1
                else:
                    if row['y'] == sup_lim_y:
                        right_n_id = nodes_df.loc[(nodes_df['x'] == x + 1) &\
                                (nodes_df['y'] == y), 'id'].to_list()[0]
                        nodes_df.loc[idx, 'left'] = right_n_id
                        nodes_df.loc[idx, 'nn'] = 1
                    else:
                        right_n_id = nodes_df.loc[(nodes_df['x'] == x + 1) &\
                                (nodes_df['y'] == y), 'id'].to_list()[0]
                        top_n_id = nodes_df.loc[(nodes_df['x'] == x) &\
                                        (nodes_df['y'] == y + 1), 'id'].to_list()[0]
                        nodes_df.loc[idx, 'left'] = right_n_id
                        nodes_df.loc[idx, 'top'] = top_n_id
                        nodes_df.loc[idx, 'nn'] = 2
        if visualization:
            tools.plot_rectangular_grid(nodes_df)
        return nodes_df

class experiments():
    """
    Set of predefined experiments to explore the lab and its capabilities
    """
    def plot_UOS_list(node_list):
        """
        Plot a network of UOS nodes connected and interacting among thenselves. Ideally
        it is made to represents the evolution of nodes connected in a line with one 
        entry and one exit, but it can represent more complex networks with few adaptations
        """
        lhv, hv, ef, c, x, y, pe, id = [], [], [], [], [], [], [], []
        for object in node_list:
            lhv.append(object.limit_holding_volume)
            hv.append(object.holding_volume)
            ef.append(object.exiting_flux)
            c.append(object.capacity)
            x.append(object.position[0])
            y.append(object.position[1])
            pe.append(object.penalty)
            id.append(object.id)
        df = pd.DataFrame({"id": id, "x": x, "y": y, 
                           "ef": ef, "c": c, 'lhv': lhv,
                           'hv': hv})
        fig, ax = plt.subplots()
        cmap = plt.cm.viridis
        norm = colors.Normalize(vmin=-10, vmax=10)
        ax.scatter(df.x, df.y, c="black", marker='o', linewidth=1, s = df.lhv, alpha = 0.1)
        ax.scatter(df.x, df.y, c="black", marker='o', linewidth=1, s = df.hv, alpha = 0.8)
        ax.set_xticks(df.x)
        ax.set_yticks(df.y)
        sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
        for i in node_list:
            ax.text(i.position[0] + 0.01, i.position[1] + 0.01,
                    s = 'node ' + str(i.id), alpha = 0.4)
            if i.neighbors_list is not None:
               for j in i.neighbors_list:
                    x_0 = node_list[i.id].position[0]
                    y_0 = node_list[i.id].position[1]
                    x_1 = node_list[j].position[0]
                    y_1 = node_list[j].position[1]
                    x = [x_0, x_1]
                    y = [y_0, y_1]
                    ax.annotate('', xy = (x_1, y_1 +  0.01),
                                    xytext = (x_0 + 0.01, y_0 + 0.01),
                                    arrowprops = {'width': 0.5, 'headwidth': 5,
                                                'alpha': 0.2})
            if i.neighbors_list is not None:
                for j in i.neighbors_list:
                    x_0 = node_list[i.id].position[0]
                    y_0 = node_list[i.id].position[1]
                    x_1 = node_list[j].position[0]
                    y_1 = node_list[j].position[1]
                    x = [x_0, x_1]
                    y = [y_0, y_1]
                    ax.plot( x, y, c='black', lw = i.capacity/2, alpha=0.1, linestyle=':')
                    ax.plot( x, y, c='black', lw = i.exiting_flux/2, alpha=0.8, linestyle=':')
        plt.show()
        return None
    
    def teste_UOS(limit_holding_volume_list = [60],
                  holding_volume_list = [50],
                  exiting_flux_list = [0],
                  position_list = [[0, 0]],
                  capacity_list = [5],
                  penalty_list = [0],
                  id_list = [0],
                  input_list = [[0, 10]],
                  output_list = [0],
                  neighbors_list = None):

        node_list = []
        for i in range(len(id_list)):
            node_list.append(UnidirectionalOpenSegment(
                            limit_holding_volume = limit_holding_volume_list[i],
                            holding_volume = holding_volume_list[i],
                            exiting_flux = exiting_flux_list[i],
                            position = position_list[i],
                            capacity = capacity_list[i],
                            penalty = penalty_list[i],
                            id = id_list[i]))
        if neighbors_list is not None:
            for i in range(len(id_list)):
                node_list[i].neighbors_list = neighbors_list[i]
                         
        
        for i in input_list:
            node_list[i[0]].entering_reservoir_from_ext_src(value = i[1])
        aux = 0
        for k in range(30):
            print(k)
            print("count", aux)
            for i in node_list:
                i.node_to_pipe()
            experiments.plot_UOS_list(node_list)
            #for j in node_list:
            #        print(j)
            for i in node_list:
                i.entering_from_reservoir(node_list)
            
            for i in output_list:
                aux = aux + node_list[i].exit_system()
                
            

        

    def teste_BOS():
        node_list = []
        node_list.append(BidirectionalOpenSegment(left_holding_volume = 10,
                                    right_holding_volume = 0,
                                    top_holding_volume = 0,
                                    bottom_holding_volume = 10,
                                    exiting_flux = 0,
                                    init_position = (0, 0),
                                    end_position = None,
                                    capacity = 2,
                                    flux_direction = ["left_to_right", "bottom_to_top"],
                                    penalty = 0,
                                    id = 0, 
                                    left_limiting_volume = 100, 
                                    right_limiting_volume = 100,
                                    top_limiting_volume = 100, 
                                    bottom_limiting_volume = 100,
                                    left_link = 1,
                                    right_link = None,
                                    top_link = 2,
                                    bottom_link = None,
                                    nn = 2))
        node_list.append(BidirectionalOpenSegment(left_holding_volume = 0,
                                    right_holding_volume = 0,
                                    top_holding_volume = 0,
                                    bottom_holding_volume = 0,
                                    exiting_flux = 0,
                                    init_position = (1, 0),
                                    end_position = None,
                                    capacity = 1,
                                    flux_direction = ["left_to_right"],
                                    penalty = 0,
                                    id = 1, 
                                    left_limiting_volume = 100, 
                                    right_limiting_volume = 100,
                                    top_limiting_volume = 100, 
                                    bottom_limiting_volume = 100,
                                    left_link = -1,
                                    right_link = None,
                                    top_link = None,
                                    bottom_link = None))
        node_list.append(BidirectionalOpenSegment(left_holding_volume = 0,
                                    right_holding_volume = 0,
                                    top_holding_volume = 0,
                                    bottom_holding_volume = 0,
                                    exiting_flux = 0,
                                    init_position = (0, 1),
                                    end_position = None,
                                    capacity = 1,
                                    flux_direction = ["bottom_to_top"],
                                    penalty = 0,
                                    id = 2, 
                                    left_limiting_volume = 100, 
                                    right_limiting_volume = 100,
                                    top_limiting_volume = 100, 
                                    bottom_limiting_volume = 100,
                                    left_link = None,
                                    right_link = None,
                                    top_link = -1,
                                    bottom_link = None))
        
        def external_source(object, incoming_flux):
            for j in object.direction:
                object.outside_incoming_flux(incoming_flux, j[0])

        def reservoir_to_pipes(object):
            if object.left_holding_volume > 0:
                object.exiting_reservoir("l")
            if object.right_holding_volume > 0:
                object.exiting_reservoir("r")
            if object.top_holding_volume > 0:
                object.exiting_reservoir("t")
            if object.bottom_holding_volume > 0:
                object.exiting_reservoir("b")

        def pipes_to_reservoir(origin_object, target_object, mode, add_flux):
            target_object.entering_reservoir_from_int_src(add_flux, origin_object, mode)

        entry_list = [[0, 0]]
        for i in entry_list:
            external_source(object = node_list[i[0]], incoming_flux = i[1])
        for m in range(0, 10):
            for i in node_list:
                reservoir_to_pipes(object = i)
            for i in node_list:
                if i.nn is not None:
                    pipe_flux = i.exiting_flux / i.nn
                    if i.left_link is not None:
                        pipes_to_reservoir(origin_object = i,
                                        target_object = node_list[i.left_link],
                                        mode = 'l',
                                        add_flux = pipe_flux)
                    if i.right_link is not None:
                        pipes_to_reservoir(origin_object = i,
                                        target_object = node_list[i.right_link],
                                        mode = 'r',
                                        add_flux = pipe_flux)
                    if i.top_link is not None:
                        pipes_to_reservoir(origin_object = i,
                                        target_object = node_list[i.top_link],
                                        mode = 't',
                                        add_flux = pipe_flux)
                    if i.bottom_link is not None:
                        pipes_to_reservoir(origin_object = i,
                                        target_object = node_list[i.bottom_link],
                                        mode = 'b',
                                        add_flux = pipe_flux)
                else:
                    if i.left_link == -1:
                        i.exiting_system_from_pipe()
                    if i.right_link == -1:
                        i.exiting_system_from_pipe()
                    if i.top_link == -1:
                        i.exiting_system_from_pipe()
                    if i.bottom_link == -1:
                        i.exiting_system_from_pipe()
            print(m,"\n\n")
            print(node_list[0])
            #print(node_list[1])
            #print(node_list[2])
    
            
        #B.entering_reservoir_from_int_src(add_flux = 1, inc_src_obj = A, mode = 'l')
        #print(A)
        #print(B)

        #print(B)
        
    def initialize_BOS(left_holding_volume, right_holding_volume,
                    top_holding_volume, bottom_holding_volume,
                    exiting_flux, init_position, end_position,
                    capacity, id, left_link = None,
                    right_link = None, top_link = None,
                    bottom_link = None, nn = None,
                    flux_direction = "left_to_right",
                    penalty = 0, left_limiting_volume = 100,
                    right_limiting_volume = 100, top_limiting_volume = 100,
                    bottom_limiting_volume = 100, type = None):
        return BidirectionalOpenSegment(left_holding_volume = left_holding_volume,
                                        right_holding_volume = right_holding_volume,
                                        top_holding_volume = top_holding_volume,
                                        bottom_holding_volume = bottom_holding_volume,
                                        exiting_flux = exiting_flux,
                                        init_position = init_position,
                                        end_position = end_position,
                                        capacity = capacity,
                                        flux_direction = flux_direction,
                                        penalty = penalty,
                                        id = id,
                                        left_limiting_volume = left_limiting_volume,
                                        right_limiting_volume = right_limiting_volume,
                                        top_limiting_volume = top_limiting_volume,
                                        bottom_limiting_volume = bottom_limiting_volume,
                                        left_link = left_link,
                                        right_link = right_link,
                                        top_link = top_link,
                                        bottom_link = bottom_link,
                                        nn = nn,
                                        type = type
                                        )

    def initialize_BOS_list(params_list):
        OL = []
        for params in params_list:
            OL.append(experiments.initialize_BOS(left_holding_volume = params[0], right_holding_volume = params[1],
                                    top_holding_volume = params[2], bottom_holding_volume = params[3],
                                    exiting_flux = params[4], init_position = params[5],
                                    end_position = params[6], capacity = params[7],
                                    flux_direction= params[8], id = params[9], penalty = params[10],
                                    left_limiting_volume = params[11], right_limiting_volume = params[12],
                                    top_limiting_volume = params[13], bottom_limiting_volume = params[14], 
                                    left_link = params[15], right_link = params[16], top_link = params[17],
                                    bottom_link = params[18], nn = params[19], type = params[20]))
        return OL
        
    def initialize_BOS_rectangular_network(inf_lim_x, sup_lim_x, inf_lim_y, sup_lim_y,
                                        entry_points_coor, exit_points_coor):
        
        #[left_holding_volume = 0,
        #right_holding_volume = 0,
        #top_holding_volume = 0,
        #bottom_holding_volume = 0,
        #exiting_flux = 0,
        #init_position = (node_list[i]["x"], node_list[i]["y"])
        #end_position = None,
        #capacity = random.random.randint(1,5),
        #flux_direction = ["right_to_left", "bottom_to_top"],
        #id = list(node_list[i].values)[0],
        #penalty = 0,
        #left_limiting_volume = 50,
        #right_limiting_volume = 50,
        #top_limiting_volume = 50,
        #bottom_limiting_volume = 50,
        #left_link = None
        #right_link = None
        #top_link = None
        #bottom_link = None
        #nn = nn
        #type = type
        #exiting_flux_type = "eq_split"]
        node_list = tools.build_retangle_grid (inf_lim_x, sup_lim_x, inf_lim_y, sup_lim_y,
                                        entry_points_coor, exit_points_coor)

        #print(node_list)
        params_list = []
        for _, row in node_list.iterrows():    
            if row["type"] == "center":
                params_list.append([0, 0, 0, 0, 0, (row["x"], row["y"]),
                                None, random.randint(1,5), ["right_to_left", "bottom_to_top"],
                                row['id'], 0, 50, 50, 50, 50, row['left'], row['right'],
                                row['top'], row['bottom'], row['nn'], row['type']])
        
            else: #row["type"] == "contour":
                if row["x"] == inf_lim_x:
                    if row["y"] == inf_lim_y:
                        params_list.append([0, 0, 0, 0, 0, (row["x"], row["y"]),
                                            None, random.randint(1,5), ["left_to_right", "bottom_to_top"],
                                            row['id'], 0, 50, 50, 50, 50, row['left'], row['right'],
                                row['top'], row['bottom'], row['nn'], row['type']])
                    elif row["y"] == sup_lim_y:           
                        params_list.append([0, 0, 0, 0, 0, (row["x"], row["y"]),
                                            None, random.randint(1,5), ["left_to_right", "top_to_bottom"],
                                            row['id'], 0, 50, 50, 50, 50, row['left'], row['right'],
                                row['top'], row['bottom'], row['nn'], row['type']])
                    else:
                        params_list.append([0, 0, 0, 0, 0, (row["x"], row["y"]),
                                            None, random.randint(1,5), ["left_to_right"],
                                            row['id'], 0, 50, 50, 50, 50, row['left'], row['right'],
                                row['top'], row['bottom'], row['nn'], row['type']])
                elif row["x"] == sup_lim_x:
                    if row["y"] == inf_lim_y:
                        params_list.append([0, 0, 0, 0, 0, (row["x"], row["y"]),
                                            None, random.randint(1,5), ["right_to_left", "bottom_to_top"],
                                            row['id'], 0, 50, 50, 50, 50, row['left'], row['right'],
                                row['top'], row['bottom'], row['nn'], row['type']])
                    elif row["y"] == sup_lim_y:           
                        params_list.append([0, 0, 0, 0, 0, (row["x"], row["y"]),
                                            None, random.randint(1,5), ["right_to_left", "top_to_bottom"],
                                            row['id'], 0, 50, 50, 50, 50, row['left'], row['right'],
                                row['top'], row['bottom'], row['nn'], row['type']])
                    else:
                        params_list.append([0, 0, 0, 0, 0, (row["x"], row["y"]),
                                            None, random.randint(1,5), ["right_to_left"],
                                            row['id'], 0, 50, 50, 50, 50, row['left'], row['right'],
                                row['top'], row['bottom'], row['nn'], row['type']])
                elif row["y"] == inf_lim_y:
                    params_list.append([0, 0, 0, 0, 0, (row["x"], row["y"]),
                                            None, random.randint(1,5), ["bottom_to_top"],
                                            row['id'], 0, 50, 50, 50, 50, row['left'], row['right'],
                                row['top'], row['bottom'], row['nn'], row['type']])
                elif row["y"] == sup_lim_y:
                    params_list.append([0, 0, 0, 0, 0, (row["x"], row["y"]),
                                            None, random.randint(1,5), ["top_to_bottom"],
                                            row['id'], 0, 50, 50, 50, 50, row['left'], row['right'],
                                row['top'], row['bottom'], row['nn'], row['type']])
                else:
                    print("Unknown type value")
                    return None
        pipes_list = experiments.initialize_BOS_list(params_list)
        objects_list = [[i.id, i] for i in pipes_list]
        
        link_list = []
        for i in node_list['id']:
            if pipes_list[i].type == 'exit':
                continue
            
            if node_list.loc[i, 'left'] is not None:
                link_list.append([i, node_list.loc[i, 'left']])
            if node_list.loc[i, 'right'] is not None:
                link_list.append([i, node_list.loc[i, 'right']])
            if node_list.loc[i, 'top'] is not None:
                link_list.append([i, node_list.loc[i, 'top']])
            if node_list.loc[i, 'bottom'] is not None:
                link_list.append([i, node_list.loc[i, 'bottom']])

        temp = node_list.loc[node_list['type'] == 'entry', 'id'].tolist()
        incoming_flow_list = [[i, 10] for i in temp]
        temp = node_list.loc[node_list['type'] == 'exit', 'id'].tolist()
        outcoming_flow_list = [[i, 0] for i in temp]
        struct = SegmentNetwork(pipes_number = len(pipes_list),
                                link_list = link_list,
                                objects_list = objects_list,
                                list_incoming_flow = incoming_flow_list,
                                list_outcoming_flow = outcoming_flow_list)

        return struct, objects_list, node_list

    def network_flux_experiment(loading_time, simulation_time, inf_lim_x, sup_lim_x, inf_lim_y, sup_lim_y,
                                        entry_points_coor, exit_points_coor):
        struct, objects_list, node_list = experiments.initialize_BOS_rectangular_network(inf_lim_x, sup_lim_x, inf_lim_y, sup_lim_y,
                                        entry_points_coor, exit_points_coor)
        
        #struct.plot_network()

        def external_source(object, incoming_flux):
            for j in object.direction:
                object.outside_incoming_flux(incoming_flux, j[0])

        def reservoir_to_pipes(object):
            if object.left_holding_volume > 0:
                object.exiting_reservoir("l")
            if object.right_holding_volume > 0:
                object.exiting_reservoir("r")
            if object.top_holding_volume > 0:
                object.exiting_reservoir("t")
            if object.bottom_holding_volume > 0:
                object.exiting_reservoir("b")

        def pipes_to_reservoir(origin_object, target_object, mode, add_flux):
            target_object.entering_reservoir_from_int_src(add_flux, origin_object, mode)

        def flux_dynamics(object):
            if object.nn is not None:
                pipe_flux = object.exiting_flux / object.nn
                if object.left_link is not None:
                    pipes_to_reservoir(origin_object = object,
                                    target_object = objects_list[object.left_link][1],
                                    mode = 'l',
                                    add_flux = pipe_flux)
                if object.right_link is not None:
                    pipes_to_reservoir(origin_object = object,
                                    target_object = objects_list[object.right_link][1],
                                    mode = 'r',
                                    add_flux = pipe_flux)
                if object.top_link is not None:
                    pipes_to_reservoir(origin_object = object,
                                    target_object = objects_list[object.top_link][1],
                                    mode = 't',
                                    add_flux = pipe_flux)
                if object.bottom_link is not None:
                    pipes_to_reservoir(origin_object = object,
                                        target_object = objects_list[object.bottom_link][1],
                                        mode = 'b',
                                        add_flux = pipe_flux)
            else:
                if object.left_link == -1:
                    object.exiting_system_from_pipe()
                if object.right_link == -1:
                    object.exiting_system_from_pipe()
                if object.top_link == -1:
                    object.exiting_system_from_pipe()
                if object.bottom_link == -1:
                    object.exiting_system_from_pipe()

        for i in range(loading_time):
            # loading from external sources 
            for j in objects_list:
                if j[1].type == "entry":
                    external_source(object = j[1], incoming_flux = 10)
            # loalding the pipes
            for j in objects_list:
                reservoir_to_pipes(j[1])
            # loading reservoirs from the pipes 
            for j in objects_list:
                flux_dynamics(j[1])
            struct.plot_network()
            
        for i in range(simulation_time - loading_time):
            for j in objects_list:
                reservoir_to_pipes(j[1])
            # loading reservoirs from the pipes 
            for j in objects_list:
                flux_dynamics(j[1])
            struct.plot_network()
        


