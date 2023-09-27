# This file was automatically generated by SWIG (https://www.swig.org).
# Version 4.1.1
#
# Do not make changes to this file unless you know what you are doing - modify
# the SWIG interface file instead.

# Import the low-level C/C++ module
if __package__ or "." in __name__:
    from . import _pywraplp
else:
    import _pywraplp

try:
    import builtins as __builtin__
except ImportError:
    import __builtin__

def _swig_repr(self):
    try:
        strthis = "proxy of " + self.this.__repr__()
    except __builtin__.Exception:
        strthis = ""
    return f"<{self.__class__.__module__}.{self.__class__.__name__}; {strthis} >"

def _swig_setattr_nondynamic_instance_variable(set):
    def set_instance_attr(self, name, value):
        if name == "this":
            set(self, name, value)
        elif name == "thisown":
            self.this.own(value)
        elif hasattr(self, name) and isinstance(getattr(type(self), name), property):
            set(self, name, value)
        else:
            raise AttributeError("You cannot add instance attributes to %s" % self)
    return set_instance_attr

def _swig_setattr_nondynamic_class_variable(set):
    def set_class_attr(cls, name, value):
        if hasattr(cls, name) and not isinstance(getattr(cls, name), property):
            set(cls, name, value)
        else:
            raise AttributeError("You cannot add class attributes to %s" % cls)
    return set_class_attr

def _swig_add_metaclass(metaclass):
    """Class decorator for adding a metaclass to a SWIG wrapped class - a slimmed down version of six.add_metaclass"""
    def wrapper(cls):
        return metaclass(cls.__name__, cls.__bases__, cls.__dict__.copy())
    return wrapper

class _SwigNonDynamicMeta(type):
    """Meta class to enforce nondynamic attributes (no new attributes) for a class"""

    __setattr__ = _swig_setattr_nondynamic_class_variable(type.__setattr__)

import numbers

from ortools.linear_solver.linear_solver_natural_api import (
    OFFSET_KEY,
    SumArray,
    VariableExpr,
)
from ortools.linear_solver.linear_solver_natural_api import (
    LinearConstraint as LinearConstraint,
)
from ortools.linear_solver.linear_solver_natural_api import (
    LinearExpr as LinearExpr,
)

class Solver:
    r"""
    This mathematical programming (MP) solver class is the main class
    though which users build and solve problems.
    """

    thisown = property(
        lambda x: x.this.own(),
        lambda x, v: x.this.own(v),
        doc="The membership flag",
    )
    __repr__ = _swig_repr
    CLP_LINEAR_PROGRAMMING = _pywraplp.Solver_CLP_LINEAR_PROGRAMMING
    GLPK_LINEAR_PROGRAMMING = _pywraplp.Solver_GLPK_LINEAR_PROGRAMMING
    GLOP_LINEAR_PROGRAMMING = _pywraplp.Solver_GLOP_LINEAR_PROGRAMMING
    PDLP_LINEAR_PROGRAMMING = _pywraplp.Solver_PDLP_LINEAR_PROGRAMMING
    SCIP_MIXED_INTEGER_PROGRAMMING = _pywraplp.Solver_SCIP_MIXED_INTEGER_PROGRAMMING
    GLPK_MIXED_INTEGER_PROGRAMMING = _pywraplp.Solver_GLPK_MIXED_INTEGER_PROGRAMMING
    CBC_MIXED_INTEGER_PROGRAMMING = _pywraplp.Solver_CBC_MIXED_INTEGER_PROGRAMMING
    GUROBI_LINEAR_PROGRAMMING = _pywraplp.Solver_GUROBI_LINEAR_PROGRAMMING
    GUROBI_MIXED_INTEGER_PROGRAMMING = _pywraplp.Solver_GUROBI_MIXED_INTEGER_PROGRAMMING
    CPLEX_LINEAR_PROGRAMMING = _pywraplp.Solver_CPLEX_LINEAR_PROGRAMMING
    CPLEX_MIXED_INTEGER_PROGRAMMING = _pywraplp.Solver_CPLEX_MIXED_INTEGER_PROGRAMMING
    XPRESS_LINEAR_PROGRAMMING = _pywraplp.Solver_XPRESS_LINEAR_PROGRAMMING
    XPRESS_MIXED_INTEGER_PROGRAMMING = _pywraplp.Solver_XPRESS_MIXED_INTEGER_PROGRAMMING
    BOP_INTEGER_PROGRAMMING = _pywraplp.Solver_BOP_INTEGER_PROGRAMMING
    SAT_INTEGER_PROGRAMMING = _pywraplp.Solver_SAT_INTEGER_PROGRAMMING

    def __init__(self, name, problem_type) -> None:
        r"""Create a solver with the given name and underlying solver backend."""
        _pywraplp.Solver_swiginit(self, _pywraplp.new_Solver(name, problem_type))
    __swig_destroy__ = _pywraplp.delete_Solver

    @staticmethod
    def CreateSolver(solver_id: str) -> Solver:
        r"""
        Recommended factory method to create a MPSolver instance, especially in
        non C++ languages.

        It returns a newly created solver instance if successful, or a nullptr
        otherwise. This can occur if the relevant interface is not linked in, or if
        a needed license is not accessible for commercial solvers.

        Ownership of the solver is passed on to the caller of this method.
        It will accept both string names of the OptimizationProblemType enum, as
        well as a short version (i.e. "SCIP_MIXED_INTEGER_PROGRAMMING" or "SCIP").

        solver_id is case insensitive, and the following names are supported:
          - CLP_LINEAR_PROGRAMMING or CLP
          - CBC_MIXED_INTEGER_PROGRAMMING or CBC
          - GLOP_LINEAR_PROGRAMMING or GLOP
          - BOP_INTEGER_PROGRAMMING or BOP
          - SAT_INTEGER_PROGRAMMING or SAT or CP_SAT
          - SCIP_MIXED_INTEGER_PROGRAMMING or SCIP
          - GUROBI_LINEAR_PROGRAMMING or GUROBI_LP
          - GUROBI_MIXED_INTEGER_PROGRAMMING or GUROBI or GUROBI_MIP
          - CPLEX_LINEAR_PROGRAMMING or CPLEX_LP
          - CPLEX_MIXED_INTEGER_PROGRAMMING or CPLEX or CPLEX_MIP
          - XPRESS_LINEAR_PROGRAMMING or XPRESS_LP
          - XPRESS_MIXED_INTEGER_PROGRAMMING or XPRESS or XPRESS_MIP
          - GLPK_LINEAR_PROGRAMMING or GLPK_LP
          - GLPK_MIXED_INTEGER_PROGRAMMING or GLPK or GLPK_MIP
        """
        return _pywraplp.Solver_CreateSolver(solver_id)
    @staticmethod
    def SupportsProblemType(problem_type):
        r"""
        Whether the given problem type is supported (this will depend on the
        targets that you linked).
        """
        return _pywraplp.Solver_SupportsProblemType(problem_type)
    def Clear(self):
        r"""
        Clears the objective (including the optimization direction), all variables
        and constraints. All the other properties of the MPSolver (like the time
        limit) are kept untouched.
        """
        return _pywraplp.Solver_Clear(self)
    def NumVariables(self):
        r"""Returns the number of variables."""
        return _pywraplp.Solver_NumVariables(self)
    def variables(self):
        r"""
        Returns the array of variables handled by the MPSolver. (They are listed in
        the order in which they were created.)
        """
        return _pywraplp.Solver_variables(self)
    def variable(self, index):
        r"""Returns the variable at position index."""
        return _pywraplp.Solver_variable(self, index)
    def LookupVariable(self, var_name):
        r"""
        Looks up a variable by name, and returns nullptr if it does not exist. The
        first call has a O(n) complexity, as the variable name index is lazily
        created upon first use. Will crash if variable names are not unique.
        """
        return _pywraplp.Solver_LookupVariable(self, var_name)
    def Var(self, lb, ub, integer, name) -> Variable:
        r"""
        Creates a variable with the given bounds, integrality requirement and
        name. Bounds can be finite or +/- MPSolver::infinity(). The MPSolver owns
        the variable (i.e. the returned pointer is borrowed). Variable names are
        optional. If you give an empty name, name() will auto-generate one for you
        upon request.
        """
        return _pywraplp.Solver_Var(self, lb, ub, integer, name)
    def NumVar(self, lb: float, ub: float, name: str) -> Variable:
        r"""Creates a continuous variable."""
        return _pywraplp.Solver_NumVar(self, lb, ub, name)
    def IntVar(self, lb: float, ub: float, name: str) -> Variable:
        r"""Creates an integer variable."""
        return _pywraplp.Solver_IntVar(self, lb, ub, name)
    def BoolVar(self, name: str) -> Variable:
        r"""Creates a boolean variable."""
        return _pywraplp.Solver_BoolVar(self, name)
    def NumConstraints(self):
        r"""Returns the number of constraints."""
        return _pywraplp.Solver_NumConstraints(self)
    def constraints(self):
        r"""
        Returns the array of constraints handled by the MPSolver.

        They are listed in the order in which they were created.
        """
        return _pywraplp.Solver_constraints(self)
    def constraint(self, index):
        r"""Returns the constraint at the given index."""
        return _pywraplp.Solver_constraint(self, index)
    def LookupConstraint(self, constraint_name):
        r"""
         Looks up a constraint by name, and returns nullptr if it does not exist.

        The first call has a O(n) complexity, as the constraint name index is
        lazily created upon first use. Will crash if constraint names are not
        unique.
        """
        return _pywraplp.Solver_LookupConstraint(self, constraint_name)
    def Constraint(self, *args):
        r"""
        *Overload 1:*

        Creates a linear constraint with given bounds.

        Bounds can be finite or +/- MPSolver::infinity(). The MPSolver class
        assumes ownership of the constraint.

        :rtype: :py:class:`MPConstraint`
        :return: a pointer to the newly created constraint.

        |

        *Overload 2:*
         Creates a constraint with -infinity and +infinity bounds.

        |

        *Overload 3:*
         Creates a named constraint with given bounds.

        |

        *Overload 4:*
         Creates a named constraint with -infinity and +infinity bounds.
        """
        return _pywraplp.Solver_Constraint(self, *args)
    def Objective(self):
        r"""Returns the mutable objective object."""
        return _pywraplp.Solver_Objective(self)
    OPTIMAL: int = _pywraplp.Solver_OPTIMAL
    r""" optimal."""
    FEASIBLE: int = _pywraplp.Solver_FEASIBLE
    r""" feasible, or stopped by limit."""
    INFEASIBLE: int = _pywraplp.Solver_INFEASIBLE
    r""" proven infeasible."""
    UNBOUNDED: int = _pywraplp.Solver_UNBOUNDED
    r""" proven unbounded."""
    ABNORMAL: int = _pywraplp.Solver_ABNORMAL
    r""" abnormal, i.e., error of some kind."""
    MODEL_INVALID: int = _pywraplp.Solver_MODEL_INVALID
    r""" the model is trivially invalid (NaN coefficients, etc)."""
    NOT_SOLVED: int = _pywraplp.Solver_NOT_SOLVED
    r""" not been solved yet."""

    def Solve(self, params: MPSolverParameters | None = None) -> int:
        r"""
        *Overload 1:*
        Solves the problem using the default parameter values.

        |

        *Overload 2:*
        Solves the problem using the specified parameter values.
        """
        return _pywraplp.Solver_Solve(self, *args)
    def ComputeConstraintActivities(self):
        r"""
        Advanced usage: compute the "activities" of all constraints, which are the
        sums of their linear terms. The activities are returned in the same order
        as constraints(), which is the order in which constraints were added; but
        you can also use MPConstraint::index() to get a constraint's index.
        """
        return _pywraplp.Solver_ComputeConstraintActivities(self)
    def VerifySolution(self, tolerance, log_errors):
        r"""
        Advanced usage: Verifies the *correctness* of the solution.

        It verifies that all variables must be within their domains, all
        constraints must be satisfied, and the reported objective value must be
        accurate.

        Usage:
        - This can only be called after Solve() was called.
        - "tolerance" is interpreted as an absolute error threshold.
        - For the objective value only, if the absolute error is too large,
          the tolerance is interpreted as a relative error threshold instead.
        - If "log_errors" is true, every single violation will be logged.
        - If "tolerance" is negative, it will be set to infinity().

        Most users should just set the --verify_solution flag and not bother using
        this method directly.
        """
        return _pywraplp.Solver_VerifySolution(self, tolerance, log_errors)
    def InterruptSolve(self):
        r"""
         Interrupts the Solve() execution to terminate processing if possible.

        If the underlying interface supports interruption; it does that and returns
        true regardless of whether there's an ongoing Solve() or not. The Solve()
        call may still linger for a while depending on the conditions.  If
        interruption is not supported; returns false and does nothing.
        MPSolver::SolverTypeSupportsInterruption can be used to check if
        interruption is supported for a given solver type.
        """
        return _pywraplp.Solver_InterruptSolve(self)
    def FillSolutionResponseProto(self, response):
        r"""Encodes the current solution in a solution response protocol buffer."""
        return _pywraplp.Solver_FillSolutionResponseProto(self, response)
    @staticmethod
    def SolveWithProto(model_request, response, interrupt=None):
        r"""
        Solves the model encoded by a MPModelRequest protocol buffer and fills the
        solution encoded as a MPSolutionResponse. The solve is stopped prematurely
        if interrupt is non-null at set to true during (or before) solving.
        Interruption is only supported if SolverTypeSupportsInterruption() returns
        true for the requested solver. Passing a non-null interruption with any
        other solver type immediately returns an MPSOLVER_INCOMPATIBLE_OPTIONS
        error.

        Note(user): This attempts to first use `DirectlySolveProto()` (if
        implemented). Consequently, this most likely does *not* override any of
        the default parameters of the underlying solver. This behavior *differs*
        from `MPSolver::Solve()` which by default sets the feasibility tolerance
        and the gap limit (as of 2020/02/11, to 1e-7 and 0.0001, respectively).
        """
        return _pywraplp.Solver_SolveWithProto(model_request, response, interrupt)
    def ExportModelToProto(self, output_model):
        r"""Exports model to protocol buffer."""
        return _pywraplp.Solver_ExportModelToProto(self, output_model)
    def SetSolverSpecificParametersAsString(self, parameters):
        r"""
        Advanced usage: pass solver specific parameters in text format.

        The format is solver-specific and is the same as the corresponding solver
        configuration file format. Returns true if the operation was successful.
        """
        return _pywraplp.Solver_SetSolverSpecificParametersAsString(self, parameters)
    FREE = _pywraplp.Solver_FREE
    AT_LOWER_BOUND = _pywraplp.Solver_AT_LOWER_BOUND
    AT_UPPER_BOUND = _pywraplp.Solver_AT_UPPER_BOUND
    FIXED_VALUE = _pywraplp.Solver_FIXED_VALUE
    BASIC = _pywraplp.Solver_BASIC

    @staticmethod
    def infinity():
        r"""
        Infinity.

        You can use -MPSolver::infinity() for negative infinity.
        """
        return _pywraplp.Solver_infinity()
    def EnableOutput(self):
        r"""Enables solver logging."""
        return _pywraplp.Solver_EnableOutput(self)
    def SuppressOutput(self):
        r"""Suppresses solver logging."""
        return _pywraplp.Solver_SuppressOutput(self)
    def iterations(self):
        r"""Returns the number of simplex iterations."""
        return _pywraplp.Solver_iterations(self)
    def nodes(self):
        r"""
        Returns the number of branch-and-bound nodes evaluated during the solve.

        Only available for discrete problems.
        """
        return _pywraplp.Solver_nodes(self)
    def SolverVersion(self):
        r"""Returns a string describing the underlying solver and its version."""
        return _pywraplp.Solver_SolverVersion(self)
    def ComputeExactConditionNumber(self):
        r"""
         Advanced usage: computes the exact condition number of the current scaled
        basis: L1norm(B) * L1norm(inverse(B)), where B is the scaled basis.

        This method requires that a basis exists: it should be called after Solve.
        It is only available for continuous problems. It is implemented for GLPK
        but not CLP because CLP does not provide the API for doing it.

        The condition number measures how well the constraint matrix is conditioned
        and can be used to predict whether numerical issues will arise during the
        solve: the model is declared infeasible whereas it is feasible (or
        vice-versa), the solution obtained is not optimal or violates some
        constraints, the resolution is slow because of repeated singularities.

        The rule of thumb to interpret the condition number kappa is:
          - o kappa <= 1e7: virtually no chance of numerical issues
          - o 1e7 < kappa <= 1e10: small chance of numerical issues
          - o 1e10 < kappa <= 1e13: medium chance of numerical issues
          - o kappa > 1e13: high chance of numerical issues

        The computation of the condition number depends on the quality of the LU
        decomposition, so it is not very accurate when the matrix is ill
        conditioned.
        """
        return _pywraplp.Solver_ComputeExactConditionNumber(self)
    def NextSolution(self):
        r"""
        Some solvers (MIP only, not LP) can produce multiple solutions to the
        problem. Returns true when another solution is available, and updates the
        MPVariable* objects to make the new solution queryable. Call only after
        calling solve.

        The optimality properties of the additional solutions found, and whether or
        not the solver computes them ahead of time or when NextSolution() is called
        is solver specific.

        As of 2020-02-10, only Gurobi and SCIP support NextSolution(), see
        linear_solver_interfaces_test for an example of how to configure these
        solvers for multiple solutions. Other solvers return false unconditionally.
        """
        return _pywraplp.Solver_NextSolution(self)
    def set_time_limit(self, time_limit_milliseconds):
        return _pywraplp.Solver_set_time_limit(self, time_limit_milliseconds)
    def wall_time(self):
        return _pywraplp.Solver_wall_time(self)
    def LoadModelFromProto(self, input_model):
        return _pywraplp.Solver_LoadModelFromProto(self, input_model)
    def LoadModelFromProtoWithUniqueNamesOrDie(self, input_model):
        return _pywraplp.Solver_LoadModelFromProtoWithUniqueNamesOrDie(
            self,
            input_model,
        )
    def LoadSolutionFromProto(self, *args):
        return _pywraplp.Solver_LoadSolutionFromProto(self, *args)
    def ExportModelAsLpFormat(self, obfuscated):
        return _pywraplp.Solver_ExportModelAsLpFormat(self, obfuscated)
    def ExportModelAsMpsFormat(self, fixed_format, obfuscated):
        return _pywraplp.Solver_ExportModelAsMpsFormat(self, fixed_format, obfuscated)
    def SetHint(self, variables, values):
        r"""
        Set a hint for solution.

        If a feasible or almost-feasible solution to the problem is already known,
        it may be helpful to pass it to the solver so that it can be used. A
        solver that supports this feature will try to use this information to
        create its initial feasible solution.

        Note that it may not always be faster to give a hint like this to the
        solver. There is also no guarantee that the solver will use this hint or
        try to return a solution "close" to this assignment in case of multiple
        optimal solutions.
        """
        return _pywraplp.Solver_SetHint(self, variables, values)
    def SetNumThreads(self, num_theads):
        r"""Sets the number of threads to be used by the solver."""
        return _pywraplp.Solver_SetNumThreads(self, num_theads)
    def Add(self, constraint: LinearConstraint, name: str = "") -> Constraint:
        if isinstance(constraint, bool):
            if constraint:
                return self.RowConstraint(0, 0, name)
            else:
                return self.RowConstraint(1, 1, name)
        else:
            return constraint.Extract(self, name)
    def Sum(self, expr_array: list[LinearExpr]) -> SumArray:
        return SumArray(expr_array)
    def RowConstraint(self, *args):
        return self.Constraint(*args)
    def Minimize(self, expr: LinearExpr) -> None:
        objective = self.Objective()
        objective.Clear()
        objective.SetMinimization()
        if isinstance(expr, numbers.Number):
            objective.SetOffset(expr)
        else:
            coeffs = expr.GetCoeffs()
            objective.SetOffset(coeffs.pop(OFFSET_KEY, 0.0))
            for (
                v,
                c,
            ) in list(coeffs.items()):
                objective.SetCoefficient(v, float(c))
    def Maximize(self, expr: LinearExpr) -> None:
        objective = self.Objective()
        objective.Clear()
        objective.SetMaximization()
        if isinstance(expr, numbers.Number):
            objective.SetOffset(expr)
        else:
            coeffs = expr.GetCoeffs()
            objective.SetOffset(coeffs.pop(OFFSET_KEY, 0.0))
            for (
                v,
                c,
            ) in list(coeffs.items()):
                objective.SetCoefficient(v, float(c))
    @staticmethod
    def Infinity():
        return _pywraplp.Solver_Infinity()
    def SetTimeLimit(self, x):
        return _pywraplp.Solver_SetTimeLimit(self, x)
    def WallTime(self):
        return _pywraplp.Solver_WallTime(self)
    def Iterations(self):
        return _pywraplp.Solver_Iterations(self)

# Register Solver in _pywraplp:
_pywraplp.Solver_swigregister(Solver)

def __lshift__(*args):
    return _pywraplp.__lshift__(*args)

class Objective:
    r"""A class to express a linear objective."""

    thisown = property(
        lambda x: x.this.own(),
        lambda x, v: x.this.own(v),
        doc="The membership flag",
    )

    def __init__(self, *args, **kwargs) -> None:
        raise AttributeError("No constructor defined")
    __repr__ = _swig_repr

    def Clear(self):
        r"""
         Clears the offset, all variables and coefficients, and the optimization
        direction.
        """
        return _pywraplp.Objective_Clear(self)
    def SetCoefficient(self, var, coeff):
        r"""
        Sets the coefficient of the variable in the objective.

        If the variable does not belong to the solver, the function just returns,
        or crashes in non-opt mode.
        """
        return _pywraplp.Objective_SetCoefficient(self, var, coeff)
    def GetCoefficient(self, var):
        r"""
         Gets the coefficient of a given variable in the objective

        It returns 0 if the variable does not appear in the objective).
        """
        return _pywraplp.Objective_GetCoefficient(self, var)
    def SetOffset(self, value):
        r"""Sets the constant term in the objective."""
        return _pywraplp.Objective_SetOffset(self, value)
    def offset(self):
        r"""Gets the constant term in the objective."""
        return _pywraplp.Objective_offset(self)
    def SetOptimizationDirection(self, maximize):
        r"""Sets the optimization direction (maximize: true or minimize: false)."""
        return _pywraplp.Objective_SetOptimizationDirection(self, maximize)
    def SetMinimization(self):
        r"""Sets the optimization direction to minimize."""
        return _pywraplp.Objective_SetMinimization(self)
    def SetMaximization(self):
        r"""Sets the optimization direction to maximize."""
        return _pywraplp.Objective_SetMaximization(self)
    def maximization(self):
        r"""Is the optimization direction set to maximize?"""
        return _pywraplp.Objective_maximization(self)
    def minimization(self):
        r"""Is the optimization direction set to minimize?"""
        return _pywraplp.Objective_minimization(self)
    def Value(self):
        r"""
        Returns the objective value of the best solution found so far.

        It is the optimal objective value if the problem has been solved to
        optimality.

        Note: the objective value may be slightly different than what you could
        compute yourself using ``MPVariable::solution_value();`` please use the
        --verify_solution flag to gain confidence about the numerical stability of
        your solution.
        """
        return _pywraplp.Objective_Value(self)
    def BestBound(self):
        r"""
        Returns the best objective bound.

        In case of minimization, it is a lower bound on the objective value of the
        optimal integer solution. Only available for discrete problems.
        """
        return _pywraplp.Objective_BestBound(self)
    def Offset(self):
        return _pywraplp.Objective_Offset(self)
    __swig_destroy__ = _pywraplp.delete_Objective

# Register Objective in _pywraplp:
_pywraplp.Objective_swigregister(Objective)

class Variable(LinearExpr):
    r"""The class for variables of a Mathematical Programming (MP) model."""

    thisown = property(
        lambda x: x.this.own(),
        lambda x, v: x.this.own(v),
        doc="The membership flag",
    )

    def __init__(self, *args, **kwargs) -> None:
        raise AttributeError("No constructor defined")
    def name(self):
        r"""Returns the name of the variable."""
        return _pywraplp.Variable_name(self)
    def SetInteger(self, integer):
        r"""Sets the integrality requirement of the variable."""
        return _pywraplp.Variable_SetInteger(self, integer)
    def integer(self):
        r"""Returns the integrality requirement of the variable."""
        return _pywraplp.Variable_integer(self)
    def solution_value(self):
        r"""
        Returns the value of the variable in the current solution.

        If the variable is integer, then the value will always be an integer (the
        underlying solver handles floating-point values only, but this function
        automatically rounds it to the nearest integer; see: man 3 round).
        """
        return _pywraplp.Variable_solution_value(self)
    def index(self):
        r"""Returns the index of the variable in the MPSolver::variables_."""
        return _pywraplp.Variable_index(self)
    def lb(self):
        r"""Returns the lower bound."""
        return _pywraplp.Variable_lb(self)
    def ub(self):
        r"""Returns the upper bound."""
        return _pywraplp.Variable_ub(self)
    def SetBounds(self, lb, ub):
        r"""Sets both the lower and upper bounds."""
        return _pywraplp.Variable_SetBounds(self, lb, ub)
    def reduced_cost(self):
        r"""
        Advanced usage: returns the reduced cost of the variable in the current
        solution (only available for continuous problems).
        """
        return _pywraplp.Variable_reduced_cost(self)
    def basis_status(self):
        r"""
        Advanced usage: returns the basis status of the variable in the current
        solution (only available for continuous problems).

        See also: MPSolver::BasisStatus.
        """
        return _pywraplp.Variable_basis_status(self)
    def branching_priority(self):
        r"""
        Advanced usage: Certain MIP solvers (e.g. Gurobi or SCIP) allow you to set
        a per-variable priority for determining which variable to branch on.

        A value of 0 is treated as default, and is equivalent to not setting the
        branching priority. The solver looks first to branch on fractional
        variables in higher priority levels. As of 2019-05, only Gurobi and SCIP
        support setting branching priority; all other solvers will simply ignore
        this annotation.
        """
        return _pywraplp.Variable_branching_priority(self)
    def SetBranchingPriority(self, priority):
        return _pywraplp.Variable_SetBranchingPriority(self, priority)
    def __str__(self) -> str:
        return _pywraplp.Variable___str__(self)
    def __repr__(self) -> str:
        return _pywraplp.Variable___repr__(self)
    def __getattr__(self, name):
        return getattr(VariableExpr(self), name)
    def SolutionValue(self) -> float | int:
        r"""
        Returns the value of the variable in the current solution.

        If the variable is integer, then the value will always be an integer (the
        underlying solver handles floating-point values only, but this function
        automatically rounds it to the nearest integer; see: man 3 round).
        """
        return _pywraplp.Variable_SolutionValue(self)
    def Integer(self):
        return _pywraplp.Variable_Integer(self)
    def Lb(self):
        return _pywraplp.Variable_Lb(self)
    def Ub(self):
        return _pywraplp.Variable_Ub(self)
    def SetLb(self, x):
        return _pywraplp.Variable_SetLb(self, x)
    def SetUb(self, x):
        return _pywraplp.Variable_SetUb(self, x)
    def ReducedCost(self):
        return _pywraplp.Variable_ReducedCost(self)
    __swig_destroy__ = _pywraplp.delete_Variable

# Register Variable in _pywraplp:
_pywraplp.Variable_swigregister(Variable)

class Constraint:
    r"""
    The class for constraints of a Mathematical Programming (MP) model.

    A constraint is represented as a linear equation or inequality.
    """

    thisown = property(
        lambda x: x.this.own(),
        lambda x, v: x.this.own(v),
        doc="The membership flag",
    )

    def __init__(self, *args, **kwargs) -> None:
        raise AttributeError("No constructor defined")
    __repr__ = _swig_repr

    def name(self):
        r"""Returns the name of the constraint."""
        return _pywraplp.Constraint_name(self)
    def Clear(self):
        r"""Clears all variables and coefficients. Does not clear the bounds."""
        return _pywraplp.Constraint_Clear(self)
    def SetCoefficient(self, var, coeff):
        r"""
        Sets the coefficient of the variable on the constraint.

        If the variable does not belong to the solver, the function just returns,
        or crashes in non-opt mode.
        """
        return _pywraplp.Constraint_SetCoefficient(self, var, coeff)
    def GetCoefficient(self, var):
        r"""
        Gets the coefficient of a given variable on the constraint (which is 0 if
        the variable does not appear in the constraint).
        """
        return _pywraplp.Constraint_GetCoefficient(self, var)
    def lb(self):
        r"""Returns the lower bound."""
        return _pywraplp.Constraint_lb(self)
    def ub(self):
        r"""Returns the upper bound."""
        return _pywraplp.Constraint_ub(self)
    def SetBounds(self, lb, ub):
        r"""Sets both the lower and upper bounds."""
        return _pywraplp.Constraint_SetBounds(self, lb, ub)
    def set_is_lazy(self, laziness):
        r"""
        Advanced usage: sets the constraint "laziness".

        **This is only supported for SCIP and has no effect on other
        solvers.**

        When **laziness** is true, the constraint is only considered by the Linear
        Programming solver if its current solution violates the constraint. In this
        case, the constraint is definitively added to the problem. This may be
        useful in some MIP problems, and may have a dramatic impact on performance.

        For more info see: http://tinyurl.com/lazy-constraints.
        """
        return _pywraplp.Constraint_set_is_lazy(self, laziness)
    def index(self):
        r"""Returns the index of the constraint in the MPSolver::constraints_."""
        return _pywraplp.Constraint_index(self)
    def dual_value(self):
        r"""
        Advanced usage: returns the dual value of the constraint in the current
        solution (only available for continuous problems).
        """
        return _pywraplp.Constraint_dual_value(self)
    def basis_status(self):
        r"""
        Advanced usage: returns the basis status of the constraint.

        It is only available for continuous problems).

        Note that if a constraint "linear_expression in [lb, ub]" is transformed
        into "linear_expression + slack = 0" with slack in [-ub, -lb], then this
        status is the same as the status of the slack variable with AT_UPPER_BOUND
        and AT_LOWER_BOUND swapped.

        See also: MPSolver::BasisStatus.
        """
        return _pywraplp.Constraint_basis_status(self)
    def Lb(self):
        return _pywraplp.Constraint_Lb(self)
    def Ub(self):
        return _pywraplp.Constraint_Ub(self)
    def SetLb(self, x):
        return _pywraplp.Constraint_SetLb(self, x)
    def SetUb(self, x):
        return _pywraplp.Constraint_SetUb(self, x)
    def DualValue(self):
        return _pywraplp.Constraint_DualValue(self)
    __swig_destroy__ = _pywraplp.delete_Constraint

# Register Constraint in _pywraplp:
_pywraplp.Constraint_swigregister(Constraint)

class MPSolverParameters:
    r"""
    This class stores parameter settings for LP and MIP solvers. Some parameters
    are marked as advanced: do not change their values unless you know what you
    are doing!

    For developers: how to add a new parameter:
    - Add the new Foo parameter in the DoubleParam or IntegerParam enum.
    - If it is a categorical param, add a FooValues enum.
    - Decide if the wrapper should define a default value for it: yes
      if it controls the properties of the solution (example:
      tolerances) or if it consistently improves performance, no
      otherwise. If yes, define kDefaultFoo.
    - Add a foo_value_ member and, if no default value is defined, a
      foo_is_default_ member.
    - Add code to handle Foo in Set...Param, Reset...Param,
      Get...Param, Reset and the constructor.
    - In class MPSolverInterface, add a virtual method SetFoo, add it
      to SetCommonParameters or SetMIPParameters, and implement it for
      each solver. Sometimes, parameters need to be implemented
      differently, see for example the INCREMENTALITY implementation.
    - Add a test in linear_solver_test.cc.

    TODO(user): store the parameter values in a protocol buffer
    instead. We need to figure out how to deal with the subtleties of
    the default values.
    """

    thisown = property(
        lambda x: x.this.own(),
        lambda x, v: x.this.own(v),
        doc="The membership flag",
    )
    __repr__ = _swig_repr
    RELATIVE_MIP_GAP = _pywraplp.MPSolverParameters_RELATIVE_MIP_GAP
    r""" Limit for relative MIP gap."""
    PRIMAL_TOLERANCE = _pywraplp.MPSolverParameters_PRIMAL_TOLERANCE
    r"""
    Advanced usage: tolerance for primal feasibility of basic solutions.

    This does not control the integer feasibility tolerance of integer
    solutions for MIP or the tolerance used during presolve.
    """
    DUAL_TOLERANCE = _pywraplp.MPSolverParameters_DUAL_TOLERANCE
    r""" Advanced usage: tolerance for dual feasibility of basic solutions."""
    PRESOLVE = _pywraplp.MPSolverParameters_PRESOLVE
    r""" Advanced usage: presolve mode."""
    LP_ALGORITHM = _pywraplp.MPSolverParameters_LP_ALGORITHM
    r""" Algorithm to solve linear programs."""
    INCREMENTALITY = _pywraplp.MPSolverParameters_INCREMENTALITY
    r""" Advanced usage: incrementality from one solve to the next."""
    SCALING = _pywraplp.MPSolverParameters_SCALING
    r""" Advanced usage: enable or disable matrix scaling."""
    PRESOLVE_OFF = _pywraplp.MPSolverParameters_PRESOLVE_OFF
    r""" Presolve is off."""
    PRESOLVE_ON = _pywraplp.MPSolverParameters_PRESOLVE_ON
    r""" Presolve is on."""
    DUAL = _pywraplp.MPSolverParameters_DUAL
    r""" Dual simplex."""
    PRIMAL = _pywraplp.MPSolverParameters_PRIMAL
    r""" Primal simplex."""
    BARRIER = _pywraplp.MPSolverParameters_BARRIER
    r""" Barrier algorithm."""
    INCREMENTALITY_OFF = _pywraplp.MPSolverParameters_INCREMENTALITY_OFF
    r""" Start solve from scratch."""
    INCREMENTALITY_ON = _pywraplp.MPSolverParameters_INCREMENTALITY_ON
    r"""
    Reuse results from previous solve as much as the underlying solver
    allows.
    """
    SCALING_OFF = _pywraplp.MPSolverParameters_SCALING_OFF
    r""" Scaling is off."""
    SCALING_ON = _pywraplp.MPSolverParameters_SCALING_ON
    r""" Scaling is on."""

    def __init__(self) -> None:
        r"""The constructor sets all parameters to their default value."""
        _pywraplp.MPSolverParameters_swiginit(self, _pywraplp.new_MPSolverParameters())
    def SetDoubleParam(self, param, value):
        r"""Sets a double parameter to a specific value."""
        return _pywraplp.MPSolverParameters_SetDoubleParam(self, param, value)
    def SetIntegerParam(self, param, value):
        r"""Sets a integer parameter to a specific value."""
        return _pywraplp.MPSolverParameters_SetIntegerParam(self, param, value)
    def GetDoubleParam(self, param):
        r"""Returns the value of a double parameter."""
        return _pywraplp.MPSolverParameters_GetDoubleParam(self, param)
    def GetIntegerParam(self, param):
        r"""Returns the value of an integer parameter."""
        return _pywraplp.MPSolverParameters_GetIntegerParam(self, param)
    __swig_destroy__ = _pywraplp.delete_MPSolverParameters

# Register MPSolverParameters in _pywraplp:
_pywraplp.MPSolverParameters_swigregister(MPSolverParameters)
cvar = _pywraplp.cvar
MPSolverParameters.kDefaultRelativeMipGap = (
    _pywraplp.cvar.MPSolverParameters_kDefaultRelativeMipGap
)
MPSolverParameters.kDefaultPrimalTolerance = (
    _pywraplp.cvar.MPSolverParameters_kDefaultPrimalTolerance
)
MPSolverParameters.kDefaultDualTolerance = (
    _pywraplp.cvar.MPSolverParameters_kDefaultDualTolerance
)
MPSolverParameters.kDefaultPresolve = _pywraplp.cvar.MPSolverParameters_kDefaultPresolve
MPSolverParameters.kDefaultIncrementality = (
    _pywraplp.cvar.MPSolverParameters_kDefaultIncrementality
)

class ModelExportOptions:
    r"""Export options."""

    thisown = property(
        lambda x: x.this.own(),
        lambda x, v: x.this.own(v),
        doc="The membership flag",
    )
    __repr__ = _swig_repr

    def __init__(self) -> None:
        _pywraplp.ModelExportOptions_swiginit(self, _pywraplp.new_ModelExportOptions())
    __swig_destroy__ = _pywraplp.delete_ModelExportOptions

# Register ModelExportOptions in _pywraplp:
_pywraplp.ModelExportOptions_swigregister(ModelExportOptions)

def ExportModelAsLpFormat(*args):
    return _pywraplp.ExportModelAsLpFormat(*args)

def ExportModelAsMpsFormat(*args):
    return _pywraplp.ExportModelAsMpsFormat(*args)

def FindErrorInModelProto(input_model):
    return _pywraplp.FindErrorInModelProto(input_model)

def setup_variable_operator(opname):
    setattr(
        Variable,
        opname,
        lambda self, *args: getattr(VariableExpr(self), opname)(*args),
    )

for opname in LinearExpr.OVERRIDDEN_OPERATOR_METHODS:
    setup_variable_operator(opname)
