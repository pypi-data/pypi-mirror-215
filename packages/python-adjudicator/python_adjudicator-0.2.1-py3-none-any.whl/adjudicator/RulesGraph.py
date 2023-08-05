from __future__ import annotations

from typing import Any, Iterable

from networkx import MultiDiGraph
from networkx.algorithms.dag import is_directed_acyclic_graph

from adjudicator.errors import MultipleMatchingRulesError, NoMatchingRulesError, RuleResolveError
from adjudicator.Rule import Rule
from adjudicator.Signature import Signature


class RulesGraph:
    """
    This graph contains types as the nodes and rules are the edges.
    """

    def __init__(self, rules: Iterable[Rule] | RulesGraph) -> None:
        self._rules: dict[str, Rule] = {}

        if isinstance(rules, RulesGraph):
            rules = list(rules._rules.values())
        else:
            rules = list(rules)

        self._graph = MultiDiGraph()
        self.update(rules)

    def __iter__(self) -> Iterable[Rule]:
        return iter(self._rules.values())

    def __len__(self) -> int:
        return len(self._rules)

    def __getitem__(self, rule_id: str) -> Rule:
        return self._rules[rule_id]

    def update(self, rules: Iterable[Rule]) -> None:
        for rule in rules:
            if rule.id in self._rules:
                raise ValueError("Duplicate rule ID: " + rule.id)
            self._rules[rule.id] = rule
            self._graph.add_nodes_from(rule.input_types)
            self._graph.add_node(rule.output_type)
            for input_type in rule.input_types:
                self._graph.add_edge(input_type, rule.output_type, rule=rule)
        if not is_directed_acyclic_graph(self._graph):  # type: ignore[no-untyped-call]
            raise ValueError("Rules graph is not acyclic")

    def rules_for(self, output_type: type[Any]) -> set[Rule]:
        """
        Return all rules that can generate the specified output type.
        """

        rules: set[Rule] = set()
        if output_type not in self._graph.nodes:
            return rules
        for edge in self._graph.in_edges(output_type):
            for data in self._graph.get_edge_data(*edge).values():
                rules.add(data["rule"])
        return rules

    def find_path(self, sig: Signature) -> list[Rule]:
        """
        Returns the path from the *input_types* to the *output_type*.
        """

        rules = self.rules_for(sig.output_type)

        results: list[list[Rule]] = []
        for rule in rules:
            # Find the paths to satisfy missing inputs of the rule.
            try:
                rules_to_satify_missing_inputs: list[Rule] = []
                for missing_input_type in rule.input_types - sig.inputs:
                    for inner_rule in self.find_path(Signature(sig.inputs, missing_input_type)):
                        if inner_rule not in rules_to_satify_missing_inputs:
                            rules_to_satify_missing_inputs.append(inner_rule)
            except RuleResolveError:
                continue

            results.append([*rules_to_satify_missing_inputs, rule])

        if len(results) > 1:
            raise MultipleMatchingRulesError(sig, results, self)
        if len(results) == 0:
            raise NoMatchingRulesError(sig, self)
        return results[0]
