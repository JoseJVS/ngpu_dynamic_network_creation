
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as patches

rng = np.random.default_rng(12344)
barcolor = 'blue'
partcolor = 'red'

Nj = 4
Ni = 10
ymax = 20

x = np.arange(Ni)
xall = np.arange(Ni*Nj)
arr = rng.integers(low=1, high=ymax, size=(Nj, Ni))
part_size = np.array([3, 2, 3, 2])

fig1 = plt.figure(figsize=(12, 8)) #, ax1 = plt.subplots(5, 8)


ax = fig1.add_subplot(3,3,1) #ax1[0,0]
ax.text(-0.1, 1.05, 'A', transform=ax.transAxes, 
            size=15, weight='bold')
arr_all = arr.reshape(Ni*Nj)
ax.bar(xall, height = arr_all, color = barcolor)
ax.set_xticklabels([])
ax.set_yticklabels([])
ax.set_xticks([])
ax.set_yticks([])
ax.set_xlim([-1, Ni*Nj])
ax.set_ylim([-0.5, ymax])
for j in range(Nj+1):
    x1, y1 = [Ni*j-0.5, Ni*j-0.5], [-0.5, ymax]
    ax.plot(x1, y1, color = 'black')

ax = fig1.add_subplot(3,3,2) #ax1[0,1]
ax.text(-0.1, 1.05, 'B', transform=ax.transAxes, 
            size=15, weight='bold')
for j in range(Nj):
    arr[j] = np.sort(arr[j])
arr_all = arr.reshape(Ni*Nj)
ax.bar(xall, height = arr_all, color = barcolor)
ax.set_xticklabels([])
ax.set_yticklabels([])
ax.set_xticks([])
ax.set_yticks([])
ax.set_xlim([-1, Ni*Nj])
ax.set_ylim([-0.5, ymax])
for j in range(Nj+1):
    x1, y1 = [Ni*j-0.5, Ni*j-0.5], [-0.5, ymax]
    ax.plot(x1, y1, color = 'black')
    

ax = fig1.add_subplot(3,3,3) #ax1[0,2]
ax.text(-0.1, 1.05, 'C', transform=ax.transAxes, 
            size=15, weight='bold')
color_all=np.array([])
for j in range(Nj):
    p = part_size[j]
    color_left = np.full(p, partcolor)
    color_right = np.full(Ni-p, barcolor)
    color_all = np.concatenate((color_all, color_left, color_right))

arr_all = arr.reshape(Ni*Nj)
ax.bar(xall, height = arr_all, color = color_all)
ax.set_xticklabels([])
ax.set_yticklabels([])
ax.set_xticks([])
ax.set_yticks([])
ax.set_xlim([-1, Ni*Nj])
ax.set_ylim([-0.5, ymax])
for j in range(Nj+1):
    x1, y1 = [Ni*j-0.5, Ni*j-0.5], [-0.5, ymax]
    ax.plot(x1, y1, color = 'black')
    
for j in range(Nj):
    p = part_size[j]
    x1, y1 = [Ni*j+p-0.5, Ni*j+p-0.5], [0, ymax]
    ax.plot(x1, y1, linestyle = 'dashed', color = 'green')

    ax.plot([-0.5, Ni*Nj], [4, 4], linestyle = 'dotted', color = 'black')
    ax.text(-3.0, 3.5, 't', size=14) 
             #transform=ax.transAxes, size=15) #, weight='bold')

    
ax = fig1.add_subplot(3,3,4) #ax1[1,0]
ax.text(-0.1, 1.05, 'D', transform=ax.transAxes, 
            size=15, weight='bold')
color_all=np.array([])
for j in range(Nj):
    p = part_size[j]
    color_left = np.full(p, partcolor)
    color_right = np.full(Ni-p, barcolor)
    color_all = np.concatenate((color_all, color_left, color_right))

arr_all = arr.reshape(Ni*Nj)
for i in range(len(arr_all)):
    if color_all[i]=='blue':
        c = 'blue'
        lw = 0.0
        f = True
    else:
        c = (1.0, 0.7, 0.7)
        lw = 1.0
        f = False
    ax.bar(xall[i], height = arr_all[i], fill = f, color = c, linewidth = lw)
    
ax.set_xticklabels([])
ax.set_yticklabels([])
ax.set_xticks([])
ax.set_yticks([])
ax.set_xlim([-1, Ni*Nj])
ax.set_ylim([-0.5, ymax])
for j in range(Nj+1):
    x1, y1 = [Ni*j-0.5, Ni*j-0.5], [-0.5, ymax]
    ax.plot(x1, y1, color = 'black')
    
for j in range(Nj):
    p = part_size[j]
    x1, y1 = [Ni*j+p-0.5, Ni*j+p-0.5], [0, ymax]
    ax.plot(x1, y1, linestyle = 'dashed', color = 'green')

    
ax = fig1.add_subplot(3,3,5) #ax1[1,1]
ax.text(-0.1, 1.05, 'E', transform=ax.transAxes, 
            size=15, weight='bold')

arr_left = np.array([])
arr_right = np.array([])
xb = Ni
xblock = np.array([xb])
for j in range(Nj):
    p = part_size[j]
    part_left = arr[j][:p]
    part_right = arr[j][p:]
    arr_left = np.concatenate((arr_left, part_left))
    arr_right = np.concatenate((arr_right, part_right))
    xb = xb + Ni - p
    xblock = np.append(xblock, xb)
arr_all = np.concatenate((arr_left, arr_right))
color_left = np.full(Ni, partcolor)
color_right = np.full((Nj-1)*Ni, barcolor)
#color_left_white = np.full(Ni, 'white')
color_all = np.concatenate((color_left, color_right))
#color_all_white = np.concatenate((color_left_white, color_right))
xblock = np.append(xblock, Ni*Nj)

ax.bar(xall, height = arr_all, color = color_all) #_white)
ax.set_xticklabels([])
ax.set_yticklabels([])
ax.set_xticks([])
ax.set_yticks([])
ax.set_xlim([-1, Ni*Nj])
ax.set_ylim([-0.5, ymax])
for j in range(Nj+1):
    x1, y1 = [Ni*j-0.5, Ni*j-0.5], [-0.5, ymax]
    ax.plot(x1, y1, color = 'black')
    
for j in range(Nj+1):
    xb = xblock[j]
    x1, y1 = [xb-0.55, xb-0.55], [0, ymax]
    ax.plot(x1, y1, linestyle = 'dashed', color = 'green')

#fig1.tight_layout()

ax = fig1.add_subplot(6, 11, 48)

x_left = np.arange(Ni)
ax.bar(x_left, height = arr_left, color = partcolor)
ax.set_xticklabels([])
ax.set_yticklabels([])
ax.set_xticks([])
ax.set_yticks([])
ax.set_xlim([-1, Ni])
ax.set_ylim([-0.5, ymax/2])

    
ax = fig1.add_subplot(3,3,6) #ax1[1,2]
ax.text(-0.1, 1.05, 'F', transform=ax.transAxes, 
            size=15, weight='bold')

arr_left = np.sort(arr_all[:Ni])
arr_all[:Ni] = arr_left
#arr_all = np.concatenate((arr_left, arr_right))

ax.bar(xall, height = arr_all, color = color_all)
ax.set_xticklabels([])
ax.set_yticklabels([])
ax.set_xticks([])
ax.set_yticks([])
ax.set_xlim([-1, Ni*Nj])
ax.set_ylim([-0.5, ymax])
for j in range(Nj+1):
    x1, y1 = [Ni*j-0.5, Ni*j-0.5], [-0.5, ymax]
    ax.plot(x1, y1, color = 'black')
    
for j in range(Nj+1):
    xb = xblock[j]
    x1, y1 = [xb-0.55, xb-0.55], [0, ymax]
    ax.plot(x1, y1, linestyle = 'dashed', color = 'green')

    
# new clear axis overlay with 0-1 limits
ax2 = plt.axes([0,0,1,1], facecolor=(1,1,1,0))

style = "Simple, tail_width=0.5, head_width=4, head_length=8"

kw = dict(arrowstyle=style, color="k")

a1 = patches.FancyArrowPatch((0.24, 0.38), (0.34, 0.3),
                             connectionstyle="arc3,rad=.3", mutation_scale=20)
a2 = patches.FancyArrowPatch((0.4, 0.3), (0.43, 0.38),
                             connectionstyle="arc3,rad=.4", mutation_scale=20)
plt.gca().add_patch(a1)
plt.gca().add_patch(a2)

plt.delaxes(fig1.add_subplot(3,3,7))
plt.delaxes(fig1.add_subplot(3,3,8))
plt.delaxes(fig1.add_subplot(3,3,9))


plt.savefig("copass.pdf", dpi=600)

plt.show()
