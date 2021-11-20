# -*- coding: utf-8 -*-
# @Time: 2021/11/11 9:21
# @Author: H
from mpl_toolkits.axisartist.axislines import AxesZero
from matplotlib import animation
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import numpy as np
from functions import energy, d_energy, dd_energy, get_t0, m


# 初始化图片
class Mani(object):
    def __init__(self, fig: plt.figure, psi):
        rido = -5
        # 计算当前t0
        self.t0, e, de, dee = get_t0(rido, psi, x0=3)
        self.x, self.y = [], []
        gs = gridspec.GridSpec(3, 2)

        ax1 = fig.add_subplot(gs[0, 0])
        ax1.set_xlabel('$\Theta$')
        ax1.set_ylabel('E/$k_u$')
        ax1.tick_params(direction='in')
        ax1.set_ylim(-7, 7)

        ax2 = fig.add_subplot(gs[1, 0], sharex=ax1)
        ax2.set_xlabel('$\Theta$')
        ax2.set_ylabel('$dE/d\Theta$')
        ax2.tick_params(direction='in')

        ax3 = fig.add_subplot(gs[2, 0], sharex=ax1)
        ax3.set_xlabel('$\Theta$')
        ax3.set_ylabel('$d^2E/d\Theta^2$')
        ax3.tick_params(direction='in')

        ax4 = fig.add_subplot(gs[:, 1])
        ax4.set_xlabel('H $[k_u/(m_s\mu_0)]$')
        ax4.set_ylabel('$m/m_s$')
        ax4.tick_params(direction='in', labelright=True, right=True, left=False, labelleft=False)

        ax1.plot(t, energy(t, rido, psi=psi), c=plt.cm.rainbow(7/7), label=f'H={rido:.2f}')  # label=f'H={rido}$k_u/(m_s\mu_0)$'
        ax1.plot([self.t0], [e], 'o', c='k', markersize=3)
        ax1.axhline(color='grey', linestyle='-', lw=0.5)

        ax2.plot(t, d_energy(t, rido, psi=psi), c=plt.cm.rainbow(6/7))
        ax2.plot([self.t0], [de], 'o', c='k', markersize=3)
        ax2.set_ylim(-7, 7)
        ax2.axhline(color='grey', linestyle='-', lw=0.5)

        ax3.plot(t, dd_energy(t, rido, psi=psi), c=plt.cm.rainbow(5/7))
        ax3.plot([self.t0], [dee], 'o', c='k', markersize=3)
        ax3.set_ylim(-7, 7)
        ax3.axhline(color='grey', linestyle='-', lw=0.5)
        ax1.legend(bbox_to_anchor=(0.3, 1.3))

        ax4.set_xlim(-6, 6)
        ax4.set_ylim(-1.1, 1.1)
        ax4.plot(self.x, self.y, c='k', ls='--')
        ax4.set_title(f'$\psi={psi/np.pi*180: .0f}$°')

    def animate(self, rido, fig, psi, t_bounds=[-2*np.pi, 2*np.pi]):
        self.t0, e, de, dde = get_t0(rido, psi, x0=self.t0, t_bounds=t_bounds)
        if self.t0 < t_bounds[0]+0.001:
            self.t0 = t_bounds[1]

        fig.axes[0].lines[0].set_data(t, energy(t, rido, psi=psi))
        fig.axes[0].lines[1].set_data([self.t0], [e])
        fig.axes[0].lines[0].set_label(f'H={rido:.2f}')
        fig.axes[0].legend(bbox_to_anchor=(0.3, 1.3))

        fig.axes[1].lines[0].set_data(t, d_energy(t, rido, psi=psi))
        fig.axes[1].lines[1].set_data([self.t0], [de])
        fig.axes[2].lines[0].set_data(t, dd_energy(t, rido, psi=psi))
        fig.axes[2].lines[1].set_data([self.t0], [dde])

        self.x.append(rido)
        self.y.append(m(psi, self.t0))

        fig.axes[3].lines[0].set_data(self.x, self.y)

        return fig.axes


t = np.linspace(-2*np.pi, 2 * np.pi, 361)
fig = plt.figure(figsize=(5, 6))
psi = 90*np.pi/180
A = Mani(fig, psi)
x = np.linspace(-5, 5, 50)
B = np.hstack((x, x[::-1]))
ani = animation.FuncAnimation(fig, A.animate, iter(B),
                               fargs=[fig, psi, [-2*np.pi, 2*np.pi]], interval=100)
ani.save(f'{psi/np.pi*180: .0f}°.gif')

