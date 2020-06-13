import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from poller import SensorPoller

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = []
ys_accel = []
ys_gyro = []
ys_rot = []


poller = SensorPoller(ip_port='192.168.20.141:8888')

max_points = 2000

def animate(i, xs, ys_accel, ys_gyro, ys_rot):
    data = poller.get_next()
    
    xs.extend(data['timestamp'])    
    ys_accel.extend(data['accel'])    
    ys_gyro.extend(data['gyro'])    
    ys_rot.extend(data['rotation'])    


    # Limit x and y lists to 20 items
    if len(xs)>max_points:
        xs = xs[-max_points:]
        ys_accel = ys_accel[-max_points:]
        ys_gyro = ys_gyro[-max_points:]
        ys_rot = ys_rot[-max_points:]


    # Draw x and y lists
    ax.clear()
    ax.plot(xs, [row[0] for row in ys_accel])
    ax.plot(xs, [row[1] for row in ys_accel])
    ax.plot(xs, [row[2] for row in ys_accel])
    ax.plot(xs, [row[0] for row in ys_gyro])
    ax.plot(xs, [row[1] for row in ys_gyro])
    ax.plot(xs, [row[2] for row in ys_gyro])
    ax.plot(xs, [row[0] for row in ys_rot])
    ax.plot(xs, [row[1] for row in ys_rot])
    ax.plot(xs, [row[2] for row in ys_rot])



# Set up plot to call animate() function periodically
ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys_accel, ys_gyro, ys_rot), interval=220)
plt.show()
