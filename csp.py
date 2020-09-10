from abc import ABC, abstractmethod

class Constraint(ABC):
    def __init__(self, variables):
        self.variables = variables

    @abstractmethod
    def satisfied(self, assignment): pass


class CSP:
    def __init__(self, variables, domains):
        self.variables = variables
        self.domains = domains 
        self.constraints = {}
        for variable in self.variables:
            self.constraints[variable] = []
            if variable not in self.domains:
                raise LookupError("Every variable should have a domain assigned to it.")

    def add_constraint(self, constraint):
        for variable in constraint.variables:
            if variable not in self.variables:
                raise LookupError("Variable in constraint not in CSP")
            else:
                self.constraints[variable].append(constraint)

    def consistent(self, variable, assignment):
        for constraint in self.constraints[variable]:
            if not constraint.satisfied(assignment):
                return False
        return True

    def backtracking_search(self, assignment):
        # assignment is complete if every variable is assigned (our base case)
        if len(assignment) == len(self.variables):
            return assignment

        # get all variables in the CSP but not in the assignment
        unassigned = [v for v in self.variables if v not in assignment]

        # get the every possible domain value of the first unassigned variable
        first = unassigned[0]
        for value in self.domains[first]:
            local_assignment = assignment.copy()
            local_assignment[first] = value
            # if we're still consistent, we recurse (continue)
            if self.consistent(first, local_assignment):
                result = self.backtracking_search(local_assignment)
                # if we didn't find the result, we will end up backtracking
                if result is not None:
                    return result
        return None



class ConstraintProblem(Constraint):
    def __init__(self, letters):
        super().__init__(letters)
        self.letters = letters

    def satisfied(self, assignment):
        # if there are duplicate values then it's not a solution
        if len(set(assignment.values())) < len(assignment):
            return False

        # if all variables have been assigned, check if it adds correctly
        if len(assignment) == len(self.letters):
            n: int = assignment["N"]
            i: int = assignment["I"]
            a: int = assignment["A"]
            s: int = assignment["S"]
            g: int = assignment["G"]
            nina: int = n * 1000 + i * 100 + n * 10 + a * 1
            sing: int = s * 1000 + i * 100 + n * 10 + g
            again: int = a * 10000 + g * 1000 + a * 100 + i * 10 + n
            return nina + sing == again

        return True # no conflict

if __name__ == "__main__":
    letters = ["N", "I", "A", "S", "G"]
    possible_digits = {}
    assignment = {}
    for letter in letters:
        possible_digits[letter] = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    possible_digits["A"] = [1]  # so we don't get answers starting with a 0
    csp = CSP(letters, possible_digits)
    csp.add_constraint(ConstraintProblem(letters))
    solution = csp.backtracking_search(assignment)
    if solution is None:
        print("No solution found!")
    else:
        print(solution)