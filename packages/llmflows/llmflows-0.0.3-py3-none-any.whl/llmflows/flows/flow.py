# pylint: disable=R0801

"""
This module provides classes for defining and executing flows, which are digraphs of
steps. Each step is represented by a `FlowStep` instance.
The `BaseFlow` class provides methods for setting the initial step of the flow, 
getting all steps in the flow, and checking that all flow steps have unique output keys
and names.
The `Flow` class extends `BaseFlow` and provides additional methods for executing the 
flow and handling input and output data.
"""

from llmflows.flows.flowstep import FlowStep


class BaseFlow:
    """
    Base class for all flows. Each flow is a sequence of steps, represented by FlowStep
    instances.

    Attributes:
        first_step (FlowStep): The initial step of the flow.
        steps (list): All steps in the flow.
        output_keys (set): Set of output keys for all steps in the flow.
        input_keys (set): Set of input keys for all steps in the flow.
        names (set): Set of names of all steps in the flow.
    """

    def __init__(self, first_step: FlowStep):
        """
        Initializes the BaseFlow with a first flowstep.

        Args:
            first_step (FlowStep): Initial step of the flow.
        """
        self.first_step = first_step
        self.steps = self._get_all_steps()
        self.output_keys = set()
        self.input_keys = set()
        self.names = set()
        self._check_unique_attributes()

    def set_first_step(self, step):
        """
        Sets the initial step of the flow.

        Args:
            step (FlowStep): The initial step for the flow.
        """
        self.first_step = step

    def _get_all_steps(self):
        """
        Traverses the flow to get all steps.

        Returns:
            list: A list containing all steps in the flow.
        """
        queue = [self.first_step]
        visited_steps = set()
        all_steps = []

        while queue:
            current_step = queue.pop(0)

            if current_step in visited_steps or current_step is None:
                continue

            visited_steps.add(current_step)
            all_steps.append(current_step)
            queue.extend(current_step.next_steps)

        return all_steps

    def _check_unique_attributes(self):
        """
        Checks that all flow steps have unique output keys and names.

        Raises:
            ValueError: If any flow steps have the same output key or name.
        """
        for step in self.steps:
            if step.output_key in self.output_keys:
                raise ValueError(
                    f"The output key '{step.output_key}' has already been used"
                    " in another FlowStep."
                )

            if step.name in self.names:
                raise ValueError(
                    f"The name '{step.name}' has already been used"
                    " for another FlowStep."
                )

            self.output_keys.add(step.output_key)
            self.names.add(step.name)

            flowstep_class = step.__class__.__name__
            if flowstep_class == "FlowStep":
                self.input_keys.update(step.prompt_template.variables)
            elif flowstep_class == "ChatFlowStep":
                self.input_keys.update(
                    step.system_prompt_template.variables,
                    step.message_prompt_template.variables,
                    {step.message_key},
                )

    def _check_all_input_keys_available(self, user_inputs):
        """
        Checks that all required input keys are available.

        Args:
            user_inputs (dict): The set of input keys provided by the user.

        Raises:
            ValueError: If not all required input keys are covered.
        """

        print(self.output_keys.union(user_inputs.keys()))
        if not self.input_keys.issubset(self.output_keys.union(user_inputs.keys())):
            raise ValueError("Some flowsteps have missing inputs")

    def execute(self, **inputs):
        """
        Placeholder method for executing the flow.

        Args:
            inputs (dict): Inputs to the flow.

        Raises:
            NotImplementedError: If not implemented in a subclass of BaseFlow.
        """
        raise NotImplementedError


class Flow(BaseFlow):
    """
    Base class for all flows. Each flow is a digraph of steps, represented by FlowStep
    instances.

    Attributes:
        first_step (FlowStep): The first step in the flow.
        results (dict): Stores the results of the executed flow steps.
        executed_steps (set): Keeps track of the steps that have been executed.
    """

    def __init__(self, first_step: FlowStep):
        super().__init__(first_step)
        self.results = {}
        self.executed_steps = set()

    def execute(self, verbose=False, **inputs):
        """
        Executes the flow with the provided inputs.

        Args:
            verbose (bool): Specifies if the flow step should print their output.
            **inputs (dict): The inputs to the flow.

        Returns:
            dict: A dictionary of the results from each flow step.

        Raises:
            ValueError: If any required inputs are missing.
        """
        self._check_all_input_keys_available(inputs)
        self._execute_step(self.first_step, inputs, verbose)
        return self.results

    def _execute_step(self, step, inputs, verbose):
        """
        Executes the given step and its next steps in a DFS-like manner.

        Args:
            step (FlowStep): The step to execute.
            inputs (dict): The inputs to the step.
            verbose (bool): Specifies if the flow step should print its output.

        Returns:
            Any: The output of the step.
        """
        if not step or any(parent.output_key not in inputs for parent in step.parents):
            return

        required_inputs = {
            key: inputs[key] for key in step.required_keys
        }

        if step not in self.executed_steps:
            flow_data = step.execute(required_inputs, verbose)
            self.executed_steps.add(step)

            if flow_data:
                self.results[step.name] = flow_data
                inputs.update(flow_data["result"])

        for next_step in step.next_steps:
            self._execute_step(next_step, inputs, verbose)
