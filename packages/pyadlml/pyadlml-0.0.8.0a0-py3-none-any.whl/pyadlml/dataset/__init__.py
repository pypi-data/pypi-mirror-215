from pyadlml.dataset._datasets.amsterdam import fetch_amsterdam
from pyadlml.dataset._datasets.aras import fetch_aras
from pyadlml.dataset._datasets.mitlab import fetch_mitlab
from pyadlml.dataset._datasets.tuebingen_2019 import fetch_tuebingen_2019
from pyadlml.dataset._datasets.uci_adl_binary import fetch_uci_adl_binary
from pyadlml.dataset._datasets.kasteren_2010 import fetch_kasteren_2010
from pyadlml.dataset._datasets.casas_houses import fetch_casas

from pyadlml.dataset._datasets.homeassistant import (
    load_homeassistant, load_homeassistant_devices
)

from pyadlml.dataset._datasets.activity_assistant import load as load_act_assist
from pyadlml.dataset import io

# TODO refactor, importing stuff from pyadlml.dataset must not require 
#                torch as a dependency to be installed. 
#from pyadlml.dataset.misc import TorchDataset
