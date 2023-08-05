# environment.py

from typing import (
    Self, Iterable, Optional,
    Type, List, Dict, Union
)
import random
from itertools import combinations
from abc import abstractmethod

from represent import BaseModel

from multithreading import Caller, multi_threaded_call

from genetic_algo.attributes import Attribute
from genetic_algo.solution import Solution, Template, eliminate_repetitions

__all__ = [
    "Generation",
    "EnvironmentDefinition",
    "Fitness",
    "History",
    "Environment",
    "scale"
]

class Generation(BaseModel):
    """A class to represent a generation of solutions."""

    def __init__(self, solutions: Iterable[Solution]) -> None:
        """
        Defines the class attributes.

        :param solutions: The solutions of the generation.
        """

        self.solutions = list(solutions)
    # end __init__

    @property
    def fitness(self) -> Dict[Solution, float]:
        """
        Returns the fitness of all the solutions in the generations.

        :return: The total fitness.
        """

        return {solution: solution.fitness for solution in self.solutions}
    # end fitness

    @classmethod
    def build(cls, solutions: Iterable[Solution]) -> Self:
        """
        Defines the class attributes.

        :param solutions: The solutions of the generation.

        :return: The generation object.
        """

        return Generation(solutions=solutions)
    # end build
# end Generation

def scale(
        value: Union[int, float],
        size: Optional[int] = None,
        name: Optional[str] = None
) -> int:
    """
    Scales the value to the given size.

    :param value: The value to scale.
    :param size: The scaling size.
    :param name: The name for the value.

    :return: The valid scaled value.
    """

    if isinstance(value, int) and (0 <= value <= size):
        return value

    elif isinstance(value, int):
        raise ValueError(
            f"{f'value {name}' or 'value'} of type {int} "
            f"must be in the range between {0} and the given "
            f"size: {size}, but {value} was given."
        )
    # end if

    if isinstance(value, float) and (0 <= value <= 1):
        if size is None:
            size = 1
        # end if

        return int(value * size)

    elif isinstance(value, float):
        raise ValueError(
            f"relative {f'value {name}' or 'value'} of type {int} "
            f"must be in the range between {0} and {1}, "
            f"but {value} was given."
        )
    # end if
# end scale

class EnvironmentDefinition(BaseModel):
    """A class to define the attributes of an environment."""

    def __init__(
            self,
            size: int,
            ascending: bool,
            successors: Optional[Union[int, float]] = None,
            continuers: Optional[Union[int, float]] = None,
            eliminations: Optional[Union[int, float]] = None,
            parents: Optional[Union[int, float]] = None,
            mutations: Optional[float] = None,
            repetitions: Optional[bool] = False,
            padding: Optional[bool] = True
    ) -> None:
        """
        Defines the class attributes.

        :param size: The size of a generation.
        :param ascending: The value for ascending order.
        :param parents: The amounts of parents in each mating.
        :param successors: The amount of the best successors to generate from mating.
        :param continuers: The amount of parents to continue to the next generation.
        :param eliminations: The amount of solutions to eliminate.
        :param mutations: The mutations rate.
        :param repetitions: The value to enable repetitions.
        :param padding: The value to pad with the solutions from the previous generation.
        """

        self.size = size

        self.ascending = ascending
        self.repetitions = repetitions
        self.padding = padding

        self.successors = scale(successors, size=size, name="successors")
        self.continuers = scale(continuers, size=size, name="continuers")
        self.eliminations = scale(eliminations, size=size, name="eliminations")
        self.parents = scale(parents, size=size, name="parents")
        self.mutations = scale(mutations, size=1, name="mutations")
    # end __init__

    def copy(self) -> Self:
        """
        Returns a copy of the definition object.

        :return: The new definition object.
        """

        return EnvironmentDefinition(
            size=self.size,
            ascending=self.ascending,
            parents=self.parents,
            repetitions=self.repetitions,
            eliminations=self.eliminations,
            successors=self.successors,
            continuers=self.continuers,
            mutations=self.mutations,
        )
    # end copy
# end EnvironmentDefinition

class Fitness(BaseModel):
    """A class to represent a fitness function."""

    def __call__(self, solution: Solution) -> float:
        """
        Calls the fitness function on the solution.

        :param solution: The solution object.

        :return: The fitness value.
        """

        return self.call(solution=solution)
    # end __call__

    @abstractmethod
    def call(self, solution: Solution) -> float:
        """
        Calls the fitness function on the solution.

        :param solution: The solution object.

        :return: The fitness value.
        """
    # end call
# end Fitness

class History(BaseModel):
    """A class to represent an environment history."""

    def __init__(self, generations: Optional[Iterable[Generation]] = None) -> None:
        """
        Defines the class attributes.

        :param generations: The generations to add to the history.
        """

        self.generations = list(generations or [])
    # end __init__

    def add(self, generation: Generation) -> None:
        """
        Adds the generation to the history.

        :param generation: The generation to add to the history.
        """

        self.generations.append(generation)
    # end add
# end History

class Environment(BaseModel):
    """A class to represent an environment."""

    OPTIMIZE = False

    def __init__(
            self,
            definition: EnvironmentDefinition,
            template: Template,
            fitness: Fitness,
            generation: Optional[Type[Generation]] = None,
            history: Optional[History] = None,
            optimize: Optional[bool] = None
    ) -> None:
        """
        Defines the attributes of the class.

        :param template: The template object.
        :param definition: The definition object.
        :param generation: The generation object.
        """

        if optimize is None:
            optimize = self.OPTIMIZE
        # end if

        if generation is None:
            generation = Generation
        # end if

        if issubclass(generation, Generation):
            generation = generation.build(
                template.build() for _ in range(definition.size)
            )
        # end if

        self.fitness = fitness
        self.definition = definition
        self.template = template
        self.generation = generation
        self.history = history
        self.optimize = optimize

        if isinstance(self.history, History):
            self.history.add(generation)
        # end if
    # end __init__

    def sort(
            self,
            solutions: Iterable[Solution],
            optimize: Optional[bool] = None
    ) -> List[Solution]:
        """
        Sorts the solutions by their fitness.

        :param solutions: The solutions to sort by fitness.
        :param optimize: The value to optimize the process with multithreading.

        :return: The sorted solutions.
        """

        if optimize is None:
            optimize = self.optimize
        # end if

        checked_solutions = [
            solution for solution in solutions
            if solution.fitness is None
        ]

        if not optimize:
            for solution in checked_solutions:
                solution.fitness = self.fitness(solution)
            # end for

        else:
            callers = []

            for solution in checked_solutions:
                callers.append(
                    Caller(
                        target=lambda sol: setattr(
                            sol, 'fitness', self.fitness(sol)
                        ), args=(solution,)
                    )
                )
            # end for

            multi_threaded_call(callers=callers)
        # end if

        return sorted(
            solutions,
            key=lambda sol: sol.fitness,
            reverse=self.definition.ascending
        )
    # end sort

    def mate(self, parents: Iterable[Solution]) -> Solution:
        """
        Mates the parents to generate the solutions.

        :param parents: The parents.

        :return: The solution.
        """

        attributes: List[Attribute] = []
        parents = list(parents)

        for i in range(len(self.template.attributes)):
            parent: Solution = random.choice(parents)
            attributes.append(parent.attributes[i])
        # end for

        return parents[0].build(attributes=attributes)
    # end mate

    def mates(
            self,
            parents: Iterable[Solution],
            optimize: Optional[bool] = None
    ) -> List[Solution]:
        """
        Mates the parents to generate the solutions.

        :param parents: The parents.
        :param optimize: The value to optimize the process with multithreading.

        :return: The solutions.
        """

        if optimize is None:
            optimize = self.optimize
        # end if

        parents = list(parents)

        size = min(len(parents), self.definition.eliminations)

        parents = parents[:size]

        random.shuffle(parents)

        successors = min(len(parents), self.definition.successors)

        parents_combinations = list(
            combinations(parents, self.definition.parents)
        )[:successors]

        if not optimize:
            return [
                self.mate(combination) for combination in
                parents_combinations
            ]

        else:
            callers = [
                Caller(target=self.mate, args=(combination,))
                for combination in parents_combinations
            ]

            return [
                result.returns for result in
                multi_threaded_call(callers=callers).callers.values()
            ]
        # end if
    # end mates

    def mutate(
            self,
            solution: Solution,
            optimize: Optional[bool] = None
    ) -> Solution:
        """
        Mates the parents to generate the solutions.

        :param solution: The solution to mutate.
        :param optimize: The value to optimize the process with multithreading.

        :return: The mutated solution.
        """

        if optimize is None:
            optimize = self.optimize
        # end if

        attributes: List[Attribute] = []

        if not optimize:
            for attribute in solution.attributes:
                attributes.append(
                    attribute.build() if (
                        random.uniform(0, 1) <= self.definition.mutations
                    ) else attribute
                )
            # end for

        else:
            callers = [
                Caller(
                    target=lambda attr: (
                        attributes.append(
                            attribute.build() if (
                                random.uniform(0, 1) <= self.definition.mutations
                            ) else attribute
                        )
                    ),
                    args=(attribute,)
                ) for attribute in solution.attributes
            ]

            multi_threaded_call(callers=callers)
        # end if

        return solution.build(attributes=attributes)
    # end mutate

    def mutations(
            self,
            solutions: Iterable[Solution],
            optimize: Optional[bool] = None
    ) -> List[Solution]:
        """
        Mates the parents to generate the solutions.

        :param solutions: The solutions to mutate.
        :param optimize: The value to optimize the process with multithreading.

        :return: The mutated solutions.
        """

        if optimize is None:
            optimize = self.optimize
        # end if

        if not optimize:
            return [self.mutate(solution) for solution in solutions]

        else:
            return [
                result.returns for result in multi_threaded_call(
                    callers=[
                        Caller(target=self.mutate, args=(solution,))
                        for solution in solutions
                    ]
                ).callers.values()
            ]
        # end if
    # end mutations

    def next(self, generation: Optional[Generation] = None) -> Generation:
        """
        Generates the next generation of solutions based on the given one.

        :param generation: The base generation of solutions.

        :return: The next generation.
        """

        generation = generation or self.generation

        size = min(
            len(generation.solutions),
            self.definition.eliminations
        )

        solutions = list(generation.solutions)

        solutions = self.sort(solutions=solutions)

        if not self.definition.repetitions:
            solutions = eliminate_repetitions(solutions=solutions)
        # end if

        solutions = solutions[:size]
        successors = min(self.definition.successors, len(solutions))
        parents = solutions[:successors]

        children = self.sort(
            solutions=self.mutations(solutions=self.mates(parents=parents))
        )

        continuers = min(len(parents), self.definition.continuers)

        parents = parents[:continuers]

        if self.definition.padding:
            left = [
                solution for solution in generation.solutions
                if (solution not in children) and (solution not in parents)
            ]

        else:
            left = []
        # end if

        length = min(len(generation.solutions), len(solutions))

        solutions = [*children, *parents, *left]
        solutions = self.sort(solutions=solutions)[:length]

        if not self.definition.repetitions:
            solutions = eliminate_repetitions(solutions=solutions)
        # end if

        generation = generation.build(solutions=solutions)

        if isinstance(self.history, History):
            self.history.add(generation)
        # end if

        self.generation = generation

        return generation
    # end next
# end Environment