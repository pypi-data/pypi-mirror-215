"""
This file is part of Apricopt.

Apricopt is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Apricopt is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Apricopt.  If not, see <http://www.gnu.org/licenses/>.

Copyright (C) 2020-2022 Sapienza University of Rome, Marco Esposito, Leonardo Picchiami.
"""

from apricopt.model.Model import Model
from apricopt.model.ModelInstance import ModelInstance
from apricopt.simulation.executable.ExecutableEngine import ExecutableEngine
from apricopt.simulation.executable.ExecutableModelInstance import ExecutableModelInstance

from typing import Dict, List

import os


class ModelicaExecutableEngine(ExecutableEngine):
    def __init__(self):
        super().__init__()
        self.start_values = dict()
        self.read_sim_out_from_stdout = True

    def load_model(self, model_filename: str, **exec_info) -> ModelInstance:
        info = list(exec_info.keys())
        self._executable_info_check(info)

        self.executable_name = model_filename
        self.cwd = exec_info['cwd']

        model_obj: str = model_filename
        return ExecutableModelInstance(self, model_obj)

    def _executable_info_check(self, exec_info: List[str]) -> None:
        if 'cwd' not in exec_info:
            raise ValueError("The ExecutableEngine needs the current working directory (CWD) to run the executable")

    def simulate_trajectory_and_set(self, model: Model, horizon: float, exclude=None) -> Dict[str, List[float]]:
        raise NotImplementedError

    def simulate_trajectory_and_get_state(self, model: Model, horizon: float, exclude=None) -> Dict[str, float]:
        raise NotImplementedError

    def restore_state(self, model: Model, changed_values: Dict[str, float]) -> None:
        raise NotImplementedError

    def read_simulation_output(self, stdout_string: str = None) -> Dict[str, List[float]]:
        results: Dict[str, List[float]] = dict()

        string = stdout_string.decode()
        string = string.strip()
        if self.read_sim_out_from_stdout:
            outputs = string.split(',')
            for out in outputs:
                parsed = out.split('=')
                results[parsed[0]] = [float(parsed[1])]
        else:
            raise ValueError('Only reading from std out is currently supported')

        self.start_values = dict()
        return results

    def write_simulation_input(self, params_values: Dict[str, float]) -> None:
        self.start_values = dict(self.start_values, **params_values)

    def get_simulation_cmd(self, horizon: float, observed_outputs=None) -> str:
        override_string = ""
        if len(self.start_values) > 0:
            override_string = "-override "
            for name, value in self.start_values.items():
                override_string += f'{name}={value},'

        output_string = ""
        if observed_outputs:
            output_string = '-output='
            for out in observed_outputs:
                output_string += f'{out},'

        return f'./{self.executable_name} -noemit {override_string[:-1]} {output_string[:-1]} -lv=-stdout,-LOG_SUCCESS,-assert'
