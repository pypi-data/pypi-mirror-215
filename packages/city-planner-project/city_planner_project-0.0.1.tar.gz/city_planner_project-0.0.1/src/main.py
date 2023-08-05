import tools

if __name__  == "__main__":
    #tools.experiments.network_flux_experiment(loading_time = 5, simulation_time = 50, inf_lim_x = 0,
    #                    sup_lim_x = 2, inf_lim_y = 0, sup_lim_y = 2,
    #                    entry_points_coor = [[0, 0]], exit_points_coor = [[5, 5]])
    tools.experiments.teste_UOS(limit_holding_volume_list = [50, 60, 40],
                                holding_volume_list = [50, 0, 0],
                                exiting_flux_list = [0, 0, 0],
                                position_list = [[0, 0], [1, 0], [2, 0]],
                                capacity_list = [5, 7, 4],
                                penalty_list = [0, 0, 0],
                                id_list = [0, 1, 2],
                                input_list = [[0, 0]],
                                output_list = [2],
                                neighbors_list = [[1], [2], None])