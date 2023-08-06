__all__ = ['qcodes', 'simulator', 'swabian_instruments', 'zurich_instruments', 'Keysight344xxA',
           'NationalInstrumentsUSB6003', 'SwabianInstrumentsTimeTagger', 'DAQSettings',
           'QoptColoredNoise', 'ZurichInstrumentsMFLIScope', 'ZurichInstrumentsMFLIDAQ']

from . import qcodes, simulator, swabian_instruments, zurich_instruments
from .qcodes import (Keysight344xxA, NationalInstrumentsUSB6003,
                     # Backwards "compatibility"
                     keysight_344xxA, national_instruments_daq)
from .settings import (BoundedSet, ContinuousInterval, DAQSettings,
                       DiscreteInterval)
from .simulator import (QoptColoredNoise,
                        # Backwards "compatibility"
                        qopt_colored_noise)
from .swabian_instruments import (SwabianInstrumentsTimeTagger,
                                  # Backwards "compatibility"
                                  timetagger)
from .zurich_instruments import (ZurichInstrumentsMFLIDAQ, ZurichInstrumentsMFLIScope,
                                 # Backwards "compatibility"
                                 MFLI_daq, MFLI_scope)
