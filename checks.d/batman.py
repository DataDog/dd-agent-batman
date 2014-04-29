from checks import AgentCheck
import time, math

class Batman(AgentCheck):
    def __init__(self, name, init_config, agentConfig):
        AgentCheck.__init__(self, name, init_config, agentConfig)

    def x(self, period, t=None):
        scale_factor = period / 14.
        if t is None:
            t = time.time()

        # Get a number between 0 and self.period
        val = float(t - (int(t) / period * period))
        # Scale that number to be between 0 and 14
        val /= scale_factor
        # Shift that number to be between -7 and 7
        val -= 7
        return val


    def g(self, x):
        return .5 * (
            abs(x / 2)
            + math.sqrt(1 - (abs(abs(x) - 2) - 1)**2)
            - ((1./112.) * (3 * math.sqrt(33) - 7) * x**2)
            + (3 * math.sqrt(1 - (1./7. * x)**2))
            - 3
        )  * (
            ((x + 4) / abs(x + 4)) - ((x - 4) / abs(x - 4))
        ) - 3 * math.sqrt(1 - (1./7. * x)**2 )

    def check(self, instance):
        period = int(instance.get('period', 600))
        tags = ['period:%s' % period]
        x = self.x(period)
        if abs(x) > 3:
            y = math.sqrt(3. - 3. * x**2 / 49.)
            if y > -3. * math.sqrt(33) / 7.:
                self.gauge('dd.batman.top', y, tags=tags)
                self.gauge('dd.batman.bottom', -y, tags=tags)
            else:
                self.gauge('dd.batman.bottom', self.g(x), tags=tags)
        else:
            self.gauge('dd.batman.bottom', self.g(x), tags=tags)
            if 1 < abs(x) <= 3:
                y = (6.*math.sqrt(10.)/7.) + (1.5 - 0.5 * abs(x)) - ((6.*math.sqrt(10)/14.) * math.sqrt(4 - math.sqrt(abs(x) - 1)))
                self.gauge('dd.batman.top', y, tags=tags)
            elif 0.75 < abs(x) <= 1:
                self.gauge('dd.batman.top', 9 - 8*abs(x), tags=tags)
            elif 0.5 < abs(x) <= 0.75:
                self.gauge('dd.batman.top', 3 * abs(x) + 0.75, tags=tags)
            elif abs(x) <= 0.5:
                self.gauge('dd.batman.top', 2.25, tags=tags)

        self.gauge('dd.batman.top', y, tags=tags)

if __name__ == '__main__':
    check = Batman('batman', {}, {})
    print check.g(check.x(period=600))

