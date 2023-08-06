# Copyright 2022 Chi-kwan Chan
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""Plasma Formulas"""


from astropy import constants as c, units as u
from phun import phun


Te = u.def_unit('Te', c.m_e * c.c**2 / c.k_B)


@phun
def gyrofrequency(u_B, u_res=u.Hz, backend=None):
    """Electron Cyclotron Frequency"""

    s = float(c.si.e * u_B / (2 * backend.pi * c.m_e) / u_res)
    return lambda B: s * B
