import math

from matplotlib import ticker
from matplotlib.ticker import is_close_to_int, nearest_long
from matplotlib import rcParams

class LogFormatter(ticker.LogFormatterMathtext):
    def __call__(self, x, pos=None):
        'Return the format for tick val *x* at position *pos*'
        b = self._base
        usetex = rcParams['text.usetex']

        # only label the decades
        if x == 0:
            if usetex:
                return '$0$'
            else:
                return '$\mathdefault{0}$'

        fx = math.log(abs(x)) / math.log(b)
        is_decade = is_close_to_int(fx)

        fx = math.floor(fx)
        mantissa = abs(x)/math.pow(b, fx)

        sign_string = '-' if x < 0 else ''

        # use string formatting of the base if it is not an integer
        if b % 1 == 0.0:
            base = '%d' % b
        else:
            base = '%s' % b

        if not is_decade and self.labelOnlyBase:
            return ''
        else:#elif not is_decade:
            # Always show the mantissa
            if is_close_to_int(mantissa):
                mantissa = int(mantissa)

            if usetex:
                return (r'$%s%s\cdot%s^{%d}$') % \
                                            (sign_string, mantissa, base, fx)
            else:
                return ('$\mathregular{%s%s\cdot%s^{%d}}$') % \
                                            (sign_string, mantissa, base, fx)
#         else:
#             if usetex:
#                 return (r'$%s%s^{%d}$') % (sign_string,
#                                            base,
#                                            nearest_long(fx))
#             else:
#                 return (r'$\mathregular{%s%s^{%d}}$') % (sign_string,
#                                                          base,
#                                                          nearest_long(fx))
