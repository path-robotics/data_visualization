import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from mpl_toolkits import mplot3d

class Data:
    def __init__(self):

        self.x = None
        self.y = None

    def load(self, filename, dtype, deliminator, header=0):
        dir = Path("/var/local/forge/log-data/")
        file = dir / filename

        all_data = []
        with open(file, 'r', newline='\n') as fid:
            for line in fid.readlines():
                data = []
                fields = line.split(deliminator)
                for f in fields[:-1]:
                    data.append(dtype(f))
                all_data.append(np.array(data))

        self.x = np.arange(len(all_data))
        self.y = all_data

def load_data(filename, dtype, deliminator,header=0):
    data = Data()
    data.load(filename, dtype, deliminator, header=header)
    return data


class myPlot:
    def __init__(self, data=None):
        self.data = data
        plt.rcParams.update({'font.size': 22})

    def plot_camera_angle(self):

        y = self.data.y
        scatter_idx = []
        scatter_data = []
        for i in range(len(y)):
            for j in range(len(y[i])):
                scatter_idx.append(i)
                scatter_data.append(y[i][j])

        plt.scatter(scatter_idx, scatter_data)
        plt.xlabel("# point")
        plt.ylabel("camera angle id")

    def plot(self, type="jacobian"):
        fig = plt.figure()

        y = self.data.y
        plt.plot(y)
        plt.xlabel("# point")
        if type == "jacobian":
            plt.ylabel("det(JTJ)")
        elif type == "vertical":
            plt.ylabel("theta (3F)")
        elif type == "zeta_prime (1F)":
            plt.ylabel("zeta_prime")
        elif type == "positioner_traj":
            plt.ylabel("positioner_traj")
        elif type == "WA":
            plt.ylabel("work angle")
        elif type == "TA":
            plt.ylabel("travel angle")

    def plot_pos_traj_with_constraints(self, num_positioner_joints):
        fig, ax = plt.subplots()

        y = self.data.y
        data_size = len(y[0])
        for i in range(data_size):
            scatter_idx = []
            scatter_data = []
            for j in range(len(y)):
                scatter_idx.append(j)
                scatter_data.append(y[j][i])
            if i < num_positioner_joints:
                ax.plot(scatter_idx, scatter_data, '-*', label ='positioner joint %d' % i)
            elif i == num_positioner_joints:
                ax.plot(scatter_idx, scatter_data, '-o', label = 'slope (3F)')
            elif i == num_positioner_joints + 1:
                ax.plot(scatter_idx, scatter_data, '-d', label = 'roll (1F)')

        plt.legend()
        plt.xlabel("# pt")

    def plot_raw_trajectory(self, type="position"):
        fig = plt.figure()

        y = self.data.y
        for i in range(7):
            scatter_idx = []
            scatter_data = []
            for j in range(len(y)):
                scatter_idx.append(j)
                scatter_data.append(y[j][i])
            plt.plot(scatter_idx, scatter_data, '-*')
        plt.legend([str(i) for i in range(7)])

        plt.xlabel("# point")
        if type == "position":
            plt.ylabel("joint position")
        elif type == "velocity":
            plt.ylabel("joint velocity")

    def plot_tool_point(self):
        y = self.data.y

        fig = plt.figure()
        ax = plt.axes(projection="3d")

        x_pt, y_pt, z_pt = [], [], []
        for i in range(len(y)):
            x_pt.append(y[i][0])
            y_pt.append(y[i][1])
            z_pt.append(y[i][2])

        ax.scatter3D(x_pt, y_pt, z_pt, c=z_pt)
        plt.show()


def main():
    # constraint plot
    # constraint = load_data("constraint_angles.txt", dtype=float, deliminator=",")
    # constraint_plot = myPlot(constraint)
    # constraint_plot.plot_pos_traj_with_constraints(1)


    # camera angle id:
    valid_id_seq = load_data("valid_id_seq.txt", dtype=int, deliminator=",")
    optimal_id_seq = load_data("optimal_id_seq.txt", dtype=int, deliminator=",")
    #singularity_id_seq = load_data("singularity_id_seq.txt", dtype=int, deliminator=",")


    # travel vec w.r.t gravity, normal w.r.t gravity
    angle_to_travel = load_data("angle_to_travel.txt", dtype=float, deliminator=",")
    angle_to_normal = load_data("angle_to_normal.txt", dtype=float, deliminator=",")

    # scaled velocity
    scaled_velocity = load_data("scaled_velocity.txt", dtype=float, deliminator=",")

    # work and travel angle

    work_angle = load_data("work_angle_offset.txt", dtype=float, deliminator=",")
    travel_angle = load_data("travel_angle_offset.txt", dtype=float, deliminator=",")

    # command velocity and position
    raw_position = load_data("raw_position.txt", dtype=float, deliminator=",")
    raw_velocity = load_data("raw_velocity.txt", dtype=float, deliminator=",")

    # tool position (raw and interpolate)
    # tool_point_raw = load_data("tool_point_raw.txt", dtype=float, deliminator=",")
    # tool_point_interpolate = load_data("tool_point_interpolate.txt", dtype=float, deliminator=",")

    # interpolated position and velocity
    interpolate_position = load_data("interpolate_position.txt", dtype=float, deliminator=",")
    interpolate_velocity = load_data("interpolate_velocity.txt", dtype=float, deliminator=",")

    valid_id = myPlot(valid_id_seq)
    optimal_id = myPlot(optimal_id_seq)
    #singularity_id = myPlot(singularity_id_seq)
    valid_id.plot_camera_angle()
    optimal_id.plot_camera_angle()
    #singularity_id.plot_camera_angle()

    # work and travel angle
    work_angle_plot = myPlot(work_angle)
    travel_angle_plot = myPlot(travel_angle)
    work_angle_plot.plot("WA")
    travel_angle_plot.plot("TA")

    # travel angle w.r.t gravity
    angle_to_travel_plot = myPlot(angle_to_travel)
    angle_to_travel_plot.plot("angle")

    angle_to_normal_plot = myPlot(angle_to_normal)
    angle_to_normal_plot.plot("angle")

    # scaled vel
    scaled_velocity_plot = myPlot(scaled_velocity)
    scaled_velocity_plot.plot("vel")


    # joint position velocity
    raw_p = myPlot(raw_position)
    raw_v = myPlot(raw_velocity)
    raw_p.plot_raw_trajectory(type="position")
    raw_v.plot_raw_trajectory(type="velocity")

    # interpolated position and velocity
    inte_pos = myPlot(interpolate_position)
    inte_pos.plot_raw_trajectory(type="position")

    inte_vel = myPlot(interpolate_velocity)
    inte_vel.plot_raw_trajectory(type="velocity")


    plt.show()


if __name__ == "__main__":
    main()